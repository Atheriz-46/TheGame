from geometry import * 
from constants import *

class Bullet(Circle):
	"""	
	Used to create bullet objects which are emitted by players
	"""
    def __init__(self,center,speed,otime, **kwargs):
    	"""
		Args:
				center (List<float>) : Coordinates of Center of bullet
				speed (List<float>) : Speed vector of bullet
				otime (float) : Origin time of the bullet
    	"""
        Circle.__init__(self,center,speed,BULLET_RADIUS,otime)

    def copy(self):
    	"""
		Used to return a copy of this object
    	"""
    	return Bullet(**self.getState())