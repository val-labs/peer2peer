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
    return msg

_SeqNo  = 132767

def next_seq_no():
    global _SeqNo
    _SeqNo += 1
    return _SeqNo

def get(key):
    p2pc.publish(Ps, "dbd",
                 ' '.join([UUID, "get", str(next_seq_no()), key]))
    ret = p2pc.get_next_published(Ps).split(' ', 1)
    return ret[1] if len(ret) > 1 else ''

def put(key, val):
    p2pc.publish(Ps, "dbd",
                 ' '.join([UUID, "put", str(next_seq_no()), key, val]))
    return p2pc.get_next_published(Ps).split(' ',1)[1]

def openfile(fname):
    return open(fname) if fname!='-' else sys.stdin
    
def main(args):
    if   args[0] == 'get':
        key = args[1]
        connect()
        val = get(key)
        if not val:
            raise SystemExit(1)
        sys.stdout.write( val )
    elif args[0] == 'put':
        key = args[1]
        dat = openfile(args[2]).read()
        connect()
        put(key, dat)
    else:
        raise Exception("BAD COMMAND")
    
if __name__ == "__main__": main(sys.argv[1:])
