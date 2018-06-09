import sys
sys.path.append("Models")
sys.path.append("Loggers")
sys.path.append("Other")
from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import datetime
from botaccount import BotAccount
from machinelearning import maclearn

class BotStrategy(object):
    def __init__(self, functions, balance, trial, details, strat):
        self.output = BotLog()
        self.prices = []
        self.startPrice = 0
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
        self.indicators = BotIndicators()

        self.dirty = False
        self.fee = 0.0025
        self.mcl = 0
        self.strat = strat
        
        self.lookback = 7 if not 'lookback' in details else details['lookback']
        self.learnProgTotal = 500 if not 'learnProgTotal' in details else details['learnProgTotal']
        self.advance = 5 if not 'advance' in details else details['advance']
        self.howSimReq = 0.95 if not 'howSimReq' in details else details['howSimReq']
        self.learnLimit = 700 if not 'learnLimit' in details else details['learnLimit']
        
        if(self.strat == '4'):
            self.mcl = maclearn(self.learnProgTotal, self.lookback, self.advance, self.howSimReq, self.learnLimit)
        
        self.trial = trial
        
        self.openTrades = []
        
        
        self.highMA = 47 if not 'highMA' in details else details['highMA']
        self.lowMA = 28 if not 'lowMA' in details else details['lowMA']
        self.mamultfactor = 1 if not 'maFactor' in details else details['maFactor']
        self.numSimulTrades = 1 if not 'simTrades' in details else details['simTrades']
        self.stoploss = 0 if not 'stoploss' in details else details['stoploss']
        
        self.lowrsi = 30 if not 'lowrsi' in details else details['lowrsi']
        self.highrsi = 70 if not 'highrsi' in details else details['highrsi']
        self.rsiperiod = 14 if not 'rsiperiod' in details else details['rsiperiod']
        
        self.upfactor = 1.1 if not 'upfactor' in details else details['upfactor']
        self.downfactor = 1.3 if not 'downfactor' in details else details['downfactor']
        
        self.trailingstop = 0.1 if not 'trailingstop' in details else details['trailingstop']
                
        
        
    def tick(self,candlestick, training=False):
        if 'weightedAverage' in candlestick:
            # HISTORIC VALUES
            self.currentPrice = float(candlestick['weightedAverage'])
        else:
            # LIVE VALUES
            self.currentPrice = float(candlestick['last'])
        self.prices.append(self.currentPrice)#
        
        if self.startPrice == 0:
            self.startPrice = self.currentPrice
        
        self.prices = self.prices[-100:]
        
        #self.currentClose = float(candlestick['close'])
        #self.closes.append(self.currentClose)
        self.currentDate = datetime.datetime.fromtimestamp(int(candlestick['date'])).strftime('%Y-%m-%d %H:%M:%S')
        
        
        self.indicators.doDataPoints(self.currentPrice, self.currentDate)
        
        #lastMax = 0 if len(self.indicators.localMax) == 0 else self.indicators.localMax[-1]
        #lastMin = 0 if len(self.indicators.localMin) == 0 else self.indicators.localMin[-1]
        
        # LOGGING
#        self.output.log("Date: "+self.currentDate+"\tPrice: "+str(self.currentPrice)+"\tLowMA: "+str(self.indicators.movingAverage(self.prices,self.lowMA))+ \
#        "\tHighMA: "+str(self.indicators.movingAverage(self.prices,self.lowMA))+"\tRSI: "+str(self.indicators.RSI (self.prices))+"\tTrend :"+str(self.indicators.trend)+"\tLast Max "+ \
#        str(lastMax) + "\tLast Min: "+str(lastMin) + "\tRes: "+str(self.indicators.currentResistance)+"\tSup: "+str(self.indicators.currentSupport))
        
        
        self.evaluatePositions(training)
        if not training:
            self.updateOpenTrades()
            if self.dirty and self.trial == 0:
                self.showAllTrades()
                self.dirty = False

    def evaluatePositions(self, training):
        changeCheck= self.trades.copy()
        self.openTrades = []
        for trade in self.trades:
            if (trade.status == "OPEN"):
                self.openTrades.append(trade)
        
        if '1' in self.strat:
            self.MACrossover()
        if '2' in self.strat:
            self.BuyLowSellHigh()   
        if '3' in self.strat:
            self.BuyUpShortCrash()
        if '4' in self.strat:
            self.LearnPatterns(training)
        
        if changeCheck != self.trades:
            self.dirty = True
                
                
    def handleStopLosses(self, trade):
        if (self.stoploss != 0):
#                print("2", trade.id , self.currentPrice, trade.stopLoss)
            if (self.currentPrice < trade.stopLoss ):
                self.trades[trade.id].close(self.currentDate, self.currentPrice, "Stoploss")
                self.balance += trade.volume * self.currentPrice
                
    def handleTrailingStop(self, trade):
        if (self.trailingstop != 0):
            if(trade.maxSeen < self.currentPrice):
                trade.maxSeen = self.currentPrice
                
            if (self.currentPrice < trade.maxSeen * (1 - self.trailingstop) ):
                trade.close(self.currentDate, self.currentPrice, "Trailing")
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
       marketProf = (self.prices[-1] - self.startPrice)/self.startPrice
       self.output.log("Market profit is " + str(marketProf))
       return totalProfit, marketProf
   
