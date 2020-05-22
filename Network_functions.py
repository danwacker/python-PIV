import numpy as np
import os
import glob
from PIL import Image
from matplotlib import pyplot as plt

 
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
    compare = Dropout(0.1)(compare)
    compare = Flatten()(compare)
    compare = Dense(256, kernel_initializer=standard_init)(compare)
#    compare = Flatten()(compare)
    compare = BatchNormalization()(compare)
    compare = Dropout(0.1)(compare)
    compare = Dense(2, kernel_initializer=standard_init)(compare)
    
    fullmod = Model(input=[im1,im2],output=compare)
    
    optimizer = Adam()
    
    fullmod.compile(loss='mean_squared_error',optimizer=optimizer,metrics=['mean_squared_error'])
    
    fullmod.save(name)
    
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




def create_training_set(direc):
    csv = glob.glob(direc + '/*.csv')
    target = np.genfromtxt(csv[0],delimiter=',')
#    target = np.transpose(target)
#    dims = np.shape(target)
#    temp = np.zeros([dims[0],dims[1],1,1])
#    temp[:,:,0,0] = target
#    target = temp
    
    files1 = glob.glob(direc + '/*_1.tif')
    files2 = glob.glob(direc + '/*_2.tif')
    
    setone = np.zeros([len(files1),16,16,1])
    settwo = setone
    
    TEST_RESERVE_PERCENT = 0.25
    train_per = 1-TEST_RESERVE_PERCENT
    
    train_num = int(np.round(train_per*len(files1)))
    
    
    for i in range(len(files1)):
        setone[i,:,:,0] = np.array(Image.open(files1[i]))
        settwo[i,:,:,0] = np.array(Image.open(files2[i]))
        
    trainone = setone[0:train_num,:,:,:]
    traintwo = settwo[0:train_num,:,:,:]
    traintarget = target[0:train_num,:]
    
    testone = setone[train_num:len(files1),:,:,:]
    testtwo = settwo[train_num:len(files1),:,:,:]
    testtarget = target[train_num:len(files1),:]
    
    return trainone, traintwo, traintarget, testone, testtwo, testtarget
    
def train(net_name, direc, epochs):

    network = load_model(net_name)
    metrics = np.zeros([3,epochs])
    trainone, traintwo, traintarget, testone, testtwo, testtarget = create_training_set(direc)
    print(np.shape(traintarget))
    for i in range(epochs):
        print ('EPOCH %d/%d' % (i,epochs-1))
        loss = network.fit([trainone, traintwo],traintarget,batch_size=100, shuffle=True,verbose=0)
        metrics[0,i] = loss.history.get('loss')[0]
    
    
        #Testing
        print('\tTesting...')
        accloss = network.evaluate([testone,testtwo],testtarget,verbose=0)
        metrics[1,i] = accloss[0]
        metrics[2,i] = accloss[1]
        print('\t\taccuracy: %f'%accloss[1])
    
    
    #creating graphs of training metrics
    increase = np.arange(epochs)
    fig, ax = plt.subplots()

    #Training loss is blue 
    ax.plot(increase,metrics[0,:],color='blue')

    #Test loss is red
    ax.plot(increase,metrics[1,:],color='red')

    #accuracy is green
    ax.plot(increase,metrics[2,:],color='green')
    ax.set(xlabel='Epoch', ylabel='Accuracy', title='Training Overview')
    fig.savefig(net_name + '_training_result_with_losses.png')

    #create a text file with training metrics
    textfile=np.zeros((4,epochs))
    textfile[0,:]=increase
    textfile[1:4,:]=metrics
    textfile = np.transpose(textfile)
    np.savetxt((net_name + '_training_out.txt'),textfile,header='epoch\ttraining loss\ttest loss\taccuracy')

    #save the model with trained weights
    print('Saving Model....')
    network.save(net_name)
    print('Model Saved\n\nThanks for training\nPlease train again soon')

