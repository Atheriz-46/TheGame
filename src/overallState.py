

import json

from src.playerState import PlayerState

class OverallState:
    def __init__(self,gameMode):
        self.players = []
        self.balloons = []
        self.gm = gameMode
    
    def createPlayer(self):
        if len(self.players)+1 > self.gm.nplayers:
            raise Exception(f"Lobby Full. Lobby limit is {self.gm.nplayers}")
        player = PlayerState()
        self.players.append(player)
        return player
        
    def getState(self):
        return {'players':[x.getState() for x in self.players], 'balloons': [x.getState() for x in self.balloons]}
    
    def setState(self,state):
        for k,v in state.items():
            for old,new in zip(getattr(self,k),v):
                old.setState(new)
        
            
        