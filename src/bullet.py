from geometry import * 
from constants import *

class Bullet(Circle):
    def __init__(self,center,speed,width,otime):
        Circle.__init__(self,center,speed,width,otime)
        self.power = round(width/BULLET_RADIUS_MULTIPLIER)