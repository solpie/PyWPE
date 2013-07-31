import sys, struct
from socket import htons
from pydbg.pydbg import *
# from pydbg.defines import *
import config


def log(msg):
    # f = open("log.txt", "a")
    # f.write(msg + "n")
    # f.close()
    pass


FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])


def dump(src, length=16):
    N = 0
    result = ''
    while src:
        s, src = src[:length], src[length:]
        hexa = ' '.join(["%X" % ord(x) for x in s])
        s = s.translate(FILTER)
        result += "%X   %-*s   %s" % (N, length * 3, hexa, s)
        N += length
    return result


class packet:
    status = 0
    s = 0
    buf = None
    buf_addr = 0
    len = 0
    tid = 0

    def __init__(self, s, buf_addr, len, tid=0):
        (self.s, self.buf_addr, self.len) = (s, buf_addr, len)
        self.tid = tid


class connection:
    s = 0
    ip_addr = 0
    port = 0
    pkt_list = []
    tid = 0

    def __init__(self, s, ip_addr=0, port=0, tid=0):
        (self.s, self.ip_addr, self.port) = (s, ip_addr, port)
        self.tid = tid

    def add_packet(self, pkt):
        self.pkt_list.append(pkt)

    def del_packet(self, pkt):
        self.pkt_list.remove(pkt)
        del pkt

    def find_pkt(self, buf_addr, tid=0):
        retval = None
        for pkt in self.pkt_list:
            if (tid):
                if (pkt.tid != tid):
                    continue
            if (pkt.buf_addr == buf_addr):
                retval = pkt
                break
        return retval


class sniff_main:
    conn_list = []

    def find_conn(self, s):
        retval = None
        for conn in self.conn_list:
            if (conn.s == s):
                retval = conn
                break
        return retval

    def add_conn(self, conn):
        self.conn_list.append(conn)


class tbp:
    tid = 0
    addr = 0
    s = 0
    buf_addr = 0

    def __init__(self, tid, addr, s, buf_addr):
        (self.tid, self.addr, self.s, self.buf_addr) = tid, addr, s, buf_addr


class tbp_main:
    tbp_list = []

    def add_tbp(self, t):
        self.tbp_list.append(t)

    def del_tbp(self, t):
        self.tbp_list.remove(t)
        del t

    def find_tbp(self, tid, addr):
        retval = None
        for t in self.tbp_list:
            if (t.tid == tid and t.addr == addr):
                retval = t
                break
        return retval


class conf:
    recv = 0
    send = 0
    connect = 0
    closesocket = 0
    t = tbp_main()
    sniff = sniff_main()


def __t(pydbg):
    t = conf.t.find_tbp(pydbg.dbg.dwThreadId, pydbg.exception_address)
    ret = int(pydbg.context.Eax)
    if t is None:
        return DBG_CONTINUE

    conn = conf.sniff.find_conn(t.s)
    if conn is None:
        print "conn not found"
        pydbg.bp_del(pydbg.exception_address)
        conf.t.del_tbp(t)
        return DBG_CONTINUE

    pkt = conn.find_pkt(t.buf_addr, t.tid)
    if pkt is None:
        print "pkt not found"
        pydbg.bp_del(pydbg.exception_address)
        conf.t.del_tbp(t)
        return DBG_CONTINUE
    if (ret > 0):
        pkt.len = ret
        pkt.buf = pydbg.read(pkt.buf_addr, ret)
        # msg = "thread %d @x" % (pydbg.dbg.dwThreadId, pydbg.exception_address)
        msg = "recv'd socket: %x, port: %d, len: %dn" % (conn.s, conn.port, ret)
        msg += dump(pkt.buf)
        log(msg)
        print msg
    pydbg.bp_del(pydbg.exception_address)
    conf.t.del_tbp(t)
    return DBG_CONTINUE


def _recv(pydbg):
    ret_addr = struct.unpack("I", pydbg.read(pydbg.context.Esp, 4))[0]
    s = struct.unpack("I", pydbg.read(pydbg.context.Esp + 4, 4))[0]
    buf_addr = struct.unpack("L", pydbg.read(pydbg.context.Esp + 8, 4))[0]
    len = struct.unpack("L", pydbg.read(pydbg.context.Esp + 12, 4))[0]

    conn = conf.sniff.find_conn(s)
    if conn is None:
        return DBG_CONTINUE

    pkt = packet(s, buf_addr, len, tid=pydbg.dbg.dwThreadId)
    conn.add_packet(pkt)

    pydbg.bp_set(ret_addr, handler=__t)
    t = tbp(pydbg.dbg.dwThreadId, ret_addr, s, buf_addr)
    conf.t.add_tbp(t)

    return DBG_CONTINUE


