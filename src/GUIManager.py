import math
from threading import Thread
from tkinter import Tk, Canvas, Frame, BOTH,Label
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
        self.parent.quit()
        exit()
    def keyboard(self):
        print(f"Keyboard is on baby")
        self.graphics.canvas.bind("<q>", lambda event: self.parent.turnAntiClock())
        self.graphics.canvas.bind("<e>", lambda event: self.parent.turnClock())
        self.graphics.canvas.bind("<p>", self.exit())
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
        
        self.endMenu.tkraise()
    
                
        
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



class Graphics(Frame):
    def __init__(self,parent):
        Frame.__init__(self,master = parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scale = min(self.canvas.winfo_width(),self.canvas.winfo_height())/ARENA_X_BOUNDARY
        self.draw()
        
        
    
    def draw(self):
        self.master.update()
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
            x,y = bullet.getPosition(time())
            r = bullet.width
            self.circle(x,y,r,'blue','bullet')
            
        
    def circle(self,x,y,r,fill='blue',tags='bullet'):
        # TODO: Fill the Circle                         
        x,y,r = (x*self.scale+self.shift_x,y*self.scale+self.shift_y,r*self.scale)
        self.canvas.create_oval(x-r,y-r,x+r,y+r,
                                fill='blue',
                                tags='bullet',
                                    )      
    def draw_gun(self,player,side):
        x,y=player.center
        # orientation = player.orientation
        orientation = player.orientation if side==0 else 180-player.orientation
        x1,y1 = x+  math.cos(orientation*0.0174)*GUN_SIZE,y+math.sin(orientation*0.0174)*GUN_SIZE
        x,y,x1,y1 = (x*self.scale+self.shift_x,y*self.scale+self.shift_y,x1*self.scale+self.shift_x,y1*self.scale+self.shift_y)
        self.canvas.create_line(x,y,x1,y1, fill="black", width=GUN_WIDTH*self.scale,tags='shooter')
    
    