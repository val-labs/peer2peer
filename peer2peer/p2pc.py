#!/usr/bin/env python
"""p2pc.py

A simple peer-to-peer websocket solution (in python)

Usage:
  p2pc.py pub <address> <channel> <msgfile>
  p2pc.py sub <address> <channel>
  p2pc.py pipe <from_address> <from_channel> <to_address> <to_channel>
  p2pc.py (-h | --help)
  p2pc.py --version

Options:
  -h --help      Show this screen.
  --version      Show version.
  <address>      remote hostname:port
  <from_address> remote hostname:port
  <to_address>   remote hostname:port
  <channel>      name of channel (no whitespace)
  <from_channel> name of channel (no whitespace)
  <to_channel>   name of channel (no whitespace) [default:]
  <msgfile>      filename of message or '-' to use stdin

"""
import os, sys, time, docopt, websocket


class WebSocket(websocket.WebSocket):
    @classmethod
    def create(cls, address):
        ws = cls()
        ws.connect(address)
        return ws
    receive = websocket.WebSocket.recv


def subscribe(ws, channel_list='0'):
    return ws.send( "sub " + channel_list )


def get_next_published(ws, cb=lambda*a:a[2]):
    return cb( ws.receive(),
               ws.receive(),
               ws.receive() )


def publish(ws, ch, msg):
    ws.send('pub '+ch) ; ws.send('2') ; ws.send(msg)


if __name__ == '__main__':
    A = docopt.docopt(__doc__, version='p2pc.py v0.0.0')

    print(A)

    if A['pub']:
        print("PUB")
        addr = A['<address>']
        chnl = A['<channel>']
        msgf = A['<msgfile>']
        fi = open(msgf) if msgf!='-' else sys.stdin
        dat = fi.read()
        ws = WebSocket.create(addr)
        print(ws)
        publish(ws, chnl, dat)
        time.sleep(0.1)
        
    elif A['sub']:
        print("SUB")
        addr = A['<address>']
        chnl = A['<channel>']
        ws = WebSocket.create(addr)
        print(ws)
        subscribe(ws, chnl)
        while 1:
            nxt = get_next_published(ws)
            print("READ", nxt)
            time.sleep(0.1)
            pass
        pass
