# -*- coding: utf-8 -*-

import numpy as np

class maclearn(object):
    def __init__(self, learnProgTotal, lookback, advance):

        self.lookback = lookback
        self.learnProg = 0
        self.learnProgTotal = learnProgTotal
        self.inAdvance = advance
        self.patternAr = []
        self.performanceAr = []
        self.learnLimit = 300
    
    def calc(self,prices):
        
        self.patternStorage(prices)
        if(self.learnProg < self.learnProgTotal):
            return "Training"
        else:
            if len(self.patternAr) > self.learnLimit:
                self.patternAr = list(self.patternAr[1:])
                self.performanceAr = list(self.performanceAr[1:])
            return self.patternRecognition(prices)
    
    def percentChange(self,x,y):
        if x != 0:
            return ((y-x)/abs(x))*100.00
        else:
            return 0
    
    def patternStorage(self,prices):
    
        learntPattern = []
        
        if(len(prices) > self.lookback+self.inAdvance):
            
            self.learnProg += 1
            
            for i in range(0,self.lookback):
                learntPattern.append(self.percentChange(prices[-self.inAdvance], prices[-i-self.inAdvance]))
    
            outcomeRange = prices[-self.inAdvance+1:]
#            Should weight/change outcome range..
            currentPoint = prices[-1]
    
            try:
                avgOutcome = sum(outcomeRange) / len(outcomeRange)
            except Exception as e:
                print(e)
                avgOutcome = 0
            futureOutcome = self.percentChange(currentPoint, avgOutcome)
    
            self.patternAr.append(learntPattern)
            self.performanceAr.append(futureOutcome)
    
    
    def patternRecognition(self, prices):
    
        patForRec = []
        for i in range(0,self.lookback):
            patForRec.append(self.percentChange(prices[-1],prices[-i]))
               
        
            
        predictedOutcomesAr = []
        plotPatAr = []
        simArray = np.zeros(self.lookback)
    
        for eachPattern in self.patternAr:
            howSim = 101
            for i in range(0,self.lookback):
                simArray[i] = 100.00 - abs(self.percentChange(eachPattern[i], patForRec[i]))
                if(simArray[i] < 0):
                    howSim = 0
                    break
    
            if howSim != 0:
                howSim = sum(simArray)/len(simArray)
    
                
            if howSim > 80:
                plotPatAr.append(eachPattern)
    
        predArray = []
        if len(plotPatAr) > 0:
            for eachPatt in range(0,len(plotPatAr)):
    
                if self.performanceAr[eachPatt] > patForRec[self.lookback-1]:
                    predArray.append(1.000)
                else:
                    predArray.append(-1.000)
                predictedOutcomesAr.append(self.performanceAr[eachPatt])
                
                
            predictionAverage = sum(predArray) / len(predArray)
            
            if predictionAverage > 0.5:
                return "Buy"
            elif predictionAverage < -0.5:
                return "Sell"
            