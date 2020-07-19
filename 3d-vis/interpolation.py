from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import random
import numpy as np
#http://fourier.eng.hmc.edu/e176/lectures/ch7/node7.html\
#http://www.ahinson.com/algorithms_general/Sections/InterpolationRegression/InterpolationBicubic.pdf
class Punkt:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
def wyswietl():
    punkty=[]
    p1=Punkt(0,0,0) #podane przez prowadzacego
    p2=Punkt(1,1,1)
    p3=Punkt(2,2,2)
    punkty.append(p1)
    punkty.append(p2)
    punkty.append(p3)
    fig = plt.figure()
    x=[]
    y=[]
    z=[]
    for i in punkty:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    plt.show()
def bilinear(x_stare,y_stare,z_stare,x_nowe,y_nowe):
    z_nowe = np.zeros((x_nowe.size, y_nowe.size))
    for n, x in enumerate(x_nowe):
        for m, y in enumerate(y_nowe):
            i=np.searchsorted(x_stare,x)-1 #znajdujemy lewa i prawa wartosc X
            k=np.searchsorted(y_stare,y)-1#znajdujemy lewa i prawa wartosc Y
            x1=x_stare[i]
            x2=x_stare[i+1]
            y1=y_stare[k]
            y2=y_stare[k+1]

            z11=z_stare[i,k]
            z12=z_stare[i,k+1]
            z21=z_stare[i+1,k]
            z22=z_stare[i+1,k+1]

            wynikowa_z=np.array([z11, z12, z21, z22]).reshape(2,2)
            wynikowa_y=np.array([y2-y,y-y1]).transpose()
            wynikowa_x=np.array([x2-x,x-x1])
            ulamek=1/((x2-x1)*(y2-y1))
            z_nowe[n,m]=ulamek*wynikowa_x@wynikowa_z@wynikowa_y
    return z_nowe

def rysuj_3d(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x,y,z,cmap=cm.coolwarm,linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
def funkcja_z(x,y):
    return np.sqrt(x**2+y**2)
def stworz_mesh(zakr_1,zakr_2,probki):
    x = np.linspace(zakr_1, zakr_2, probki)  #stare
    y = np.linspace(zakr_1, zakr_2, probki)
    xx, yy = np.meshgrid(x, y)
    return x,y,xx,yy
def wyswietl_przeciecie(x_s,y_s,z_s,x_n,y_n,z_n):
    plt.plot(x_s[0,:], z_s[0,:],'ro' ,label='oryginalne z(x)') #przeciecie po X
    plt.plot(x_n[0,:], z_n[0, :], label='wynikowe z(x)')
    plt.legend()
    plt.grid()
    plt.show()



x_stare,y_stare,xx_stare,yy_stare=stworz_mesh(-10,10,20)
z_stare=funkcja_z(xx_stare,yy_stare)
rysuj_3d(xx_stare,yy_stare,z_stare)

x_nowe,y_nowe,xx_nowe,yy_nowe=stworz_mesh(-10,10,100)
z_nowe = bilinear(x_stare,y_stare,z_stare,x_nowe,y_nowe)

rysuj_3d(xx_nowe,yy_nowe,z_nowe)
wyswietl_przeciecie(xx_stare,yy_stare,z_stare,xx_nowe,yy_nowe,z_nowe)
