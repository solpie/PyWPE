# -*- coding: utf-8 -*-
__author__ = 'SolPie'
from deco import BaseView, singleton
from PyQt4 import QtCore




@singleton
class PyWPEView(BaseView):
    LIST_DIR = 'list dir'
    TagView = QtCore.pyqtSignal()

    def __init__(self):
        super(BaseView, self).__init__()
    # def init_map(self):
    #     self.map('refresh_process',get_process_list)

view = PyWPEView()