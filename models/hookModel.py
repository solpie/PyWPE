# -*- coding: utf-8 -*-
__author__ = 'SolPie'

from deco import singleton

from pydbg.pydbg import *

from proto import *

import threading


@singleton
class HookModel():
    dbg = pydbg()
    conf = None

    def get_process_list(self):
        l = list()
        for (pid, name) in self.dbg.enumerate_processes():
            l.append([pid, name.lower()])
        return l

    def daemon(self, pid):
        self.pid = pid
        d_bus = threading.Thread(target=self.attach)
        d_bus.setDaemon(0)
        d_bus.start()

    def attach(self):
        pid = self.pid
        self.dbg.attach(pid)
        print "attaching to pid:%d" % pid

        self.recv = self.dbg.func_resolve("ws2_32", "recv")
        print "recv addr: %#x" % self.recv

        self.send = self.dbg.func_resolve("ws2_32", "send")
        print "send addr: %#x" % self.send

        self.connect = self.dbg.func_resolve("ws2_32", "connect")
        print "connect addr: %#x" % self.connect

        self.closeSocket = self.dbg.func_resolve("ws2_32", "closesocket")
        print "closesocket addr: %#x" % self.closeSocket

        addr = self.dbg.func_resolve("kernel32", "CreateThread")
        print "CreateThread addr: %#x" % addr
        # self.dbg.bp_set(addr, handler=CreateThread)
        # self.dbg.bp_set(self.recv, handler=_recv)
        self.dbg.bp_set(self.send, handler=send)
        # self.dbg.bp_set(self.connect, handler=_connect)
        self.dbg.run()

    def __init__(self):
        pass