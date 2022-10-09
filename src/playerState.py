

class PlayerState:
    def __init__(self,parent):
        self.parent = parent
        self.orientations = []
        self.x,self.y,self.t = [],[],[]
        self.bulletsList = []
        self.bulletLeft = self.parent.gm.maxBullets
        self.points = 0
        
    def getState(self):
        return {k: getattr(self,k) if k!='bulletsList' else getattr(self,k).getState() for k in ['point','x','y','t','orientations','bulletsList','bulletLeft'] }
    
    def setState(self,state):
        for k,v in state.items():
            if k=='bulletList':
                getattr(self,k).setState(v)
            else:
                setattr(self,k,v)
                
        