from tkinter import Tk
from Menu import StartMenu,EndMenu
from ScoreBoard import ScoreBoard
from Graphics import Graphics
# import keyboard
class GUIManager(Tk):
    """The main GUI manager class for the game

    Inherited:
        tkinter.Tk : Tkinter Window Class
    """
    def __init__(self,parent):
        """Initialises the GUI Manager class

        Args:
            parent (Client): The client object which contains this object's instance
        """
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
        """Signals start of the game.
        """
        if not self.isStarted:
            self.graphics.tkraise()
            self.isStarted = True
            self.keyboard()
    def exit(self):
        """
        Exits the game
        """
        print("Game Quitted!!")
        exit()
    def keyboard(self):
        """Binds the keyboard control to functions
        """
        print(f"Keyboard is on baby")
        self.graphics.canvas.bind("<Button-1>", lambda event: self.parent.rotateAntiClock())
        self.graphics.canvas.bind("<Button-3>", lambda event: self.parent.rotateClock())  
    
                
        
