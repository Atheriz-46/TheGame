from overallState   import OverallState
from gameMode       import GameMode
from nServer        import NetworkServer
from threading      import Thread, Lock
from tick           import *
from time           import sleep
class Server:
    """
    Class to handle overall Server operations.
    """
    def __init__(self,ip = '127.0.0.1',port = 65432,**kwargs):
        """Initializer for Server

        Args:
            ip (str, optional): IP address for the server. Defaults to '127.0.0.1'.
            port (int, optional): Port to start the register socket on. Defaults to 65432.
        """
        self.gm = GameMode(**kwargs)
        self.leftGame = 0
        self.game = OverallState(self.gm)
        self.moveList = [] 
        self.moveList.append([])
        self.moveList.append([])
        self.qMutex         = Lock()
        self.sMutex         = Lock()
        self.lMutex         = Lock()
        self.network = NetworkServer(parent = self,game = self.game,ip = ip, port = port)
        self.updateThread   = Thread(target=self.updateState)
        self.updateThread.start()
        self.updateThread.join()
        
    def vacate(self):
        """
        Cleans the server after the game is over.
        """
        self.lMutex.acquire()
        try:
            self.leftGame+=1
            if self.leftGame==2:
                self.leftGame = 0
                self.flush()
        finally:
            self.lMutex.release()
        
    def updateState(self):
        """
        Updates the overall state of the game.
        """
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
        """Adds moves to the queues of both the players.

        Args:
            playerNumber (int): Denotes the index of the player
            mList (list[(float,str)]): time stamped moves list.
        """
        self.qMutex.acquire()
        try:
            for i in mList:
                self.moveList[playerNumber].append(i)
        finally:
            self.qMutex.release()

    def flush(self):
        """
        Cleans the server moves list
        """
        self.sMutex.acquire()
        self.qMutex.acquire()
        try:
            self.game = OverallState(self.gm)
            self.moveList[0] = []
            self.moveList[1] = []
        finally:
            self.qMutex.release()
            self.sMutex.release()

    def getGameCopy(self):
        """Creates a copy of the game. It is thread safe.

        Returns:
            Server: a copy of the current server class.
        """
        self.sMutex.acquire()
        try:
            cp = self.game.copy()
        finally:
            self.sMutex.release()
        return cp 