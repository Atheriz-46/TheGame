import tkinter as tk
import constants


class AskIP(tk.Tk):
    """
    Extends tkinter Window to create a prompt to ask for IP, Port of the Server and Latency of the connection
    """

    def handleSubmit(self):
        """
        Handles when submit button is pressed in UI
        """
        ip = self.serverIP.get()
        if ip:
            self.str.IP = ip
        p = self.serverPort.get()
        if p:
            self.str.Port = int(p)
        l = self.Latency.get()
        if l:
            self.str.Latency = int(l)
        self.destroy()

    def __init__(self, txt):
        """
        Args:
                txt (ServerData) : Reference to ServerData object
        """
        tk.Tk.__init__(self)
        self.str = txt
        self.title("Enter Server Details")
        self.textServerIP = tk.Label(master=self, text="IP of your server")
        self.textServerIP.pack(side="left", fill="both", expand=True)
        self.serverIP = tk.Entry(master=self)
        self.serverIP.pack(side="left", fill="both", expand=True)
        self.textServerPort = tk.Label(master=self, text="Server Port")
        self.textServerPort.pack(side="left", fill="both", expand=True)
        self.serverPort = tk.Entry(master=self)
        self.serverPort.pack(side="left", fill="both", expand=True)
        self.textLatency = tk.Label(master=self, text="Latency (ms) (Advanced)")
        self.textLatency.pack(side="left", fill="both", expand=True)
        self.Latency = tk.Entry(master=self)
        self.Latency.pack(side="left", fill="both", expand=True)
        self.buttonForDirectory = tk.Button(
            master=self, text="Submit", command=self.handleSubmit
        )
        self.buttonForDirectory.pack(side="right", fill="both")


class ServerData:
    """
    Used to create object to store information about Server Data
    """

    IP = constants.IP
    Port = constants.port
    Latency = 0
