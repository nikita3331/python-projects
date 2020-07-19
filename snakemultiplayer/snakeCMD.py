import numpy as np
import random
from clint.textui import colored
import keyboard  
import os
import time


class Cell():
    def __init__(self,x,y,width,height): #x,y coordinates of center of hex
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.dummyPlansza=[]
        self.apply()
    def apply(self): #wspolrzedne scianek
        self.dummyPlansza=np.zeros([self.width,self.height])
        y=self.y
        x=self.x
        self.dummyPlansza[x-1][y-3]=1
        self.dummyPlansza[x][y-3]=1
        self.dummyPlansza[ x+1][y-3]=1

        self.dummyPlansza[ x-2 ][y-2]=1
        self.dummyPlansza[ x+2][y-2]=1

        self.dummyPlansza[ x-3][y-1]=1
        self.dummyPlansza[ x+3][y-1]=1

        self.dummyPlansza[ x-4][y]=1
        self.dummyPlansza[x+4][y]=1

        self.dummyPlansza[ x-3][y+1]=1
        self.dummyPlansza[ x+3][y+1]=1

        self.dummyPlansza[ x-2][y+2]=1
        self.dummyPlansza[ x+2][y+2]=1

        self.dummyPlansza[ x-1][y+3]=1
        self.dummyPlansza[ x][y+3]=1
        self.dummyPlansza[ x+1][y+3]=1

class Mapa():
    def __init__(self,width,height,klocki):
        self.width=width
        self.height=height
        self.plansza=[]
        self.klocki=klocki
        self.agentsPositions=[]
        self.fruitX=0
        self.fruitY=0
        self.create()
        self.setFruit()
    def create(self):
        self.plansza=np.zeros([self.width,self.height])
        for i in self.klocki:
            self.plansza+=i.dummyPlansza
    def show(self):
        
        for i in range(0,self.height,1):
            for j in range(0,self.width,1):
                if self.plansza[j][i]==0:
                    print(' ',end='')
                if self.plansza[j][i]==1 or self.plansza[j][i]==2 or self.plansza[j][i]==3:
                    print('#',end='')
                if self.plansza[j][i]==4: #snake
                    print(colored.yellow('s'),end='')
                if self.plansza[j][i]==5: #jablko
                    print(colored.red('J'),end='')
                if self.plansza[j][i]==6: #gruszka
                    print(colored.green('G'),end='')
                if self.plansza[j][i]==7: #pomarancza
                    print(colored.yellow('P'),end='')
            print('') #like endline
    def setAgent(self,agent):
        for i in range(0,agent.lengt):
            posX=0
            posY=0
            dire=abs(agent.direction)%6
            if dire==0: #prawo-gora
                posX=agent.x+i
                posY=agent.y-i
            if dire==1: #gora
                posX=agent.x
                posY=agent.y-i
            if dire==2:#lewo-gora
                posX=agent.x-i
                posY=agent.y-i
            if dire==3:#lewo-dol
                posX=agent.x-i
                posY=agent.y+i
            if dire==4: #dol
                posX=agent.x
                posY=agent.y+i
            if dire==5:#prawo-dol
                posX=agent.x+i
                posY=agent.y+i
            self.plansza[posX][posY]=4 #snake sign
            self.agentsPositions.append((posX,posY)) #we append it ,so we can remove them in next move
        wasOnFruit=self.checkAgentFruit()
        return wasOnFruit
    def checkAgentFruit(self): #check if we ate fruit
        onFruit=False
        for i in self.agentsPositions:
            x,y=i
            if x==self.fruitX and y==self.fruitY:
                onFruit=True
                self.setFruit() #add another fruit
        return onFruit


    def removePreviousAgent(self): #delete last positions
        for i in self.agentsPositions:
            x,y=i
            self.plansza[x][y]=0
        self.agentsPositions=[] #clear table,for memory purposes
    def setFruit(self): #pick random center and put random fruit 
        chosenTile=random.choice(self.klocki)
        self.plansza[chosenTile.x][chosenTile.y]=random.choice([5,6,7])
        self.fruitX=chosenTile.x
        self.fruitY=chosenTile.y

class Snake():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.lengt=1 #starting length of snake
        self.direction=0 #prawo-gora, gora,lewo-gora ,lewo-dol ,dol,prawo-dol
        self.width=width
        self.height=height
    def ad(self):
        self.lengt+=1
    def left(self):
        self.direction+=1
    def right(self):
        self.direction-=1
    def move(self):
        dire=abs(self.direction)%6
        if dire==0: #prawo-gora
            self.x+=1
            self.y-=1
        if dire==1: #gora
            self.y-=1
        if dire==2: #lewo-gora
            self.x-=1
            self.y-=1  
        if dire==3: #lewo-dol
            self.x-=1
            self.y+=1
        if dire==4: #dol
            self.y+=1   
        if dire==5: #prawo-dol
            self.x+=1
            self.y+=1
        if self.x<self.lengt: #if we get out of frame,appear on different side
            self.x=self.width+self.x
        if self.x>self.width-self.lengt: 
            self.x=self.width-self.x
        if self.y<self.lengt:
            self.y=self.height+self.y
        if self.y>self.height-self.lengt:
            self.y=self.height-self.y

def ustawKlocki(klockiRzad,klockiKolumna): #put tiles in list of tiles
    klocki=[]
    for j in range(0, klockiKolumna):
        for i in range(0,klockiRzad):
            if i%2==0:
                klocek=Cell(5*(i+1),3+j*6,widthPlanszy,heightPlanszy)
            else:
                klocek=Cell(5*(i+1),6+j*6,widthPlanszy,heightPlanszy)
            klocki.append(klocek)
    return klocki

klockowWRzedzie=10
klockowWKolumnie=3
szerokoscKlocka=9
wysokoscKlocka=7
widthPlanszy=(klockowWRzedzie)*szerokoscKlocka-3*klockowWRzedzie
heightPlanszy=(klockowWKolumnie+1)*wysokoscKlocka-1*klockowWKolumnie
klocki=ustawKlocki(klockowWRzedzie,klockowWKolumnie)
mapka=Mapa(widthPlanszy,heightPlanszy,klocki)

snak=Snake(4,15,widthPlanszy,heightPlanszy)
mapka.setAgent(snak)


def dzialaj():
    endflag=0
    while endflag!=1: 

        if keyboard.is_pressed('x'):  # x sets fruit 
            mapka.setFruit()
        if keyboard.is_pressed('z'):  # z ads snakes element
            snak.ad()
        if keyboard.is_pressed('a'):  # a turns left
            snak.right()
        if keyboard.is_pressed('d'):  # d turns right
            snak.left() 
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('thank you', flush=True)
            endflag=1
            break
        os.system('cls')
        snak.move()
        mapka.removePreviousAgent()
        fruitEaten=mapka.setAgent(snak)
        if fruitEaten:
            snak.ad()
        mapka.show()
        time.sleep(0.3)        

dzialaj()        
        

        
        
        


