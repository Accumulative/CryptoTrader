from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import datetime
from botaccount import BotAccount

class BotStrategy(object):
    def __init__(self, functions, balance, trial, details):
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
        self.numSimulTrades = 1 if not 'simTrades' in details else details['simTrades']
        self.indicators = BotIndicators()
        self.currentId = 0
        self.dirty = False
        self.fee = 0.0025
        self.mamultfactor = 1.1 if not 'maFactor' in details else details['maFactor']
        self.trial = trial
        self.highMA = 60 if not 'highMA' in details else details['highMA']
        self.lowMA = 40 if not 'lowMA' in details else details['lowMA']
        self.openTrades = []
                
        
    def tick(self,candlestick):
        if 'weightedAverage' in candlestick:
            # HISTORIC VALUES
            self.currentPrice = float(candlestick['weightedAverage'])
        else:
            # LIVE VALUES
            self.currentPrice = float(candlestick['last'])
        self.prices.append(self.currentPrice)#
        self.prices = self.prices[-100:]
        
        #self.currentClose = float(candlestick['close'])
        #self.closes.append(self.currentClose)
        self.currentDate = datetime.datetime.fromtimestamp(int(candlestick['date'])).strftime('%Y-%m-%d %H:%M:%S')
        
        
        self.indicators.doDataPoints(self.currentPrice, self.currentDate)
        
        lastMax = 0 if len(self.indicators.localMax) == 0 else self.indicators.localMax[-1]
        lastMin = 0 if len(self.indicators.localMin) == 0 else self.indicators.localMin[-1]
        
        # LOGGING
#        self.output.log("Date: "+self.currentDate+"\tPrice: "+str(self.currentPrice)+"\tLowMA: "+str(self.indicators.movingAverage(self.prices,self.lowMA))+ \
#        "\tHighMA: "+str(self.indicators.movingAverage(self.prices,self.lowMA))+"\tRSI: "+str(self.indicators.RSI (self.prices))+"\tTrend :"+str(self.indicators.trend)+"\tLast Max "+ \
#        str(lastMax) + "\tLast Min: "+str(lastMin) + "\tRes: "+str(self.indicators.currentResistance)+"\tSup: "+str(self.indicators.currentSupport))
        
        
        self.evaluatePositions()
        self.updateOpenTrades()
        if self.dirty and self.trial == 0:
            self.showAllTrades()
            self.dirty = False

    def evaluatePositions(self):
        changeCheck= self.trades.copy()
        self.openTrades = []
        for trade in self.trades:
            if (trade.status == "OPEN"):
                self.openTrades.append(trade)
        
        
        self.MACrossover()        
        
        if changeCheck != self.trades:
            self.dirty = True
    
    def MACrossover(self):
        fifteenDayMA = self.indicators.movingAverage(self.prices,self.lowMA)
        fiftyDayMA = self.indicators.movingAverage(self.prices,self.highMA)
        if (len(self.openTrades) < self.numSimulTrades):
            if (fifteenDayMA > fiftyDayMA * self.mamultfactor ):
                amountToBuy = self.balance * 0.2 / self.currentPrice
                fee = amountToBuy * self.currentPrice * self.fee
                stoploss = self.currentPrice * 0.1
                self.currentId += 1
                self.balance -= (amountToBuy * self.currentPrice + fee)
                self.trades.append(BotTrade(self.functions, self.currentDate, amountToBuy, self.currentPrice,self.currentId,stopLoss=stoploss, fee=fee))

        for trade in self.openTrades:
            if (fifteenDayMA < fiftyDayMA / self.mamultfactor):
                self.balance += trade.volume * self.currentPrice
                trade.close(self.currentDate, self.currentPrice, "MA Crossover")
            elif (trade.stopLoss):
                if (trade.entryPrice - self.currentPrice > trade.stopLoss):
                    trade.close(self.currentDate, self.currentPrice, "Stoploss")
                    self.balance += trade.volume * self.currentPrice
    
    def updateOpenTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.tick(self.currentPrice)
    
    def showAllTrades(self):
        self.output.logTrades(self.trades, self.origBalance, self.trial)
        self.indicators.graphIndicators(self.trades)
    
    
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
       marketProf = (self.prices[-1] - self.prices[0])/self.prices[0]
       self.output.log("Market profit is " + str(marketProf))
       return totalProfit, marketProf