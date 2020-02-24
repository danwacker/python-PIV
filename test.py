import numpy as np

a = np.zeros((3,3))
b = np.zeros((3,3))
print(a)
print(b)
c =np.reshape(np.array([np.reshape(a,(9,1)),np.reshape(b,(9,1))]),(9,2))
print(c)
