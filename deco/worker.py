__author__ = 'SolPie'
from PyQt4 import QtCore
from deco import singleton
import threading

class Thread(QtCore.QThread):
    message = QtCore.pyqtSignal(str)
    url = None

    def run(self):
        self.printf()
        pass

    def printf(self):
        # self.message.emit(msg)
        pass

@singleton
class Worker(threading.Thread):
    def run(self):
        pass