#==============================================================================
# Strategies
#==============================================================================

#    Strat 1
    def MACrossover(self):
        fifteenDayMA = self.indicators.movingAverage(self.prices,self.lowMA)
        fiftyDayMA = self.indicators.movingAverage(self.prices,self.highMA)
        if (fifteenDayMA > fiftyDayMA * self.mamultfactor ):
            amountToBuy = (self.balance-10) / (self.currentPrice * (1+self.fee))
            fee = amountToBuy * self.currentPrice * self.fee
            if (len(self.openTrades) < self.numSimulTrades and self.balance >= fee + amountToBuy * self.currentPrice + 10):
                
                stoplossn = self.currentPrice * (1-self.stoploss)
                
                self.balance -= (amountToBuy * self.currentPrice + fee)
                self.trades.append(BotTrade(self.functions, self.currentDate, amountToBuy, self.currentPrice,len(self.trades),stopLoss=stoplossn, fee=fee))

        for trade in self.openTrades:
            if (fifteenDayMA < fiftyDayMA / self.mamultfactor):
                self.balance += trade.volume * self.currentPrice
                self.trades[trade.id].close(self.currentDate, self.currentPrice, "MA Crossover")
            else:
                #                    self.handleStopLosses(trade)
                self.handleTrailingStop(trade)
                
                
#   Strat 2
    def BuyLowSellHigh(self):
        rsi = self.indicators.RSI(self.prices,self.rsiperiod)
        if (rsi < self.lowrsi ):
            amountToBuy = (self.balance-10) / (self.currentPrice * (1+self.fee))
            fee = amountToBuy * self.currentPrice * self.fee
            if (len(self.openTrades) < self.numSimulTrades and self.balance >= fee + amountToBuy * self.currentPrice + 10):
                
                stoplossn = self.currentPrice * (1-self.stoploss)
                
                self.balance -= (amountToBuy * self.currentPrice + fee)
                self.trades.append(BotTrade(self.functions, self.currentDate, amountToBuy, self.currentPrice,len(self.trades),stopLoss=stoplossn, fee=fee))

        for trade in self.openTrades:
            if (rsi > self.highrsi ):
                self.balance += trade.volume * self.currentPrice
                self.trades[trade.id].close(self.currentDate, self.currentPrice, "Overbought RSI")
            else:
                self.handleStopLosses(trade)
          
            
#    Strat 3
    def BuyUpShortCrash(self):
#        SIm trades can only be 1
        if len(self.prices) > self.lookback:
            if(self.currentPrice > self.prices[-self.lookback] * self.upfactor):
                amountToBuy = (self.balance-10) / (self.currentPrice * (1+self.fee))
                fee = amountToBuy * self.currentPrice * self.fee
                if (self.balance >= fee + amountToBuy * self.currentPrice + 10):
                    
                    stoplossn = self.currentPrice * (1-self.stoploss)
                    
                    self.balance -= (amountToBuy * self.currentPrice + fee)
                    self.trades.append(BotTrade(self.functions, self.currentDate, amountToBuy, self.currentPrice,len(self.trades),stopLoss=stoplossn, fee=fee))
    
            for trade in self.openTrades:
                if(self.currentPrice < self.prices[-self.lookback] * self.downfactor):
                    self.balance += trade.volume * self.currentPrice
                    self.trades[trade.id].close(self.currentDate, self.currentPrice, "In crash")
                else:
                    self.handleStopLosses(trade)
                    
                    
#    Strat 4
    def LearnPatterns(self, training):
        
        toBuy = self.mcl.calc(self.prices)
        if not training:
            for trade in self.openTrades:
                if trade.expiry != 0:
                    if trade.age >= trade.expiry:
                        self.balance += trade.volume * self.currentPrice
                        self.trades[trade.id].close(self.currentDate, self.currentPrice, "Expired")
                    else:
                        self.trades[trade.id].age += 1
                        self.handleStopLosses(trade)
            
            if toBuy == "Buy":
                amountToBuy = (self.balance-10) / (self.currentPrice * (1+self.fee))
                fee = amountToBuy * self.currentPrice * self.fee
                if (self.balance >= fee + amountToBuy * self.currentPrice + 10) and (fee + amountToBuy * self.currentPrice + 10) > 100:
                    stoplossn = self.currentPrice * (1-self.stoploss)
                        
                    self.balance -= (amountToBuy * self.currentPrice + fee)
                    self.trades.append((BotTrade(self.functions, self.currentDate, amountToBuy, self.currentPrice,len(self.trades),stopLoss=stoplossn, fee=fee, expiry = self.advance, log=self.trial)))
                    
                    
            elif toBuy == "Sell"and len(self.trades) > 0:
                if self.trades[-1].status != "CLOSED":
                    self.balance += self.trades[-1].volume * self.currentPrice
                    #print(self.balance, self.trades[-1].volume, self.currentPrice, '', self.trades[-1].id)
                    self.trades[-1].close(self.currentDate, self.currentPrice, "Sell indicator")
                
                
            
                        
            
        