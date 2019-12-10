import random
import string


class OTACGen:

    def __init__(self):
        print()

    def generateOTAC(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
