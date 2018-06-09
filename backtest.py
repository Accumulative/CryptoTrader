import sys, getopt

sys.path.append("Strategy")
sys.path.append("Loggers")
sys.path.append("Other")
sys.path.append("Helpers")

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botdatalog import BotDataLog
from botgraph import BotGraph
from createindex import CreateIndex
import time
import datetime
import numpy as np
from poloniex_functions import BotFunctions
from datehelper import DateHelper
with open('Currencies/Exchange1.txt','r') as file:
    currencies = file.read().split("\n")

from math import isclose

tradeCurrencies = ['BTC_ETC','BTC_DGB','BTC_LTC','BTC_XCP','USDT_BTC']

# Instantiate libraries
functions = BotFunctions()
output = BotLog()
botgrapher = BotGraph()

numberOfStrats = 4
strat = 1
period = 300
startTime = ""
endTime = ""
pair = "BTC_XMR"
prevPair = ""
totalBalance = 5000
liveTrading = False    
environment = 'PI'
total = 1
trialResults = []
chart = ""
dataoutput = ""
now = 0
def trial(toPerform, curr):
    global dataoutput
    global pair
    dataoutput = BotDataLog(pair, startTime, endTime, period)
    
    global chart
    global prevPair
    global now
    now += 1
    
    num = "_".join(map(str, ("-".join(map(str, a)) for a in toPerform)))
    strategyDetails = {}
    
    for z in toPerform:
        if z[0] == "currency":
            pair = tradeCurrencies[z[1]-1]
        strategyDetails[z[0]] = z[1]
    print("{} | {}/{} | {}".format(str(num),now,total,  str(datetime.datetime.now())[:10]))
#    print(pair, prevPair)
#    time.sleep(int(3))
    if pair != prevPair:
        chart = BotChart(functions,pair)
        chart.getHistorical(period,startTime,endTime)
        prevPair = pair
    strategy = BotStrategy(functions, totalBalance, num, strategyDetails, strat)
    for candlestick in chart.getPoints(): 
        dataoutput.logPoint(candlestick)
        strategy.tick(candlestick)
  
    strategy.closeAllTrades()
    totalProfit, marketProfit = strategy.calculateTotalProft()
    global trialResults
#    print([num, toPerform, totalProfit])
    trialResults.append([num, toPerform.copy(), totalProfit, (marketProfit)*totalBalance])
    
def performTrial(y, n, curr):
    
    if n >= 1:
        toPerform = y.copy()
        old = y[n-1]
        for x in range(1, int((y[n-1][2]-y[n-1][1])/y[n-1][3])+2):
            
            toPerform[n-1] = [old[0],old[1]+old[3]*(x-1)]
            
            #print(toPerform)
            curr[n-1]=x
            performTrial(toPerform, n - 1, curr)
    else:
       trial(y, curr)

def main(argv):
    global period
    global pair
    global startTime
    global endTime
    global totalBalance
    global liveTrading  
    global environment
    global chart
    global dataoutput
    global strat
    
    output.log("------------STARTING BACKTESTER------------")
    
#    Handle all the incoming arguments
    try:
        opts, args = getopt.getopt(argv,"hp:c:s:e:b:v:u:l:",["period=","currency="])
    except getopt.GetoptError:
        print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time> -u <strategy> -b <balance> -v <environment> -l <live>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time> -u <strategy> -b <balance> -v <environment> -l <live>')
            sys.exit()
        elif opt in ("-p", "--period"):
            if (int(arg) in [30,300,900,1800,7200,14400,86400]):
                period = int(arg)
            else:
                print('Poloniex requires periods in 300 (5mins),900 (15),1800 (30),7200 (2hr),14400(4hr), or 86400(24hr) second increments')
                sys.exit(2)
        elif opt in ("-s"):
            startTime = DateHelper.ut(datetime.datetime.strptime(arg, '%d/%m/%Y')) if "/" in arg else arg
        elif opt in ("-v"):
            environment = arg
        elif opt in ("-e"):
            endTime = DateHelper.ut(datetime.datetime.strptime(arg, '%d/%m/%Y')) if "/" in arg else arg
        elif opt in ("-b"):
            totalBalance = int(arg)
        elif opt in ("-l"):
            liveTrading = True if int(arg)==1 else False
        elif opt in ("-c"):
            if arg in currencies:
                pair = arg
            else:
                print("incorrect pair")
                sys.exit()
        elif opt in ("-u"):
            if len(list(set([str(i+1) for i in range(numberOfStrats)]) & set(str(arg).split(',')))) > 0:
                strat = arg
            else:
                print("Bad strat params")
                sys.exit()
    
#    Instanstiate GUI for results
    createIndex = CreateIndex(environment)
    
    if not liveTrading:
          
#==============================================================================
#             [factor, lower limit, higher limit, step] is the format
#==============================================================================
#        trialDetails = [['trailingstop',0,0.3,0.15],['maFactor',1,1.05,0.025],['lowMA',15,17,1],['highMA',35,55,10]]
        trialDetails= [['advance', 13, 13, 4],['stoploss', 0.1, 0.1, 0.1]]
#        trialDetails = [['highRSI',60,80,2],['lowRSI',20,40,2],['stoploss',0,0.4,0.04],['rsiperiod',10,20,2]]
#        trialDetails = [['upfactor',1,1.1,0.02],['downfactor',1,1.1,0.02],['lookback',28,40,1]]
        
        
        global total
        total = 1
        for i in trialDetails:
            add = ((i[2] - i[1] ) / i[3])
            if isclose(add,round(add)): # fix this
                total *= (add+1)
            else:
                print("bad params")
                sys.exit(2)
        performTrial(trialDetails, len(trialDetails), np.zeros(len(trialDetails)))
        output.logTrials(trialDetails, trialResults)        
        
#       N dimensional views
        botgrapher.heatmap(trialResults)  
        
#         2 dimensional views
        if len(trialDetails) == 2:
            botgrapher.graph(trialResults)
        
        createIndex.CreatePages()
    else:
        chart = BotChart(functions,pair)
        dataoutput = BotDataLog(pair, DateHelper.ut(datetime.datetime.now()), "LIVE", period)  
        strategyDetails = {'howSimReq':0.9}
        strategy = BotStrategy(functions,totalBalance,0, strategyDetails, strat)
        if(strat == "4"):
            print("Pretraining STARTED")
            if(endTime == ""):
                endTime = DateHelper.ut(datetime.datetime.now())
            chart.getHistorical(period,startTime,endTime)
            num_x = 0
            for candlestick in chart.getPoints(): 
                num_x = num_x + 1
                if(num_x % 10 == 0):
                    print(str(DateHelper.dt(int(candlestick['date']))))
                strategy.tick(candlestick, True)
            print("Pretraining finished")
        while True:
            start = time.time()
            currTick = dict(chart.getNext())
            currTick['date'] = str(DateHelper.ut(datetime.datetime.now()))
            strategy.tick(currTick)
            dataoutput.logPoint(currTick)
            createIndex.CreatePages()
            print('{}: Sleeping ...'.format(currTick['date']))
            end = time.time()
            if int(period)-(end-start) > 0:
                time.sleep(int(period)-(end-start))
            else:
                print("Calculation took too long. Continuing to next tick...")
    


if __name__ == "__main__":
    main(sys.argv[1:])
