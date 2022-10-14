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
        for i in self.speed:
            i = round(i,2)
        self.otime   = otime 

    def getPosition(self,currTime):
        timediff = currTime - self.otime 
        # print(self.center,self.speed,timediff)
        return [self.center[0]+self.speed[0]*timediff,self.center[1] + self.speed[1]*timediff]
        #TODO: check:  return [self.center[0]+self.speed[0]*timediff,self.center[1] + self.speed[1]*timediff,self.center[2]]

    def intersects(self,other,currTime):
        if currTime < self.otime or currTime < other.otime: 
            return False
        otherPos =  other.getPosition(currTime)
        myPos    =  self.getPosition(currTime)
        return circleIntersection(*myPos,self.width,*otherPos,other.width)

    def getState(self):
        return {'center':self.center,'width':self.width,'speed':self.speed,'otime':self.otime}
    
    def setState(self):
        for k,v in self.state.items():
            setattr(self,k,v)

    def copy(self):
        return Circle(**self.getState())