import math
from tick import * 
from constants import *
from bullet import Bullet

class PlayerState:
    def __init__(self,parent,center):
        self.parent = parent
        self.center = center 
        self.orientation = 45
        self.bulletsList = []
        self.points = 0

    def cleanBullets(self,x):
        newBulletList = []
        for i in self.bulletsList:
            if i.otime > x:
                newBulletList.append(i)
        self.bulletsList = newBulletList 

    def shoot(self):
        newBullet = Bullet(self.center,[math.cos(self.orientation*0.0174)*BULLET_SPEED,math.sin(self.orientation*0.0174)*BULLET_SPEED], timeFromTick(self.parent.offset))
        self.bulletsList.append(newBullet)

    def turnClock(self):
        self.orientation += SENSTIVITY  
        self.orientation = min(90,self.orientation) 

    def turnAntiClock(self):
        self.orientation -= SENSTIVITY
        self.orientation = max(0,self.orientation) 

    def getState(self):
        # @TODO fix this  
        return {k: getattr(self,k) if k!='bulletsList' else [ getattr(self,k)[i].getState() for i in range(len(getattr(self,k))) ] for k in ['points','orientation','bulletsList','center'] }
    
    def setState(self,state):
        for k,v in state.items():
            if k=='bulletsList':
                newBulletList = []
                for i in v :
                    newBulletList.append(Bullet(**i))

                setattr(self,k, newBulletList)

            else:
                setattr(self,k,v)
                
    def copy(self):
        bulletList = [x.copy() for x in self.bulletsList]
        cop = PlayerState(self.parent,self.center.copy())
        for k,v in zip(['points','orientation','bulletsList'],[self.points,self.orientation,bulletList]):
            setattr(cop,k,v)
        return cop