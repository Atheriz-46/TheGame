from tkinter import Frame,Label
from PIL import Image, ImageTk
class StartMenu(Frame):
    """StartMenu Page Frame Class

    Inherits:
        Frame : Tkinter Frame Class
    """
    def __init__(self,parent):
        """Initialises Start menu

        Args:
            parent (tkinter.Tk): The parent object(Frame/Window).
        """
        Frame.__init__(self, parent)
        
        self.parent = parent
        image1 = Image.open("./test.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self,image=test)
        label1.image = test
        label1.pack()        
class EndMenu(Frame):
    """EndMenu Page Frame Class

    Inherits:
        Frame : Tkinter Frame Class
    """
    def __init__(self,parent):
        """Initialises Start menu

        Args:
            parent (tkinter.Tk): The parent object(Frame/Window).
        """
        Frame.__init__(self, parent)
        self.parent = parent
        self.L =  Frame(master = self)
        self.W =  Frame(master = self)
        self.T =  Frame(master = self)
        image1 = Image.open("./Lose.png")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self.L,image=test)
        label1.image = test
        label1.grid(row=0, column=0, sticky="nsew")
        image1 = Image.open("./Win.png")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self.W,image=test)
        label1.image = test
        label1.grid(row=0, column=0, sticky="nsew")
        image1 = Image.open("./Tie.png")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self.T,image=test)
        label1.image = test
        label1.grid(row=0, column=0, sticky="nsew")    
        self.L.grid(row=0, column=0, sticky="nsew")  
        self.W.grid(row=0, column=0, sticky="nsew")  
        self.T.grid(row=0, column=0, sticky="nsew")  

    def fix(self):
        self.tkraise()
        t = self.master.parent.state.me 
        if self.master.parent.state.players[t].points < self.master.parent.state.players[1 - t].points:
            self.L.tkraise()
        elif self.master.parent.state.players[t].points > self.master.parent.state.players[1 - t].points:
            self.W.tkraise()
        else:
            self.T.tkraise()
        
