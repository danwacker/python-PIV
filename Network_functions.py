import numpy as np
import os
 
from keras.layers.core import Dense, Dropout, Flatten, Activation
from keras.layers.convolutional import Convolution2D
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.layers import Input, MaxPooling2D, Subtract
from keras.models import Model
from keras.layers.noise import GaussianNoise
from keras.initializers import RandomNormal
from keras.metrics import binary_accuracy
from keras.models import load_model


def cnn_load(location,name):
    return load_model(location + name)
    
    
def cnn_create(name):
    
    