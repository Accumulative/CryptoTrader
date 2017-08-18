import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botdatalog import BotDataLog
from botgraph import BotGraph
from createindex import CreateIndex
import time
import datetime
import numpy as np
from botfunctions import BotFunctions

from datehelper import DateHelper

currencies = ['BTC_LSK',
 'ETH_GNO',
 'BTC_BURST',
 'BTC_GAME',
 'BTC_BELA',
 'USDT_NXT',
 'USDT_STR',
 'BTC_VRC',
 'BTC_GNT',
 'BTC_NOTE',
 'BTC_ARDR',
 'BTC_GNO',
 'BTC_POT',
 'USDT_REP',
 'BTC_HUC',
 'BTC_RADS',
 'BTC_XMR',
 'BTC_STEEM',
 'BTC_VTC',
 'BTC_ETH',
 'USDT_ZEC',
 'BTC_FLO',
 'ETH_REP',
 'BTC_BTS',
 'BTC_BCY',
 'USDT_XRP',
 'XMR_NXT',
 'BTC_AMP',
 'USDT_XMR',
 'BTC_SC',
 'BTC_DGB',
 'BTC_OMNI',
 'BTC_NXC',
 'XMR_DASH',
 'BTC_FCT',
 'BTC_FLDC',
 'USDT_LTC',
 'BTC_VIA',
 'BTC_NMC',
 'ETH_STEEM',
 'BTC_RIC',
 'ETH_LSK',
 'USDT_ETH',
 'BTC_DOGE',
 'BTC_EMC2',
 'BTC_LBC',
 'BTC_ZEC',
 'BTC_NAUT',
 'BTC_ETC',
 'BTC_EXP',
 'BTC_LTC',
 'BTC_BCN',
 'ETH_ZEC',
 'BTC_BTCD',
 'XMR_BTCD',
 'BTC_NAV',
 'ETH_ETC',
 'BTC_SYS',
 'BTC_PPC',
 'ETH_GNT',
 'USDT_BTC',
 'XMR_MAID',
 'BTC_DCR',
 'BTC_PINK',
 'BTC_DASH',
 'BTC_STR',
 'XMR_BLK',
 'BTC_CLAM',
 'USDT_ETC',
 'BTC_XBC',
 'BTC_MAID',
 'XMR_LTC',
 'BTC_XCP',
 'XMR_BCN',
 'BTC_BLK',
 'BTC_GRC',
 'BTC_SJCX',
 'BTC_NEOS',
 'BTC_XRP',
 'BTC_REP',
 'BTC_PASC',
 'USDT_DASH',
 'XMR_ZEC',
 'BTC_BTM',
 'BTC_SBD',
 'BTC_XVC',
 'BTC_XPM',
 'BTC_NXT',
 'BTC_STRAT',
 'BTC_XEM']

tradeCurrencies = ['BTC_ETC','BTC_DGB','BTC_LTC','BTC_XCP','USDT_BTC']

functions = BotFunctions()
period = 300
startTime = ""
endTime = ""
pair = "BTC_XMR"
prevPair = ""
totalBalance = 5000
liveTrading = False    
environment = 'PI'
output = BotLog()
botgrapher = BotGraph()
trialResults = []
chart = ""
dataoutput = ""

def trial(toPerform, curr):
    global dataoutput
    dataoutput = BotDataLog(pair, startTime, endTime)
    global pair
    global chart
    global prevPair
    
    num = "_".join(map(str, ("-".join(map(str, a)) for a in toPerform)))
    strategyDetails = {}
    
    for z in toPerform:
        if z[0] == "currency":
            pair = tradeCurrencies[z[1]-1]
        strategyDetails[z[0]] = z[1]
    print("Starting trial {0}...".format(str(num)))
    print(pair, prevPair)
#    time.sleep(int(3))
    if pair != prevPair:
        chart = BotChart(functions,pair)
        chart.getHistorical(period,startTime,endTime)
        prevPair = pair
    strategy = BotStrategy(functions,totalBalance,num, strategyDetails)
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
    
    output.log("------------STARTING BACKTESTER------------")
    
    try:
        opts, args = getopt.getopt(argv,"hp:c:s:e:b:v:",["period=","currency="])
    except getopt.GetoptError:
        print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time> -b <balance> -v <environment>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time> -b <balance> -v <environment>')
            sys.exit()
        elif opt in ("-p", "--period"):
            if (int(arg) in [30,300,900,1800,7200,14400,86400]):
                period = int(arg)
            else:
                print('Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments')
                sys.exit(2)
        elif opt in ("-s"):
            startTime = DateHelper.ut(datetime.datetime.strptime(arg, '%d/%m/%Y')) if "/" in arg else arg
        elif opt in ("-v"):
            environment = arg
        elif opt in ("-e"):
            endTime = DateHelper.ut(datetime.datetime.strptime(arg, '%d/%m/%Y')) if "/" in arg else arg
        elif opt in ("-b"):
            totalBalance = int(arg)
    
    if startTime == "" and endTime == "":
        # Using real
        liveTrading = True
    elif (startTime == "" and endTime != "") or (startTime != "" and endTime == ""):
        # Error
        print('Cant just use one date. Require two.')
        sys.exit(2)
    else:
        # Practice
        liveTrading = False
    
    
    
    
    
    
    
    
    createIndex = CreateIndex(environment)
    
    if not liveTrading:
          
        chart.getHistorical(period,startTime,endTime)
        
#==============================================================================
#             [factor, lower limit, higher limit, step] is the format
#==============================================================================
        trialDetails = [['highMA',60,60,40],['lowMA',30,30,30],['maFactor',1,1,1],['simTrades',1,1,1]]
        
        performTrial(trialDetails, len(trialDetails), np.zeros(len(trialDetails)))
#        print(trialResults)
        output.logTrials(trialDetails, trialResults)        
        
        
        # N dimensional views
        #botgrapher.heatmap(trialResults)  
        
        # 2 dimensional views
        if len(trialDetails) == 2:
            botgrapher.graph(trialResults)
        
        createIndex.CreatePages()
    else:
        chart = BotChart(functions,pair)
        dataoutput = BotDataLog(pair, DateHelper.ut(datetime.datetime.now()), "LIVE")  
        strategyDetails = {'highMA':50,'lowMA':20,'maFactor':1,'simTrades':1}
        strategy = BotStrategy(functions,totalBalance,0, strategyDetails)
        while True:
            currTick = dict(chart.getNext())
            currTick['date'] = str(DateHelper.ut(datetime.datetime.now()))
            strategy.tick(currTick)
            dataoutput.logPoint(currTick)
            createIndex.CreatePages()
#            output.log("Sleeping...")
            time.sleep(int(period))
    


if __name__ == "__main__":
    main(sys.argv[1:])
