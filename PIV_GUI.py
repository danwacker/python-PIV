import sys
import os
import glob

import numpy as np
from PIL import Image

from PyQt5.QtWidgets import QListWidget, QPushButton, QLabel, QListWidgetItem, QRadioButton, QWidget, QFileDialog, QLineEdit, QApplication
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QGuiApplication
#from PyQt5.QtCore import 

from PyPIV_FFT import PyPIV_FFT

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from GUI_objects import PYPIV_window, PYPIV_checkbox, PYPIV_button, PYPIV_text_input, PYPIV_int_input, PYPIV_label 


#this is the main class which everything runs from
#contains the QApplication to exectue
#also creates the main window of the program
class PIV_GUI():
    def __init__(self):
        #all of this is just laying out the window
        app = QApplication([])
        window = PYPIV_window(30,100,1000,750)
        
        #declare variables
        self.imagearray = np.zeros((2,2,2))
        
        #creates button connected to file selection routine
        self.fileSelection = PYPIV_button(window, 'Choose Images', 0,0)
        self.fileSelection.clicked.connect(self.fileWindow)
        
        #checking masks files
        self.mask = PYPIV_checkbox(window,'Masks option',550,310)
        
        #straddling Boolean
        self.straddle = PYPIV_checkbox(window, 'Straddling', 400, 310)
        
        #laying out numberical input objects
        self.windowSize = PYPIV_int_input(window,'Window Size',400,10)
        
        self.stepSize = PYPIV_int_input(window,'Step Size',400,85)
        
        self.numImage = PYPIV_int_input(window,'Number of Image Pairs',400,160)
        
        self.imageStep = PYPIV_int_input(window,'Image Step',400,235)
        
        #run buttons
        self.Xcorr = PYPIV_button(window,'PIV FFT',20,440)
        self.Xcorr.clicked.connect(self.Xcorr_run)
        
        self.CNN = PYPIV_button(window,'PIV CNN',120,440)
        self.CNN.clicked.connect(self.CNN_run)
        
        window.show()
        app.exec_()
        
        
        
    #creates window to run cross correlation from
    def Xcorr_run(self):
        self.Xcorr_window = PYPIV_window(200,200,500,500)
        
        #directory selection button
        self.outdir = PYPIV_button(self.Xcorr_window,'Choose Output Directory',0,0)
        self.outdir.clicked.connect(self.direcSelection)
        
        #button to initiate FFT
        self.fftbutton = PYPIV_button(self.Xcorr_window,'Run FFT',0,40)
        self.fftbutton.clicked.connect(self.FFT_analysis)
        
        #brings up window
        self.Xcorr_window.show()
        
    def direcSelection(self):
        self.outdirec = QFileDialog.getExistingDirectory()
        
        
        
        
        
        
