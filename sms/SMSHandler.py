#!/usr/bin/env python

"""\
Demo: handle incoming SMS messages by replying to them
Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""

from __future__ import print_function
from gsmmodem.modem import GsmModem
import logging

PORT = 'COM11'
BAUDRATE = 115200
PIN = None  # SIM card PIN (if any)


class SMSHandler:
    def __init__(self):
        print('stuff')
        print('Initializing modem...')
        # Uncomment the following line to see what the modem is doing:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        self.modem = GsmModem(PORT, BAUDRATE)
        self.modem.smsTextMode = False
        self.modem.connect(PIN)

    def sendKeyThroughSms(self, destination, body):
        try:
            self.modem.sendSms(destination,
                               "Distributors Network\nPlease enter the following OTAC to authenticate your login:\n " + body,
                               True,
                               15,
                               False)
            print("Sms sent to: " + destination)
            return True
        except:
            print("An error occurred while sending the message")
            return False


if __name__ == '__main__':
    # main()

    obj = SMSHandler()
    # gsm = GsmModem(PORT)

    obj.main()
    # obj.sendSms(gsm)
