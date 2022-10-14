from AskIP import AskIP, ServerData
from Client import Client
from constants import IP,port

print("Client started")
from time import sleep
sleep(2)
data = ServerData()  
askip = AskIP(data)
askip.mainloop()
# print(f"IP:{data.IP}, Port:{data.Port}, Latency:{data.Latency}")
cl = Client(data.IP,data.Port,data.Latency)

while True:
    if cl.gameStarted:
        cl.gui.startGame()
        break

cl.gui.mainloop()