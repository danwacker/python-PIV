import numpy as np

#function for creating a gaussian from 3 points
#returns max value and coordinate of resulting gaussian

def gauss_inter(points):
    if points.size==3:
        a = np.log(points[0])
        b = np.log(points[1])
        c = np.log(points[2])
        sig = -1/(a + c - 2 * b)
        mu = sig * (c - a)/2
        A = np.exp(b+(mu**2)/(2*sig))
    else:
        A = points[points.size-1]
        mu = 0
    return np.array([A,mu])