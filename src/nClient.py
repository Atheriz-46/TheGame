import socket
import threading
import re
import argparse
import time
import sys

class NetworkClient:
    def register(self,,uid):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect((self.server_ip,self.server_port))
        t1 = threading.Thread(target=send,args=(sender,uid))
        t2 = threading.Thread(target=recieve,args=(reciever,sender,uid))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def __init__(self,server_ip,server_port):
        self.server_ip = server_ip
        self.server_port = server_port