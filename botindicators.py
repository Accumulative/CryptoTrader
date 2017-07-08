import numpy as np
from botgraph import BotGraph

class BotIndicators(object):
    def __init__(self):
        self.currentResistance = 0.018
        self.localMax = []
        self.dataPoints = []
        self.grapher = BotGraph()
        
    def graphIndicators(self):
        self.grapher.outputGraph(self.dataPoints)

    def movingAverage(self, dataPoints, period):
        if (len(dataPoints) > 1):
            return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
        return 0
        
    def momentum (self, dataPoints, period=14):
        if (len(dataPoints) > period -1):
            return dataPoints[-1] * 100 / dataPoints[-period]
        
    def RSI (self, prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter

            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(period - 1) + upval)/period
            down = (down*(period - 1) + downval)/period

            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)

        if len(prices) > period:
            return rsi[-1]
        else:
            return 50 # output a neutral amount until enough prices in list

    def doDataPoints(self, currentPrice, currentDate):
        
        self.dataPoints.append({'date':currentDate, 'price': str(currentPrice), 'trend': str(self.currentResistance), 'label': 'null', 'desc': 'null'})        
        
        if ( (len(self.dataPoints) > 2) and (self.dataPoints[-2]['price'] > self.dataPoints[-1]['price']) and (self.dataPoints[-2]['price'] > self.dataPoints[-3]['price']) ):
            self.dataPoints[-2]['label'] = "'MAX'"
            self.dataPoints[-2]['desc'] = "'This is a local maximum'"
            
            numberOfSimilarLocalMaxes = 0
            for oldMax in self.localMax:
                if ( (float(oldMax) > (float(self.dataPoints[-2]['price']) - .0001) ) and (float(oldMax) < (float(self.dataPoints[-2]['price']) + .0001) ) ):
                    numberOfSimilarLocalMaxes = numberOfSimilarLocalMaxes + 1

            if (numberOfSimilarLocalMaxes > 2):
                self.currentResistance = self.dataPoints[-2]['price']
                self.dataPoints[-2]['trend'] = self.dataPoints[-2]['price']
                self.dataPoints[-1]['trend'] = self.dataPoints[-2]['price']

            self.localMax.append(self.dataPoints[-2]['price'])
