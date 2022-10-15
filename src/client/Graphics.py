from tkinter import Canvas, Frame
import math

from ..common.constants import *
from ..common.tick import *
class Graphics(Frame):
    def __init__(self,parent):
        """Initialises the Grapics object

        Args:
            parent (tkinter.Frame, tkinter.Tk): Frame/Window object which contains the current
        """
        Frame.__init__(self,master = parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # self.scoreboard  = ScoreBoard(self)
        self.scale = min(self.canvas.winfo_width(),self.canvas.winfo_height())/ARENA_X_BOUNDARY
        self.draw()
        
        
    
    def draw(self):
        """Draws the current state on canvas
        """
        self.master.update()
        self.time = time()
        w,h = self.canvas.winfo_width(),self.canvas.winfo_height()
        self.scale = min(w,h)/ARENA_X_BOUNDARY
        if w>h:
            self.shift_x,self.shift_y = (w-h)/2,0
        else: 
            self.shift_x,self.shift_y = 0,(h-w)/2
       
        state = self.parent.parent.getGameCopy()
        self.canvas.delete("balloon")
        self.canvas.delete("bullet")
        self.canvas.delete("shooter")
        self.draw_balloon(state.balloons)
        self.draw_players(state.players)
        self.parent.scoreboard.updatePoints(state)
        self.canvas.update()
        self.master.after(10,self.draw)

    def draw_balloon(self,balloons):
        """
        Used to draw balloons

        Args:
                balloons (List<Balloon>) : List of balloons objects to be drawn
        """
        for balloon in balloons:
            x,y = balloon.center
            r = balloon.width
            self.circle(x,y,r,'red','balloon')

    def draw_players(self,players):
        """
        Draws players by calling draw_player()

        Args:
            players (List<PlayerState>) : List of players to be drawn
        """
        for idx,player in enumerate(players):
            self.draw_player(player,idx)

    def draw_player(self,player,side):
        """
        Used to draw a player (represented visually by their gun)

        Args:
                player (PlayerState) : Reference to PlayerState object to be drawn
        """
        self.draw_gun(player,side)
        for bullet in player.bulletsList:
            x,y = bullet.getPosition(self.time)
            r = bullet.width
            self.circle(x,y,r,'blue','bullet')
            
        
    def circle(self,x,y,r,fill='blue',tags='bullet'):
        """
        Creates Canvas in shape of a circle

        Args:
            x (float) : x coordinate of circle to be drawn
            y (float) : y coordinate of circle to be drawn
            r (float) : Radius of circle to be drawn
            fill (str) : Colour of circle
            tags (str) : Tag of canvas element
        """
        
        # TODO: Fill the Circle                         
        x,y,r = (x*self.scale+self.shift_x,y*self.scale+self.shift_y,r*self.scale)
        self.canvas.create_oval(x-r,y-r,x+r,y+r,
                                fill=fill,
                                tags=tags,
                                    )      
    def draw_gun(self,player,side):
        """
        Used to draw gun for player

        Args:
                player (PlayerState) : Reference to PlayerState object used to draw their gun
        """
        x,y=player.center
        orientation = player.orientation
        #orientation = player.orientation if side==0 else 180-player.orientation
        x1,y1 = x+  math.cos(orientation*0.0174)*GUN_SIZE,y+math.sin(orientation*0.0174)*GUN_SIZE
        x,y,x1,y1 = (x*self.scale+self.shift_x,y*self.scale+self.shift_y,x1*self.scale+self.shift_x,y1*self.scale+self.shift_y)
        self.canvas.create_line(x,y,x1,y1, fill="black", width=GUN_WIDTH*self.scale,tags='shooter')
    