#calls the FFT function with objects from the main window
    def FFT_analysis(self):
        self.Xcorr_window.close()
        self.progresswindow = PYPIV_window(300,300,200,200)
        
         #Labels to show progress 
        self.imageloading = PYPIV_label(self.progresswindow,'Analyzing Sets',0,0)
        self.analysisprogress = PYPIV_label(self.progresswindow,'                  ',0,20)
        self.progresswindow.show()
        
        imshape = np.shape(self.imagearray)
        
        progressstr = '%d / ' + '%d' % imshape[2]
        self.analysisprogress.setText(progressstr % 0)
        
        self.figwin = QWidget()
        self.figwin.show()
        pic = QLabel(self.figwin)
        self.figwin.setGeometry(500,300,1100,800)
        self.figwin.show()
        for i in range(imshape[2]-1):
            #update progress display
            self.analysisprogress.setText(progressstr % i)
            #necessary for updating the GUI while processes are running
            QGuiApplication.processEvents()
            
            head = 'image %d and %d x,y,u,v' % (i,(i+1))
            
            #funstion that computes the velocities through simple FFT
            x,y,u,v = PyPIV_FFT(self.imagearray[:,:,i], self.imagearray[:,:,i+1], self.windowSize.value(), self.stepSize.value())
            
            #creating output file
            filename = self.outdirec + '/PIV_%04d.txt' % i
            #shaping data for output file
            dims = np.shape(x)
            out = np.reshape(np.transpose([np.reshape(x,(1,dims[0]*dims[1])), np.reshape(y,(1,dims[0]*dims[1])), np.reshape(u,(1,dims[0]*dims[1])), np.reshape(v,(1,dims[0]*dims[1]))]),(dims[0]*dims[1],4))
            np.savetxt(filename,out,fmt='%03.5f',delimiter='   ',header=head)
        
            
            #complicated matplotlib to pyqt stuff
            del pic
            fig,ax = plt.subplots(figsize=(dims[1], dims[0]))
            ax.quiver(u,v,headwidth=2,headlength=3)
            plt.savefig('out.png')
        
            pic = QLabel(self.figwin)
            graph = QPixmap('out.png')
            pic.setPixmap(graph.scaledToWidth(300))
        
        self.progresswindow.close()
        
        
    def CNN_run(self):
        self.cnn_window = PYPIV_window(300,300,200,200)
        
        self.cnn_direc_button = PYPIV_button(self.cnn_window, 'CNN directory', 20, 0)
        
        self.cnn_name = PYPIV_text_input(self.cnn_window, 'CNN name', 20, 50)
    
        
        self.cnn_load = PYPIV_button(self.CNN_window, 'Load CNN', 120,100)
        self.cnn_load.clicked.connect(self.load_cnn)
        
        self.cnn_create = PYPIV_button(self.CNN_window, 'Create New CNN',20,100)
        self.cnn_create.clicked.connect(self.create_cnn)
        
    def load_cnn(self):
        self.cnn_file = QFileDialog.getOpenFileName()
        self.cnn = cnn_load(self.cnn_file)
        
    def create_cnn(self):
        self.cnn_file = self.cnn_direc + self.cnn_name.value()
        self.cnn = cnn_create(self.cnn_file)
        
        
        
    #function creates and lays out a new window for choosing images
    def fileWindow(self):
       
        
        #create new window
        self.selectionWindow = PYPIV_window(200,200,500,600)
        
        
        #button to select first image
        self.firstImage = PYPIV_button(self.selectionWindow,'Choose First Image',0,0)
        self.firstImage.clicked.connect(self.imageSelection)
        
        #button to load images into program
        self.loadimages = PYPIV_button(self.selectionWindow,'Load Images',150,550)
        self.loadimages.clicked.connect(self.load)
        
        #textbox for directory
        self.directory = PYPIV_text_input(self.selectionWindow,'Directory',0,50)
        
        
        #textbox for file basename
        self.basename = PYPIV_text_input(self.selectionWindow,'Image Base Name',0,125)
        
        #textbox for filetype
        self.filetype = PYPIV_text_input(self.selectionWindow,'File Type',0,200)
        
        #textbox for number of digits 
        self.numdigits = PYPIV_int_input(self.selectionWindow,'Number of Digits',0,275)
        
        #textbox for first image
        self.firstimage = PYPIV_int_input(self.selectionWindow,'First Image',0,350)
        
        #textbox for number of images
        self.numimages = PYPIV_int_input(self.selectionWindow,'Number of Images',0,425)
        
        #brings up window
        self.selectionWindow.show()
        
    def imageSelection(self):
        #funcion to extract and seperate information about files
        #autofills fields in the selection window
        
        #get name of a file from GUI file selection
        file = QFileDialog.getOpenFileName()
        file = file[0]
        
        #extracting the extension of the album
        ftype = file[(file.find('.')):len(file)]
        self.filetype.setText(ftype)
        
        #extract the directory from the full address
        revfile = file[::-1]
        direc=file[0:(len(file)-revfile.find('/'))]
        self.directory.setText(direc)
        
        #cut file down to just the file name with no directory or extension
        file = file[(len(file)-revfile.find('/')):file.find('.')]
        
        #find the number of digits used to enumerate
        self.numdigits.setText(str(len(file)-file.find('0')))
        
        #filename with enumeration digits removed
        base = file[0:file.find('0')]
        self.basename.setText(base)
        
        #finds all files in the same directory with the same base name
        files = glob.glob(direc + base + '*' + ftype)
        self.numimages.setText(str(len(files)))
        
        #takes digits from the first image file in the list
        firstim = files[0]
        firstim = firstim[(firstim.find('\\')+1):firstim.find('.')]
        firstim = firstim[firstim.find('0'):len(firstim)]
        self.firstimage.setText(firstim)
        
    def load(self):
        
        #create a new window to show progress
        self.selectionWindow.close()
        self.loadwindow = PYPIV_window(300,300,200,200)
        
         #Labels to show progress 
        self.imageloading = PYPIV_label(self.loadwindow,'Loading Images',0,0)
        self.progress = PYPIV_label(self.loadwindow,'                   ',0,20)
        self.loadwindow.show()
        
        
        
        #create template to call each file individually
        filename = self.directory.value() + self.basename.value() + '%0' + ('%d'%self.numdigits.value()) + 'd' + self.filetype.value()
        
        #shape imarray with sample image
        files = glob.glob(self.directory.value() + self.basename.value() + '*' + self.filetype.value())
        dim = np.shape(np.array(Image.open(files[0])))
        self.imagearray = np.zeros((dim[0], dim[1], self.numimages.value()))
        
        #set up a string to show progress
        progressstr = '%d / ' + '%d' % self.numimages.value()
        self.progress.setText(progressstr % 0)
        
        #load images in loop
        for i in range(self.numimages.value()):
            
            #update progress display
            self.progress.setText(progressstr % i)
            #necessary for updating the GUI while processes are running
            QGuiApplication.processEvents()
            
            #actually fills the global imarray with images converted to arrays
            self.imagearray[:,:,i] = np.array(Image.open(filename % i))
        
        self.loadwindow.close()
        
        
        
