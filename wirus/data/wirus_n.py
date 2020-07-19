import pandas as pd
import os
import glob
import numpy as np
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit




path = 'C:/Users/Nikita/Desktop/wirus/data/dane'
os.chdir(path)

print('Kraj','Last Update','Confirmed','Recovered','Deaths')
def przybliz(data_czas,y,dni_do_przodu,od_ktorego_dnia):
    x=np.arange(0,len(data_czas),1)
    x=np.array(x)
    wartosci_wsp=curve_fit(lambda t,a,b,k: a*np.exp(b*t)+k,  x,  y,  p0=(0.01, 0.01,0.01)) #aproksymacja eksponenta
    x_n=0
    przewidywania=0
    calosc=0
    if od_ktorego_dnia==-1:#zeby zobaczyc calosc
        x_n=np.arange(len(x)-1,len(x)+dni_do_przodu,1) 
        przewidywania=wartosci_wsp[0][0]*np.exp(wartosci_wsp[0][1]*x_n)+wartosci_wsp[0][2]
        calosc=len(x_n)+len(x)-2
    elif len(x)>od_ktorego_dnia and od_ktorego_dnia>-1 : #zeby czesciowo sie pokrywalo
        print('weszlismy')
        x_n=np.arange(od_ktorego_dnia-1,len(x)+dni_do_przodu,1)
        przewidywania=wartosci_wsp[0][0]*np.exp(wartosci_wsp[0][1]*x_n)+wartosci_wsp[0][2]
        calosc=len(x_n)+len(x)-od_ktorego_dnia
    return x,x_n,przewidywania,calosc
def rysuj_wykres(kraj,tytul,mnoznik,dni_do_przodu,od_ktorego_dnia):
    nasz_x,nasz_y,pierwszy=szukaj_kraju(kraj)
    nasz_y = np.asarray(nasz_y) * mnoznik
    #razy zageszczenie w gdansku/zageszczenie w polsce
    x,x_n,przewidywania,cala_data=przybliz(nasz_x,nasz_y,dni_do_przodu,od_ktorego_dnia)
    plt.plot(x,nasz_y,x_n,przewidywania)
    plt.title(tytul)
    plt.ylabel('Potwierdzone')

    koncowa_data=pierwszy
    for i in range(0,cala_data): #liczy koncowa date
        koncowa_data+=timedelta(days=1)
    print('Przedzial dat wykresu w',kraj,'od=',pierwszy,'do=',koncowa_data)
    plt.show()
def szukaj_kraju(kraj):
    czy_bylo=[]
    nazwy_plikow=[]

    for file_name in glob.glob('*.csv'): #otwieramy nasze pliki
        dane = pd.read_csv(file_name, low_memory=False)
        bylo_w_pliku=0
        nazwy_plikow.append(file_name)

        for idx,i in enumerate(dane['Country/Region']): #sprawdzamy czy polska jest w pliku
            if i ==kraj:
                bylo_w_pliku=1
        czy_bylo.append(bylo_w_pliku)
    pierwsza_data=0
    
    for idx,i in enumerate(czy_bylo): #szukalismy pierwszej daty
        if i==1 and pierwsza_data==0:
            pierwsza_data=idx

    data_poczatkowa=nazwy_plikow[pierwsza_data]
    data_poczatkowa=data_poczatkowa[0:len(data_poczatkowa)-4]


    miesiac=int(data_poczatkowa[1:2])
    dzien=int(data_poczatkowa[4:5])
    rok=int(data_poczatkowa[6:10])
  
    data_nowa_moja= datetime(rok,miesiac,dzien)
    data_kopia=data_nowa_moja
    xs=[]
    ys=[]


    for file_name in nazwy_plikow:
        dane = pd.read_csv(file_name, low_memory=False)

        for idx,i in enumerate(dane['Country/Region']):
            if i ==kraj:
                indeks=idx
                data_nowa_moja+=timedelta(days=1)
                xs.append(data_nowa_moja)
                ys.append(dane['Confirmed'][indeks])
    
    return xs,ys,data_kopia



ludzie_w_trojm=748986
ludzie_w_pl=38386000
mnoznik=(ludzie_w_trojm/ludzie_w_pl)
ile_dni_do_przodu=10
od_ktorego_dnia_przewidujemy=-1 
#od_ktorego_dnia_przewidujemy=-1 #jezeli damy to rowne -1 to wtedy od konca przewidujemy

rysuj_wykres('Poland','Gdansk',mnoznik,ile_dni_do_przodu,od_ktorego_dnia_przewidujemy)
  