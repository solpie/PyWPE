# -*- coding: utf-8 -*-
__author__ = 'SolPie'
from PyQt4 import QtGui


VALUE_CHANGED = 'valueChanged(int)'
CURRENT_INDEX_CHANGED = 'currentIndexChanged(int)'


def trans(text, disambig=None):
    return QtGui.QApplication.translate("", text, disambig, QtGui.QApplication.UnicodeUTF8)


UI_MAIN_WINDOW_TITLE = 'PyWPE'
UI_MENU_FILE = '文件'
UI_MENU_FILE_OPEN = '打开'
UI_MENU_FILE_EXIT = '退出'

CSS_WIDGET_ENTITY = 'Entity'
CSS_WIDGET_DIR_TREE = 'DirTree'
CSS_WIDGET_DIR_TREE_FLAT = 'DirTreeFlat'
CSS_LABEL_DIR_TREE_LABEL = 'DirTreeLabel'
CSS_LABEL_TAG_NODE = 'TagNode'
CSS_BUTTON_DIR_TREE_NODE = 'DirTreeNode'
CSS_WIDGET_TAG_NODE_FUNC = 'TagNodeFunc'

print '[const] init...'