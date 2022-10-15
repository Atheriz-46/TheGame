python3 -m src.server.main.py &
python3 -m src.client.main.py &
python3 -m src.client.main.py &
sleep 40
trap 'kill $(jobs -p)' EXIT