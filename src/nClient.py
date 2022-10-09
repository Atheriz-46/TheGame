import socket
import threading
import re
import argparse
import time
import sys
from constants import * 

class NetworkClient:
    
    def send(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            self.sender.send(m.encode(self.parent.getState()))
    
    def recieve(self):
        while True:
            message = self.reciever.recv(STATE_MESSAGE_SIZE).decode()
            parent.setState(message)
    
    def register(self):
        self.sender   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender.connect((self.server_ip,self.server_port)) 
        self.reciever.connect((server_ip, PORT))  
        recvThread = threading.Thread(target=self.recieve)
        sendThread = threading.Thread(target=self.send)
        recvThread.start()
        sendThread.start()
        recvThread.join()
        sendThread.join()

    def __init__(self,server_ip,server_port,parent):
        self.server_ip = server_ip
        self.server_port = server_port
        self.parent = parent
        register()