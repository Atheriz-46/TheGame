from src.overallState import OverallState
from src.gameMode import GameMode
from src.Network import NetworkServer

# Needs to update timestamps in returing state and also .me character 
# add a timestamp before message 
class Server:
    def __init__(self,**kwargs):
        self.game = OverallState()
        self.gm = GameMode(**kwargs)
        self.network = NetworkServer(game = self.game)
          
    def mergeState(self):
        # TODO Finish merger and add a lock for Overall State 
        pass