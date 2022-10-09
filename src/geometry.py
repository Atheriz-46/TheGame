from constants import * 

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def circleIntersection(x1,y1,r1,x2,y2,r2):
    return distance(x1,y1,x2,y2) < r1 + r2 + EPSILON 

class Circle:
    def __init__(self,center,speed,width,otime):
        self.center  = center
        self.width   = width
        self.speed   = speed
        self.otime   = otime 

    def position(self,currTime):
        timediff = currTime - otime 
        return [center[0]+speed[0]*timediff,center[1] + speed[1]*timediff,center[2]]

    def intersects(self,other,currTime):
        if currTime < self.otime or currTime < other.otime: 
            return false
        auto otherPos =  other.position(currTime)
        auto myPos    =  self.position(currTime)
        return circleIntersection(*myPos,self.width,*otherPos,other.width)