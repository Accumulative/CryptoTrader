import sys, getopt
import calendar
from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botdatalog import BotDataLog
from createindex import CreateIndex
import time
import datetime
import numpy as np
from botfunctions import BotFunctions

def dt(u): return datetime.datetime.utcfromtimestamp(u)
def ut(d): return calendar.timegm(d.timetuple())

functions = BotFunctions()
period = 300
pair = "BTC_XMR"
startTime = ""
endTime = ""
totalBalance = 5000
liveTrading = False    
environment = 'PI'
output = BotLog()

chart = ""
dataoutput = ""

def trial(toPerform, curr):
    num = "_".join(map(str, (":".join(map(str, a)) for a in toPerform)))
    strategyDetails = {}
    for z in toPerform:
        strategyDetails[z[0]] = z[1]
    print("Starting trial {0}...".format(str(num)))
    strategy = BotStrategy(functions,totalBalance,num, strategyDetails)
    for candlestick in chart.getPoints():
        dataoutput.logPoint(candlestick)
        strategy.tick(candlestick)
  
    strategy.closeAllTrades()
    strategy.calculateTotalProft()
    
def performTrial(y, n, curr):
    
    if n >= 1:
        toPerform = y.copy()
        old = y[n-1]
        for x in range(1, int((y[n-1][2]-y[n-1][1])/y[n-1][3])+2):
            
            toPerform[n-1] = [old[0],old[1]+old[3]*(x-1)]
            
            print(toPerform)
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
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-s"):
            startTime = ut(datetime.datetime.strptime(arg, '%d/%m/%Y'))
        elif opt in ("-v"):
            environment = arg
        elif opt in ("-e"):
            endTime = ut(datetime.datetime.strptime(arg, '%d/%m/%Y'))
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
    
    
    chart = BotChart(functions,pair)
    
    createIndex = CreateIndex(environment)
    
    if not liveTrading:
        dataoutput = BotDataLog(pair, startTime, endTime)  
        chart.getHistorical(period,startTime,endTime)
        
#==============================================================================
#             [factor, lower limit, higher limit, step] is the format
#==============================================================================
        trialDetails = [['highMA',40,60,10],['lowMA',10,30,5]]
        
        performTrial(trialDetails, len(trialDetails), np.zeros(len(trialDetails)))
        
        createIndex.CreatePages()
    else:
        dataoutput = BotDataLog(pair, ut(datetime.datetime.now()), "LIVE")  
        strategyDetails = {'highMA':50,'lowMA':20}
        strategy = BotStrategy(functions,totalBalance,0, strategyDetails)
        while True:
            currTick = dict(chart.getNext())
            currTick['date'] = str(ut(datetime.datetime.now()))
            strategy.tick(currTick)
            dataoutput.logPoint(currTick)
            createIndex.CreatePages()
#            output.log("Sleeping...")
            time.sleep(int(period))
    


if __name__ == "__main__":
    main(sys.argv[1:])