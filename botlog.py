import os
import datetime

class BotLog(object):
    def __init__(self):
        folder = "Logs/" + datetime.datetime.now().strftime('%Y%m%d')
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.destination = folder + "/output.txt"
        pass

    def log(self, m):
        with open(self.destination, "a") as text_file:
            print(m, file=text_file)
        print(m)