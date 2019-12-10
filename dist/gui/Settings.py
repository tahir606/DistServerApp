import os
import sys

from PyQt5 import QtWidgets, uic, QtCore

from prog.FileHandler import FileHandler

qtCreatorFile = "./gui/settings.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Settings(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.fHandler = FileHandler()
        self.btn_save.clicked.connect(self.saveSettings)
        self.contents = self.fHandler.readSmsSettings()
        self.arr = self.contents.split(",")
        index = self.combo_port.findText(self.arr[0], QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.combo_port.setCurrentIndex(index)
        self.txt_baudrate.setText(self.arr[1])

    def saveSettings(self):
        baudrate = self.txt_baudrate.text()
        port = self.combo_port.currentText()
        self.fHandler.saveSmsSettings(port, baudrate)
        self.close()
