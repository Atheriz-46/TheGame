python3 -m src.server &
python3 -m src.client &
python3 -m src.client &
sleep 40
trap 'kill $(jobs -p)' EXIT