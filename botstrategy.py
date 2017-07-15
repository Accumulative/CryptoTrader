from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import datetime
from botaccount import BotAccount

class BotStrategy(object):
    def __init__(self, balance):
        self.output = BotLog()
        self.prices = []
        self.closes = [] # Needed for Momentum Indicator
        self.trades = []
        self.currentPrice = 0
        self.currentDate = ""
        self.currentClose = ""
        self.balance = balance
        self.account = BotAccount()
        self.account.createBalancePage()
        self.startingPositions = self.account.getBalance()
        self.numSimulTrades = 1
        self.indicators = BotIndicators()
        self.currentId = 0
        self.dirty = False
        

    def tick(self,candlestick):
        if 'weightedAverage' in candlestick:
            # HISTORIC VALUES
            self.currentPrice = float(candlestick['weightedAverage'])
        else:
            # LIVE VALUES
            self.currentPrice = float(candlestick['last'])
        self.prices.append(self.currentPrice)
        
        #self.currentClose = float(candlestick['close'])
        #self.closes.append(self.currentClose)
        self.currentDate = datetime.datetime.fromtimestamp(int(candlestick['date'])).strftime('%Y-%m-%d %H:%M:%S')
        
        # LOGGING
        self.output.log("Date: "+self.currentDate+"\tPrice: "+str(self.currentPrice)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

        self.indicators.doDataPoints(self.currentPrice, self.currentDate)
        self.evaluatePositions()
        self.updateOpenTrades()
        if self.dirty:
            self.showAllTrades()
            self.dirty = False

    def evaluatePositions(self):
        changeCheck= self.trades.copy()
        openTrades = []
        for trade in self.trades:
            if (trade.status == "OPEN"):
                openTrades.append(trade)

        if (len(openTrades) < self.numSimulTrades and self.balance > self.currentPrice * 5 ):
            if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
                self.currentId += 1
                self.balance -= 5000 * self.currentPrice
                self.trades.append(BotTrade(self.currentDate, 5000, self.currentPrice,self.currentId,stopLoss=.001))

        for trade in openTrades:
            if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
                trade.close(self.currentDate, self.currentPrice)
                self.balance += 5000 * self.currentPrice
            elif (trade.stopLoss):
                if (self.currentPrice - trade.entryPrice < trade.stopLoss):
                    trade.close(self.currentDate, self.currentPrice)
                    self.balance += 5000 * self.currentPrice
        if changeCheck != self.trades:
            self.dirty = True

    def updateOpenTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.tick(self.currentPrice)
    
    def showAllTrades(self):
        self.output.logTrades(self.trades)
        self.indicators.graphIndicators()
    
    
    def closeAllTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.close(self.currentPrice)
                self.balance += 5000 * self.currentPrice
        
        
   
    def calculateTotalProft(self):
       totalProfit = 0
       for trade in self.trades:
           totalProfit += (trade.exitPrice - trade.entryPrice) * trade.volume
           
       self.output.log("Total profit is:"+ str(totalProfit))
       self.output.log("Total balance is:"+ str(self.balance))