import time

class Circle:
    def __init__(self,center,speed,otime):
        self.center  = center
        self.speed   = speed
        self.otime   = otime 

    def position(self):
        timediff = time.time - otime 
        return [center[0]+speed[0]*timediff,center[1] + speed[1]*timediff,center[2]]

    def intersects(self,other):
        