import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
from matplotlib import cm
import random
import numpy as np
import cv2


def rysuj_3d(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x,y,z,facecolors=img_kolor_res/255,linewidth=0, antialiased=False)
    plt.show()





img = cv2.imread('11D0_4_Depth.png', 0)
img_kolor= cv2.imread('11C0_4_Color.png', 1)
height, width = img.shape
img_kolor_res = cv2.resize(img_kolor, dsize=(width, height), interpolation=cv2.INTER_CUBIC)

jp=np.array([[1,1,1],[2,2,2],[3,3,3],[4,4,4]])
nowe_zdj=[]
for i in range(height):
    a = pd.Series(img[i,:]) #prawa to xowa
    a.replace(0, np.NaN, inplace=True)
    a.interpolate(method='linear', inplace=True,limit=1500,limit_direction='both')
    a.replace( np.NaN,0, inplace=True)
    nowe_zdj.append(a)


noweczka=np.asarray(nowe_zdj, dtype=np.uint8)
xx, yy = np.mgrid[0:noweczka.shape[0], 0:noweczka.shape[1]]


rysuj_3d(xx,yy,noweczka)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)#by sie normalnie skalowalo
# cv2.imshow('image',noweczka)
# cv2.resizeWindow('image', 700,700)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
