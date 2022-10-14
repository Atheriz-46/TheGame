import socket
import threading
import re
import argparse
import time
import sys
from constants import *
from overallState import OverallState
from playerState import PlayerState
import json
class NetworkServer:
    def __init__(self,parent,ip = '127.0.0.1',port = 65432,game=None):
        self.game = game
        self.parent = parent
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = ip,port
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.ip, self.port))
        self.regThread = threading.Thread(target=self.register)
        self.regThread.start()
        # self.regThread.detach()

    def register(self):
        i = 0
        while True:
            
            self.lsock.listen()
            
            conn, address = self.lsock.accept()
            i+=1
            print(f"Connection from {address}, i={i}")
            self.parent.sMutex.acquire()
            try:
                player,playerNumber = self.game.createPlayer()
                sender_object = Connection(self,player,conn,address,self.game,playerNumber)
                sender_object.start()
            finally:
                self.parent.sMutex.release()
            
class Connection(threading.Thread):

    def __init__(self,parent,player, socket,retAddr,game,playerNumber):
        threading.Thread.__init__(self)
        self.communicator = socket
        self.retAddr = retAddr
        self.playerNumber = playerNumber 
        self.player = player
        self.game = game
        self.delta = 0
        self.parent = parent
        
    def run(self):
        recvThread = threading.Thread(target=self.receive)
        sendThread = threading.Thread(target=self.send)
        recvThread.start()
        sendThread.start()
        recvThread.join()
        sendThread.join()


    def receive(self):
        while True:
            message = self.communicator.recv(STATE_MESSAGE_SIZE).decode('utf-16')
            newMessage = message.split(" ",1)
            #TODO: Check if the time is valid
            currTime = float(newMessage[0])
            if self.delta == 0:
                self.delta = time.time() - currTime
            else : 
                self.delta = ALPHA*delta + (1 - ALPHA)*(time.time() - currTime)
            
            moveList = json.loads(newMessage[1])
            for i in moveList:
                i[0] += self.delta
            self.parent.parent.addMoves(self.playerNumber,moveList)

    def send(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            cpState = self.parent.parent.getGameCopy()
            cpState.changeTimeBy(-1*self.delta)
            cpState.me = self.playerNumber
            self.communicator.send(json.dumps(self.game.getState()).encode('utf-16'))