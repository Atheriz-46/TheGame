from GUIManager import GUIManager
from time import sleep
from tick import *
from nClient import NetworkClient
from overallState import OverallState
from gameMode import GameMode
from threading import Thread, Lock
from AskIP import AskIP


class Client:
    """
    Class to handle overall Client operations and sub objects
    """

    def __init__(self, server_ip, server_port, latencyMode=0):
        """
        Args:
            server_ip (String) : IP address of server to connect to
            server_port (int) :  port of the server to connect to
            latencyMode (int) : Artificial latency to be added for testing purposes
        """
        self.eventQueue = []
        self.qMutex = Lock()
        self.sMutex = Lock()
        self.state = OverallState(GameMode())
        self.latencyMode = latencyMode
        self.networkManager = NetworkClient(server_ip, server_port, self)
        self.gui = GUIManager(self)
        self.updateThread = Thread(target=self.updateState)
        self.updateThread.start()
        self.gameStarted = False
        # self.updateThread.join()

    def updateState(self):
        """
        Loops over a thread to constanly update the local instance of game based on user inputs
        """
        while True:
            sleep(STATE_UPDATE_LATENCY / 2)
            self.sMutex.acquire()
            self.qMutex.acquire()
            try:
                if self.state.me == 0:
                    self.state.updateState(self.eventQueue, [])
                else:
                    self.state.updateState([], self.eventQueue)
                if len(self.state.players) >= 2:
                    self.gameStarted = True
            finally:
                self.qMutex.release()
                self.sMutex.release()

    def rotateClock(self):
        """
        API for handelling clockwise rotation of gun by the user
        """
        self.qMutex.acquire()
        try:
            self.eventQueue.append([time(), "C"])
        finally:
            self.qMutex.release()

    def rotateAntiClock(self):
        """
        API for handelling Anticlockwise rotation of gun by the user
        """
        self.qMutex.acquire()
        try:
            self.eventQueue.append([time(), "A"])
        finally:
            self.qMutex.release()

    def getState(self):
        """
        creates a json compaitiable Client object
        Returns:
            List<float,string>: List of inputs by user to be send to server
        """
        self.qMutex.acquire()
        try:
            ret = self.eventQueue.copy()
            self.eventQueue = []
        finally:
            self.qMutex.release()
            return ret

    def setState(self, state):
        """
        Sets the state of OverallState of the Client game using JSON
        Args:
            state (JSON String): Client OverallState recieved from server
        """
        self.sMutex.acquire()
        try:
            self.state.setState(state)
        finally:
            self.sMutex.release()

    def getGameCopy(self):
        """
        Returns a copy of game State in the Client
        Returns:
            OverallState: game State in the Client
        """
        self.sMutex.acquire()
        try:
            cp = self.state.copy()
        finally:
            self.sMutex.release()
        return cp
