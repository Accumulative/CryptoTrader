from botlog import BotLog
import os
import json
import time

class BotChart(object):
    def __init__(self, functions, pair):
        self.pair = pair
        self.output = BotLog()
        self.conn = functions.poloniex_conn
    
    def getHistorical(self, period, startTime, endTime):
        self.period = period
        self.startTime = startTime
        self.endTime = endTime

        if not os.path.exists("Data/"+self.pair+"_"+ str(startTime) + "_" + str(endTime)+"_"+str(self.period) + ".txt"):
            self.output.log("Getting chart data (API)...")
            while True:
                try:
                    self.data = self.conn.getHistoricTicks(self.pair, self.startTime, self.endTime, self.period) 
                    break
                except Exception as e:
                    self.output.log("Error: " + str(e))
                    time.sleep(20)
                    continue
        else:
            self.output.log("Getting chart data (Local)...")
            self.data = self.__getDataFromFile("Data/"+self.pair+"_"+ str(startTime) + "_" + str(endTime)+"_"+str(self.period) + ".txt")

    def getPoints(self):
        return self.data
    
    def __getDataFromFile(self,path):
        dictionary = []
        with open(path, "r") as text_file:
            for line in text_file:
                json_acceptable_string = line.replace("'", "\"")
                dictionary.append(json.loads(json_acceptable_string))
        return dictionary
        
    def getNext(self):
        self.output.log("Getting next tick...")
        return self.conn.getNextTick(self.pair)