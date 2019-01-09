from database.MySQLCon import MySQLCon
from sms.OTACGen import OTACGen

class Main:
    def __init__(self):  # this is the java equivalent of a constructor
        print("Michael Freaking Scott")


if __name__ == '__main__':  # this is the main function java equivalent of static void main(String args[]){}
    obj = Main()
    print("I'm in the main function")

    my = MySQLCon()
    result = my.checkForSignUpRequests()

    otac = OTACGen()
    otac.generateOTAC()


