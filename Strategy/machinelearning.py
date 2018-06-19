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
        
        self.performanceAr = []
        self.learnLimit = learnLimit
        self.howSimReq = howSimReq
        self.training_set = training_set

        for i in range(self.lookback+self.inAdvance, len(training_set)):
            self.patternStorage(np.array(training_set)[:i])
    
    def calc(self,prices):
        
        self.patternStorage(prices)
        if(self.learnProg < self.learnProgTotal):
            
            return "Training"
        else:
            if len(self.patternAr) > self.learnLimit:
                self.patternAr = list(self.patternAr[1:])
                self.resultAr = list(self.resultAr[1:])
            return self.patternRecognition(prices)
    
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
        # prices_to_test = np.concatenate((np.array(self.training_set),np.array(prices))) 
        currPattern = np.divide(prices[-tstep:], prices[-tstep-1])
        matches = 0
        guess = 0
        # print(prices_to_test)
        # print(np.array([currPattern]), np.array(self.patternAr)[:20])#, np.array(self.patternAr)[:, 0])

        # print(currPattern)
        covAr = self.generate_correlation_map(np.array([currPattern]), np.array(self.patternAr))
        mask = np.array((covAr > self.howSimReq)[0])
        for result in np.array(self.resultAr)[mask]:
            res_tracker += (1 if result > 0 else -1)
            guess += result
            matches += 1

        return [res_tracker, matches, guess / matches if matches != 0 else 0]


        # for i in range(tstep, len(prices_to_test)-tstep-self.inAdvance):
        #     prevPattern = prices_to_test[i : i + tstep]
        #     similarity = self.similar(prevPattern, currPattern, prices_to_test[i-1], prices_to_test[-tstep-1])
        #     if( similarity != 0 ):
        #         future_outcome = (np.average(prices_to_test[i+tstep:i+tstep+self.inAdvance]) - prices_to_test[i+tstep-1])/ prices_to_test[i+tstep-1]
        #         res_tracker += (1 if future_outcome > 0 else -1)
        #         guess += (np.average(prices_to_test[i+tstep:i+tstep+self.inAdvance]) - prices_to_test[i-1])/ prices_to_test[i-1]
        #         matches += 1

        # return [res_tracker, matches, guess / matches if matches != 0 else 0]
        
    def patternStorage(self,prices):
        
        if(len(prices) > self.lookback+self.inAdvance+1):
            
            self.learnProg += 1
            
            learntPattern = np.divide(prices[-self.inAdvance-self.lookback:-self.inAdvance], prices[-self.inAdvance -self.lookback - 1])  
#            Should weight/change outcome range..
            
            futureOutcome = (np.average(prices[-self.inAdvance:]) - prices[-self.inAdvance-1])/ prices[-self.inAdvance-1]
    
            self.patternAr.append(learntPattern)
            self.resultAr.append(futureOutcome)
    
    
    def patternRecognition(self, prices):            
        
        if(len(prices) > self.lookback+1):
            res = self.runTest(self.lookback, prices)
            
            if (res[0] > 0):
                return "Buy"
            elif (res[0] < 0):
                return "Sell"
        
        return 'nothing'
        
        
        
        
        
        
        
        
        
        
            