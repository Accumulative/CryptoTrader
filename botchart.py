from botlog import BotLog
import os
import json
import time
import pandas as pd

class BotChart(object):
    def __init__(self, functions, pair):
        self.pair = pair
        self.output = BotLog()
        self.conn = functions.poloniex_conn
    
    def getHistorical(self, period, startTime, endTime):
        self.period = period
        self.startTime = startTime
        self.endTime = endTime

        if not os.path.exists("Data/"+self.pair+"_"+ str(startTime) + "_" + str(endTime)+"_"+str(self.period) + ".pkl"):
            self.output.log("Getting chart data (API)...")
            while True:
                try:
                    self.data = pd.DataFrame(self.conn.getHistoricTicks(self.pair, self.startTime, self.endTime, self.period))
                    self.data.to_pickle("Data/"+self.pair+"_"+ str(startTime) + "_" + str(endTime)+"_"+str(self.period) + ".pkl")
                    break
                except Exception as e:
                    self.output.log("Error: " + str(e))
                    time.sleep(20)
                    continue
        else:
            self.output.log("Getting chart data (Local)...")
            self.data = self.__getDataFromFile("Data/"+self.pair+"_"+ str(startTime) + "_" + str(endTime)+"_"+str(self.period) + ".pkl")

    def getPoints(self):
        return self.data
    
    def __getDataFromFile(self,path):
        
        return pd.read_pickle(path)
        
    def getNext(self):
        self.output.log("Getting next tick...")
        return self.conn.getNextTick(self.pair)