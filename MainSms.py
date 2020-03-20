#!/usr/bin/env python

"""\
Demo: handle incoming SMS messages by replying to them
Simple demo app that listens for incoming SMS messages, displays the sender's number
and the messages, then replies to the SMS by saying "thank you"
"""

from __future__ import print_function

import logging

PORT = 'COM11'
BAUDRATE = 115200
PIN = None  # SIM card PIN (if any)

from gsmmodem.modem import GsmModem

class MainSms:
    def __init__(self):
        print('stuff')

    def handleSms(self, sms):
        print(
            u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
        print('Replying to SMS...')
        sms.reply(u'SMS received: "{0}{1}"'.format(sms.text[:20], '...' if len(sms.text) > 20 else ''))
        print('SMS sent.\n')

    def main(self):
        print('Initializing modem...')
        # Uncomment the following line to see what the modem is doing:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=self.handleSms)
        modem.smsTextMode = False
        modem.connect(PIN)

        # modem.sendSms("+923342132778", "Text SMS", False, 15, False)
        print('Waiting for SMS message...')
        try:
            modem.rxThread.join(2 ** 20)  # Specify a (huge) timeout so that it essentially blocks indefinitely,
            # but still receives CTRL+C interrupt signal
        finally:
            modem.close()


if __name__ == '__main__':
    # main()

    obj = MainSms()
    # gsm = GsmModem(PORT)

    obj.main()
    # obj.sendSms(gsm)
