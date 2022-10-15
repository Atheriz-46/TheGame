from tkinter import LEFT, RIGHT, SUNKEN, X, Frame, Label


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

        self.lbl_leftScore = Label(text = 0, fg = "white" , bg = "black", master = self)
        self.lbl_rightScore = Label(text = 0, fg = "white" , bg = "black", master = self)

        self.lbl_leftScore.pack(fill = X, side = LEFT)
        self.lbl_rightScore.pack(fill = X, side = RIGHT)

        self.grid_rowconfigure(1, weight = 2)
        self.grid_columnconfigure(0, weight = 2)
        self.grid(row = 1, column = 0)

    def updatePoints(self,state):
        """
        Updates player scores to be displayed on the frame labels
        """
        if len(state.players)>=1:
            self.lbl_leftScore.config(text = state.players[0].points)
        if len(state.players)>=2:
            self.lbl_rightScore.config(text = state.players[1].points)