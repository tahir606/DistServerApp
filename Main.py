import sys
import time
import traceback

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal

from database.MySQLCon import MySQLCon

from gui.Settings import Settings
from prog.EmailHandler import EmailHandler
from sms.OTACGen import OTACGen
from sms.SMSHandler import SMSHandler

# This is the class used to start the program

qtCreatorFile = "./gui/Dash.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class ProcessSignUpRequests(QThread):
    displayMsgSignal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.id = ''
        self.phone = ''
        self.emailAddress = ''

    def __del__(self):
        self.wait()

    def processOTACRequests(self):
        sql = MySQLCon()
        otac = OTACGen()

        try:
            sms = SMSHandler()
            isSMS = True
        except Exception as e:
            self.displayMsgSignal.emit("Error: " + str(e))
            isSMS = False
            traceback.print_exc()
        email = EmailHandler()

        while True:
            try:
                result = sql.checkForSignUpRequests()
                for row in result:
                    key = otac.generateOTAC()
                    # Save OTAC with phone number
                    self.id = row['NO']
                    self.phone = row['PHONE']
                    self.emailAddress = row['EMAIL']
                    sql.updateOTACwithPhone(key, self.phone, str(self.id))
                    email.sendEmail(self.emailAddress, 'Dist Network OTAC',
                                    "Distributors Network\nPlease enter the following OTAC to authenticate "
                                    "your login:\n " + key)
                    msg = "OTAC Email Sent to: " + self.emailAddress
                    if isSMS:
                        sms.sendSms(self.phone, "Distributors Network\nPlease enter the following OTAC to authenticate "
                                                "your login:\n " + key)
                        msg = msg + "\nOTAC SMS Sent to: " + self.phone

                    self.displayMsgSignal.emit(msg)

                smswaiting = sql.checkForSmsToBeSent()
                for row in smswaiting:
                    code = row['SNO']
                    self.phone = row['SPHONE']
                    self.emailAddress = row['SEMAIL']
                    subject = row['SUBJ']
                    body = row['SBODY']

                    msg = ""
                    isEmail = True
                    try:
                        email.sendEmail(self.emailAddress, subject, str(body))
                        msg = "Notif Email Sent to: " + self.emailAddress
                    except Exception as e:
                        isEmail = False
                        self.displayMsgSignal.emit("Error: " + str(e))
                        traceback.print_exc()

                    if isSMS:
                        sms.sendSms(self.phone, body)
                        msg = "\nNotif SMS Sent to: " + self.phone

                    self.displayMsgSignal.emit(msg)

                    if isEmail or isSMS:
                        # Update SMS Flag to not send a notification Again
                        sql.updateSmsFlag(code)
                    else:
                        self.displayMsgSignal.emit("Unable to notify " + self.phone + " or " + self.emailAddress)

                time.sleep(5)
            except Exception as e:
                self.displayMsgSignal.emit('Exception: ' + str(e))
                traceback.print_exc()
                time.sleep(10)

    def run(self):
        self.processOTACRequests()


class Dashboard(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.get_thread = ProcessSignUpRequests()
        self.setupUi(self)
        self.displayMsg.setWordWrap(True)
        self.displayMsg.setText('')
        self.get_thread.displayMsgSignal.connect(self.my_event)
        self.startBtn.clicked.connect(self.startProcessing)
        self.actionSettings.triggered.connect(self.openSettings)
        self.exitBtn.clicked.connect(self.exitThread)

    def my_event(self, str):
        self.displayMsg.setText(str)

    def startProcessing(self):
        self.get_thread.start()
        self.displayMsg.setText('Listening for SMS Requests')
        self.startBtn.setEnabled(False)

    def openSettings(self):
        dialog = Settings(self)
        dialog.show()

    def exitThread(self):
        if self.get_thread is not None:
            self.get_thread.terminate()
        self.displayMsg.setText('Terminated')
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Dashboard()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
