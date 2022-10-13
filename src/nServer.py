import socket
import threading
import re
import argparse
import time
import sys
from constants import *
from overallState import OverallState
from playerState import PlayerState

class NetworkServer:
    def __init__(self,parent,ip = '127.0.0.1',port = 65432,game=None):
        # self.port = port
        self.game = game
        self.parent = parent
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = ip,port
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.ip, self.port))

        # self.server.bind(('
    def register(self):

        while True:
            self.lsock.listen()
            conn, address = self.lsock.accept()
            self.parent.sMutex.acquire()
            try:
                player,playerNumber = self.game.createPlayer()
                sender_object = Connection(player,conn,address,self.game,playerNumber)
                sender_object.start()
            finally:
                self.sMutex.release()
            
class Connection(threading.Thread,player_id):

    def __init__(self,player, socket,retAddr,game,playerNumber):
        threading.Thread.__init__(self)
        self.communicator = socket
        self.retAddr = retAddr
        self.playerNumber = playerNumber 
        self.player = player
        self.game = game
        self.delta = 0
        
    def run(self):
        recvThread = threading.Thread(target=self.recieve)
        sendThread = threading.Thread(target=self.send)
        recvThread.start()
        sendThread.start()
        recvThread.join()
        sendThread.join()


    def receive(self):
        while True:
            message = self.communicator.recv(STATE_MESSAGE_SIZE).decode()
            newMessage = message.split(" ",2)
            currTime = int(newMessage[0])
            if self.delta == 0:
                delta = time.time() - currTime
            else : 
                delta = ALPHA*delta + (1 - ALPHA)*(time.time() - currTime)
            moveList = [] # get from newMessage[1]
            # update timestamps in moveList  
            self.parent.addMoves(self.playerNumber,moveList)

    def send(self):
        while True:
            time.sleep(STATE_SYNC_LATENCY)
            cpState = self.parent.getGameCopy()
            cpState.changeTimeBy(self.delta)
            cpState.me = self.playerNumber
            self.communicator.send(self.game.getState().encode('utf-8'))