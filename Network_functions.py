import numpy as np
import os
 
from keras.layers.core import Dense, Dropout, Flatten, Activation
from keras.layers.convolutional import Convolution2D
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.layers import Input, MaxPooling2D, concatenate
from keras.models import Model
from keras.layers.noise import GaussianNoise
from keras.initializers import RandomNormal
from keras.metrics import binary_accuracy
from keras.models import load_model


def cnn_load(name):
    return load_model(name)
    
    
def cnn_create(name):
    #defining the architecture for a side
    standard_init = RandomNormal(0,0.1)
    
    input_layer = Input(shape=(16,16,1),dtype='float32') #16x16
    
    #running size is commented on the side
    side = conv(input_layer,32,3,1) 
    side = conv(side,64,3,1) 
    side = pool(side,2) 
    side = conv(side,128,3,1)
    
    #declaring each side
    sidemod = Model(input_layer,side)
    im1 = Input(shape=(16,16,1),dtype='float32',name='one')
    im2 = Input(shape=(16,16,1),dtype='float32',name='two')
    mod1 = sidemod(im1)
    mod2 = sidemod(im2)
    
    #single channel
    #find the difference of the sides
    compare = concatenate([mod1, mod2])
#    compare = Flatten()(compare)
    compare = Dropout(0.2)(compare)
    compare = Dense(256, kernel_initializer=standard_init)(compare)
    compare = BatchNormalization()(compare)
    compare = Dropout(0.25)(compare)
    compare = Dense(2, kernel_initializer=standard_init)(compare)
    
    fullmod = Model(input=[im1,im2],output=compare)
    
    optimizer = Adam()
    
    fullmod.compile(loss='mean_squared_error',optimizer=optimizer,metrics=['accuracy'])
    
    fullmod.save(name + '.h5')
    
    return
    
    
    
    
    
    
#functions to make the network design more readable
def conv(net,numfilt,fsize,ssize,pad=False):
    border_mode = 'same' if pad else 'valid'
    init = RandomNormal(0,0.1)
    net = Convolution2D(numfilt,fsize,fsize,subsample=(ssize,ssize),border_mode=border_mode,kernel_initializer=init)(net)
    net = Activation('relu')(net)
    return net

def pool(net,psize):
    net = MaxPooling2D(pool_size=(psize,psize))(net)
    return net