import sys
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread

from database.MySQLCon import MySQLCon
from gui.QTDash import Ui_MainWindow
from sms.OTACGen import OTACGen
from sms.SMSHandler import SMSHandler

qtCreatorFile = "Dash.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class ProcessSignUpRequests(QThread):
    def __init__(self):
        print('Processing')
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def processOTACRequests(self):
        sql = MySQLCon()
        otac = OTACGen()
        sms = SMSHandler()

        while True:
            result = sql.checkForSignUpRequests()
            for row in result:
                key = otac.generateOTAC()
                phone = row['PHONE']
                print('Sending key: ' + key + ' to ' + phone)
                success = sms.sendKeyThroughSms(phone, key)
                if success is True:
                    sql.updateOTACwithPhone(key, phone)
            time.sleep(5)

    def run(self):
        self.processOTACRequests()


class Dashboard(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        print('Inflating Dashboard')
        super(self.__class__, self).__init__()
        self.get_thread = ProcessSignUpRequests()
        self.setupUi(self)
        self.startBtn.clicked.connect(self.startProcessing)  # if you write function_name() the function will run
        self.exitBtn.clicked.connect(self.exitThread)

    def startProcessing(self):
        self.get_thread.start()
        self.startBtn.setEnabled(False)

    def exitThread(self):
        if self.get_thread is not None:
            self.get_thread.terminate()
        print('Terminated')
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Dashboard()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
