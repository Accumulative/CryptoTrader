import sys
sys.path.append("Models")
sys.path.append("Loggers")
sys.path.append("Other")
from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import datetime
from botaccount import BotAccount

class BotStrategy(object):
    def __init__(self, period, functions, balance, trial, details, strat, trained_model="", defTrades = []):
        self.output = BotLog()
        self.prices = []
        self.period = period
        self.startPrice = 0
        self.closes = [] # Needed for Momentum Indicator
        self.trades = defTrades
        self.currentPrice = 0
        self.startDate = ""
        self.currentDate = ""
        self.currentClose = ""
        self.functions = functions
        self.balance = balance
        self.origBalance = balance
        self.account = BotAccount(self.functions)
        self.account.createBalancePage()
        self.startingPositions = self.account.getBalance()
        self.indicators = BotIndicators()
        self.trained_model = trained_model

        self.dirty = True
        self.fee = 0.0025
        self.strat = strat
        
        self.lookback = 7 if not 'lookback' in details else int(details['lookback'])
        
        self.trial = trial
        
        self.openTrades = []
        self.balanceRecord = []
        
        self.highMA = 47 if not 'highMA' in details else details['highMA']
        self.lowMA = 28 if not 'lowMA' in details else details['lowMA']
        self.mamultfactor = 1 if not 'maFactor' in details else details['maFactor']
        self.numSimulTrades = 1 if not 'simTrades' in details else details['simTrades']
        self.stoploss = 0 if not 'stoploss' in details else float(details['stoploss'])
        self.advance = 13 if not 'advance' in details else int(details['advance'])
        
        self.lowrsi = 30 if not 'lowrsi' in details else details['lowrsi']
        self.highrsi = 70 if not 'highrsi' in details else details['highrsi']
        self.rsiperiod = 14 if not 'rsiperiod' in details else details['rsiperiod']
        self.learnProgTotal = 1400 if not 'learnProgTotal' in details else int(details['learnProgTotal'])
        
        self.upfactor = 1.1 if not 'upfactor' in details else details['upfactor']
        self.downfactor = 1.3 if not 'downfactor' in details else details['downfactor']
        self.trailingstop = 0.1 if not 'trailingstop' in details else details['trailingstop']

        self.prev_run_time = 0 if not 'running_time' in details else int(details['running_time'])

        self.stoploss_day_count = 0
        self.stoploss_day_count_set = 0 if not 'stoplossDayCount' in details else details['stoplossDayCount']    
        
        
        # initiate any trades left over from last time
        for trade in self.trades:
            trade.stopLoss = trade.entryPrice * (1-self.stoploss)
            if '4' in self.strat:
                trade.expiry = self.advance
            trade.log = self.trial
        
    def tick(self,candlestick, training=False):
        if not self.trial == 0 or training:
            # HISTORIC VALUES
            self.currentPrice = float(candlestick['weightedAverage'])
        else:
            # LIVE VALUES
            self.currentPrice = float(candlestick['last'])
        self.prices.append(self.currentPrice)#
        
        
        self.prices = self.prices[-self.learnProgTotal-10:]
        
        #self.currentClose = float(candlestick['close'])
        #self.closes.append(self.currentClose)
        self.currentDateOrig = int(candlestick['date'])
        self.currentDate = datetime.datetime.fromtimestamp(int(candlestick['date'])).strftime('%Y-%m-%d %H:%M:%S')
        
        if self.startPrice == 0 and not training:
            self.startPrice = self.currentPrice
            self.startDate = self.currentDateOrig
        
        #self.indicators.doDataPoints(self.currentPrice, self.currentDateOrig, self.strat)
        
        if(self.stoploss_day_count != 0):
            self.stoploss_day_count -= 1
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
                # self.showAllTrades()
                self.dirty = False
                totalAssets, totalFees, totalTime, _ = self.calculateCurrentPosition()
                stats = { "balance" : self.balance, 
                          "assets"  : totalAssets,
                    "running_time"  : self.prev_run_time + int(self.currentDateOrig) - int(self.startDate)
                        }
                self.functions.mysql_conn.storeStatistics(stats);

    def evaluatePositions(self, training):
        changeCheckTrades = self.trades.copy()
        changeCheckBal = self.balance

        self.getOpenTrades();
        
        if '1' in self.strat:
            self.MACrossover()
        if '2' in self.strat:
            self.BuyLowSellHigh()   
        if '3' in self.strat:
            self.BuyUpShortCrash()
        if '4' in self.strat:
            self.LearnPatterns(training)
            
        
        if changeCheckTrades != self.trades or self.balance != changeCheckBal:
            self.dirty = True
            assets, _, _, marketProf = self.calculateCurrentPosition()
            self.balanceRecord.append([self.currentDateOrig, self.balance+assets,self.origBalance* marketProf])
            # print(self.balance)

    def getOpenTrades(self):
        self.openTrades = []
        for trade in self.trades:
            if (trade.status == "OPEN"):
                self.openTrades.append(trade)
                
    def handleStopLosses(self, trade):
        if (self.stoploss != 0):
            if ((self.currentPrice < trade.stopLoss and trade.volume < 0) or (self.currentPrice > trade.stoploss and trade.volume >= 0)):
                self.trades[trade.id].close(self.currentDateOrig, self.currentPrice, "Stoploss")
                self.balance += trade.volume * self.currentPrice
                self.stoploss_day_count = self.stoploss_day_count_set
                
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
        #self.indicators.graphIndicators(self.trades, self.balanceRecord)
    
    
    def closeAllTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                if(trade.volume >= 0):
                    self.closeLong(trade.id);
                else:
                    self.closeShort(trade.id);
        self.showAllTrades()
        
    def calculateCurrentPosition(self):
        totalAssets = 0
        totalFees = 0
        totalTime = 0
        for trade in self.trades:
            if trade.status == "OPEN":
                totalAssets += self.currentPrice * trade.volume
            totalFees += trade.fee
            totalTime += (int(self.currentDateOrig) - int(trade.dateOpened) if trade.dateClosed == "" else int(trade.dateClosed) - int(trade.dateOpened))
        marketProf = (self.currentPrice - self.startPrice)/self.startPrice
        return totalAssets, totalFees, totalTime, marketProf
   
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
        
        toBuy, predictions = self.trained_model.calc(self.prices)
        if not training:
            
            for trade in self.openTrades:
                # if trade.expiry != 0:
                    # if trade.age >= trade.expiry:
                        # self.balance += trade.volume * self.currentPrice
                        # self.trades[trade.id].close(self.currentDate, self.currentPrice, "Expired")
                    # else:
                self.trades[trade.id].age += 1
                self.handleStopLosses(trade)

            self.getOpenTrades();

            if (self.stoploss_day_count == 0 or self.stoploss_day_count_set == 0):
                if toBuy == "Buy":
                    if len(self.openTrades) > 0:
                        if self.trades[-1].volume < 0:
                            self.closeShort(-1);
                    else:
                        amountToBuy = (self.balance-10) / (self.currentPrice * (1+self.fee))
                        self.openLong(amountToBuy);
                        
                elif toBuy == "Sell":
                    if len(self.openTrades) > 0:
                        if self.trades[-1].volume >= 0:
                            self.closeLong(-1);
                    else:
                        amountToSell = (self.balance-10) / (self.currentPrice * (1+self.fee))
                        self.openShort(amountToSell)

            if self.trial == 0 :
                self.functions.mysql_conn.storePredictions(self.currentDateOrig, self.period, predictions)
                
    def openLong(self, amt):
        fee = amt * self.currentPrice * self.fee
        if (self.balance >= fee + amt * self.currentPrice) and (fee + amt * self.currentPrice) > self.origBalance * 0.02:
            stoplossn = self.currentPrice * (1-self.stoploss)
            self.balance -= (amt * self.currentPrice + fee)
            self.trades.append((BotTrade(self.functions, self.currentDateOrig, amt, self.currentPrice,len(self.trades),stopLoss=stoplossn, fee=fee, expiry = self.advance, log=self.trial)))
                
    def closeLong(self, tradeId):
        if self.trades[tradeId].status != "CLOSED":
            self.balance += self.trades[tradeId].volume * self.currentPrice
            self.trades[tradeId].close(self.currentDateOrig, self.currentPrice, "Sell indicator")

    def openShort(self, amt):
        fee = amt * self.currentPrice * self.fee
        if (self.balance >= fee + amt * self.currentPrice + 10) and (fee + amt * self.currentPrice + 10) > self.origBalance * 0.02:
            stoplossn = self.currentPrice * (1+self.stoploss)
            self.balance += (amt * self.currentPrice - fee)
            self.trades.append((BotTrade(self.functions, self.currentDateOrig, -1*amt, self.currentPrice,len(self.trades),stopLoss=stoplossn, fee=fee, expiry = self.advance, log=self.trial)))
                
    def closeShort(self, tradeId):
        if self.trades[tradeId].status != "CLOSED":
            self.balance += self.trades[tradeId].volume * self.currentPrice
            self.trades[tradeId].close(self.currentDateOrig, self.currentPrice, "Buy indicator")
            
                        
            
        