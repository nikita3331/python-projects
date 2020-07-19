import socket
import os
from threading import Thread
import threading
import pickle
import time
#cd C:\Users\Nikita\Desktop\snakeMulti & python server.py
clients = set()
clients_lock = threading.Lock()
def listener(client, address):
    print ("Accepted connection from: ", address)
    koniec=0
    with clients_lock:
        clients.add(client)
    try:
        while True:
            if client:
                data = client.recv(1024)
                time.sleep(0.1)
                if not data:
                    break
                else:
                    with clients_lock:
                        for c in clients:
                            c.sendall(data)
            else:
                break
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()

#host = socket.gethostname()
host = 'localhost'
port = 10016

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []

while True:
    print ("Server is listening for connections...")
    client, address = s.accept()
    th.append(Thread(target=listener, args = (client,address)).start())

s.close()
