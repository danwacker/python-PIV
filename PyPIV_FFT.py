import numpy as np
from PIL import Image
from Gauss_fitter import gauss_inter

def PyPIV_FFT(image1,image2,sectionSize,step):
    
    #threshold for cross correlation strength
    threshold = 1;
    
#importing pictures into arrays
#    img1 = Image.open(image1)
#    img2 = Image.open(image2)
#    imArray1 = np.array(img1)
#    imArray2 = np.array(img2)

    imArray1 = image1
    imArray2 = image2
#calculating important numbers
    width, height = np.shape(imArray1)
    #number of steps
    hstep = int(width//step-(sectionSize//step-1))
    vstep = int(height//step-(sectionSize//step-1))
    
    
    #velocity arrays
    vx = np.zeros([hstep, vstep])
    vy = np.zeros([hstep, vstep])
    
    #zero point for velocity
    xy_0 = sectionSize/2 + 1
    
#loop for completing FFT
#this pretty quickly becomes a line by line of Saya's matlab code
    for i in range(hstep):
        for j in range(vstep):
            fig1 = imArray1[i*step:(i*step+sectionSize),j*step:(j*step+sectionSize)]
            fig2 = imArray2[i*step:(i*step+sectionSize),j*step:(j*step+sectionSize)]
            avg1 = np.mean(fig1)
            avg2 = np.mean(fig2)
            savg1 = np.mean(np.square(fig1))
            savg2 = np.mean(np.square(fig2))
            if (savg1*savg2)==0:
                transform1 = np.fft.fft2(fig1-avg1)
                transform2 = np.fft.fft2(fig2-avg2)
                fft_cross = np.fft.fftshift(np.fft.ifft2(np.multiply(np.conj(transform2),transform1)))
            else:
                transform1 = np.fft.fft2((fig1-avg1)/savg1)
                transform2 = np.fft.fft2((fig2-avg2)/savg2)
                fft_cross = np.fft.fftshift(np.fft.ifft2(np.multiply(np.conj(transform2),transform1)))
            
            C1 = np.amax(fft_cross,1)
            I1 = np.argmax(fft_cross,1)
            C2 = np.amax(C1)
            I2 = np.argmax(C1)
            C3 = np.amax(fft_cross,0)
            I3 = np.argmax(fft_cross,0)
            C4 = np.amax(C3)
            I4 = np.argmax(C3)
            I2 = I2 if I2 >= 1 else 1
            I4 = I4 if I4 >= 1 else 1
            I2 = I2 if I2 <= width-2 else width-2
            I4 = I4 if I4 <= width-2 else width-2
            if (C2 > threshold):
                #vx[i,j] = I2 - xy_0
                #vy[i,j] = I4 - xy_0
                vx[i,j] = I2 + gauss_inter(C1[I2-1:I2+2])[1] - xy_0
                vy[i,j] = I4 + gauss_inter(C3[I4-1:I4+2])[1] - xy_0
            else:
                vx[i,j] = 0
                vy[i,j] = 0
                
    #simple median filtering to remove some zany values
    medvx = vx
    medvy = vy
    stdx = np.std(vx)
    stdy = np.std(vy)
    ux = np.mean(vx)
    uy = np.mean(vy)
              
    for i in range(1,hstep-1):
        for j in range(1,vstep-1):
            #std filtering
            if np.abs(medvx[i,j]-ux) > 3*stdx:
                medvx[i,j] = np.median(vx[i-1:i+2,j])
            if np.abs(medvy[i,j]-uy) > 3*stdy:
                medvy[i,j] = np.median(vy[i,j-1:j+2])
            #straight median filtering
#            medvx[i,j] = np.median(vx[i-1:i+2,j])
#            medvy[i,j] = np.median(vy[i,j-1:j+2])
            
    x = np.zeros_like(medvx)        
    y = x
    dims = np.shape(x)
    for i in range(dims[0]):
        for j in range(dims[1]):
            x[i,j] = i*step + sectionSize//2
            y[i,j] = j*step + sectionSize//2
                
    return x,y,medvx,medvy