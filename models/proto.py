# -*- coding: utf-8 -*-
__author__ = 'SolPie'
import struct
from pydbg.pydbg import *

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


def CreateThread(pydbg):
    print "kernel32.CreateThread() called from thread %d @%x" % (pydbg.dbg.dwThreadId, pydbg.exception_address)
    return DBG_CONTINUE


def send(pydbg):
    ret_addr = struct.unpack("I", pydbg.read(pydbg.context.Esp, 4))[0]
    s = struct.unpack("I", pydbg.read(pydbg.context.Esp + 4, 4))[0]
    buf_addr = struct.unpack("L", pydbg.read(pydbg.context.Esp + 8, 4))[0]
    buf_len = struct.unpack("L", pydbg.read(pydbg.context.Esp + 12, 4))[0]
    pkt = packet(s, buf_addr, buf_len)
    pkt.buf = pydbg.read(buf_addr, buf_len)

    if buf_len == 8 or buf_len == 15:
        print dump(pkt.buf)
        if pkt.buf == '\x00\x00\x00\x08\x00\x9f\x4d\x44':
            pydbg.write(buf_addr, '\x00\x00\x00\x08\x00\x9f\x4d\x43', 8)
        if pkt.buf == '\x00\x00\x00\x08\x00\x9f\x9b\x6a':
            pydbg.write(buf_addr, '\x00\x00\x00\x08\x00\x9f\x4d\x41', 8)
            #10380016
        if pkt.buf == '\x00\x00\x00\x0f\x00\x9e\x62\xf0\x08\x02\x10\xf5\x9e\x94\x07':#00 00 00 0f 00 9e 62 f0 08 02 10 f5 9e 94 07
            pass
            #up strongpoint
        if pkt.buf == '\x00\x00\x00\x0D\x00\x9E\x62\xEF\x08\xF5\x9E\x94\x07':
            pass

    return DBG_CONTINUE