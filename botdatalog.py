import os

class BotDataLog(object):
    def __init__(self, pair, startDate, endDate):
        if not os.path.exists("Data"):
            os.makedirs("Data")
        self.destination = "Data/"+pair+"_"+ str(startDate) + "_" + str(endDate) + ".txt"
        self.write = (False if os.path.exists(self.destination) else True)
  
    def logPoint(self, point):
        if self.write:
            with open(self.destination, "a") as text_file:
                print(point, file=text_file)