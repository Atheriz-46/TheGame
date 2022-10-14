import socket
import threading
import re
import argparse
import time
import sys
from constants import * 
import json

class NetworkClient:
    
    def send(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            self.communicator.send((str(time.time())+" "+json.dumps(self.parent.getState())).encode('utf-16'))
    
    def recieve(self):
        while True:
            message = self.communicator.recv(STATE_MESSAGE_SIZE).decode()
            self.parent.setState(message)
    
    def register(self):
        self.communicator   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.communicator.connect((self.server_ip,self.server_port)) 
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
        self.register()