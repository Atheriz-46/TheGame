from time import sleep

from .AskIP import AskIP, ServerData
from .Client import Client

sleep(2)
data = ServerData()
askip = AskIP(data)
askip.mainloop()
# print(f"IP:{data.IP}, Port:{data.Port}, Latency:{data.Latency}")
cl = Client(data.IP, data.Port, data.Latency)
print("Client started")
while True:
    if cl.gameStarted:
        cl.gui.startGame()
        break

cl.gui.mainloop()
