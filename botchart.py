from poloniex import Poloniex
from botlog import BotLog

class BotChart(object):
    def __init__(self, exchange, pair, period):
        self.output = BotLog()
        
        self.output.log("Logging in...")
        self.conn = Poloniex('key','secret')
        
        self.pair = pair
        self.period = period

        self.startTime = 1491048000
        self.endTime = 1491591200

        self.output.log("Getting chart data...")
        self.data = self.conn.returnChartData(currencyPair=self.pair,start=self.startTime,end=self.endTime,period=self.period)    
        

    def getPoints(self):
        return self.data