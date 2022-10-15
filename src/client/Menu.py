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
        image1 = Image.open("./test.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = Label(master=self,image=test)
        label1.image = test
        label1.pack()
        
