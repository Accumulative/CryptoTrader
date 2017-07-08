from poloniex import Poloniex
from botlog import BotLog

class BotChart(object):
    def __init__(self, exchange, pair, period, startTime, endTime):
        self.output = BotLog()
        
        self.conn = Poloniex('key','secret')
        
        self.pair = pair
        self.period = period

        self.startTime = startTime
        self.endTime = endTime

        self.output.log("Getting chart data...")
        self.data = self.conn.returnChartData(currencyPair=self.pair,start=self.startTime,end=self.endTime,period=self.period)    
        

    def getPoints(self):
        return self.data