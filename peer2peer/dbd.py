import sys, time, leveldb, toolz, traceback as tb
from peer2peer import p2pc

PID_FNAME = 'dbd.pid'

def connect(address = 'ws://127.1:9090'):
    global Ps
    Ps = p2pc.WebSocket.create(address)
    pass

def init():
    global db
    print "OPEN DB"
    db = leveldb.LevelDB('db')
    print "SERVE IT UP"
    connect()
    print "CONNECTED"
    pass

def main():
    while 1:
        print "BEFORE"
        try:
            p2pc.subscribe(Ps, 'dbd')
            while 1:
                print("QQQ")
                msg = p2pc.get_next_published(Ps)
                print("ATN", msg )
                arr = msg.split()
                print "ARR", arr
                if   arr[1] == 'hola':
                    p2pc.publish(Ps, arr[0], arr[2] + " YO!")
                elif arr[1] == 'put':
                    print(repr((arr[2], arr[3])))
                    db.Put(arr[2], arr[3])
                    p2pc.publish(Ps, arr[0], arr[2] + " OK")
                elif arr[1] == 'get':
                    try:
                        result = db.Get(arr[3])
                        p2pc.publish(Ps, arr[0], arr[2] + ' ' + result)
                    except KeyError:
                        p2pc.publish(Ps, arr[0], arr[2])
                else:
                    print "ERROR, DONT KNOW HOW TO DO THAT"
                    pass
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
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
