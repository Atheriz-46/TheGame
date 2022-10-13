class GameMode:
    def __init__(self,velocityBullets = 1,regenBullets= 1,balloonSeed = 800,balloonCount = 20):
        self.velocityBullets = velocityBullets
        self.regenBullets    = regenBullets
        self.balloonSeed     = balloonSeed
        self.balloonCount    = balloonCount

    def getState(self):
    	return {'velocityBullets' : self.velocityBullets, 'regenBullets': self.regenBullets, 'balloonSeed' : self.balloonSeed, 'balloonCount' : self.balloonCount}

    def setState(self, state):

        for k,v in state.items():
        	setattr(self,k,v)		
