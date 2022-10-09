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
        self.game = OverallState()
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
            sender_object = Connection(conn,address)
            self.game.addPlayer(sender_object)
            sender_object.start()
            

class Connection(threading.Thread):

    def __init__(self, socket,retAddr,):

        threading.Thread.__init__(self)
        self.communicator = socket
        self.retAddr = retAddr
        self.player = PlayerState()
        
    def run(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            # if self.mode==SENDER:
            #     self.send()
            # else:
            #     self.receive()
            recvThread = threading.Thread(target=self.recieve)
            sendThread = threading.Thread(target=self.send)
            recvThread.start()
            sendThread.start()
            recvThread.join()
            sendThread.join()


    def receive(self):
        while True:
            message = self.communicator.recv(STATE_MESSAGE_SIZE).decode()
            self.player.setState(message)
    def send(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            self.communicator.send(self.player.getState().encode())