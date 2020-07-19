from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QPushButton

from PyQt5.QtGui import QPainter, QBrush, QPen,QColor,QGuiApplication

from PyQt5.QtCore import Qt
import pprint
import sys
import random
import numpy as np
class Window(QMainWindow): 

    def __init__(self):

        super().__init__()
        self.skala=3
        self.liczba_klockow=15
        self.title = "Tetromino Mykyta Brazhynskyy"

        self.permutacje_klockow=1000
        self.ruchy_na_klocek=10
        self.czy_robimy_ruchy_w_bok=1 #bo przy liczeniu objetosci,objetosc sie nie zmienia jesli robimy ruch w bok
        self.dozwolone_zle_ruchy=2
        self.top= 150

        self.left= 150
        self.width_klocuszka=40
        self.width_planszy=24
        self.height_planszy=15

        self.width = self.width_klocuszka*self.width_planszy +200 # dajemy 200 na sterowanie
        self.height = self.width_klocuszka*self.height_planszy

        self.plansza=np.zeros((self.height_planszy,self.width_planszy))

    
        self.wybrany_klocek=''
        self.klocuszki=[] 
        self.InitWindow()
        self.generuj_figury()
        
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.label_wybrany= QLabel(self)
        self.label_wybrany.setText('Wybor')
        self.label_wybrany.move(int((8/10)*self.width), int((3/10)*self.height))
        self.label_wybrany.resize(int((8/10)*self.width), int((3/10)*self.height))
        

        self.label_procent= QLabel(self)
        self.label_procent.setText('0')
        self.label_procent.move(int((8/10)*self.width), int((2/10)*self.height))

        self.label_objetosc_stara= QLabel(self)
        self.label_objetosc_stara.setText('0')
        self.label_objetosc_stara.move(int((8/10)*self.width), int((1/10)*self.height))

        
        self.label_objetosc_stara_prawo= QLabel(self)
        self.label_objetosc_stara_prawo.setText('-stara objetosc ')
        self.label_objetosc_stara_prawo.move(int((83/100)*self.width), int((1/10)*self.height))

        self.label_objetosc_nowa= QLabel(self)
        self.label_objetosc_nowa.setText('0')
        self.label_objetosc_nowa.move(int((8/10)*self.width), int((0/10)*self.height))

        self.label_objetosc_nowa_prawo= QLabel(self)
        self.label_objetosc_nowa_prawo.setText('-nowa objetosc ')
        self.label_objetosc_nowa_prawo.move(int((83/100)*self.width), int((0/10)*self.height))

        button_lewo = QPushButton('←', self)
        button_lewo.clicked.connect(self.lewo)
        button_lewo.move(int((85/100)*self.width), int((5/10)*self.height))
        button_lewo.resize(int((1/20)*self.width), int((1/20)*self.height))

        button_prawo = QPushButton('→', self)
        button_prawo.clicked.connect(self.prawo)
        button_prawo.move(int((95/100)*self.width), int((5/10)*self.height))
        button_prawo.resize(int((1/20)*self.width), int((1/20)*self.height))

        button_dol = QPushButton('↓', self)
        button_dol.clicked.connect(self.dol)
        button_dol.move(int((90/100)*self.width), int((6/10)*self.height))
        button_dol.resize(int((1/20)*self.width), int((1/20)*self.height))

        button_gora = QPushButton('↑', self)
        button_gora.clicked.connect(self.gora)
        button_gora.move(int((90/100)*self.width), int((4/10)*self.height))
        button_gora.resize(int((1/20)*self.width), int((1/20)*self.height))

        button_porzadek = QPushButton('Porządkuj', self)
        button_porzadek.clicked.connect(self.porzadek)
        button_porzadek.move(int((90/100)*self.width), int((7/10)*self.height))
        button_porzadek.resize(int((1/20)*self.width), int((1/20)*self.height))

        self.show()
    def licz_objetosc(self,tablica):
        values = np.array([1,2,3,1,2,4,5,6,3,2,1])
        searchval = 3
        ii = np.where(values == searchval)[0]
        objetosc=0
        for i in range(self.height_planszy):
            wiersz=tablica[i]
            jedynki=np.where(wiersz==1)[0]
            ostatnia=0
            if len(jedynki)>0:
                ostatnia=max(jedynki)+1 #przesuwamy,by brak uznac jako 0
            objetosc+=ostatnia
        return objetosc
    def wybierz_ruch(self,wybor):
        nazwy_ruchow=['prawo','dol','gora','lewo']
        if nazwy_ruchow[wybor]=='prawo':
            return self.prawo()
        if nazwy_ruchow[wybor]=='dol':
            return self.dol()
        if nazwy_ruchow[wybor]=='gora':
            return self.gora()
        if nazwy_ruchow[wybor]=='lewo':
            return self.lewo()
    def porzadek(self):
        licznik=0

        odj_0=str(self.licz_objetosc(self.plansza))
        self.label_objetosc_stara.setText(odj_0)
        
        nowa_obj=0
        for i in range(self.permutacje_klockow):
            tablica_ruchow=[]
            wybrany=random.choice(self.klocuszki)#wybieramy klocek,dla niego dzialamy dopoki nastepny ruch nie bedzie gorszy
            licznik_zlych_ruchow=0
            for j in range(self.ruchy_na_klocek):
                self.wybrany_klocek=wybrany[1]
                wybor=random.randint(0,3)
                stara_obj=self.licz_objetosc(self.plansza)
                self.wybierz_ruch(wybor)
                nowa_obj=self.licz_objetosc(self.plansza)
                if self.czy_robimy_ruchy_w_bok: 
                    if stara_obj-nowa_obj<0:
                        
                        licznik_zlych_ruchow+=1
                    if licznik_zlych_ruchow==self.dozwolone_zle_ruchy:
                        self.wybierz_ruch(3-wybor)#wykonalismy zly ruch,cofamy ,ustawienie ruchow jak kod greya
                        licznik_zlych_ruchow=0
                else:
                    if stara_obj-nowa_obj<0:
                        self.wybierz_ruch(3-wybor)
                licznik+=1
                if licznik%100==0:
                    self.label_procent.setText(str(licznik*100/(self.permutacje_klockow*self.ruchy_na_klocek))+' %')
                    QGuiApplication.processEvents()


        self.label_objetosc_nowa.setText(str(nowa_obj))    
        self.update()
                
    def szukaj_wybranego(self):
        for idx,i in enumerate(self.klocuszki):
            if i[1]==self.wybrany_klocek:
                return idx
    def ustaw(self,test,ustawio,nasz,wsp,kierunek_y,kierunek_x):
        if 2 not in test and ustawio:
            self.plansza=test
            for idx,i in enumerate(wsp):
                self.plansza[i[0]][i[1]]=0 #kasujemy stare wspolrzedne
                self.plansza[i[0]+kierunek_y][i[1]+kierunek_x]=1 #zapelniamy plansze
                nasz[0][idx]=(i[0]+kierunek_y,i[1]+kierunek_x) #przesuwamy   
    def prawo(self):
        wybrany=self.szukaj_wybranego()
        nasz=self.klocuszki[wybrany]
        wspolrzedne=nasz[0]
        lista_x, lista_y = zip(*wspolrzedne)       
        pomocnicza=np.zeros((self.height_planszy,self.width_planszy))
        testowa=self.plansza.copy()
        ustawione=0
        for i in wspolrzedne:
            if max(lista_y)+1<self.width_planszy: #patrzymy czy nowy ruch nie wyjdzie poza plansze
                pomocnicza[i[0]][i[1]+1]=1
                testowa[i[0]][i[1]]=0
                ustawione=1
        testowa=testowa+pomocnicza
        self.ustaw(testowa,ustawione,nasz,wspolrzedne,0,1)

            
        self.update() #aktualizuj rysowanie
    def lewo(self):
        wybrany=self.szukaj_wybranego()
        nasz=self.klocuszki[wybrany]
        wspolrzedne=nasz[0]
        lista_x, lista_y = zip(*wspolrzedne)       
        pomocnicza=np.zeros((self.height_planszy,self.width_planszy))
        testowa=self.plansza.copy()
        ustawione=0
        for i in wspolrzedne:
            if min(lista_y)>0:
                pomocnicza[i[0]][i[1]-1]=1
                testowa[i[0]][i[1]]=0
                ustawione=1
        testowa=testowa+pomocnicza
        self.ustaw(testowa,ustawione,nasz,wspolrzedne,0,-1)
        self.update() #aktualizuj rysowanie
    def dol(self):
        wybrany=self.szukaj_wybranego()
        nasz=self.klocuszki[wybrany]
        wspolrzedne=nasz[0]
        lista_x, lista_y = zip(*wspolrzedne)       
        pomocnicza=np.zeros((self.height_planszy,self.width_planszy))
        testowa=self.plansza.copy()
        ustawione=0
        for i in wspolrzedne:
            if max(lista_x)+1<self.height_planszy:
                pomocnicza[i[0]+1][i[1]]=1
                testowa[i[0]][i[1]]=0
                ustawione=1
        testowa=testowa+pomocnicza
        self.ustaw(testowa,ustawione,nasz,wspolrzedne,1,0)
        self.update() #aktualizuj rysowanie
    
    def gora(self):
        wybrany=self.szukaj_wybranego()
        nasz=self.klocuszki[wybrany]
        wspolrzedne=nasz[0]
        lista_x, lista_y = zip(*wspolrzedne)       
        pomocnicza=np.zeros((self.height_planszy,self.width_planszy))
        testowa=self.plansza.copy()
        ustawione=0
        for i in wspolrzedne:
            if min(lista_x)>0:
                pomocnicza[i[0]-1][i[1]]=1
                testowa[i[0]][i[1]]=0
                ustawione=1
        testowa=testowa+pomocnicza
        self.ustaw(testowa,ustawione,nasz,wspolrzedne,-1,0)
        self.update() #aktualizuj rysowanie
    def figs(self,wybor,start_x,start_y):
        figurka=np.zeros((self.height_planszy,self.width_planszy))

        
        if wybor==0:
            # kwadrat
            if start_x<self.height_planszy-1 and start_y<self.width_planszy-1:
                figurka[start_x][start_y]=1
                figurka[start_x][start_y+1]=1
                figurka[start_x+1][start_y]=1
                figurka[start_x+1][start_y+1]=1
                wsp=[(start_x,start_y),(start_x,start_y+1),(start_x+1,start_y),(start_x+1,start_y+1)]
                typ=0
                return figurka,wsp,typ
            else:
                return [0],[0],[0]
        if wybor==1:
        #piramidka srodkowy 
            if start_x<self.height_planszy-1 and start_x>0 and start_y<self.width_planszy-1 and start_y>0:
                figurka[start_x][start_y]=1
                figurka[start_x][start_y-1]=1
                figurka[start_x][start_y+1]=1
                figurka[start_x-1][start_y]=1
                wsp=[(start_x,start_y),(start_x,start_y-1),(start_x,start_y+1),(start_x-1,start_y)]
                typ=1
                return figurka,wsp,typ
            else :
                return [0],[0],[0]
        if wybor==2:
        #pasek lewy
            if start_x<self.height_planszy-3: 
                figurka[start_x][start_y]=1
                figurka[start_x][start_y+1]=1
                figurka[start_x][start_y+2]=1
                figurka[start_x][start_y+3]=1
                wsp=[(start_x,start_y),(start_x,start_y+1),(start_x,start_y+2),(start_x,start_y+3)] 
                typ=2
                return figurka,wsp,typ
            else:
                return [0],[0],[0]
    def sprawdz_najblizszy(self,x,y):
        for idx, i in enumerate(self.klocuszki):
            wsp,nazwa,_,typ=i
            for j in wsp:
                x_wsp,y_wsp=j
                if y>x_wsp*self.width_klocuszka and y<(x_wsp+1)*self.width_klocuszka  and x>y_wsp*self.width_klocuszka and x<(y_wsp+1)*self.width_klocuszka:
                    if self.wybrany_klocek!=nazwa:
                        self.wybrany_klocek=nazwa
                        self.label_wybrany.setText(self.wybrany_klocek)
                        self.update()


    def generuj_figury(self):
        dodano=0
        wybor_kwadrat=0
        wybor_piramida=0
        wybor_pasek=0
        iteracje=0
        while dodano<self.liczba_klockow and iteracje<1000:
            start_x=random.randint(0,24)
            start_y=random.randint(0,15)
            wybor=random.randint(0,2)
            nazwa=0

            wynik,wsp,typ=self.figs(wybor,start_x,start_y)
            if len(wynik)>1:
                plansza_test=self.plansza+wynik
                if 2 not in plansza_test:
                    self.plansza=plansza_test
                    wspolrzedne=0
                    if wybor==0:
                        nazwa='kwadrat '+str(wybor_kwadrat)
                        wybor_kwadrat+=1
                    if wybor==1:
                        nazwa='piramida '+str(wybor_piramida)
                        wybor_piramida+=1
                    if wybor==2:
                        nazwa='pasek '+str(wybor_pasek)
                        wybor_pasek+=1
                    kolor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    klocek=(wsp,nazwa,kolor,typ)
                    self.klocuszki.append(klocek)
                    dodano+=1
            iteracje+=1 #by nie wpasc w nieskonczona petle jesli sie nie da
        if iteracje==1000:
            print('nie da sie ustawic',self.liczba_klockow,'ustawilismy',dodano)
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            x=e.pos().x()
            y=e.pos().y()
            self.sprawdz_najblizszy(x,y)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        for i in self.klocuszki:
            wsp,nazwa,kolor,_=i
            painter.setBrush(QBrush(QColor(kolor[0],kolor[1],kolor[2], 127), Qt.SolidPattern))
            for j in wsp:
                x_j,y_j=j
                w=self.width_klocuszka
                painter.drawRect(y_j*w , x_j*w, w, w) #x0,y0,x1,y1


App = QApplication(sys.argv)
App.setStyle('Fusion')

window = Window()


sys.exit(App.exec())