import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
    chart = BotChart("poloniex","BTC_XMR",300)

    strategy = BotStrategy()

    for candlestick in chart.getPoints():
        strategy.tick(candlestick)
  
    strategy.showPositions()
    strategy.closeAllTrades()
    strategy.calculateTotalProft()

if __name__ == "__main__":
    main(sys.argv[1:])