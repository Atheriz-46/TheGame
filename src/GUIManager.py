import math
import tkinter as tk
from threading import Thread
from tkinter import Tk, Canvas, Frame, BOTH,Label, SUNKEN, LEFT, RIGHT, X
from tick import *
from constants import *
# import keyboard
from PIL import Image, ImageTk
class GUIManager(Tk):
    def __init__(self,parent):
        Tk.__init__(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.scoreboard = ScoreBoard(self)        
        self.graphics = Graphics(self)
        self.graphics.grid(row=0, column=0, sticky="nsew")
        self.endMenu = EndMenu(self)
        self.endMenu.grid(row=0, column=0, sticky="nsew")
        self.startMenu = StartMenu(self)
        self.startMenu.grid(row=0, column=0, sticky="nsew")
        self.isStarted = False

    def startGame(self):
        if not self.isStarted:
            self.graphics.tkraise()
            # self.keyboardThread   = Thread(target=self.keyboard)
            # self.keyboardThread.start()
            self.isStarted = True
            self.keyboard()
    def exit(self):
        # self.parent.quit()
        print("Game Quitted!!")
        exit()
    def keyboard(self):
        print(f"Keyboard is on baby")
        self.graphics.canvas.bind("<Button-1>", lambda event: self.parent.rotateAntiClock())
        self.graphics.canvas.bind("<Button-3>", lambda event: self.parent.rotateClock())  
       
        # while True:
        #     try:
        #         if keyboard.is_pressed('q'):
        #             print('Q')
        #             self.parent.turnAntiClock()
        #         elif keyboard.is_pressed('e'):
        #             print('E')
        #             self.parent.turnClock()
        #         elif keyboard.is_pressed('p'):
        #             print('P')
        #             self.parent.quit()
        #             break
        #     except:
        #         pass
        
        # self.endMenu.tkraise()
    
                
        
class StartMenu(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        image1 = Image.open("./test.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self,image=test)
        label1.image = test
        label1.pack()        
class EndMenu(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent
        image1 = Image.open("./test.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self,image=test)
        label1.image = test
        label1.pack()

class ScoreBoard(Frame):
    """
    Creates Frame to display player points
    """
    def __init__(self,parent):

        """
        Args:
                parent (GUIManager) : Reference to GUIManager master window into which ScoreBoard is packed
        """

        Frame.__init__(self,master = parent,relief=SUNKEN, borderwidth=1)
        self.parent = parent

        self.lbl_leftScore = Label(text = self.parent.parent.state.players[0].points, fg = "white" , bg = "black", master = self)
        self.lbl_rightScore = Label(text = self.parent.parent.state.players[1].points, fg = "white" , bg = "black", master = self)

        self.lbl_leftScore.pack(fill = tk.X, side = LEFT)
        self.lbl_rightScore.pack(fill = tk.X, side = RIGHT)

        self.grid_rowconfigure(1, weight = 2)
        self.grid_columnconfigure(0, weight = 2)
        self.grid(row = 1, column = 0)

    def updatePoints(self):
        """
        Updates player scores to be displayed on the frame labels
        """
        self.lbl_leftScore.config(text = self.parent.parent.state.players[0].points)
        self.lbl_rightScore.config(text = self.parent.parent.state.players[1].points)

class Graphics(Frame):
    def __init__(self,parent):
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
        self.parent.scoreboard.updatePoints()
        self.canvas.update()
        self.master.after(10,self.draw)

    def draw_balloon(self,balloons):
        for balloon in balloons:
            x,y = balloon.center
            r = balloon.width
            self.circle(x,y,r,'red','balloon')
    def draw_players(self,players):
        for idx,player in enumerate(players):
            self.draw_player(player,idx)
    def draw_player(self,player,side):
        self.draw_gun(player,side)
        for bullet in player.bulletsList:
            x,y = bullet.getPosition(self.time)
            r = bullet.width
            self.circle(x,y,r,'blue','bullet')
            
        
    def circle(self,x,y,r,fill='blue',tags='bullet'):
        # TODO: Fill the Circle                         
        x,y,r = (x*self.scale+self.shift_x,y*self.scale+self.shift_y,r*self.scale)
        self.canvas.create_oval(x-r,y-r,x+r,y+r,
                                fill=fill,
                                tags=tags,
                                    )      
    def draw_gun(self,player,side):
        x,y=player.center
        orientation = player.orientation
        #orientation = player.orientation if side==0 else 180-player.orientation
        x1,y1 = x+  math.cos(orientation*0.0174)*GUN_SIZE,y+math.sin(orientation*0.0174)*GUN_SIZE
        x,y,x1,y1 = (x*self.scale+self.shift_x,y*self.scale+self.shift_y,x1*self.scale+self.shift_x,y1*self.scale+self.shift_y)
        self.canvas.create_line(x,y,x1,y1, fill="black", width=GUN_WIDTH*self.scale,tags='shooter')
    
    