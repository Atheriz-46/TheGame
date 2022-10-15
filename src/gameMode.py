class GameMode:
	"""
	Used to create object to store game parameters
	"""

	def __init__(self,velocityBullets = 10,regenBullets=10,balloonSeed = 800,balloonCount = 20):
		"""
		Args:
				velocityBullets (float) : Velocity of bullets shot by players
				regenBullets (float) : Cooldown for bullet regeneration 
				balloonSeed (float) : Seed for random generation of balloons
				balloonCount (float) : Max number of spawned balloons at any time instant
		"""
		self.velocityBullets = velocityBullets
		self.regenBullets    = regenBullets
		self.balloonSeed     = balloonSeed
		self.balloonCount    = balloonCount

	def getState(self):
		"""
		Used to get state of this object in JSON
		"""
		return {'velocityBullets' : self.velocityBullets, 'regenBullets': self.regenBullets, 'balloonSeed' : self.balloonSeed, 'balloonCount' : self.balloonCount}

	def setState(self, state):
		"""
		Used to set attributes of this object from JSON format

		Args:
				state (Dict<str, Object>) : Object state to be set in JSON format
		"""
		for k,v in state.items():
			setattr(self,k,v)	
   
	def copy(self):
		"""
        Returns a copy of this object

        """
		return GameMode(**self.getState())
