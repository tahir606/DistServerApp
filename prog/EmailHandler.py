import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = 'burhanisolutions.com.pk'
PORT = 26
MY_ADDRESS = 'sales@burhanisolutions.com.pk'
PASSWORD = 'burhanisales'

# Create a secure SSL context
# context = ssl.create_default_context()


class EmailHandler:
    def __init__(self):
        print('In email handler')

    def sendEmail(self, to, subject, body):
        # set up the SMTP server
        server = smtplib.SMTP(host=HOST, port=PORT)
        server.ehlo()  # Can be omitted
        server.starttls()  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(MY_ADDRESS, PASSWORD)

        msg = MIMEMultipart()  # create a message

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = to
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(body, 'plain'))

        # send the message via the server set up earlier.
        server.sendmail(MY_ADDRESS, to, msg.as_string())
        del msg

        # Terminate the SMTP session and close the connection
        server.quit()


if __name__ == '__main__':
    email = EmailHandler()
    email.sendEmail('tahir60652@gmail.com', 'Test Subject', 'Test body')
