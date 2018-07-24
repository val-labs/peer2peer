import os, sys, peer2peer, time, toolz, uuid

_UUID = uuid.uuid4()
UUID = str(_UUID)

def connect():
    global Ps
    Ps = peer2peer.conn()
    peer2peer.subscribe(Ps, "dbd " + UUID)
    peer2peer.publish(Ps, "dbd", "hello from " + UUID)

    while 1:
        msgs = peer2peer.recv(Ps)
        print "M", msgs
        time.sleep(0.2)
        pass
    pass

def dbd_msg(*a, **kw):
    print "DBD MSG", repr((a, kw))
    pass

def main():
    while 1:
        print "BEFORE"
        try:
            peer2peer.loop_ws(Ps, [], dbd_msg)
        except:
            print "ERR"
            time.sleep(1)
            try:
                connect()
            except:
                print "ERR2"
                pass
            pass
        print "AFTER"

if __name__ == "__main__":
    print "I AM", UUID
    connect()
    print "ok2"
