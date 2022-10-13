import tkinter as tk


class AskIP(tk.Tk):
    """
    Extends tkinter Window to create a prompt to ask for directory of wiki [DEPRECIATED]
    Args:
        articleName (str): String contains the directory of wiki to be passed back
    """

    def handleSubmit(self):
        """
        Handles when submit button is pressed in UI
        """

        self.str.Port = self.serverPort.get()
        self.str.IP = int(self.serverIP.get())
    
        self.destroy()

    def __init__(self, txt):
        tk.Tk.__init__(self)
        self.str = txt
        self.title("Enter Server Details")
        self.textServerIP = tk.Label(
            master=self, text="IP of your server"
        )
        self.textServerIP.pack(side="left", fill="both", expand=True)
        self.serverIP = tk.Entry(master=self)
        self.serverIP.pack(side="right", fill="both", expand=True)
        self.textServerPort = tk.Label(
            master=self, text="Server Port"
        )
        self.textServerPort.pack(side="left", fill="both", expand=True)
        self.serverPort = tk.Entry(master=self)
        self.serverPort.pack(side="right", fill="both", expand=True)
        self.buttonForDirectory = tk.Button(
            master=self, text="Submit", command = self.handleSubmit
        )
        self.buttonForDirectory.pack(side="bottom")


class ServerData:
    IP = '127.0.0.1'
    Port = 5000