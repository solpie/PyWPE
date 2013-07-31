#coding=utf-8
#!/ur/bin/env python
import sys

from PyQt4 import QtGui
from gui.mainwin import MainWin


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWin()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()