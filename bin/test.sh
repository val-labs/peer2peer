#!/bin/sh
HOST=127.0.0.1:9999
python -u peer2peer.py pub $HOST -<peer2peer.py
python -u peer2peer.py pub $HOST channel1 -<Makefile
python -u peer2peer.py pub $HOST abc -<test.sh

echo .w | python -u peer2peer.py pub $HOST CTL -
