from PyQt5.QtWidgets import QPushButton, QLabel, QRadioButton, QWidget, QLineEdit
from PyQt5.QtGui import QIntValidator, QFont
#from PyQt5.QtCore import 

global font
font = QFont('sansserif',15)

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
        self.move(x,y+30)
        self.setFont(font)
        self.title = PYPIV_label(window,text,x,y)
        self.setValidator(QIntValidator())
        
    def value(self):
        return int(self.text())
            
            
#text input box
#use self.value to retrieve string
class PYPIV_text_input(QLineEdit):
    def __init__(self,window,text,x,y):
        super(PYPIV_text_input,self).__init__(window)
        self.move(x,y+30)
        self.setFont(font)
        self.title = PYPIV_label(window,text,x,y)
        
    def value(self):
        return self.text()
            
            
            
#Boolean input
#use self.value to retrieve boolean value
class PYPIV_checkbox(QRadioButton):
    def __init__(self,window,text,x,y):
        super(PYPIV_checkbox,self).__init__(window)
        self.title = PYPIV_label(window,text,x,y)
        self.value = False
        self.toggled.connect(self.change)
        self.move(x,y+30)
        
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
        self.setFont(font)