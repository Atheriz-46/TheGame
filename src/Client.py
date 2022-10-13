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
        self.updateThread   = threading.Thread(target=self.updateState)
        updateThread.start()
        updateState.join()
        
    def updateState(self):
        while(True):
            time.sleep(STATE_SYNC_LATENCY/2)
            self.sMutex.acquire()
            self.qMutex.acquire()
            try:
                if self.state.me == 0:
                    self.state.updateState(self.eventQueue,[])
                else:
                    self.state.updateState([],self.eventQueue)
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