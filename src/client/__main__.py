from client.AskIP import AskIP, ServerData
from client.Client import Client
from common.constants import IP, port

from time import sleep

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
