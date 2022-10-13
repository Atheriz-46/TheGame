from src.overallState import OverallState
from src.gameMode import GameMode
from src.Network import NetworkServer
 
class Server:
    def __init__(self,**kwargs):
        self.game = OverallState()
        self.gm = GameMode(**kwargs)
        self.network = NetworkServer(game = self.game)
        self.moveList = [] 
        self.moveList.append([])
        self.moveList.append([])
        self.qMutex         = Lock()
        self.sMutex         = Lock()
        self.updateThread   = threading.Thread(target=self.updateState)
        updateThread.start()
        updateState.join()
          
    def updateState(self):
        while(True):
            time.sleep(STATE_SYNC_LATENCY/2)
            self.sMutex.acquire()
            try:
                self.state.updateState(self.parent.moveList[0],self.parent.moveList[1])
                moveList[0] = []
                moveList[1] = []
            finally:
                self.sMutex.release()
    
    def addMoves(self,playerNumber,mList):
        self.qMutex.acquire()
        try:
            for i in mList:
                self.parent.moveList[playerNumber].append(i)
        finally:
            self.qMutex.release()

    def getGameCopy():
        self.sMutex.acquire()
        try:
            cp = self.game.copy()
        finally:
            self.sMutex.release()
        return cp 