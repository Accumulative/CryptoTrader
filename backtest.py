import sys, getopt
import calendar
from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botdatalog import BotDataLog
from createindex import CreateIndex
import time
import datetime

def dt(u): return datetime.datetime.utcfromtimestamp(u)
def ut(d): return calendar.timegm(d.timetuple())

def main(argv):
    period = 300
    pair = "BTC_XMR"
    startTime = ""
    endTime = ""
    totalBalance = 5000
    liveTrading = False    
    
    output = BotLog()
    output.log("------------STARTING BACKTESTER------------")
    
    try:
        opts, args = getopt.getopt(argv,"hp:c:s:e:b:",["period=","currency="])
    except getopt.GetoptError:
        print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time> -b <balance>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time> -b <balance>')
            sys.exit()
        elif opt in ("-p", "--period"):
            if (int(arg) in [300,900,1800,7200,14400,86400]):
                period = int(arg)
            else:
                print('Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments')
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-s"):
            startTime = arg
        elif opt in ("-e"):
            endTime = arg
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
    
    
    dataoutput = BotDataLog(pair, ut(datetime.datetime.now()), "LIVE")  
    chart = BotChart("poloniex",pair)
    strategy = BotStrategy(totalBalance)
    
    if not liveTrading:
        
        chart.getHistorical(period,startTime,endTime)
        
        for candlestick in chart.getPoints():
            dataoutput.logPoint(candlestick)
            strategy.tick(candlestick)
      
        strategy.closeAllTrades()
        strategy.calculateTotalProft()
    else:
        while True:
            tick = chart.getNext()
            tick['date'] = ut(datetime.datetime.now())
            strategy.tick(tick)
            dataoutput.logPoint(tick)
            time.sleep(int(period))
    
    
    createIndex = CreateIndex()

if __name__ == "__main__":
    main(sys.argv[1:])