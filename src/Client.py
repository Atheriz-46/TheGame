from tick               import *
from src.nClient        import NetworkClient
from src.overallState   import OverallState
from src.gameMode       import GameMode
from threading          import Thread, Lock

class Client:
    
    def __init__(self,server_ip,server_port,velocityBullets,regenBullets,maxBullets,balloonSeed,balloonCount):
        self.eventQueue     = []
        self.qMutex         = Lock()
        self.sMutex         = Lock()
        self.networkManager = NetworkClient(server_ip,server_port,self)
        self.state          = OverallState(GameMode(regenBullets, maxBullets, balloonSeed, balloonCount))
        self.updateThread   = threading.Thread(target=self.updateState)
        updateThread.start()
        updateState.join()
        
    def updateState(self):
        while(True):
            time.sleep(STATE_SYNC_LATENCY/2)
            self.sMutex.acquire()
            try:
                if self.state.me == 0:
                    self.state.updateState(self.eventQueue,[])
                else:
                    self.state.updateState([],self.eventQueue)
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

    def getState():
        self.qMutex.acquire()
        try:
            ret = {x.getState() for x in self.eventQueue}
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