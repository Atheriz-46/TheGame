from geometry import * 
from constants import *

class Bullet(Circle):
    def __init__(self,center,speed,otime, **kwargs):
        Circle.__init__(self,center,speed,BULLET_RADIUS,otime)

    def copy(self):
    	return Bullet(**self.getState())