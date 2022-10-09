

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
        return json.dumps({'players':[x.getState() for x in self.players], 'balloons': [x.getState() for x in self.balloons]})
        