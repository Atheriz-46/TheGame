

import json

class OverallState:
    def __init__(self,gameMode):
        self.players = []
        self.balloons = []
        self.gm = gameMode
    
    def addPlayer(self,player):
        if len(self.players)+1 > self.gm.nplayers:
            raise Exception(f"Lobby Full. Lobby limit is {self.gm.nplayers}")
        self.players.append(player)
        
    def getState(self):
        return {'players':[x.getState() for x in self.players], 'balloons': [x.getState() for x in self.balloons]}
    
    def setState(self,state):
        for k,v in state.items():
            for old,new in zip(getattr(self,k),v):
                old.setState(v)
        
            
        