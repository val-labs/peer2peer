import os, sys, peer2peer, time

def main(sub_to, pub_to, channel):
    print "SERVE IT UP", sub_to, pub_to, channel
    ws1 = peer2peer.conn(sub_to)
    peer2peer.subscribe(ws1, channel)
    print "CONNECTED1"
    ws2 = peer2peer.conn(pub_to)
    print "CONNECTED2"
    while 1:
        msgs = peer2peer.recv(ws1)
        msg = msgs[2]
        print "MMM", msg
        peer2peer.publish(ws2, channel, msg)
        time.sleep(0.2)
        pass

if __name__ == "__main__": main(*sys.argv[1:])
