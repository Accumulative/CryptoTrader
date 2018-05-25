# -*- coding: utf-8 -*-

import numpy as np
import math

class maclearn(object):
    def __init__(self, learnProgTotal, lookback, advance, howSimReq, learnLimit):

        self.lookback = lookback
        self.learnProg = 0
        self.learnProgTotal = learnProgTotal
        self.inAdvance = advance
        self.patternAr = []
        self.performanceAr = []
        self.learnLimit = learnLimit
        self.howSimReq = howSimReq
        self.minPat = 6
    
    def calc(self,prices):
        
        self.patternStorage(prices)
        if(self.learnProg < self.learnProgTotal):
            return "Training"
        else:
            if len(self.patternAr) > self.learnLimit:
                self.patternAr = list(self.patternAr[1:])
            return self.patternRecognition(prices)
    
    def percentChange(self,x,y):
        if x != 0:
            return ((y-x)/abs(x))*100.00
        else:
            return 0
    
#    def getLinearity(self, X, Y):
#        diff = np.subtract(X, Y)
#        c = np.arange(1, len(diff)+1)
#        sumX2 = np.sum(np.square(c))
#        sumY2 = np.sum(np.square(diff))
#        sumXY = np.sum(np.multiply(c,diff))
#        sumX = np.sum(c)
#        sumY = np.sum(diff)
#        n = len(diff)
#        r = (n * sumXY - sumX * sumY) / (math.sqrt(n * sumX2 - sumX * sumX) * math.sqrt(n * sumY2 - sumY * sumY))
#        return r
    def getLinearity(self, X, Y):
        z, residuals, rank, singular_values, rcond = np.polyfit(X, Y, 1, full=True)
        return residuals[0]
        
    def patternStorage(self,prices):
    
        learntPattern = []
        
        if(len(prices) > self.lookback+self.inAdvance):
            
            self.learnProg += 1
            
            for i in range(0,self.lookback):
                learntPattern.append(self.percentChange(prices[-self.inAdvance], prices[-i-self.inAdvance]))
    
            outcomeRange = prices[-self.inAdvance+1:]
#            Should weight/change outcome range..
            currentPoint = prices[-self.inAdvance]
    
            try:
                avgOutcome = sum(outcomeRange) / len(outcomeRange)
            except Exception as e:
                print(e)
                avgOutcome = 0
            futureOutcome = self.percentChange(currentPoint, avgOutcome)
    
            self.patternAr.append([learntPattern, futureOutcome])
    
    
    def patternRecognition(self, prices):
    
        patForRec = np.zeros(self.lookback)
        for i in range(0,self.lookback):
            patForRec[i] = self.percentChange(prices[-i], prices[-1])
               
        
            
#        predictedOutcomesAr = []
        plotPatAr = []
        n = len(patForRec)
        for eachPattern in self.patternAr:
            simArray = []
            for x in range(self.minPat, n + 1):
                c = eachPattern[0][n-x:]
                d = patForRec[n-x:]
                lin = self.getLinearity(c,d)
                simArray.append([x, lin, lin / math.sqrt(x)])
            
            simArray.sort(key=lambda xa: abs(xa[2]))
                
            if abs(simArray[-1][1]) > self.howSimReq:
                plotPatAr.append([eachPattern[0][n-simArray[-1][0]:], eachPattern[1]])
#        if(len(plotPatAr) != 0):
#            print(plotPatAr, patForRec)
    
        predArray = []
        if len(plotPatAr) > 0:
            for eachPatt in range(0,len(plotPatAr)):
    
                if plotPatAr[eachPatt][1] > 0: #patForRec[self.lookback-1]: price[-1] / price[-2] < price
                    predArray.append(1.000)
                else:
                    predArray.append(-1.000)
#                predictedOutcomesAr.append(self.performanceAr[eachPatt][1])
                
                
            predictionAverage = sum(predArray) / len(predArray)
            
            if predictionAverage > 0.5:
                return "Buy"
            elif predictionAverage < -0.5:
                return "Sell"
        return 'nothing'
            