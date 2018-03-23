#!/bin/sh
sh bin/kill.sh
PORT=9999
python -u peer2peer.py p2svr $PORT & echo $!>peer2peer.pid

