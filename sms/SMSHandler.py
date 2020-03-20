#!/usr/bin/env python

"""\
Demo: handle incoming SMS messages by replying to them
Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""

from __future__ import print_function
from gsmmodem.modem import GsmModem
import logging

from prog.FileHandler import FileHandler


# PORT = 'COM11'
# BAUDRATE = 115200
# PIN = None  # SIM card PIN (if any)


class SMSHandler:
    def __init__(self):
        print('Initializing modem...')
        fHelper = FileHandler()
        contents = fHelper.readSmsSettings()
        arr = contents.split(",")
        PORT = arr[0]
        BAUDRATE = int(arr[1])
        PIN = None
        print(PORT, BAUDRATE)
        # Uncomment the following line to see what the modem is doing:
        # logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.modem = GsmModem(PORT, BAUDRATE)
        self.modem.smsTextMode = False
        try:
            self.modem.connect(PIN)
        except Exception as e:
            print(str(e))
            raise e

    def sendSms(self, destination, body):
        try:
            self.modem.sendSms(destination,
                               body,
                               True,
                               15,
                               False)
            print("Sms sent to: " + destination)
            return True
        except Exception as e:
            print("An error occurred while sending the message: " + str(e))
            raise e


if __name__ == '__main__':
    sms = SMSHandler()
    sms.sendSms('03342132778', 'Test SMS')
