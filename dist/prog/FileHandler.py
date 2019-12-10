class FileHandler:
    def __init__(self):
        print('File Handler')

    def saveSmsSettings(self, port, baudrate):
        print(port, baudrate)
        f = open("settings.txt", "w+")
        f.write(port + "," + baudrate)
        f.close()

    def readSmsSettings(self):
        try:
            f = open("settings.txt", "r")
            if f.mode == 'r':
                contents = f.read()
                print(contents)
                return contents
        except Exception as e:
            print(e)
