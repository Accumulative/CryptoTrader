from poloniex import Poloniex
from botlog import BotLog
import time

class poloniex_functions(object):
    def __init__(self):
        self.output = BotLog()
        self.conn = Poloniex('secret','key')
        
        
    def getBalance(self):
        while True:
            try:
                balData = {k: v for k, v in self.conn.returnBalances().items() if float(v) != 0} 
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return balData
      
    def getCurrencies(self):
        while True:
            try:
                tickData = [k for k,v in self.conn.returnTicker().items()]
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return tickData
    
    def getNextTick(self, pair):
        while True:
            try:
                tickData = self.conn.returnTicker()[pair]  
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return tickData
        
    def getHistoricTicks(self, pair,startTime,endTime,period):
        while True:
            try:
                result = self.conn.returnChartData(currencyPair=pair,start=startTime,end=endTime,period=period)  
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return result
        
        
    def sell(self, pair, rate, amount):
        try:
            result = self.conn.sell(currencyPair = pair, rate = rate, amount = amount)  
        except Exception as e:
            self.output.log("Error: " + str(e))
            time.sleep(20)
        return result
        
        
    def buy(self, pair, rate, amount):
        try:
            result = self.conn.buy(currencyPair = pair, rate = rate, amount = amount)  
        except Exception as e:
            self.output.log("Error: " + str(e))
            time.sleep(20)
        return result
        
    def returnOrderTrades(self, orderId):
        while True:
            try:
                result = self.conn.returnOrderTrades(orderId)
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return result
    
#==============================================================================
#     Returns your open orders for a given market, specified by the "currencyPair" POST parameter, 
#     e.g. "BTC_XCP". Set "currencyPair" to "all" to return open orders for all markets. Sample output for single market:
#==============================================================================
    def returnOpenOrders(self, currencyPair = 'All'):
        while True:
            try:
                result = self.conn.returnOpenOrders(currencyPair)
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return result
    
#==============================================================================
#     Cancels an order you have placed in a given market. Required POST parameter is "orderNumber". If successful, the method will return:
#==============================================================================
    def cancelOrder(self, orderNumber):
        while True:
            try:
                result = self.conn.cancelOrder(orderNumber)
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return result
    
#==============================================================================
#     Cancels an order and places a new one of the same type in a single atomic transaction, meaning either both operations will succeed or both will fail. 
#     Required POST parameters are "orderNumber" and "rate"; you may optionally specify "amount" if you wish to change 
#     the amount of the new order. "postOnly" or "immediateOrCancel" may be specified for exchange orders, but will have no effect on margin orders.
#==============================================================================
    def moveOrder(self, orderNumber, rate, amount):
        while True:
            try:
                result = self.conn.moveOrder(orderNumber, rate, amount)
                break
            except Exception as e:
                self.output.log("Error: " + str(e))
                time.sleep(20)
                continue
        return result