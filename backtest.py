import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botdatalog import BotDataLog

def main(argv):
    period = 300
    pair = "BTC_XMR"
    startTime = 1491048000
    endTime = 1491091200
    
    file = ""#Data/0
    dataoutput = BotDataLog(startTime, endTime)   
    output = BotLog()
    output.log("------------STARTING BACKTESTER------------")
    
    try:
        opts, args = getopt.getopt(argv,"hp:c:s:e:",["period=","currency="])
    except getopt.GetoptError:
        print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('backtest.py -p <period length> -c <currency pair> -s <start time> -e <end time>')
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
    
    if file != "":
        pass
    else:
        chart = BotChart("poloniex",pair,period,startTime,endTime)

    strategy = BotStrategy()

    for candlestick in chart.getPoints():
        dataoutput.logPoint(candlestick)
        strategy.tick(candlestick)
  
    strategy.showPositions()
    strategy.closeAllTrades()
    strategy.calculateTotalProft()

if __name__ == "__main__":
    main(sys.argv[1:])