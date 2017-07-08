
from poloniex import Poloniex
from botlog import BotLog

class BotChart(object):
    def __init__(self, exchange, pair, period, startTime, endTime):
        self.output = BotLog(startTime, endTime)
        
        self.conn = Poloniex('key','secret')
        
        self.pair = pair
        self.period = period

        self.startTime = startTime
        self.endTime = endTime

        self.output.log("Getting balance data...")
        self.data = {k: v for k, v in self.conn.returnBalances().items() if float(v) != 0}     
        

    def getBalance(self):
        return self.data 