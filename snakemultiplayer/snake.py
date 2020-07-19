from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem,QLabel,QGraphicsRectItem,QGraphicsPixmapItem,QLineEdit,QPushButton
from PyQt5.QtGui import QPen, QBrush,QPixmap
import json
from PyQt5.Qt import Qt
import math
import sys
import random
import socket,pickle
import base64
import uuid
import re
import resources


class SnakeWindow(QMainWindow):
    def __init__(self,parentPort,parentName,parentHost):
        super().__init__()
        self.parentPort=parentPort
        self.parentName=parentName
        self.parentHost=parentHost
        self.title = "Snake"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 1000
        self.pozycjeSrodkowHex=[]
        self.nazwaPrzeciwnika=''


        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.parentHost, int(self.parentPort)))

        self.ilosc_rzedow=10
        self.w_kolumnie=20
        self.dlugoscBoku=20
        self.szerokosc_planszy=int(self.w_kolumnie*self.dlugoscBoku*math.sqrt(3))
        self.wysokosc_planszy=int(self.ilosc_rzedow*self.dlugoscBoku*(3/2)*2)
        self.szerokosc_grafiki=800
        self.wysokosc_grafiki=800
        self.pozycjeSegmentowPrzeciwnika=[]
        self.pozycjeSegmentowPrzeciwnikaStare=[]
        self.segmentyPrzeciwnika=[]
        self.koniec=0
        self.wynikPrzeciwnika=0
        self.ID=self.stworz_klucz()
        print(self.ID)
        self.historiaPozycjiGracza=[]
        self.historiaPozycjiPrzeciwnika=[]


        self.pozycjeSegmentowWeza=[(0,0)]
        self.dummy1=0

        self.owocX=0
        self.owocY=0
        self.start=0
        self.segmenty=[]
        
        self.vWeza=math.sqrt(3)*self.dlugoscBoku
        self.wynik=0
        self.katWeza=0
        self.frames=10
        self.InitWindow()

    def stworz_klucz(self):
        rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
        return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 

        
        self.createGraphicView()
 
        self.show()
    def timerFunc(self):
        if self.koniec==0:
            
            self.wyslij_odbierz()
            
            if self.start==1:
                self.ustawWeza()
                self.ustawPrzeciwnika()
                self.label_wynik_przeciwnik_2.setText(str( self.wynikPrzeciwnika))
                self.zapiszRuchy()
        else:
            self.label_koniec.setText('KONIEC!!!')
            self.Frametimer.stop()
            self.wyslij_odbierz()
            self.sock.close()
    def zapiszRuchy(self):
        data = {}
        data['myName']=self.parentName
        data['oponentName']=self.nazwaPrzeciwnika
        data['myMoves']=self.historiaPozycjiGracza
        data['oponentMoves']=self.historiaPozycjiGracza
        myFile=open('save.json','r+')
        json.dump(data, myFile)
        myFile.close()
    def wyslij_odbierz(self):
        
        
        self.historiaPozycjiGracza.append(self.pozycjeSegmentowWeza)
        obiekt={'id':self.ID,'pozycje':self.pozycjeSegmentowWeza,'koniec':self.koniec,'wynik':self.wynik,'nazwa':self.parentName}
        data_string = pickle.dumps(obiekt)
        self.sock.sendall(data_string)
        data = self.sock.recv(1024)
        otrzymana=eval(repr(pickle.loads(data)))



        
        if otrzymana['id']!=self.ID:
            self.start=1
            self.pozycjeSegmentowPrzeciwnikaStare=self.pozycjeSegmentowPrzeciwnika
            self.pozycjeSegmentowPrzeciwnika=otrzymana['pozycje']
            self.historiaPozycjiPrzeciwnika.append(self.pozycjeSegmentowPrzeciwnika)
            self.wynikPrzeciwnika=otrzymana['wynik']
            self.nazwaPrzeciwnika=otrzymana['nazwa']
            self.label_wynik_przeciwnik.setText(self.nazwaPrzeciwnika)
            if otrzymana['koniec']==1: #jezeli jedno z dwoch zje ogon
                self.koniec=1
    def createGraphicView(self):

       

        self.scene  =QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)
        
        self.pen = QPen(Qt.red)


        
 
        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0,0,self.szerokosc_grafiki,self.wysokosc_grafiki)

        self.label_wynik=QLabel(self)
        self.label_wynik2=QLabel(self)
        self.label_koniec=QLabel(self)
        self.label_wynik_przeciwnik=QLabel(self)
        self.label_wynik_przeciwnik_2=QLabel(self)
        

        self.label_wynik.setText(self.parentName)
        self.label_wynik.move(0,0)
        self.label_wynik2.setText(str(self.wynik))
        self.label_wynik2.move(130,0)
        
        self.label_koniec.setText('')
        self.label_koniec.move(200,0)

        self.label_wynik_przeciwnik.setText('Wynik przeciwnika to')
        self.label_wynik_przeciwnik.move(300,0)
        self.label_wynik_przeciwnik_2.setText(str( self.wynikPrzeciwnika))
        self.label_wynik_przeciwnik_2.move(450,0)

        self.label_podpisPix=QLabel(self)
        self.label_podpisPix.setText('.qrc img')
        self.label_podpisPix.move(660,0)
        
        pixmap = QPixmap(":/grafika/smile.jpg")
        pixmapRes = pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio)
        
        imgHolder=QGraphicsPixmapItem()
        imgHolder.setPixmap(pixmapRes)
        imgHolder.moveBy(500,-200)
        self.scene.addItem(imgHolder)
        

        self.addHex()

        pierwszy = QGraphicsRectItem(QtCore.QRectF(self.pozycjeSegmentowWeza[0][0]-5, self.pozycjeSegmentowWeza[0][1]-5, 10, 10))
        pierwszy.setPen(QPen(Qt.green))
        pierwszy.setBrush(QBrush(Qt.green))
        pierwszy.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.scene.addItem(pierwszy)
        # self.segmenty.append(self.scene.addRect(self.pozycjeSegmentowWeza[0][0]-5,self.pozycjeSegmentowWeza[0][1]-5,10,10,QPen(Qt.green),QBrush(Qt.green)))
        self.segmenty.append(pierwszy)
        

        self.generujOwoc()
        self.Frametimer = QtCore.QTimer()
        self.Frametimer.timeout.connect(self.timerFunc)
        self.Frametimer.start(int((1/self.frames)*1000))

        

    def addHex(self):


        a=self.dlugoscBoku
        x=0
        y=0

        for rzad in range(0,self.ilosc_rzedow): 
            for i in range(0,self.w_kolumnie): #nieparzysty
                srodekX=x+i*(a*math.sqrt(3))
                srodekY=y+(3/2)*a*(rzad*2)
                p1=(srodekX-(a*math.sqrt(3)/2),srodekY+a/2)
                p2=(srodekX-(a*math.sqrt(3)/2),srodekY-a/2)
                p3=(srodekX,srodekY-a)
                p4=(srodekX+(a*math.sqrt(3)/2),srodekY-a/2)
                p5=(srodekX+(a*math.sqrt(3)/2),srodekY+a/2)
                p6=(srodekX,srodekY+a)
                punkty=[p1,p2,p3,p4,p5,p6]
                self.pozycjeSrodkowHex.append((srodekX,srodekY))
                for i in range(0,6):
                    if i+1<len(punkty):
                        self.scene.addLine(punkty[i][0],punkty[i][1], punkty[i+1][0],punkty[i+1][1],  QPen(Qt.black))
                    else:
                        self.scene.addLine(punkty[i][0],punkty[i][1], punkty[0][0],punkty[0][1],  QPen(Qt.black))
            
            for i in range(0,self.w_kolumnie): #parzysty
                srodekX=x+i*(a*math.sqrt(3))-a*math.sqrt(3)/2
                srodekY=y+(3/2)*a*(rzad*2+1)
                p1=(srodekX-(a*math.sqrt(3)/2),srodekY+a/2)
                p2=(srodekX-(a*math.sqrt(3)/2),srodekY-a/2)
                p3=(srodekX,srodekY-a)
                p4=(srodekX+(a*math.sqrt(3)/2),srodekY-a/2)
                p5=(srodekX+(a*math.sqrt(3)/2),srodekY+a/2)
                p6=(srodekX,srodekY+a)
                punkty=[p1,p2,p3,p4,p5,p6]
                self.pozycjeSrodkowHex.append((srodekX,srodekY))

                for i in range(0,6):
                    if i+1<len(punkty):
                        self.scene.addLine(punkty[i][0],punkty[i][1], punkty[i+1][0],punkty[i+1][1],  QPen(Qt.black))
                    else:
                        self.scene.addLine(punkty[i][0],punkty[i][1], punkty[0][0],punkty[0][1],  QPen(Qt.black))
        

    
    def ustawWeza(self):
        
        dummy=[]
        self.czyZjadlOwoc()
        kopiaSegmentow=self.pozycjeSegmentowWeza.copy()
        for i in range(0,len(self.pozycjeSegmentowWeza)):
            if i==0:
                nowyX=self.vWeza*math.cos(math.radians(self.katWeza))+self.pozycjeSegmentowWeza[i][0]
                nowyY=self.vWeza*math.sin(math.radians(self.katWeza))+self.pozycjeSegmentowWeza[i][1]
                if nowyX>self.szerokosc_planszy:
                    nowyX=nowyX-self.szerokosc_planszy
                if nowyX<-self.dlugoscBoku:
                    nowyX=nowyX+self.szerokosc_planszy
                if nowyY>self.wysokosc_planszy:
                    nowyY=nowyY-self.wysokosc_planszy
                if nowyY<-self.dlugoscBoku:
                    nowyY=nowyY+self.wysokosc_planszy
                self.pozycjeSegmentowWeza[i]=(nowyX,nowyY)
            
            else:
                nowyX=kopiaSegmentow[i-1][0]
                nowyY=kopiaSegmentow[i-1][1]
                self.pozycjeSegmentowWeza[i]=(nowyX,nowyY)
            

        
        for idx,j in enumerate(self.segmenty):
            dx=self.pozycjeSegmentowWeza[idx][0]-kopiaSegmentow[idx][0]
            dy=self.pozycjeSegmentowWeza[idx][1]-kopiaSegmentow[idx][1]
            j.moveBy(dx,dy)

        self.czyZjadlOgon()
        self.czyZjadlPrzeciwnika()

        self.update()
    def ustawPrzeciwnika(self):
        dummy=[]
        for i in self.pozycjeSegmentowPrzeciwnika:
            segm = QGraphicsRectItem(QtCore.QRectF(i[0]-5, i[1]-5, 10, 10))
            segm.setPen(QPen(Qt.blue))
            segm.setBrush(QBrush(Qt.blue))
            dummy.append(segm)
        for j in self.segmentyPrzeciwnika:
            self.scene.removeItem(j)
        self.segmentyPrzeciwnika=dummy
        for k in self.segmentyPrzeciwnika:
            self.scene.addItem(k)

        
        


        self.update()
    def dodajSegment(self):
        ostatniX=self.pozycjeSegmentowWeza[len(self.pozycjeSegmentowWeza)-1][0]+25*math.cos(math.radians(self.katWeza))
        ostatniY=self.pozycjeSegmentowWeza[len(self.pozycjeSegmentowWeza)-1][1]+25*math.sin(math.radians(self.katWeza))
        self.pozycjeSegmentowWeza.append((ostatniX,ostatniY))

        segm = QGraphicsRectItem(QtCore.QRectF(ostatniX-5, ostatniY-5, 10, 10))
        segm.setPen(QPen(Qt.green))
        segm.setBrush(QBrush(Qt.green))
        segm.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.scene.addItem(segm)
        self.segmenty.append(segm)
        #self.segmenty.append(self.scene.addRect(ostatniX-5,ostatniY-5,10,10,QPen(Qt.green),QBrush(Qt.green)))

    def czyZjadlPrzeciwnika(self):
        
        for j in self.pozycjeSegmentowPrzeciwnika:
            x_przeciwnika=j[0]
            y_przeciwnika=j[1]
            for i in self.pozycjeSegmentowWeza:
                x=i[0]
                y=i[1]
                if x_przeciwnika>x-self.dlugoscBoku/2 and x_przeciwnika<x+self.dlugoscBoku/2 and y_przeciwnika>y-self.dlugoscBoku/2 and y_przeciwnika<y+self.dlugoscBoku/2:
                    self.koniec=1
                    self.wyslij_odbierz()   
    def czyZjadlOgon(self):

        x=self.pozycjeSegmentowWeza[0][0]
        y=self.pozycjeSegmentowWeza[0][1]
        if len(self.pozycjeSegmentowWeza)>1:
            for j in self.pozycjeSegmentowWeza[1:]:
                x_nowe=j[0]
                y_nowe=j[1]
                if x_nowe>x-10 and x_nowe<x+10 and y_nowe>y-10 and y_nowe<y+10:
                    self.koniec=1
                    self.wyslij_odbierz()
    def czyZjadlOwoc(self):

        for i in self.pozycjeSegmentowWeza:
            x=i[0]
            y=i[1]
            if self.owocX>x-self.dlugoscBoku/1.5 and self.owocX<x+self.dlugoscBoku/1.5 and self.owocY>y-self.dlugoscBoku/1.5 and self.owocY<y+self.dlugoscBoku/1.5:
                self.dodajSegment()
                self.scene.removeItem(self.owocek)
                self.generujOwoc()
                self.wynik+=1
                self.label_wynik2.setText(str(self.wynik))

    def generujOwoc(self):
        wybrany=random.choice(self.pozycjeSrodkowHex)
        self.owocek=self.scene.addRect(wybrany[0]-5,wybrany[1]-5,10,10,QPen(Qt.red),QBrush(Qt.red))
        self.owocX=wybrany[0]
        self.owocY=wybrany[1]
    def skrecWLewo(self):
        self.katWeza-=60
    def skrecWPrawo(self):
        self.katWeza+=60
    def keyPressEvent(self, event):
        if event.key()==65:
            self.skrecWLewo()
        if event.key()==68:
            self.skrecWPrawo()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = "Main Window"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 1000
        self.pozycjeSrodkowHex=[]
        self.ipHosta='localhost'
        self.nazwaGracza=''
        self.port=10016
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 

        
        self.createGraphicView()
 
        self.show() 
    def createGraphicView(self):
        self.label_adres=QLabel(self)
        self.label_adres.setText('Adres serwera')
        self.label_adres.move(30,0)
        self.input_adres = QLineEdit(self)
        self.input_adres.setText(self.ipHosta)
        self.input_adres.resize(100,40)
        self.input_adres.move(30,60)

        self.label_nazwa=QLabel(self)
        self.label_nazwa.setText('Nazwa gracza')
        self.label_nazwa.move(150,0)
        self.input_nazwa = QLineEdit(self)
        self.input_nazwa.resize(100,40)
        self.input_nazwa.move(150,60)

        self.label_port=QLabel(self)
        self.label_port.setText('Port')
        self.label_port.move(270,0)
        self.input_port = QLineEdit(self)
        self.input_port.setText(str(self.port))
        self.input_port.resize(100,40)
        self.input_port.move(270,60)


        self.labelWarning=QLabel(self)
        self.labelWarning.setText('')
        self.labelWarning.move(520,30)

        wczytajGre_button = QPushButton('Wczytaj', self)
        wczytajGre_button.clicked.connect(self.wczytajGre)
        wczytajGre_button.move(400,70)
        zapiszGre_button = QPushButton('Zapisz', self)
        zapiszGre_button.clicked.connect(self.zapiszGre)
        zapiszGre_button.move(400,10)
        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.start)
        start_button.move(400,100)
    def start(self):
        if self.input_nazwa.text()!='' and self.input_port.text()!='' and self.input_adres.text()!='':
            self.snakeWin=SnakeWindow(self.input_port.text(),self.input_nazwa.text() ,self.input_adres.text())
        else:
            if self.input_nazwa.text()=='':
                self.labelWarning.setText('Nazwa pusta')
            if self.input_port.text()=='':
                self.labelWarning.setText('Port pusty')
            if self.input_adres.text()=='':
                self.labelWarning.setText('Adres pusty')
        
    def wczytajGre(self):
        myFile=open('settings.json','r+')
        data = json.load(myFile)
        myFile.close()
        self.input_adres.setText(str(data['settings'][0]['host']))
        self.input_port.setText(str(data['settings'][0]['port']))
        self.input_nazwa.setText(str(data['settings'][0]['name']))
    def zapiszGre(self):
        if self.input_nazwa.text()!='' and self.input_port.text()!='' and self.input_adres.text()!='':
            data = {}
            obj={'name':self.input_nazwa.text(),'port':self.input_port.text(),'host':self.input_adres.text()}
            data['settings'] = []
            data['settings'].append(obj)
            myFile=open('settings.json','r+')
            json.dump(data, myFile)
            myFile.close()
        else:
            if self.input_nazwa.text()=='':
                self.labelWarning.setText('Nazwa pusta')
            if self.input_port.text()=='':
                self.labelWarning.setText('Port pusty')
            if self.input_adres.text()=='':
                self.labelWarning.setText('Adres pusty')


 
 
 

App = QApplication(sys.argv)
mainWindow=MainWindow()
#window = SnakeWindow()
sys.exit(App.exec())