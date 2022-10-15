import socket
import threading
import re
import argparse
import time as T
from common.tick import *
import sys
from common.constants import *
from common.overallState import OverallState
from common.playerState import PlayerState
from common.networkLibrary import *
import json


class NetworkServer:
    """
    Handles the network layer of Server.
    """

    def __init__(self, parent, ip="127.0.0.1", port=65432, game=None):
        self.game = game
        self.parent = parent
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = ip, port
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.ip, self.port))
        self.regThread = threading.Thread(target=self.register)
        self.regThread.start()
        # self.regThread.detach()

    def register(self):
        """Registers the listening socket of the server to accept new connections"""
        i = 0
        while True:

            self.lsock.listen()

            conn, address = self.lsock.accept()
            i += 1
            print(f"Connection from {address}, i={i}")
            self.parent.sMutex.acquire()
            try:
                player, playerNumber = self.game.createPlayer()
                sender_object = Connection(
                    self, player, conn, address, self.game, playerNumber
                )
                sender_object.start()
            finally:
                self.parent.sMutex.release()


class Connection(threading.Thread):
    """A custom class to simulate a single send-receive connection

    Inherited:
        threading.Thread: Base Threading class of python.
    """

    def __init__(self, parent, player, socket, retAddr, game, playerNumber):
        """Initializes the Connection Library.

        Args:
            parent (NetworkServer): The server which makes this connection.
            player (PlayerState): The player who is using this connection.
            socket (socket object): The socket object for the connection.
            retAddr (address info): The return address for the connection.
            game (OverallState): The Game whic is using this connection.
            playerNumber (int): The index of the player in the game.
        """
        threading.Thread.__init__(self)
        self.communicator = socket
        self.active = True
        self.retAddr = retAddr
        self.playerNumber = playerNumber
        self.player = player
        self.game = game
        self.delta = 0
        self.parent = parent

    def run(self):
        """
        Function handling the running of the thread.
        """
        recvThread = threading.Thread(target=self.receive)
        sendThread = threading.Thread(target=self.send)
        recvThread.start()
        sendThread.start()
        recvThread.join()
        sendThread.join()
        self.parent.vacate()
        try:
            self.communicator.close()
        finally:
            return

    def receive(self):
        """
        Threading function for perodically recieving user data its activity
        """
        while self.active:
            try:
                message = recieveMessage(self.communicator)
            except:
                self.active = False
                break
            newMessage = message.split(" ", 1)
            # TODO: Check if the time is valid
            currTime = float(newMessage[0])
            if self.delta == 0:
                self.delta = time() - currTime
            else:
                self.delta = ALPHA * self.delta + (1 - ALPHA) * (time() - currTime)

            # print(newMessage)
            try:
                moveList = json.loads(newMessage[1])
                for i in moveList:
                    i[0] += self.delta
                self.parent.parent.addMoves(self.playerNumber, moveList)
            except:
                continue

    def send(self):
        """
        Threading function for perodically sending game states to user.
        """
        while self.active:
            T.sleep(STATE_SYNC_LATENCY)
            cpState = self.parent.parent.getGameCopy()
            cpState.changeTimeBy(-1 * self.delta)
            cpState.me = self.playerNumber
            try:
                sendMessage(self.communicator, json.dumps(self.game.getState()))
            except:
                self.active = False
                break
            if cpState.gameEnded:
                self.active = False
