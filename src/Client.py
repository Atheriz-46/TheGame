from GUIManager import GUIManager
from tick               import *
from nClient            import NetworkClient
from overallState       import OverallState
from gameMode           import GameMode
from threading          import Thread, Lock

class Client:
    
    def __init__(self,server_ip,server_port):
        self.eventQueue     = []
        self.qMutex         = Lock()
        self.sMutex         = Lock()
        self.networkManager = NetworkClient(server_ip,server_port,self)
        self.state          = OverallState(GameMode())
        self.updateThread   = Thread(target=self.updateState)
        self.updateThread.start()
        self.updateState.join()
        self.gui = GUIManager(self)
        
    def updateState(self):
        while(True):
            time.sleep(STATE_SYNC_LATENCY/2)
            self.sMutex.acquire()
            try:
                if self.state.me == 0:
                    self.state.updateState(self.eventQueue,[])
                else:
                    self.state.updateState([],self.eventQueue)
                if len(self.state.players)>=2:
                    self.gui.startGame()
            finally:
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
            ret = [x.getState() for x in self.eventQueue]
            self.eventQueue = []
        finally:
            self.qMutex.release()
            return ret 

    def setState(self,state):
        self.sMutex.acquire()
        try:
            self.OverallState.setState(state)   
        finally:
            self.sMutex.release()
    def getGameCopy(self):
        self.sMutex.acquire()
        try:
            cp = self.game.copy()
        finally:
            self.sMutex.release()
        return cp 