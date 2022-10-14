import socket
import threading
import re
import argparse
import time as T
from tick import *
import sys
from constants import * 
import json

class NetworkClient:
    
    def send(self):
        while True:
            T.sleep(max(STATE_SYNC_LATENCY,self.parent.latencyMode))
            self.communicator.send((str(time())+" "+json.dumps(self.parent.getState())).encode('utf-16'))
    
    def recieve(self):
        while True:
            message = self.communicator.recv(STATE_MESSAGE_SIZE).decode('utf-16')
            if self.parent.latencyMode:
                T.sleep(self.parent.latencyMode)
            message = json.loads(message)
            self.parent.setState(message)
    
    def register(self):
        self.communicator   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.communicator.connect((self.server_ip,self.server_port)) 
        recvThread = threading.Thread(target=self.recieve)
        sendThread = threading.Thread(target=self.send)
        recvThread.start()
        sendThread.start()
        # recvThread.detach()
        # sendThread.detach()

    def __init__(self,server_ip,server_port,parent):
        self.server_ip = server_ip
        self.server_port = server_port
        self.parent = parent
        self.register()