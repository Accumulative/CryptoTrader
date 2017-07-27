from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import datetime
from botaccount import BotAccount

class BotStrategy(object):
    def __init__(self, functions, balance):
        self.output = BotLog()
        self.prices = []
        self.closes = [] # Needed for Momentum Indicator
        self.trades = []
        self.currentPrice = 0
        self.currentDate = ""
        self.currentClose = ""
        self.functions = functions
        self.balance = balance
        self.origBalance = balance
        self.account = BotAccount(self.functions)
        self.account.createBalancePage()
        self.startingPositions = self.account.getBalance()
        self.numSimulTrades = 1
        self.indicators = BotIndicators()
        self.currentId = 0
        self.dirty = False
        self.fee = 0.0025
        

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
        #self.output.log("Date: "+self.currentDate+"\tPrice: "+str(self.currentPrice)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

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
        
        fifteenDayMA = self.indicators.movingAverage(self.prices,20)
        fiftyDayMA = self.indicators.movingAverage(self.prices,50)
        factor = 1.00
        if (len(openTrades) < self.numSimulTrades):
            if (fifteenDayMA > fiftyDayMA * factor ):
                amountToBuy = self.balance * 0.2 / self.currentPrice
                fee = amountToBuy * self.currentPrice * self.fee
                stoploss = self.currentPrice * 0.1
                self.currentId += 1
                self.balance -= (amountToBuy * self.currentPrice + fee)
                self.trades.append(BotTrade(self.functions, self.currentDate, amountToBuy, self.currentPrice,self.currentId,stopLoss=stoploss, fee=fee))

        for trade in openTrades:
            if (fifteenDayMA < fiftyDayMA / factor):
                self.balance += trade.volume * self.currentPrice
                trade.close(self.currentDate, self.currentPrice, "MA Crossover")
            elif (trade.stopLoss):
                if (trade.entryPrice - self.currentPrice > trade.stopLoss):
                    trade.close(self.currentDate, self.currentPrice, "Stoploss")
                    self.balance += trade.volume * self.currentPrice
        if changeCheck != self.trades:
            self.dirty = True

    def updateOpenTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.tick(self.currentPrice)
    
    def showAllTrades(self):
        self.output.logTrades(self.trades, self.origBalance)
        self.indicators.graphIndicators()
    
    
    def closeAllTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.close(self.currentDate, self.currentPrice, "Last trade")
                self.balance += trade.volume * self.currentPrice
        self.showAllTrades()
        
   
    def calculateTotalProft(self):
       totalProfit = 0
       totalFees = 0
       for trade in self.trades:
           totalProfit += (trade.exitPrice - trade.entryPrice) * trade.volume - trade.fee
           totalFees += trade.fee
           
       self.output.log("Total profit is:"+ str(totalProfit))
       self.output.log("Total balance is:"+ str(self.balance))
       self.output.log("Total fees are:"+ str(totalFees))