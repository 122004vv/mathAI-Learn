import os

#some system configuration will be defined here

__author__ = 'Vidya'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
SAVE_FOLDER = os.path.join(os.getcwd(), 'static')
MODEL_DIR = os.path.join(os.getcwd(), "my_cnn_model_config5")
RELEVANT_URL = os.path.join(os.getcwd(), 'dataset1')

NUMBER_OF_PICTURES = 400

TRAINING_STEPS = 4000

EPOCHS = 10
BATCH_SIZE = 32

PICTURE_SIZE = 45
IMG_SIZE = 45

TRAININT_RATIO = 0.6
EVAL_RATIO = 0.4
# this is all the symbol or function name in the CHROME dataset
# ['beta', 'pm, 'Delta', 'gamma', 'infty', 'rightarrow', '.DS_Store', 'div',
#  'gt', 'forward_slash', 'leq', 'mu', 'exists', 'in', 'times', 'point', 'sin',
#  'R', 'u', '9', '0', '{', '7', 'i', 'n', 'G', '+', ',', '6', 'z', '}', '1',
#  '8', 'T', 's', 'cos', 'a', '-', 'f', 'o', 'H', 'sigma', 'sqrt', 'pi', 'int',
#  'sum', 'lim', 'lambda', 'neq', 'log', 'ldots', 'forall', 'lt', 'theta', 'ascii_124',
#  'M', '!', 'alpha', 'j', 'c', ']', '(', 'd', 'v', 'prime', 'q', '=', '4', 'x', 'phi',
#  '3', 'tan', 'e', ')', '[', 'b', 'k', 'l', 'geq', '2', 'y', '5', 'p', 'w']

SYMBOLS = ['0','1','2','3','4','5','6','7','8','9',',',
            '-','+','times','div','=','int','d','infty',
            'cos','x','sin','log','e','lim','rightarrow',
            'pi','(',')','point','sqrt','tan']
# SYMBOLS = ['0','1','2','3','4','5','6','7','8','9',
#             '-','+','times','div','=','int','a','b',
#             'c','x','y','z','s','i','n','l','o','e',
#             'pi','(',')','point','frac','sin','cos','log']
FILELIST = ['infty', 'rightarrow', 'div', 'times', 'point',
             'sin', '9', '0', '7', '+', ',', '6', '1', '8',
             'cos', '-', 'sqrt', 'pi', 'int', 'lim', 'log',
             '(', 'd', '=', '4', 'x', '3', 'tan', 'e', ')',
             '2', '5']
# FILELIST = ['div', 'times', 'point', '9', '0', '7',
#             'i', 'n', '+', '6', 'z', '1', '8', 's',
#             'a', '-', 'o', 'pi', 'int', 'c', '(',
#             '=', '4', 'x', '3', 'e', ')', 'b', 'l',
#             '2', 'y', '5','frac']

UNCONTINOUS_SYMBOLS = ['div','=','rightarrow'] #,'sin','cos','tan','lim','ln','log']

SPACIAL_RELATIONSHIP = {'including':0,'included':1,'unknown':2,
                        'superscript':3,'subscript':4,'up':5,
                        'down':6,'right':7,'left':8,'left_up':9,'left_down':10}

LARGEST_NUMBER_OF_SYMBOLS = 50

SCALSIZE = 1

NUM_OF_CANDIDATES = 1

TOKEN_TYPE = {'OPERATOR':0,'CONSTANT_INTEGER':1,'CONSTANT_DECIMAL':2,'FUNCTION':3,'VARIABLE':4,'CMP':5,'RESERVE':6,'ERROR':7,'END':8,'SPECIAL':9}
OPERATOR = ['+','-','times','div','sqrt']
DIGIT = ['0','1','2','3','4','5','6','7','8','9']
SPECIAL = ['(',')','d',',','rightarrow']
VARIABLE = ['x','y','z']
RESERVE = ['e','pi','infty']
FUNCTION = ['cos','sin','log','tan','lim']
CIRCULAR_FUNCTIONS = ['cos','sin','tan']
DECIMAL_POINT = ['point','1'] 
CMP = ['=','<','>','le','ge']

DFA_STATE = {'START':0,'INCONSTANT':2,'INDECIMAL':3,'INRESERVE':4,'INVARIABLE':5,'INFUNCTION':6,'DONE':7}

NODE_TYPE = {'default':0,'bracket':1,'integer':2,'decimal':3,'variable':4,'t_pi':5,
             't':6,'e_pi':7,'e':8,'me':9,'me_pi':10,'fraction':11,'int':12,'power':13,
             'equation':14,'operator':15,'function':16,'empty':17,'f':18,'sqrt':19,'constant':20,'derivation':21,'limitation':22}

POWERABLE = [2,3,4,20]

OPERATABLE = ['0','1','2','3','4','5','6','7','8','9','x']

TOKEN_TO_NODE = {0:15,1:2,2:3,3:16,4:4,5:0,6:20,7:0,8:0,9:0}

OP_TYPE = {'power':0,'int':1,'fraction':2,'equation':3,'normal':4,'sqrt':5,'function':6}

STATUS = {'solved':0,'poly1':1,'poly2':2,'eq1':3,'eq2':4,'other':5}
VARIABLE_STATUS = [1,2,5]

REJECT_SYMBOLS = ['0','d','2','3','4','5','6','7','8','9']

TEST_URL = '../testImgs'