import json
from tick               import *
from constants          import *
from playerState        import PlayerState
from random             import random,seed,randint
from balloonState       import Balloon
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
        
        if len(self.players)+1 > N_PLAYERS:
            raise Exception(f"Lobby Full. Lobby limit is {N_PLAYERS}.\n Current Players in Lobby : {len(self.players)}")
        
        if len(self.players) == 0:
            player = PlayerState(self,LEFT_CENTER)
            self.players.append(player)
            return player,0
        else:
            player = PlayerState(self,RIGHT_CENTER)
            self.players.append(player)
            return player,1

    def updateState(self,leftPlayerInputs,rightPlayerInputs):
        if len(self.players) < 2:
            return 
        
        leftIterator  = 0
        rightIterator = 0

        # Ignore Inputs that occured before the state 
        while leftIterator!=len(leftPlayerInputs) and tickValue(leftPlayerInputs[leftIterator][0]) <= self.offset:
            leftIterator+=1
            
        while rightIterator!=len(rightPlayerInputs) and tickValue(rightPlayerInputs[rightIterator][0]) <= self.offset:
            rightIterator+=1
            

        #Process Inputs that occured after current state
        changed = 0
        while leftIterator!=len(leftPlayerInputs) or rightIterator!=len(rightPlayerInputs) or changed<2:

            changed += 1 
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
            for balloon in self.balloons:
                flag = True 
                for currPlayer in self.players:
                    for bullet in currPlayer.bulletsList:
                        if balloon.intersects(bullet,timeFromTick(self.offset)):
                            flag = False
                            currPlayer.points+=1
                if flag:
                    newBalloonList.append(balloon)
            
            self.balloons = newBalloonList
            
            # Generate Balloons 
            while len(self.balloons) < self.gm.balloonCount:
                seed(self.gm.balloonSeed)
                x = randint(0,655356)%(ARENA_X_BOUNDARY - 2*BALLOON_RADIUS)
                y = randint(0,655356)%(ARENA_Y_BOUNDARY - 2*BALLOON_RADIUS)
                newBalloon = Balloon([x,y],timeFromTick(self.offset))
                self.gm.balloonSeed+=1
                canBeInserted = True 
                
                for ballon in self.balloons:
                    if ballon.intersects(newBalloon,0):
                        canBeInserted = False

                for currPlayer in self.players:
                    for bullet in currPlayer.bulletsList:
                        if bullet.intersects(newBalloon,timeFromTick(self.offset)):
                            canBeInserted = False

                if canBeInserted:
                    self.balloons.append(newBalloon)
        
        for currPlayer in self.players:
            currPlayer.cleanBullets(timeFromTick(self.offset)-10)
        
    def getState(self):
        return {'players':[x.getState() for x in self.players], 'balloons': [x.getState() for x in self.balloons], 'offset' : self.offset, 'me': self.me, 'gm' : self.gm.getState()}
    
    def setState(self,state):

        for k, v in state.items():
            if (k == 'gm'):
                # Potential Error
                getattr(self, k).setState(v)

            elif (k in ['offset', 'me']):
                setattr(self, k, v)

            elif (k == 'balloons'):
                newBalloons = []
                for i in v:
                    newBalloons.append(Balloon(**i))
                setattr(self, k, newBalloons)
            
            elif k=='players':
                newPlayers = []
                for i in v:

                    player = PlayerState(self, [0,0])
                    player.setState(i)
                    newPlayers.append(player)

                setattr(self, k, newPlayers)


    def changeTimeBy(self,x):

        # change offset 
        self.offset += tickValue(x)
        
        # update balloon
        for balloon in self.balloons:
            balloon.otime += x 

        # update players 
        for player in self.players:
            for bullet in player.bulletsList:
                bullet.otime += x 
    
    def copy(self):
        players = [x.copy() for x in self.players]
        balloons = [x.copy() for x in self.balloons]
        
        gm = self.gm.copy()
        cop = OverallState(gm)
        for k,v in zip(['players','balloons','offset','me'],[players,balloons,self.offset,self.me]):
            setattr(cop,k,v)
        return cop
        