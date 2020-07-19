import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication,QLineEdit,QMessageBox
import socket
import sys
import json
import pickle
from threading import Thread
soket=0
polaczenie=0
stop_flaga=0
import sched, time


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 600
        self.height = 600
        self.initUI()
        self.polaczono=0
        self.dummy=0
    def initUI(self):
        self.textbox_wiadomosc = QLineEdit(self)
        self.textbox_wiadomosc.move(100, 100)
        self.textbox_wiadomosc.resize(100,40)
        self.textbox_wiadomosc.setText('halko')

        self.textbox_port = QLineEdit(self)
        self.textbox_port.move(220, 100)
        self.textbox_port.resize(100,40)
        self.textbox_port.setText('10016')

        self.textbox_id = QLineEdit(self)
        self.textbox_id.move(340, 100)
        self.textbox_id.resize(100,40)
        self.textbox_id.setText('bolek')

        qbtn = QPushButton('Wyslij ', self)
        qbtn.clicked.connect(self.on_click_wyslij)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(100, 70)

        qbtn_polacz = QPushButton('Polacz ', self)
        qbtn_polacz.clicked.connect(self.on_click_polacz)
        qbtn_polacz.resize(qbtn_polacz.sizeHint())
        qbtn_polacz.move(220, 70)

        qbtn_id = QPushButton('Dodaj ID ', self)
        qbtn_id.clicked.connect(self.on_click_dodaj_id)
        qbtn_id.resize(qbtn_id.sizeHint())
        qbtn_id.move(340, 70)

        qbtn_stop = QPushButton('Stop', self)
        qbtn_stop.clicked.connect(self.on_click_stop)
        qbtn_stop.resize(qbtn_stop.sizeHint())
        qbtn_stop.move(200, 150)


        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('tcp/ip')
        self.show()
    def on_click_wyslij(self):
        wartosc = self.textbox_wiadomosc.text()
        self.wyslij(wartosc)
        self.textbox_wiadomosc.setText("")
    def on_click_stop(self):
        global stop_flaga
        stop_flaga=1
    def on_click_polacz(self):
        port = self.textbox_port.text()
        self.polacz_z_serwerem(int(port))

    def on_click_dodaj_id(self):
        self.id = self.textbox_id.text()

    def polacz_z_serwerem(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)
        global soket
        soket=self.sock
        self.polaczono=1
        global polaczenie
        polaczenie=1
    def wyslij(self,wiadomosc):
        try:
            if str(self.id)=="":
                self.id="zero"
            message=str.encode(str(self.id)+' '+wiadomosc)
            self.sock.sendall(message)
        finally:
             self.dummy=self.dummy+1
def wlacz_apke():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

def zczytuj():
    global polaczenie
    global soket  #bierzemy info z pyqt
    if polaczenie==1:
        data = soket.recv(1024)
        print( repr(data))
if __name__ == '__main__':
    th=Thread(target=wlacz_apke).start()
#cd desktop & python qt.py
    while stop_flaga!=1:
        czytanie=Thread(target=zczytuj, daemon=True).start()
    print('skonczylismy')
