from geometry import * 
from constants import *

class Balloon(Circle):
    def __init__(self,center,otime,**kwargs):
        Circle.__init__(self,center,[0,0],BALLOON_RADIUS,otime)

    def copy(self):
    	return Balloon(**self.getState())