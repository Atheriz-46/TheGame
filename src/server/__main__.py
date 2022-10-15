from .Server import Server
from ..common.constants import IP, port
import argparse
parser = argparse.ArgumentParser(description='Start a server')
parser.add_argument('--ip', type=str, default=IP, help='IP address of the server')
parser.add_argument('--port', type=int, default=port, help='Port of the server')
args = parser.parse_args()
print("Server started")
Server(ip=args.ip, port=args.port)

