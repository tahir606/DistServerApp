from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QThread
import sys
import json
import time

qtCreatorFile = "Dash.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class ThreadingTutorial(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.startBtn.clicked.connect(self.start_thread)
        self.exitBtn.clicked.connect(self.exitThread)

    def start_thread(self):
        self.get_thread.start()
        self.startBtn.setEnabled(False)

    def exitThread(self):
        if self.get_thread is not None:
            self.get_thread.terminate()
        print('Terminated')
        self.close()


def main():
    print('in here')
    # app = QtWidgets.QApplication(sys.argv)
    # form = ThreadingTutorial()
    # form.show()
    # app.exec_()


if __name__ == '__main__':
    main()
