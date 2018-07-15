
from machinelearning import maclearn

class MachineStrat(object):
 def __init__(self, strat, details):
  self.strat = strat
  self.lookback = 7 if not 'lookback-mc' in details else int(details['lookback-mc'])
  self.learnProgTotal = 1400 if not 'learnProgTotal' in details else int(details['learnProgTotal'])
  self.advance = 13 if not 'advance' in details else int(details['advance'])
  self.howSimReq = 0.9 if not 'howSimReq' in details else float(details['howSimReq'])
  self.learnLimit = self.learnProgTotal if not 'learnLimit' in details else int(details['learnLimit'])
  self.trained = False

 def train(self, training_set):
  self.trained = True
  if(self.strat == '4'):
   return maclearn(self.learnProgTotal, self.lookback, self.advance, self.howSimReq, self.learnLimit, training_set)