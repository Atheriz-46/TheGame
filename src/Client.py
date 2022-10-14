from GUIManager import GUIManager
from time import sleep
from tick               import *
from nClient            import NetworkClient
from overallState       import OverallState
from gameMode           import GameMode
from threading          import Thread, Lock
from AskIP import AskIP
class Client:
    
    def __init__(self,server_ip,server_port,latencyMode = 0):
        self.eventQueue     = []
        self.qMutex         = Lock()
        self.sMutex         = Lock()
        self.state          = OverallState(GameMode())
        self.latencyMode    = latencyMode
        self.networkManager = NetworkClient(server_ip,server_port,self)
        self.gui = GUIManager(self)
        self.updateThread   = Thread(target=self.updateState)
        self.updateThread.start()
        self.gameStarted = False
        # self.updateThread.join()
        
    def updateState(self):
        while(True):
            sleep(STATE_UPDATE_LATENCY/2)
            self.sMutex.acquire()
            self.qMutex.acquire()
            try:
                if self.state.me == 0:
                    self.state.updateState(self.eventQueue,[])
                else:
                    self.state.updateState([],self.eventQueue)
                if len(self.state.players)>=2:
                    self.gameStarted = True
            finally:
                self.qMutex.release()
                self.sMutex.release()

    def rotateClock(self):
        self.qMutex.acquire()
        try:
            self.eventQueue.append([time(),'C'])
        finally:
            self.qMutex.release()

    def rotateAntiClock(self):
        self.qMutex.acquire()
        try:
            self.eventQueue.append([time(),'A'])
        finally:
            self.qMutex.release()

    def getState(self):
        self.qMutex.acquire()
        try:
            ret = self.eventQueue.copy()
            self.eventQueue = []
        finally:    
            self.qMutex.release()
            return ret 

    def setState(self,state):
        self.sMutex.acquire()
        try:
            self.state.setState(state)   
        finally:
            self.sMutex.release()
    def getGameCopy(self):
        self.sMutex.acquire()
        try:
            cp = self.state.copy()
        finally:
            self.sMutex.release()
        return cp 