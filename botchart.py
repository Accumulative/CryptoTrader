from poloniex import Poloniex
from botlog import BotLog
import os
import json

class BotChart(object):
    def __init__(self, exchange, pair, period, startTime, endTime):
        self.output = BotLog()
        
        self.conn = Poloniex('key','secret')
        
        self.pair = pair
        self.period = period

        self.startTime = startTime
        self.endTime = endTime

        
        
        if not os.path.exists("Data/"+pair+"_"+ str(startTime) + "_" + str(endTime) + ".txt"):
            self.output.log("Getting chart data (API)...")
            self.data = self.conn.returnChartData(currencyPair=self.pair,start=self.startTime,end=self.endTime,period=self.period)    
        else:
            self.output.log("Getting chart data (Local)...")
            self.data = self.getDataFromFile("Data/"+pair+"_"+ str(startTime) + "_" + str(endTime) + ".txt")

    def getPoints(self):
        return self.data
    
    def getDataFromFile(self,path):
        dictionary = []
        with open(path, "r") as text_file:
            for line in text_file:
                json_acceptable_string = line.replace("'", "\"")
                dictionary.append(json.loads(json_acceptable_string))
        print(dictionary)
        return dictionary