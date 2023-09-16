import numpy as np
import cv2
import math as mt
from PIL import Image
from scipy import signal
from matplotlib import pyplot as plt


# plantillas  0 al 9
digitos=[
[[1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
 [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
 [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
 [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
 [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1]],

[[1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
 [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

[[1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
 [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
 [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
 [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],


[[1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]],


[[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
 [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
 [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
 [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1]],

[[1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
  [1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
  [1,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1],
  [1,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1],
  [1,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1],
  [1,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1],
  [1,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1],
  [1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
  [1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   1],
  [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
  [0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1]],


[[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
 [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
 [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
 [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1]],


 [[0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
  [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   1],
  [1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   1],
  [1,   1,   1,   1,   1,   1,   0,   0,   0,   1,   1],
  [1,   1,   1,   1,   1,   0,   0,   0,   0,   1,   1],
  [1,   1,   1,   1,   1,   0,   0,   0,   1,   1,   1],
  [1,   1,   1,   1,   0,   0,   0,   0,   1,   1,   1],
  [1,   1,   1,   1,   0,   0,   0,   1,   1,   1,   1],
  [1,   1,   1,   0,   0,   0,   0,   1,   1,   1,   1],
  [1,   1,   1,   0,   0,   0,   1,   1,   1,   1,   1],
  [1,   1,   0,   0,   0,   0,   1,   1,   1,   1,   1],
  [1,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1]],


 [[1,   1,   0,   0,   0,   0,   0,   0,   0,   1,   1],
  [1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
  [0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0],
  [0,   0,   0,   1,   1,   1,   1,   1,   0,   0,   0],
  [0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0],
  [1,   0,   0,   0,   0,   1,   0,   0,   0,   0,   1],
  [1,   1,   0,   0,   0,   0,   0,   0,   0,   1,   1],
  [1,   1,   0,   0,   0,   0,   0,   0,   0,   1,   1],
  [1,   0,   0,   0,   0,   1,   0,   0,   0,   0,   1],
  [0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0],
  [0,   0,   0,   1,   1,   1,   1,   1,   0,   0,   0],
  [0,   0,   0,   1,   1,   1,   1,   1,   0,   0,   0],
  [0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0],
  [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
  [1,   1,   0,   0,   0,   0,   0,   0,   0,   1,   1]],

 [[1,   1,   0,   0,   0,   0,   0,   0,   1,   1,   1],
  [1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
  [0,   0,   0,   0,   1,   1,   0,   0,   0,   0,   1],
  [0,   0,   0,   1,   1,   1,   1,   0,   0,   0,   0],
  [0,   0,   0,   1,   1,   1,   1,   1,   0,   0,   0],
  [0,   0,   0,   1,   1,   1,   1,   1,   0,   0,   0],
  [0,   0,   0,   0,   1,   1,   1,   0,   0,   0,   0],
  [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
  [1,   1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   1,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   1,   0,   0,   0,   0],
  [1,   1,   1,   1,   1,   1,   0,   0,   0,   0,   1],
  [1,   1,   1,   1,   1,   0,   0,   0,   0,   0,   1],
  [0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1],
  [0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1]]


]


hogs = [
        [67390.53344727, 86282.72131348, 73772.97595215, 36485.01855469,
         51271.85595703, 17767.60754395, 48275.00067139, 23748.94104004,
         49281.4664917 , 67390.53344727, 86282.72131348, 73772.97595215,
         36485.01855469,51271.85595703, 17767.60754395 ,48275.00067139,
         23748.94104004, 49281.4664917 ],
        [363120.0      ,        0.0      ,       0.0       ,      0.0,
          77243.82348633,  14081.81494141,   9030.61175537 , 19337.42932129,
          42493.31066895, 223044.93652344,  10730.42297363 , 31023.71264648,
          30522.35253906, 121521.23242188,  21056.38964844 , 22719.34082031,
          10730.42297363,  30099.41333008],
        [ 32382.140625  ,  37403.55737305, 163596.12219238 , 59173.64892578,
          66620.10327148,  32885.828125  ,  27975.44104004 , 23333.30908203,
          14852.12841797,  63543.80200195, 111933.80090332 ,162425.18341064,
              0.0       , 171184.60302734,   7876.15673828 , 21037.38342285,
          19698.21655273,  19766.67480469],
        [ 53860.67272949,  10567.18469238,  39063.40332031 , 38552.67285156,
         120465.68530273,  69610.60498047,  79982.88085938 , 63957.484375,
          23659.25439453,  78716.10498047,  47926.54541016 , 61897.24835205,
          62104.76074219, 203387.54980469,  18379.94287109 ,  8690.9597168,
          24913.38122559,  21241.91552734],
        [149985.21911621,  42334.74829102,  20716.97766113 ,  3551.73901367,
         141208.11767578,  12953.25402832,  34500.68475342 , 32081.2644043,
          58546.51599121, 121949.52160645, 154574.0111084  , 32547.98327637,
           4357.44189453,  58413.13134766,      0.0        ,  5781.24951172,
          20940.63647461,  29162.59460449],
        [ 59321.96606445,  10730.42297363,  65626.48413086 , 43537.22961426,
         212343.79638672,  45012.92431641,  35297.28338623 , 28838.50256348,
          22865.06738281,  95170.42285156,  19624.62902832 , 25793.3661499,
          30496.80273438, 234646.5402832 ,  40004.01782227 , 68195.23693848,
           9243.53027344,  23358.47558594],
        [ 76419.96624756,  43214.79943848,  70192.67724609 , 92665.28759766,
         118332.53881836,  18137.73632812,  35508.61621094 , 23736.38049316,
          18124.44067383,  84136.56933594,  24247.17822266 , 74598.36206055,
          24990.17163086, 151474.83154297,  86580.86621094 , 36803.59509277,
          55943.09936523,  41150.94799805],
        [ 58664.30224609, 240812.16015625,   3695.03430176 ,     0.0,
         209333.10180664,   7876.15673828,  15759.37133789 , 14415.82897949,
           5701.97314453,  50292.66796875, 320857.44482422 ,  1081.87335205,
              0.0       ,   9690.0       ,      0.0        ,     0.0,
              0.0       ,      0.0       ],
        [ 89025.35888672,  49748.43310547,  72271.75488281,  22289.16101074,
         128010.        ,  21874.10266113,  64698.64135742,  55592.7677002,
          57907.1940918 ,  52887.36352539,  50715.35839844,  71158.1640625,
          33073.34191895, 130319.12329102,  34430.39172363,  62142.55273438,
          53341.27111816,  26050.92236328],
        [ 87968.27490234,  25734.07092285,  76851.23120117,  23584.66577148,
         129070.98193359,  98722.75537109,  60282.53674316,  30919.21252441,
          35123.35595703,  43609.34912109,  57571.21691895,  91780.2578125,
          44949.29638672, 170741.22314453,  15512.35058594,  52835.75268555,
          19624.62902832,  18124.44067383]
    ]

pos_pix={0:(0,11), 1:(12,23), 2:(24,35),3:(36,47),4:(48,59),5:(72,83),6:(84,95)
         ,7:(96,107),8:(108,119),9:(120,131)}

def custom(im,temp): #image and template
    n=np.array(im,dtype=np.uint8)
    w = np.logical_xor(n,temp)
    #(c, a, b) = np.shape(w)
    # img = np.zeros([a,b,3])
    # img[:,:,0] = w[:,:]
    # img[:,:,1] = w[:,:]
    # img[:,:,2] = w[:,:]
    img = 0
    unos = (w).sum()
    unos = unos / 165
    if (unos < 0.18):
        return True, img, unos
    else:
        return False, img, unos

def hog(img):
    img = cv2.cvtColor(np.float32(img), cv2.COLOR_RGB2GRAY)
    gx = cv2.Sobel(img,cv2.CV_32F,1,0,ksize=5)
    gy = cv2.Sobel(img,cv2.CV_32F,0,1,ksize=5)
    mag, ang = cv2.cartToPolar(gx, gy)
    bin_n = 18 # Number of bins
    bin = np.int32(bin_n*ang/(2*np.pi))
    hist = np.bincount(bin.ravel(),mag.ravel(),bin_n)
    #print(hist)
    return hist

def compareHog(img):
    a, b = np.shape(img)
    im = np.zeros([a,b,3])
    im[:,:,0] =img
    im[:,:,1] =img
    im[:,:,2] =img
    hist = hog(im)
    i = 0
    for ho in hogs:
        d = np.corrcoef(hist, ho)[1,0]
        print(i,d)
        i += 1
    return i

def diffImg(img,temp):
    n=np.array(img,dtype=np.uint8)
    w = n - temp
    total = w.sum()
    total = total / (165*255)
    (c, a, b) = np.shape(w)
    img = np.zeros([a,b,3])
    img[:,:,0] = w[:,:]
    img[:,:,1] = w[:,:]
    img[:,:,2] = w[:,:]

    if (total < 0.85):
        return True, img, total
    else:
        return False, img, total


def corrImg(im, realNum):
    i = 0
    correlations= []
    for n in digitos:
        #im = np.asArray(im,dtype=np.uint8)
        m =np.array(n,dtype=np.uint8)
        m=cv2.bitwise_not(m*255) #los unos indican el numero,se escala de 0-1 a 0-255
        cor = signal.correlate2d (im, m)
        cor = cor.astype('uint8')
        #print(cor)
        a,b = cor.shape
        img = np.zeros([a,b,3])
        img[:,:,0] = cor[:,:]
        img[:,:,1] = cor[:,:]
        img[:,:,2] = cor[:,:]
        #img *= 255.0/100    #asume 100 max value
        #print(img[:,:,0])
        maxVal = np.amax(cor)
        correlations.append(maxVal)
        # plt.imshow(img.astype('uint8'))
        # plt.title("Correlación "+str(realNum)+" vs plantilla "+str(i)+" max Val: "+str(maxVal))
        # plt.show()
        i += 1
    return correlations.index(max(correlations))

def extrae_numeros(img):
    numero1 = 0
    numero2 = 0
    img2 = img[413:428 , 525:656]
    th1 = img2
    #print(" ")
    for i in pos_pix:
        p = 0
        j,k = pos_pix[i]
        im = th1[0:15 , j:k]
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        im_1 = cv2.threshold(im[0:8, 0:5 ], 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        im_2 = cv2.threshold(im[0:8 , 5:11], 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        im_3 = cv2.threshold(im[8:15, 0:5], 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        im_4 = cv2.threshold(im[8:15, 5:11], 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        imgg = im
        imgg[0:8, 0:5 ]=im_1
        imgg[0:8 , 5:11]=im_2
        imgg[8:15, 0:5]=im_3
        imgg[8:15, 5:11]=im_4
        im = imgg

        #cv2.imshow('number',im)
        #print(im)
        a=cv2.split(im)

        #h = compareHog(im)
        for p in range(10):
            m =np.array(digitos[p],dtype=np.uint8)
            m=cv2.bitwise_not(m*255) #los unos indican el numero,se escala de 0-1 a 0-255
            #r, img, s = custom(a,m)

            r, imgd, tot = diffImg(a,m)
            # if numero1 > 0:
            #     name = "diff plantilla: "+str(p)+ " --> "+str(round((1-tot), 3))+" "
            #     cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
            #     cv2.imshow(name,imgd)
            #     cv2.waitKey()
            #     cv2.destroyWindow(name)
            if r :
                valor = p
                #print(valor, end="   | ")
                if i < 5 :
                    numero1 += (valor * (10 ** (4 - i)))
                else :
                    numero2 += (valor * (10 ** (9 - i)))
                break

        # nro = corrImg(im,0)
        # #print("Número de correlación ", nro)
        # if i < 5 :
        #     numero1 += (nro * (10 ** (4 - i)))
        # else :
        #     numero2 += (nro * (10 ** (9 - i)))


    return numero1, numero2


def agrega_temperatura(img,tmin,tmax, Ec, em, Ta, Corr,dist):
    d = float(dist)
    E = float(em)
    tAmb = float(Ta)
    if Ec == 0 :
        a = 1.089247464*(10**-16)*tmin**4 - 1.148710973*(10**-11)*tmin**3 + 1.269505043*(10**-7)*tmin**2 + 2.470194145*(10**-2)*tmin - 640.9709413
        b = 1.089247464*(10**-16)*tmax**4 - 1.148710973*(10**-11)*tmax**3 + 1.269505043*(10**-7)*tmax**2 + 2.470194145*(10**-2)*tmax - 640.9709413

    elif Ec == 1 :
        a = (1308.45/(mt.log(4.59064950609725*(10**5)/(tmin - 0.267584022320203*10**5) + 1.0 )))-273.15
        b = (1308.45/(mt.log(4.59064950609725*(10**5)/(tmax - 0.267584022320203*10**5) + 1.0 )))-273.15

    if Corr :
        if(d>10):
            err = 1.762026991*(10**-9)*d**3 - 6.324618148*(10**-6)*d**2 + 1.826922911*(10**-2)*d + 1.443509426
        else:
            err = 0

        a = (a*0.96) + (0.04*22)
        b = (b*0.96) + (0.04*22)
        a = (a - ((1-E)*tAmb))/E
        b = (b - ((1-E)*tAmb))/E  + err
    if( a>500 or a < -80):
        a = "--"
    else:
        a=str('%.3f'%(a))

    if( b>500 or b < -80):
        b = "--"
    else :
        b=str('%.3f'%(b))


    font = cv2.FONT_HERSHEY_DUPLEX
    img = cv2.putText(img,'min: ',(10,20), font, 0.5,(200,255,155),1,cv2.LINE_AA)
    img = cv2.putText(img,'max: ',(10,40), font, 0.5,(200,255,155),1,cv2.LINE_AA)
    img = cv2.putText(img,a,(50,20), font, 0.5,(200,255,155),1,cv2.LINE_AA)
    img = cv2.putText(img,b,(50,40), font, 0.5,(200,255,155),1,cv2.LINE_AA)


    return img,a,b

def recortaImagen(img):
    im=img.copy()
    im = cv2.circle(im,(648,48), 17, (0,0,0), -1)
    return im[0:392,:]
def pixel_Temp(img,imgP, tmin, tmax, x, y, Ec, em, ta):
    E = float(em)
    tAmb = float(ta)
    try:
        t_min = float(tmin)
        t_max = float(tmax)
    except ValueError:
        print("Error de temperatura")
        t_min = 0.0
        t_max = 0.0

    mn = np.amin(imgP[:,:,0])
    mx = np.amax(img[:,:,0])
    print("límites:",mn,mx)

    p = (float(img[y,x,0]) + float(img[y,x,1]) + float(img[y,x,2]))/3
    print("Valor pixel:",img[y,x,0],img[y,x,1],img[y,x,2])
    tp = ((p-mn)/(mx-mn))
    tp = tp*(t_max - t_min)+t_min
    return tp


def cursor(img,x,y):
    img = cv2.circle(img,(x,y), 2, (250,210,1), 2)
    return img

def punto_caliente(img):
    mn,mx,mnLoc,mxLoc = cv2.minMaxLoc(img[:,:,0])
    top = (mxLoc[0]-5,mxLoc[1]-5)
    bot = (mxLoc[0]+5, mxLoc[1]+5)
    try:
        im = cv2.rectangle(img,top,bot,(0,255,2555),2)
    except:
        im=img
    return im
