python3 src/server_main.py &
python3 src/client_main.py &
python3 src/client_main.py &
sleep 40
trap 'kill $(jobs -p)' EXIT