def _send(pydbg):
    ret_addr = struct.unpack("I", pydbg.read(pydbg.context.Esp, 4))[0]
    s = struct.unpack("I", pydbg.read(pydbg.context.Esp + 4, 4))[0]
    buf_addr = struct.unpack("L", pydbg.read(pydbg.context.Esp + 8, 4))[0]
    buf_len = struct.unpack("L", pydbg.read(pydbg.context.Esp + 12, 4))[0]
    pkt = packet(s, buf_addr, buf_len)
    pkt.buf = pydbg.read(buf_addr, buf_len)

    dbg.resume_all_threads()
    # dbg.detach()
    print 'dbg.detach'
    if buf_len == 8:
        print dump(pkt.buf)
        print pkt.buf
        if pkt.buf == '\x00\x00\x00\x08\x00\x9f\x4d\x44':
            pydbg.write(buf_addr, '\x00\x00\x00\x08\x00\x9f\x4d\x43', 8)
        if pkt.buf == '\x00\x00\x00\x08\x00\x9f\x9b\x6a':
            pydbg.write(buf_addr, '\x00\x00\x00\x08\x00\x9f\x4d\x41', 8)

    conn = conf.sniff.find_conn(s)
    if conn is None:
        return DBG_CONTINUE
    conn.add_packet(pkt)

    msg = "send sock: %#x, port: %d, len: %d\n" % (s, conn.port, buf_len)
    msg += dump(pkt.buf)
    log(msg)
    print msg
    return DBG_CONTINUE


def _connect(pydbg):
    print 'connect'
    s = struct.unpack("I", pydbg.read(pydbg.context.Esp + 4, 4))[0]
    p = struct.unpack("L", pydbg.read(pydbg.context.Esp + 8, 4))[0]
    info = struct.unpack("HH", pydbg.read(p, 4))
    port = htons(info[1])
    print "ws2_32.connect() called from thread %d @%#x" % (pydbg.dbg.dwThreadId, pydbg.exception_address)

    if (config.port == port or config.port == 0):
        print "socket: %x, port: %d" % (s, port)
        conn = connection(s, 0, port)
        conf.sniff.add_conn(conn)
    return DBG_CONTINUE


def _CreateThread(pydbg):
    print "kernel32.CreateThread() called from thread %d @%x" % (pydbg.dbg.dwThreadId, pydbg.exception_address)
    return DBG_CONTINUE


dbg = pydbg()


def main():
    global conf

    # try:
    #     proc_name = sys.argv[1]
    # except:
    #     print "usage: %s <proc_name>" % sys.argv[0]
    #     return -1

    # proc_name="firefox.exe"
    proc_name = "plugin-container.exe"

    found = False

    for (pid, name) in dbg.enumerate_processes():
        if (name.lower() == proc_name.lower()):
            print "%s pid = %d" % (name, pid)
            found = True
            break

    if not found:
        print "proc %s not found" % proc_name
        return -1

    print "attaching to pid:%d" % pid
    dbg.attach(pid)

    conf.recv = dbg.func_resolve("ws2_32", "recv")
    print "recv addr: %#x" % conf.recv

    conf.send = dbg.func_resolve("ws2_32", "send")
    print "send addr: %#x" % conf.send

    conf.connect = dbg.func_resolve("ws2_32", "connect")
    print "connect addr: %#x" % conf.connect

    conf.closeSocket = dbg.func_resolve("ws2_32", "closesocket")
    print "closesocket addr: %#x" % conf.closeSocket

    addr = dbg.func_resolve("kernel32", "CreateThread")
    print "CreateThread addr: %#x" % addr
    dbg.bp_set(addr, handler=_CreateThread)

    dbg.bp_set(conf.recv, handler=_recv)
    dbg.bp_set(conf.send, handler=_send, restore=False)
    dbg.bp_set(conf.connect, handler=_connect)

    print "-----------------------------"
    dbg.run()
    # dbg.bp_del_all()
    # dbg.bp_del_hw_all()

    print "---------detach--------------------"
    # dbg.ret_self()


# s = ("This 10 line function is just a sample of pyhton power "
#      "for string manipulations.n"
#      "The code is x07evenx08 quite readable!")

#print dump(s)

main()