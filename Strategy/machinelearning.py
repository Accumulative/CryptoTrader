# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import math

class maclearn(object):
    def __init__(self, learnProgTotal, lookback, advance, howSimReq, learnLimit, training_set):

        self.lookback = lookback
        self.learnProg = 0
        self.learnProgTotal = learnProgTotal
        self.inAdvance = advance
        self.patternAr = []
        self.resultAr = []
        self.predAr = []

        self.performanceAr = []
        self.learnLimit = learnLimit
        self.howSimReq = howSimReq
        self.training_set = training_set

        for i in range(self.lookback+self.inAdvance, len(training_set)):
            self.patternStorage(np.array(training_set)[:i])
    
    def calc(self,prices):
        
        self.patternStorage(prices)
        if(self.learnProg < self.learnProgTotal):
            
            return [self.learnProg, self.learnProgTotal], []
        else:
            if len(self.patternAr) > self.learnLimit:
                self.patternAr = list(self.patternAr[1:])
                self.resultAr = list(self.resultAr[1:])
                self.predAr = list(self.predAr[1:])
            res, predictions = self.patternRecognition(prices)
            return res, predictions
    
    def similar(self, A, B, A_prev, B_prev):
        A_p = np.divide(A, A_prev)
        B_p = np.divide(B, B_prev)
        # AB_p_corr = np.corrcoef(A_p, B_p)
        AB_diff = np.subtract(A_p, B_p)
        if (np.sum(np.abs(AB_diff)) < 0.1 and max(A_p)-min(B_p) > 0.005):
            return [np.sum(np.abs(AB_diff)), max(A_p)-min(B_p)]
        else:
            return 0

    def generate_correlation_map(self, x, y):
        """Correlate each n with each m.

        Parameters
        ----------
        x : np.array
        Shape N X T.

        y : np.array
        Shape M X T.

        Returns
        -------
        np.array
        N X M array in which each element is a correlation coefficient.

        """
        mu_x = x.mean(1)
        mu_y = y.mean(1)
        n = x.shape[1]
        if n != y.shape[1]:
            raise ValueError('x and y must ' +
                            'have the same number of timepoints.')
        s_x = x.std(1, ddof=n - 1)
        s_y = y.std(1, ddof=n - 1)
        cov = np.dot(x,
                    y.T) - n * np.dot(mu_x[:, np.newaxis],
                                    mu_y[np.newaxis, :])
        return cov / np.dot(s_x[:, np.newaxis], s_y[np.newaxis, :])
    
    def runTest(self, tstep, prices):
        res_tracker = 0 
        currPattern = np.divide(prices[-tstep:], prices[-tstep-1])
        guess = np.zeros(self.inAdvance)
        minGuess = np.empty(self.inAdvance)
        minGuess.fill(100000)
        maxGuess = np.zeros(self.inAdvance)
        covAr = self.generate_correlation_map(np.array([currPattern]), np.array(self.patternAr))
        mask = np.array((covAr > self.howSimReq)[0])
        for result, pred in list(zip(np.array(self.resultAr)[mask], np.array(self.predAr)[mask])):
            res_tracker += (1 if result > 0 else -1)
            guess = np.add(guess, pred);
            minGuess = np.amin([minGuess, pred], axis=0)
            maxGuess = np.amax([maxGuess, pred], axis=0)
        matches = len(np.array(self.resultAr)[mask])
        guess = np.divide(guess, matches)
        return res_tracker, [guess, minGuess, maxGuess]
        
    def patternStorage(self,prices):
        
        if(len(prices) > self.lookback+self.inAdvance+1):
            
            self.learnProg += 1
            
            learntPattern = np.divide(prices[-self.inAdvance-self.lookback:-self.inAdvance], prices[-self.inAdvance -self.lookback - 1])  

            futureOutcome = (np.average(prices[-self.inAdvance:]) - prices[-self.inAdvance-1])/ prices[-self.inAdvance-1]
    
            predictions = np.divide(np.subtract(prices[-self.inAdvance:], prices[-self.inAdvance-1]), prices[-self.inAdvance-1])

            self.patternAr.append(learntPattern)
            self.resultAr.append(futureOutcome)
            self.predAr.append(predictions)
    
    
    def patternRecognition(self, prices):            
        
        if(len(prices) > self.lookback+1):
            res, predictions = self.runTest(self.lookback, prices)
            predictions = np.multiply(np.add(predictions,1), prices[-1]);
            if res != 0:
                if (res > 0):
                    return "Buy", predictions
                elif (res < 0):
                    return "Sell", predictions
        
            return 'nothing', predictions
        return 'nothing', []
        
        
        
        
        
        
        
        
        
            