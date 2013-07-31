# -*- coding: utf-8 -*-
__author__ = 'SolPie'

from deco import singleton
from PyQt4 import QtGui, QtCore


@singleton
class RcModel():
    loaded = False

    def __init__(self):
        self.load()

    def load(self):
        self.icon = QtGui.QPixmap()
        self.icon.load('res/glyphicons-halflings.png')

        self.icon_white = QtGui.QPixmap()
        self.icon_white.load('res/glyphicons-halflings-white.png')

    def getCopy(self, x, y):
        return self.icon.copy(x * 20, y * 20, 20, 20)

    def getCssString(self):
        f = QtCore.QFile("darkstyle.css")
        f.open(QtCore.QFile.ReadOnly)
        style_sheet = QtCore.QLatin1String(f.readAll())
        return style_sheet
