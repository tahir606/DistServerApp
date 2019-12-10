import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = 'burhanisolutions.com.pk'
PORT = 26
MY_ADDRESS = 'sales@burhanisolutions.com.pk'
PASSWORD = 'burhanisales'


class EmailHandler:
    def __init__(self):
        print('In email handler')

    def sendEmail(self, to, subject, body):
        # set up the SMTP server
        s = smtplib.SMTP(host=HOST, port=PORT)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)

        msg = MIMEMultipart()  # create a message

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = to
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(body, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

        # Terminate the SMTP session and close the connection
        s.quit()


if __name__ == '__main__':
    email = EmailHandler()
    email.sendEmail('tahir60652@gmail.com', 'Test Subject', 'Test body')
