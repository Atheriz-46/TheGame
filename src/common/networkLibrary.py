from .constants import FIXED_SIZE
from time import sleep
from threading import Thread,Lock
class messenger:
    """Handles the message sending and recieving over a socket"""
    def __init__(self,conn,latency = 0):
        self.buffer = []
        self.messageBuffer = []
        self.conn = conn
        self.latency = latency
        self.rlock = Lock()
        self.readThread = Thread(target=self.reader)
        self.readThread.start()
    def sendMessage(self,sock,s):
        """
        Used to send message s using Socket conn.
        Handles underflow and overflow of messages.
        Acts as a middle layer between networks buffers and higher level functions.

        Args:
                conn (Socket) : Socket over which message is to be sent
                s (str) : Message to be sent
        """

        s += "%"
        p = ""
        for i in s:
            p += i
            if len(p.encode("utf-8")) >= FIXED_SIZE:
                self.conn.send(p.encode("utf-8"))
                p = ""
        if len(p):
            self.conn.send(p.encode("utf-8"))


    def recieveMessage(self,sock):
        """
        Used to receive messages over Socket conn

        Args:
                conn (Socket) : Socket over which messages are to be received
        """
        s = ""
        while True:
            self.rlock.acquire()
            if len(self.messageBuffer):
                p = self.messageBuffer[0]
                # print(p)
                self.messageBuffer.pop(0)
                self.rlock.release()
                return p 
            else:
                self.rlock.release()
                sleep(0.01)
            
    def reader(self):
        """Used to read the messages and store them in a buffer"""

        while True:
            curr = self.conn.recv(FIXED_SIZE).decode("utf-8") 
            if self.latency:
                sleep(self.latency)
            # print(curr)
            for i in curr:
                if i == '%':
                    self.rlock.acquire()
                    self.messageBuffer.append("".join(self.buffer))
                    self.buffer = []
                    self.rlock.release()
                else:
                    self.buffer.append(i)
