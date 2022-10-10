from geometry import * 
from constants import *

class Bullet(Circle):
    def __init__(self,center,speed,otime):
        Circle.__init__(self,center,speed,BULLET_RADIUS,otime)