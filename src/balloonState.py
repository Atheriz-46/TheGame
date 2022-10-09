from geometry import * 
from constants import *

class Bullet(Circle):
    def __init__(self,center,otime):
        Circle.__init__(self,center,[0,0],BALLOON_RADIUS,otime)