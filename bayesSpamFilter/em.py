import os
import glob
import numpy as np
import re
import pprint
os.chdir('./desktop/wno/spam')
class Message():
    def __init__(self,filem):
        self.fromWho=''
        self.to=''
        self.date=''
        self.subject=''
        self.mess=''
        self.filem=filem
        self.subjectWordsArray=[]
        self.messWordsArray=[]
        self.type=self.filem.split(' ')[0]
        self.read()
    def read(self):
        lines=[]  
        for line in open(self.filem, 'r'):
            words=line.split(':')
            newWord=words[1].rstrip()
            lines.append(newWord)
        self.fromWho=lines[0]
        self.to=lines[1]
        self.date=lines[2]
        self.subject=lines[3] 
        self.mess=lines[4]
        self.subjectWordsArray=self.clearWord(self.subject.split(' '))  
        self.messWordsArray= self.clearWord(self.mess.split(' ')) 
    def show(self):
        print('From:',self.fromWho)
        print('To:',self.to)
        print('Date:',self.date)
        print('Subject:',self.subject)
        print('Message:',self.mess)
    def clearWord(self,arr):
        newArr=[]
        for i in arr:
            tring = re.sub('\s+', '', i)
            newArr.append(tring)
        newArr = [i for i in newArr if i] 
        return newArr
        

def findFiles():
    messagesList=[]
    for file_name in glob.glob('*.txt'):
        messagesList.append(Message(file_name))
    return messagesList
def AllWords(mess):
    allWords_spam=[]
    allWords_ham=[]
    for i in mess:
        if i.type=='ham':
            for j in i.subjectWordsArray:
                allWords_ham.append(j)
            for k in i.messWordsArray:
                allWords_ham.append(k)
        else:
            for j in i.subjectWordsArray:
                allWords_spam.append(j)
            for k in i.messWordsArray:
                allWords_spam.append(k)
    return allWords_ham,allWords_spam
def createDict(mess):
    ham,spam=AllWords(mess)
    my_dict_ham = {i:ham.count(i) for i in ham}
    my_dict_spam = {i:spam.count(i) for i in spam}
    return my_dict_ham,my_dict_spam

def wordisSpam(messages):
    #wzor wzieto stad https://en.wikipedia.org/wiki/Naive_Bayes_spam_filtering
    ham_dict,spam_dict=createDict(messages)
    allWordsInSpam=0
    for key in spam_dict:
        allWordsInSpam+=spam_dict[key]
    allWordsInHam=0
    for key in ham_dict:
        allWordsInHam+=ham_dict[key]
    allMessagesSpam=3/7
    allMessagesHam=4/7
    for i in messages:
        wordsInMessage=[]
        probablitiesArray=[]
        
        for j in i.subjectWordsArray:
            wordsInMessage.append(j)
        for k in i.messWordsArray:
            wordsInMessage.append(k)
        for word in wordsInMessage:  
            word = word.replace(',', '')

            if word in spam_dict or word in ham_dict:
                probaSpam=0
                probaHam=0
                alfa=2
                if word in spam_dict:
                    probaSpam=(spam_dict[word])/(allWordsInSpam)
                if word in ham_dict:
                    probaHam=(ham_dict[word])/(allWordsInHam)  
                fullProbability=(probaSpam*allMessagesSpam+alfa)/(probaSpam*allMessagesSpam+probaHam*allMessagesHam +alfa*2)
                probablitiesArray.append(fullProbability)        
        res='HAM'
        eta=0
        for xx in probablitiesArray:
            eta+=np.log(1-xx)-np.log(xx)
        probFullMessageSpam=1/(1+np.exp(eta) )


        if probFullMessageSpam>0.5:
            res='SPAM'
        print(i.filem,probFullMessageSpam*100,'%','message is',res)
def checkExample(filename,messages):
    examp=Message(filename)

    ham_dict,spam_dict=createDict(messages)

    allWordsInSpam=0
    for key in spam_dict:
        allWordsInSpam+=spam_dict[key]
    allWordsInHam=0
    for key in ham_dict:
        allWordsInHam+=ham_dict[key]
    allMessagesSpam=3/7
    allMessagesHam=4/7

    wordsInMessage=[]
    probablitiesArray=[]
    for j in examp.subjectWordsArray:
        wordsInMessage.append(j)
    for k in examp.messWordsArray:
        wordsInMessage.append(k)
    for word in wordsInMessage:
        word = word.replace(',', '')

        probaSpam=0
        probaHam=0
        fullProbability=0
        
        if word in spam_dict:
            probaSpam=spam_dict[word]/allWordsInSpam
        if word in ham_dict:
            probaHam=ham_dict[word]/allWordsInHam
        if (probaSpam*allMessagesSpam+probaHam*allMessagesHam)!=0:
            alfa=2 #do laplace
            fullProbability=(probaSpam*allMessagesSpam+alfa)/(probaSpam*allMessagesSpam+probaHam*allMessagesHam +alfa*2)
            probablitiesArray.append(fullProbability)

    
    eta=0
    for xx in probablitiesArray:
        eta+=np.log(1-xx)-np.log(xx)
    probFullMessageSpam=1/(1+np.exp(eta) )
    res='HAM'
    if probFullMessageSpam>0.5:
        res='SPAM'
    print(examp.filem,probFullMessageSpam*100,'%','message is',res)

myMessages=findFiles()
wordisSpam(myMessages)
checkExample('example/example.txt',myMessages)

