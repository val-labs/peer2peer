import sys, time, leveldb, toolz, traceback as tb, functools
from peer2peer import p2pc


def reconnect(times = 999999999, address = 'ws://127.1:9090'):
    global Ps
    for n in xrange(times):
        try:
            Ps = p2pc.WebSocket.create(address)
            return Ps
        except: tb.print_exc()
        time.sleep(1)


def init():
    global Db
    Db = leveldb.LevelDB('db')
    return reconnect(5)


def new_req(x, y, msg):
    arr = msg.split(' ', 4)
    rid = arr.pop(0)
    publish = functools.partial(p2pc.publish, Ps, rid)
    cmd = arr.pop(0)
    seq = arr.pop(0)
    if cmd == 'hola':    return publish(seq + " YO!")
    key = arr.pop(0)
    if cmd == 'get':
        try:             return publish(seq + ' ' + Db.Get(key))
        except KeyError: return publish(seq)
    val = arr.pop(0)
    if cmd == 'put':
        Db.Put(key, val);return publish(seq + " OK")
    raise Exception("ERROR, BAD COMMAND")


def main():
    while 1:
        try:
            p2pc.subscribe(Ps, 'dbd')
            while 1:
                p2pc.get_next_published(Ps, new_req)
                time.sleep(0.2)
        except KeyboardInterrupt:
            return sys.stderr.write("^C\nBye!\n")
        except:
            tb.print_exc()
            reconnect()


if __name__ == "__main__":
    PID_FNAME = 'dbd.pid'
    toolz.kill(PID_FNAME)
    #try: toolz.kill(PID_FNAME)
    #except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-i': init() and main()
    else: init(), toolz.daemon(main, PID_FNAME)
