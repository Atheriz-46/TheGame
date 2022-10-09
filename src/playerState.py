

class PlayerState:
    def __init__(self,parent):
        self.parent = parent
        self.orientation = 0
        self.x,self.y = 0,0
        self.bulletsList = []
        self.bulletLeft = self.parent.gm.maxBullets
        self.health = self.parent.gm.health