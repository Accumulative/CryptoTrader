# -*- coding: utf-8 -*-
from bottrade import BotTrade
from botindicators import BotIndicators

class StrategyLib(object):
    def __init__(self):
        self.indicators = BotIndicators()
    
    def MACrossover(self, lowMA, highMA):
        fifteenDayMA = self.indicators.movingAverage(self.prices,self.lowMA)
        fiftyDayMA = self.indicators.movingAverage(self.prices,self.highMA)
    #        print(fifteenDayMA, fiftyDayMA)
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