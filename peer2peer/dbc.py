import sys, time, traceback as tb, uuid
from peer2peer import p2pc

_UUID = uuid.uuid4()
UUID = str(_UUID)

def connect(address = 'ws://127.1:9090'):
    global Ps
    Ps = p2pc.WebSocket.create(address)
    p2pc.subscribe(Ps, "dbd " + UUID)
    p2pc.publish(Ps, "dbd", UUID + " hola 200")
    msg = p2pc.get_next_published(Ps)
    print "CON MSG", msg
    return msg

_SeqNo  = 132767

def next_seq_no():
    global _SeqNo
    _SeqNo += 1
    return _SeqNo

def get(key):
    seq = next_seq_no()
    p2pc.publish(Ps, "dbd", UUID + " get 50 " + key)
    msg = p2pc.get_next_published(Ps)
    print "GET MSG", msg
    return msg

def put(key, val):
    seq = next_seq_no()
    msg = ' '.join([UUID, "put", str(seq), val])
    p2pc.publish(Ps, "dbd", msg)
    msg = p2pc.get_next_published(Ps)
    print "PUT MSG", msg
    return msg

def dbd_msg(*a, **kw):
    print "DBD MSG", repr((a, kw))
    pass

def main():
    while 1:
        print "BEFORE"
        try:
            p2pc.loop_ws(Ps, [], dbd_msg)
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

    if   sys.argv[1] == 'get':
        key   = sys.argv[2]
        dat   = None
        print("GET", key)

    elif sys.argv[1] == 'put':
        key   = sys.argv[2]
        fname = sys.argv[3]
        fi = open(fname) if fname!='-' else sys.stdin
        dat   = fi.read()
        print("PUT", key, fname, dat)

    else:
        print("DUNNO")
       
    print "I AM", sys.argv
    connect()
    print "ok2"

    if dat:
        print("WRITE")
        put(key, dat)
        
    else:
        print("READ")
        get(key)
