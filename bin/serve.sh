#!/bin/sh
sh bin/kill.sh
PORT=9999
python -u peer2peer.py serve $PORT & echo $!>peer2peer.pid
