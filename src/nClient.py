import socket
import threading
import re
import argparse
import time as T
from tick import *
import sys
from constants import * 
from networkLibrary import * 
import json

class NetworkClient:
    
    def send(self):
        while self.active:
            T.sleep(max(STATE_SYNC_LATENCY,self.parent.latencyMode))
            try:
                sendMessage(self.communicator,str(time())+" "+json.dumps(self.parent.getState()))
            except:
                self.active = False
                self.parent.gui.endMenu.tkraise()

    def recieve(self):
        while self.active:
            try:
                message = recieveMessage(self.communicator)
            except:
                self.active = False
                self.parent.gui.endMenu.tkraise()
                break
            if self.parent.latencyMode:
                T.sleep(self.parent.latencyMode)
            message = json.loads(message)
            print(message)
            self.parent.setState(message)
            cp = self.parent.getGameCopy()
            if(cp.gameEnded):
                self.active = False
                self.parent.gui.endMenu.tkraise()

    def register(self):
        self.communicator   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.communicator.connect((self.server_ip,self.server_port)) 
        recvThread = threading.Thread(target=self.recieve)
        sendThread = threading.Thread(target=self.send)
        recvThread.start()
        sendThread.start()

    def __init__(self,server_ip,server_port,parent):
        self.server_ip = server_ip
        self.server_port = server_port
        self.parent = parent
        self.active = True
        self.register()