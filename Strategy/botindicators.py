import sys

sys.path.append("Visualisation")

import numpy as np
from botgraph import BotGraph

class BotIndicators(object):
    def __init__(self):
        self.currentResistance = 0.018
        self.localMax = []
        self.localMin = []
        self.dataPoints = []
        self.grapher = BotGraph()
        self.timescale = 50
        self.closeratio = 0.05
        self.resistances = []
        self.supports = []
        self.currentSupport = 0.018
        self.trend = 'side' #side, up, down
        
    def graphIndicators(self, trades, balanceRec):
        self.grapher.outputGraph(self.dataPoints, trades, balanceRec)

    def movingAverage(self, dataPoints, period):
        if (len(dataPoints) > 1):
            return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
        return 0
    
    
    def momentum (self, dataPoints, period=14):
        if (len(dataPoints) > period -1):
            return dataPoints[-1] * 100 / dataPoints[-period]
        
    def RSI (self, prices, period=14):
        
        if len(prices) <= period:
            return 50 # output a neutral amount until enough prices in list
        
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

        self.currentRSI = rsi[-1]
        return rsi[-1]
            
    def doDataPoints(self, currentPrice, currentDate, strat):
        
        self.dataPoints.append({'date':currentDate, 'price': str(currentPrice), 'lowtrend': str(self.currentSupport),'hightrend': str(self.currentResistance), 'label': 'null', 'desc': 'null', 'buy': 'null', 'sell': 'null', 'myprof': 'null', 'bench': 'null'})        
#        self.dataPoints = self.dataPoints[-self.timescale-10:]
        if(strat != 4):
            if len(self.dataPoints) > self.timescale:
                localHigh = False
                for point in self.dataPoints[-self.timescale:-1]:
                    if self.dataPoints[-1]['price'] >= point['price']:
                        localHigh = True
                        if point['label'] == "'MAX'":
                            point['label'] = 'null'
                            self.localMax.pop()
                    else:
                        localHigh = False
                        break
                        
                if localHigh == False:
                    localLow = False
                    for point in self.dataPoints[-self.timescale:-1]:
                        if self.dataPoints[-1]['price'] <= point['price']:
                            localLow = True
                            if point['label'] == "'MIN'":
                                point['label'] = 'null'
                                self.localMin.pop()
                        else:
                            localLow = False
                            break
                
                if localHigh == True:
                    self.dataPoints[-1]['label'] = "'MAX'"
                    self.dataPoints[-1]['desc'] = "This is a local maximum"
                    self.localMax.append(float(self.dataPoints[-1]['price']))
                    
                elif localLow == True:
                    self.dataPoints[-1]['label'] = "'MIN'"
                    self.dataPoints[-1]['desc'] = "This is a local minimum"
                    self.localMin.append(float(self.dataPoints[-1]['price']))
                
                numberOfSimilarLocalMaxes = 0
                for oldMax in self.localMax:
                    if ( (float(oldMax) > (float(self.dataPoints[-1]['price']) / (1+self.closeratio)) ) and (float(oldMax) < (float(self.dataPoints[-1]['price']) * (1+self.closeratio)) ) ):
                        numberOfSimilarLocalMaxes = numberOfSimilarLocalMaxes + 1

                if (numberOfSimilarLocalMaxes >= 2):
                    self.currentResistance = self.dataPoints[-1]['price']
                    self.resistances.append(self.currentResistance)
                    self.dataPoints[-1]['lowtrend'] = self.dataPoints[-1]['price']
                    
                numberOfSimilarLocalMins = 0
                for oldMin in self.localMin:
                    if ( (float(oldMin) > (float(self.dataPoints[-1]['price']) / (1+self.closeratio)) ) and (float(oldMin) < (float(self.dataPoints[-1]['price']) * (1+self.closeratio)) ) ):
                        numberOfSimilarLocalMins = numberOfSimilarLocalMins + 1

                if (numberOfSimilarLocalMins >= 2):
                    self.currentSupport = self.dataPoints[-1]['price']
                    self.supports.append(self.currentSupport)
                    self.dataPoints[-1]['hightrend'] = self.dataPoints[-1]['price']
                    
                connectedHighsUpTrend = 0
                connectedLowsUpTrend = 0
                prevHigh =0
                prevLow =10000000000
                
                for i in range(0, len(self.localMax)-1):
                    if  self.localMax[len(self.localMax)-i-1] > prevHigh:
                        connectedHighsUpTrend += 1
                        prevHigh = self.localMax[len(self.localMax)-i-1]
                    else:
                        break
                        
                for i in range(0, len(self.localMin)-1):
                    if self.localMin[len(self.localMin)-i-1] < prevLow:
                        connectedLowsUpTrend += 1
                        prevLow = self.localMin[len(self.localMin)-i-1]
                    else:
                        break
                
                connectedHighsDownTrend = 0
                connectedLowsDownTrend = 0
                prevHigh = 1000000000
                prevLow = 0
                for i in range(0, len(self.localMax)-1):
                    if  self.localMax[len(self.localMax)-i-1] < prevHigh:
                        connectedHighsDownTrend += 1
                        prevHigh = self.localMax[len(self.localMax)-i-1]
                    else:
                        break
                        
                for i in range(0, len(self.localMin)-1):
                    if  self.localMin[len(self.localMin)-i-1] > prevLow:
                        connectedLowsDownTrend += 1
                        prevLow = self.localMin[len(self.localMin)-i-1]
                    else:
                        break
                    
                if connectedHighsUpTrend >= 2 and connectedLowsUpTrend >= 2:
                    self.trend = 'up'
                elif connectedHighsUpTrend >= 2 and connectedLowsDownTrend >= 2:
                    self.trend = 'expand'
                elif connectedHighsDownTrend >= 2 and connectedLowsUpTrend >= 2:
                    self.trend = 'contract'
                elif connectedHighsDownTrend >= 2 and connectedLowsDownTrend >= 2:
                    self.trend = 'down'
                else:
                    self.trend = 'side'
            
                self.dataPoints[-1]['desc'] = "'"+self.dataPoints[-1]['desc']+" - "+self.trend+"'"
            

            
