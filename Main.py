import time
from tkinter import Tk

from database.MySQLCon import MySQLCon
from sms.OTACGen import OTACGen
from sms.SMSHandler import SMSHandler
from gui.Dashboard import Dashboard

class Main:
    def __init__(self):  # this is the java equivalent of a constructor
        print("Michael Freaking Scott")


if __name__ == '__main__':  # this is the main function java equivalent of static void main(String args[]){}

    root = Tk()
    dash = Dashboard(root)
    root.mainloop()

    obj = Main()
    mySql = MySQLCon()
    otac = OTACGen()
    sms = SMSHandler()

    while True:
        result = mySql.checkForSignUpRequests()
        for row in result:
            key = otac.generateOTAC()
            phone = row['PHONE']
            print('Sending key: ' + key + ' to ' + phone)
            success = sms.sendKeyThroughSms(phone, key)
            if success is True:
                mySql.updateOTACwithPhone(key, phone)
        time.sleep(5)
