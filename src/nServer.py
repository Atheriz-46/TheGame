import socket
import threading
import re
import argparse
import time
import sys
from constants import *

class NetworkServer:
    def __init__(self,ip = '127.0.0.1',port = 65432):
        # self.port = port
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = ip,port
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.ip, self.port))


        # self.server.bind(('
    def register(self):

        while True:
            self.lsock.listen()
            conn, address = self.lsock.accept()
            # message = conn.recv(STATE_MESSAGE_SIZE).decode()
            sender_object = Connection(conn,address,SENDER)
            sender_object.start()
            receiver_object = Connection(conn,address,RECEIVER)
            receiver_object.start()
    
            

class Connection(threading.Thread):

    def __init__(self, socket,retAddr,mode):

        threading.Thread.__init__(self)
        self.socket = socket
        self.retAddr = retAddr
        self.mode = mode
        
    def run(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            if self.mode==SENDER:
                self.send()
            else:
                self.receive()
        

    def receive(self):
        while True:
            message = self.reciever.recv(STATE_MESSAGE_SIZE).decode()
            self.parent.setState(message)
    def send(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            self.sender.send(m.encode(self.parent.getState()))