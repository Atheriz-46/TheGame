from src.overallState import OverallState
from src.gameMode import GameMode
from src.Network import NetworkServer

class Server:
    def __init__(self,**kwargs):
        self.game = OverallState()
        self.gm = GameMode(**kwargs)
        self.network = NetworkServer(game = self.game)
        
        
    def mergeState(self):
        pass
    