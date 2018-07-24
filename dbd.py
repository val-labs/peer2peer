import os, sys, peer2peer, time, toolz, traceback as tb

PID_FNAME = 'dbd.pid'

def connect():
    global Ps
    Ps = peer2peer.conn()
    pass

def init():
    print "SERVE IT UP"
    connect()
    print Ps
    pass

def dbd_msg(*a, **kw):
    print "DBD MSG", repr((a, kw))
    pass

def main():
    while 1:
        print "BEFORE"
        try:
            peer2peer.subscribe(Ps, 'dbd')
            while 1:
                print "X"
                msgs = peer2peer.recv(Ps)
                print "M1", msgs
                msg = msgs[2]

                if msg.startswith('hello from '):
                    frm = msg[len('hello from '):]
                    print frm
                    peer2peer.publish(Ps, frm, "HI!")
                
                time.sleep(0.2)
        except:
            tb.print_exc()
            print "ERR"
            time.sleep(1)
            try:
                connect()
            except:
                print "ERR2"
                tb.print_exc()
                pass
            pass
        print "AFTER"

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)    
    except: pass
    #init(); toolz.daemon(main, PID_FNAME)
    init(); main()

