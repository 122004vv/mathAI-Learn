from scan import get_token
import tensorflow as tf
import tools
import config
import numpy as np
import keras

def detect_uncontinous_symbols(symbols,original_img):
    for projection_type in range(1):
        projection = tools.get_projection(symbols,projection_type)
        # print('projection',projection)
        locations = [x['location'] for x in symbols]
        end_index = 0
        for line_segment in projection:
            start_index = end_index
            for end_index in range(start_index, len(locations)):
                x11, x12 = locations[end_index][projection_type], locations[end_index][projection_type] + locations[end_index][projection_type + 2]
                x21, x22 = line_segment[0], line_segment[1]
                if (x11 >= x21 and x12 <= x22):
                    end_index += 1
                else:
                    break
            location_segment = locations[start_index:end_index]
            symbol_segment = symbols[start_index:end_index]
            sub_symbol = [x['src_img'] for x in symbol_segment]
            # print(symbol_segment)
            if (len(location_segment) > 1 and len(location_segment)<4):
                location = tools.join_locations(location_segment)
                extracted_img = tools.extract_img(location,original_img)
                input_data = np.array(tools.normalize_matrix_value(extracted_img))
                if isinstance(tools.cnn_symbol_classifier, keras.Model):
                    input_data = np.expand_dims(input_data, axis=-1)  # Ensure grayscale images have correct shape
                    predictions = tools.cnn_symbol_classifier.predict(np.array([input_data]))
                else:
                    raise TypeError("cnn_symbol_classifier should be a Keras model in TensorFlow 2.x")
                characters = []
                for i, p in enumerate(predictions):
                    # print(p['classes'],FILELIST[p['classes']])
                    candidates = tools.get_candidates(p['probabilities'])
                    characters.append({'candidates': candidates})
                # print('detect uncontinuous symbols',characters)
                for candidate in characters[0]['candidates']:
                    recognized_symbol = candidate['symbol']
                    probability = candidate['probability']

                    if recognized_symbol in config.UNCONTINOUS_SYMBOLS and probability>0.5:
                        # print('yesssssss',characters[2]['candidates'][0]['symbol'],characters[1]['candidates'][0]['symbol'].isdigit(),characters[3]['candidates'][0]['symbol'].isdigit())
                        if recognized_symbol == 'div' and len(characters) == 4 and \
                                characters[2]['candidates'][0]['symbol'] in ['-',',','point'] and \
                                characters[1]['candidates'][0]['symbol'].isdigit() == False and \
                                characters[3]['candidates'][0]['symbol'].isdigit() == False:
                            joined_symbol = {'location': location, 'src_img': extracted_img}

                            for i in range(end_index - start_index):
                                del symbols[start_index]
                                locations.remove(locations[start_index])
                            symbols.insert(start_index, joined_symbol)
                            locations.insert(start_index, location)
                            end_index = start_index + 1
                            break
                        elif recognized_symbol == '=' and len(characters) == 3 and \
                                characters[2]['candidates'][0]['symbol'] in ['-',',','point'] and \
                                characters[1]['candidates'][0]['symbol'] in ['-',',','point']:
                            joined_symbol = {'location': location, 'src_img': extracted_img}
                            for i in range(end_index - start_index):
                                symbols.remove(symbols[start_index])
                                locations.remove(locations[start_index])
                            symbols.insert(start_index, joined_symbol)
                            locations.insert(start_index, location)
                            end_index = start_index + 1
                            break
                        elif recognized_symbol == 'rightarrow' and len(characters) == 3 and \
                             characters[2]['candidates'][0]['symbol'] in [')', '>'] and \
                             characters[1]['candidates'][0]['symbol'] in ['-', ',', 'point']:
                            joined_symbol = {'location': location, 'src_img': extracted_img}
                            for i in range(end_index - start_index):
                                symbols.remove(symbols[start_index])
                                locations.remove(locations[start_index])
                            symbols.insert(start_index, joined_symbol)
                            locations.insert(start_index, location)
                            end_index = start_index + 1
                            break
    return symbols

# sin/cos/log
def detect_functions(symbols,original_img):
    sub_symbol_cnt = 3
    for j in range(2):
        stride = sub_symbol_cnt-j

        length = len(symbols)
        i = 0
        t_symbols = []
        locations = [x['location'] for x in symbols]
        while i<length-stride+1:
            location = tools.join_locations(locations[i:i+stride])
            segment_img = tools.extract_img(location,original_img)
            segment = {'src_img':segment_img,'start_index':i,'end_index':i+3,'location':location}
            t_symbols.append(segment)
            i = i+1
        # print([x['start_index'] for x in t_symbols])
        img_to_predict = [x['src_img'] for x in t_symbols]
        normalized_images = tools.normalize_matrix_value(img_to_predict)

        # Convert list to NumPy array
        input_data = np.array(normalized_images)

        # Reshape input data to match CNN input shape (Assuming 28x28 grayscale images)
        input_data = input_data.reshape((-1, 28, 28, 1))  # Adjust shape as needed

        # Get predictions using Keras model
        predictions = tools.cnn_symbol_classifier.predict(input_data)
        characters = []
        for p in predictions:  # predictions is now a NumPy array
            candidates = tools.get_candidates(p.tolist())  # Directly pass probabilities
            characters.append(candidates[0])  # Take the most probable class

        # print(characters)
        length = len(t_symbols)
        i = 0
        shift = 0

        while i<length:
            if characters[i]['symbol'] in config.FUNCTION and characters[i]['probability'] >0.9:
                start_index = t_symbols[i]['start_index']
                end_index = t_symbols[i]['end_index']
                # print('detect function',i,start_index,end_index,shift)
                start_index = start_index - shift
                end_index = end_index - shift
                for j in range(end_index - start_index):
                    symbols.remove(symbols[start_index])
                symbols.insert(start_index, t_symbols[i])
                shift = shift + end_index-start_index-1
                if i+2 < length:
                    i = i+2
                elif i+1 < length:
                    i = i+1

            i = i+1
    return symbols

def group_into_tokens(characters):
    tokens = []
    next_index = 0
    while next_index < len(characters):
        prev_index = next_index  # Store previous index
        try:
            token, next_index = get_token(characters, next_index)
            # Prevent infinite loop (if index does not advance)
            if next_index == prev_index:
                raise ValueError(f"get_token() did not advance index at position {next_index}. Possible infinite loop.")
            tokens.append(token)
        
        except Exception as e:
            raise RuntimeError(f"Error while processing tokens at index {next_index}: {str(e)}")
    return tokens