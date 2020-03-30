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



#just a label
class PYPIV_label(QLabel):
    def __init__(self,window,text,x,y):
        super(PYPIV_label,self).__init__(window)
        self.move(x,y)
        self.setFont(font)
        self.setText(text)
        
        
        
#integer input box
#use self.value to retrieve integer  
class PYPIV_int_input(QLineEdit):
    def __init__(self,window,text,x,y):
        super(PYPIV_int_input,self).__init__(window)
        self.move(x,y+15)
        self.setFont(font)
        self.title = PYPIV_label(window,text,x,y)
        self.setValidator(QIntValidator())
        self.value = 0
        self.textChanged.connect(self.change)
        
        def change(self,num):
            self.value = int(num)
            
            
#text input box
#use self.value to retrieve string
class PYPIV_text_input(QLineEdit):
    def __init__(self,window,text,x,y):
        super(PYPIV_int_input,self).__init__(window)
        self.move(x,y+15)
        self.setFont(font)
        self.title = PYPIV_label(window,text,x,y)
        self.value = ''
        self.textChanged.connect(self.change)
        
        def change(self,text):
            self.value = text
            
            
            
#Boolean input
#use self.value to retrieve boolean value
class PYPIV_checkBox(QRadioButton):
    def __init__(self,window,text,x,y):
        super(PYPIV_checkBox,self).__init__(window)
        self.title = PYPIV_label(window,text,x,y)
        self.value = False
        self.toggled.connect(self.change)
        self.move(x,y+15)
        
    def change(self, value):
        self.value = value
        
        
        
class PYPIV_window(QWidget):
    def __init__(self,x,y,width,height):
        super(PYPIV_window,self).__init__()
        self.setGeometry(x,y,width,height)
        
class PYPIV_button(QPushButton):
    def __init__(self,window,text,x,y):
        super(PYPIV_button,self).__init__(window)
        self.move(x,y)
        self.setText(text)