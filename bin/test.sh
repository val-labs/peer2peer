#!/bin/sh
HOST=127.0.0.1:9999
python -u peer2peer.py p2pub $HOST <peer2peer.py
python -u peer2peer.py p2pub $HOST channel1 <Makefile
python -u peer2peer.py p2pub $HOST abc <test.sh

python -u peer2peer.py p2pub $HOST .w </dev/null
