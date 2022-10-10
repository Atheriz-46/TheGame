from tick               import *
from src.nClient        import NetworkClient
from src.overallState   import OverallState
from src.gameMode       import GameMode

class Client:

    def __init__(self,server_ip,server_port,velocityBullets,regenBullets,maxBullets,balloonSeed,balloonCount):
        self.eventQueue     = []
        self.networkManager = NetworkClient(server_ip,server_port,self)
        self.state          = OverallState(GameMode(regenBullets, maxBullets, balloonSeed, balloonCount))
 
    def rotateClock(self):
        self.eventQueue.append([time(),'C'])
    
    def rotateAntiClock(self):
        self.eventQueue.append([time(),'A'])

    def getState():
        # TODO clear Queue after doing this 
        return {x.getState() for x in self.eventQueue}

    def setState(self,state):
        self.OverallState.setState(state)