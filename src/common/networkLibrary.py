from .constants import FIXED_SIZE
from time import sleep
from threading import Thread,Lock
class messenger:
    def __init__(self):
        self.buffer = []
        self.messageBuffer = []
    def sendMessage(conn, s):
        """
        Used to send message s using Socket conn.
        Handles underflow and overflow of messages.
        Acts as a middle layer between networks buffers and higher level functions.

        Args:
                conn (Socket) : Socket over which message is to be sent
                s (str) : Message to be sent
        """

        s += "%"
        for i in s:
            p += i
            if len(p.encode("utf-16")) >= FIXED_SIZE:
                conn.send(p.encode("utf-16"))
                p = ""
        if len(p):
            conn.send(p.encode("utf-16"))


    def recieveMessage(self,conn):
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
                messageBuffer.pop(0)
                self.rlock.release()
                return p 
            else:
                self.rlock.release()
                sleep(0.05)

            
    def reader(self,conn):
        while True:
            curr = conn.recv(FIXED_SIZE).decode("utf-16") 
            for i in curr:
                if i == '%':
                    self.rlock.acquire()
                    self.messageBuffer.append("".join(self.buffer))
                    self.rlock.release()
                else:
                    self.buffer.append(i)
