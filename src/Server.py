from overallState   import OverallState
from gameMode       import GameMode
from nServer        import NetworkServer
from threading      import Thread, Lock
from tick           import *
from time           import sleep
class Server:
    def __init__(self,ip = '127.0.0.1',port = 65432,**kwargs):
        self.gm = GameMode(**kwargs)
        self.game = OverallState(self.gm)
        self.moveList = [] 
        self.moveList.append([])
        self.moveList.append([])
        self.qMutex         = Lock()
        self.sMutex         = Lock()
        self.network = NetworkServer(parent = self,game = self.game,ip = ip, port = port)
        self.updateThread   = Thread(target=self.updateState)
        self.updateThread.start()
        self.updateThread.join()
          
    def updateState(self):
        while(True):
            sleep(STATE_UPDATE_LATENCY/2)
            self.sMutex.acquire()
            self.qMutex.acquire()
            try:
                self.game.updateState(self.moveList[0],self.moveList[1])
                self.moveList[0] = []
                self.moveList[1] = []
            finally:
                self.qMutex.release()
                self.sMutex.release()
    
    def addMoves(self,playerNumber,mList):
        self.qMutex.acquire()
        try:
            for i in mList:
                self.moveList[playerNumber].append(i)
        finally:
            self.qMutex.release()

    def getGameCopy(self):
        self.sMutex.acquire()
        try:
            cp = self.game.copy()
        finally:
            self.sMutex.release()
        return cp 