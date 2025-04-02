# import os
# import cv2
# import numpy as np
# from config import *
# import tensorflow as tf
# from tools.cnn_model import cnn_symbol_classifier
# from tools.image_input import *



# # def main(unused_argv):
# train_data,train_data_labels = read_img_file('train')
# eval_data,eval_data_labels = read_img_file('eval')

# # set up logging for predictions
# # log the values in the "softmax" tensor with label "probabilities"
# tensors_to_log = {"probabilities": "softmax_tensor"}
# logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

# # evaluate the model and print results
# eval_input_fn = tf.estimator.inputs.numpy_input_fn(
#     x={"x": eval_data},
#     y=eval_data_labels,
#     num_epochs=1,
#     shuffle=False)
# eval_results = cnn_symbol_classifier.evaluate(input_fn=eval_input_fn)
# print(eval_results)

import os
import cv2
import numpy as np
import tensorflow as tf
import keras
from config import *
from tools.cnn_model import cnn_symbol_classifier
from tools.image_input import read_img_file

# Load training and evaluation data
train_data, train_data_labels = read_img_file('train')
eval_data, eval_data_labels = read_img_file('eval')

# Convert data to TensorFlow datasets
train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_data_labels)).batch(32)
eval_dataset = tf.data.Dataset.from_tensor_slices((eval_data, eval_data_labels)).batch(32)

# Set up TensorBoard logging
tensorboard_callback = keras.callbacks.TensorBoard(log_dir="./logs", histogram_freq=1)

# Ensure the model is a Keras model
if not isinstance(cnn_symbol_classifier, keras.Model):
    raise TypeError("cnn_symbol_classifier should be a Keras model in TensorFlow 2.x")

# Compile the model (update optimizer/loss/metrics based on task)
cnn_symbol_classifier.compile(optimizer='adam',
                              loss='sparse_categorical_crossentropy',
                              metrics=['accuracy'])

# Train the model
cnn_symbol_classifier.fit(train_dataset, epochs=10, validation_data=eval_dataset, callbacks=[tensorboard_callback])

# Evaluate the model
eval_results = cnn_symbol_classifier.evaluate(eval_dataset)
print(eval_results)