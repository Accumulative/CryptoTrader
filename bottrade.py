from botlog import BotLog

class BotTrade(object):
    def __init__(self,dateO, volume, currentPrice,tradeId,stopLoss=0):
        self.output = BotLog()
        self.status = "OPEN"
        self.entryPrice = currentPrice
        self.exitPrice = ""
        self.dateOpened = dateO
        self.volume = volume
        self.dateClosed = ""
        self.output.log("Trade opened ({0}) at {1}".format(tradeId,currentPrice))
        if (stopLoss):
            self.stopLoss = currentPrice - stopLoss
        self.id = tradeId
    
    def close(self, dateC, currentPrice):
        self.status = "CLOSED"
        self.exitPrice = currentPrice
        self.dateClosed = dateC
        self.output.log("Trade opened ({0}): {1} at {2}".format(self.id,self.volume, self.exitPrice))

    def tick(self, currentPrice):
        pass


    def showTrade(self):
        tradeStatus = [str(self.entryPrice),str(self.status),str(self.exitPrice)]

#        if (self.status == "CLOSED"):
#            tradeStatus = tradeStatus + " Profit: "
#            if (self.exitPrice > self.entryPrice):
#                tradeStatus = tradeStatus + "\033[92m"
#            else:
#                tradeStatus = tradeStatus + "\033[91m"
#
#            tradeStatus = tradeStatus+str(self.exitPrice - self.entryPrice)+"\033[0m"
        
        self.output.logTrade(tradeStatus)
    