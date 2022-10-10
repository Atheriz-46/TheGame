from tick import *

class Client:

    def __init__(self):
        self.eventQueue = []
        
    def rotateClock(self):
        self.eventQueue.append([time(),'C'])
    
    def rotateAntiClock(self):
        self.eventQueue.append([time(),'A'])