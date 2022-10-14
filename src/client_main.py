from Client import Client
from constants import IP,port

print("Client started")
from time import sleep
sleep(2)
cl = Client(IP,port)

while True:
    if cl.gameStarted:
        cl.gui.startGame()
        break

cl.gui.mainloop()