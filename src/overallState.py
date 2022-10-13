import json
from tick               import *
from constants          import *
from playerState        import PlayerState
from random             import random,seed

class OverallState:

    def tickValue(self):
        return currTicks() - self.offset
    
    def __init__(self,gameMode):
        self.players = []
        self.balloons = []
        self.gm = gameMode
        self.offset = currTicks()
        self.me     = 0
    
    def createPlayer(self):
        
        if len(self.players)+1 > self.gm.nplayers:
            raise Exception(f"Lobby Full. Lobby limit is {self.gm.nplayers}")
        
        if len(self.players) == 0:
            player = PlayerState(self,LEFT_CENTER)
            self.players.append(player)
            return [player,0]
        else:
            player = PlayerState(self,RIGHT_CENTER)
            self.players.append(player)
            return [player,1]

    def updateState(self,leftPlayerInputs,rightPlayerInputs):
        
        leftIterator  = 0
        rightIterator = 0

        # Ignore Inputs that occured before the state 
        while leftIterator!=len(leftPlayerInputs):
            if tickValue(leftPlayerInputs[leftIterator][0]) <= self.offset:
                leftIterator+=1
            
        while rightIterator!=len(rightPlayerInputs):
            if tickValue(rightPlayerInputs[rightIterator][0]) <= self.offset:
                rightIterator+=1
        
        #Process Inputs that occured after current state
        while leftIterator!=len(leftPlayerInputs) and rightIterator!=len(rightPlayerInputs): 
            
            next = self.offset + 1

            while leftIterator!=len(leftPlayerInputs) and tickValue(leftPlayerInputs[leftIterator][0])<=next:
                if leftPlayerInputs[leftIterator][1] == 'C':
                    self.players[0].turnClock()
                else: 
                    self.players[0].turnAntiClock()
                leftIterator+=1
            
            while rightIterator!=len(rightPlayerInputs) and tickValue(rightPlayerInputs[rightIterator][0])<=next:
                if rightPlayerInputs[rightIterator][1] == 'A':
                    self.players[1].turnClock()
                else: 
                    self.players[1].turnAntiClock()
                rightIterator+=1 

            self.offset = next

            # shoot if modulo fire rate 

            if self.offset%self.gm.regenBullets==0:
                for currPlayer in self.players:
                    currPlayer.shoot()

            newBalloonList = []
            # Process Bullets hitting Balloons 
            for ballon in self.balloons:
                flag = True 
                for currPlayer in self.players:
                    for bullet in self.bulletsList:
                        if ballon.intersects(bullet,timeFromTick(self.offset)):
                            flag = False
                            currPlayer.points+=1
                if flag:
                    newBalloonList.append(ballon)
            
            self.balloons = newBalloonList
            
            # Generate Balloons 
            while len(self.balloons) < self.gm.balloonCount:
                random.seed(self.gm.balloonSeed)
                x = random.randint(0,655356)%(ARENA_X_BOUNDARY - 2*BALLOON_RADIUS)
                y = random.randint(0,655356)%(ARENA_Y_BOUNDARY - 2*BALLOON_RADIUS)
                newBalloon = Balloon([x,y],timeFromTick(self.offset))
                self.gm.balloonSeed+=1
                canBeInserted = True 
                
                for ballon in self.balloons:
                    if ballon.intersects(newBalloon,0):
                        canBeInserted = False

                for currPlayer in self.players:
                    for bullet in self.bulletsList:
                        if bullet.intersects(newBalloon,timeFromTick(self.offset)):
                            canBeInserted = False

                if canBeInserted:
                    self.balloons.append(newBalloon)
        
        for currPlayer in self.players:
            currPlayer.cleanBullets(timeFromTick(self.offset)-10)
        
    def getState(self):
        # @TODO add gamemode and .me and offset
        return {'players':[x.getState() for x in self.players], 'balloons': [x.getState() for x in self.balloons]}
    
    def setState(self,state):
        for k,v in state.items():
            for old,new in zip(getattr(self,k),v):
                old.setState(new)

    def changeTimeBy(x):

        # change offset 
        self.offset += tickValue(x)
        
        # update balloon
        for balloon in self.balloons:
            balloon.otime += x 

        # update players 
        for player in self.players:
            for bullet in player.bulletList:
                bullet.otime += x 