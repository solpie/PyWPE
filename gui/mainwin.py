# -*- coding: utf-8 -*-
__author__ = 'SolPie'
from PyQt4 import QtCore, QtGui as Gui
from models.rcModel import RcModel
from models.hookModel import HookModel
import const
from view import view
from deco.worker import Thread


class MainWin(Gui.QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__(None)
        self.setupUI()
        self.addConnection()

        # self.setWindowFlags(Core.Qt.FramelessWindowHint)#全屏无标题栏


    def setupUI(self):
        rc = RcModel()
        self.hook = HookModel()
        self.setStyleSheet(rc.getCssString())

        self.setWindowTitle(const.UI_MAIN_WINDOW_TITLE)
        # self.showMaximized()
        self.resize(1024, 768)
        self.centralWidget = Gui.QWidget(self)
        self.setCentralWidget(self.centralWidget)



        self.process_list = Gui.QComboBox()
        self.process_list.setParent(self.centralWidget)
        self.process_list.resize(300, 25)
        self.process_list.move(5, 5)

        self.btn_refresh = Gui.QPushButton()
        self.btn_refresh.setText('refresh')
        self.btn_refresh.setParent(self.centralWidget)
        self.btn_refresh.move(310, 5)

        self.btn_detach = Gui.QPushButton()
        self.btn_detach.setText('detach')
        self.btn_detach.setParent(self.centralWidget)
        self.btn_detach.move(self.btn_refresh.x()+100, 5)

        self.edit_proto = Gui.QLineEdit()
        self.edit_proto.setParent(self.centralWidget)
        self.edit_proto.move(5, 35)

    def addConnection(self):
        self.btn_refresh.mousePressEvent = self.on_comboBox_click
        self.btn_detach.mousePressEvent = self.on_detach
        self.connect(self.process_list, QtCore.SIGNAL(const.CURRENT_INDEX_CHANGED), self.on_process_select)

    def on_comboBox_click(self, e):
        l = self.hook.get_process_list()
        self.process_list.clear()
        for i in l:
            self.process_list.addItem(str(i[0]) + ' - ' + i[1])
        print 'refresh....', l

    def on_detach(self, e):
        print 'detach...'
        self.hook.dbg.detach()

    def on_process_select(self, e=None):
        # self.hook.attach()
        pid = int(self.process_list.itemText(e).split(' ')[0])
        if pid != 0:
            print self.hook.daemon(pid)
            # print 'select..', e
            # '''
            # 菜单
            # '''
            # self.menu_bar = MenuBar(self)
            # self.setMenuBar(self.menu_bar)