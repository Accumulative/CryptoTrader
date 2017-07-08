from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import datetime

class BotStrategy(object):
    def __init__(self):
        self.output = BotLog()
        self.prices = []
        self.closes = [] # Needed for Momentum Indicator
        self.trades = []
        self.currentPrice = ""
        self.currentDate = ""
        self.currentClose = ""
        self.numSimulTrades = 1
        self.indicators = BotIndicators()
        

    def tick(self,candlestick):
        self.currentPrice = float(candlestick['weightedAverage'])
        self.prices.append(self.currentPrice)
        
        self.currentClose = float(candlestick['close'])
        self.closes.append(self.currentClose)
        self.currentDate = datetime.datetime.fromtimestamp(int(candlestick['date'])).strftime('%Y-%m-%d %H:%M:%S')
        
        # LOGGING
        self.output.log("Date: "+self.currentDate+"\tPrice: "+str(self.currentPrice)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

        self.indicators.doDataPoints(self.currentPrice, self.currentDate)
        self.evaluatePositions()
        self.updateOpenTrades()
        #self.showPositions()

    def evaluatePositions(self):
        openTrades = []
        for trade in self.trades:
            if (trade.status == "OPEN"):
                openTrades.append(trade)

        if (len(openTrades) < self.numSimulTrades):
            if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
                self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))

        for trade in openTrades:
            if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
                trade.close(self.currentPrice)

    def updateOpenTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.tick(self.currentPrice)

    def showPositions(self):
        for trade in self.trades:
            trade.showTrade()
            
    def closeAllTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.close(self.currentPrice)
        
        self.indicators.graphIndicators()
   
    def calculateTotalProft(self):
       totalProfit = 0
       for trade in self.trades:
           totalProfit += trade.exitPrice - trade.entryPrice
           
       self.output.log("Total profit is:"+ str(totalProfit))