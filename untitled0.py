# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 19:51:41 2017

@author: Kieran
"""

import time
import sys, getopt
import datetime
from poloniex import Poloniex
polo = Poloniex('key','secret')

def main(argv):
    period = 10
    pair = "BTC_XMR"
    prices = []
    currentMovingAverage = 0;
    lengthOfMA = 0
    startTime = False
    endTime = False
    historicalData = False
    tradePlaced = False
    typeOfTrade = False
    dataDate = ""
    orderNumber = ""
    dataPoints = []
    localMax = []
    currentResistance = 0.018
    
    try:
        opts, args = getopt.getopt(argv,"hp:c:n:s:e:",["period=","currency=","points="])
    except getopt.GetoptError:
        print('trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>')
            sys.exit()
        elif opt in ("-p", "--period"):
            if (int(arg) in [300,900,1800,7200,14400,86400]):
                period = int(arg)
            else:
                print('Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments')
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-n", "--points"):
            lengthOfMA = int(arg)
        elif opt in ("-s"):
            startTime = arg
        elif opt in ("-e"):
            endTime = arg
    
    
    if (startTime):
        balance = getBalance()
        print(balance)
        historicalData = polo.returnChartData(currencyPair=pair,start=startTime,end=endTime,period=period)    
    
    output = open("output.html",'w')
    output.truncate()
    output.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'trend');data.addRows([""")    
    
    
    while True:
        if (startTime and historicalData):
            nextDataPoint = historicalData.pop(0)
            lastPairPrice = float(nextDataPoint['weightedAverage'])
            dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
        elif(startTime and not historicalData):
            for point in dataPoints:
                output.write("['"+point['date']+"',"+point['price']+","+point['label']+","+point['desc']+","+point['trend'])
                output.write("],\n")
            output.write("""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
            exit()
        else:
            currentValues = polo.returnTicker()
            lastPairPrice = float(currentValues[pair]["last"])
            dataDate = datetime.datetime.now()
   
        
        dataPoints.append({'date':dataDate, 'price': str(lastPairPrice), 'trend': str(currentResistance), 'label': 'null', 'desc': 'null'})        
        
        if ( (len(dataPoints) > 2) and (dataPoints[-2]['price'] > dataPoints[-1]['price']) and (dataPoints[-2]['price'] > dataPoints[-3]['price']) ):
            dataPoints[-2]['label'] = "'MAX'"
            dataPoints[-2]['desc'] = "'This is a local maximum'"
            
            numberOfSimilarLocalMaxes = 0
            for oldMax in localMax:
                if ( (float(oldMax) > (float(dataPoints[-2]['price']) - .0001) ) and (float(oldMax) < (float(dataPoints[-2]['price']) + .0001) ) ):
                    numberOfSimilarLocalMaxes = numberOfSimilarLocalMaxes + 1

            if (numberOfSimilarLocalMaxes > 2):
                currentResistance = dataPoints[-2]['price']
                dataPoints[-2]['trend'] = dataPoints[-2]['price']
                dataPoints[-1]['trend'] = dataPoints[-2]['price']

            localMax.append(dataPoints[-2]['price'])
    
        if (len(prices) > 0):
            currentMovingAverage = sum(prices) / float(len(prices))
            previousPrice = float(prices[-1])
            if (not tradePlaced):
                if ( (lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice) ):
                    print("SELL ORDER")
                    #orderNumber = conn.sell(pair,lastPairPrice,.01)
                    tradePlaced = True
                    typeOfTrade = "short"
                elif ( (lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice) ):
                    print("BUY ORDER")
                    #orderNumber = conn.buy(pair,lastPairPrice,.01)
                    tradePlaced = True
                    typeOfTrade = "long"
            elif (typeOfTrade == "short"):
                if ( lastPairPrice < currentMovingAverage ):
                    print("EXIT TRADE")
                    #conn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
            elif (typeOfTrade == "long"):
                if ( lastPairPrice > currentMovingAverage ):
                    print("EXIT TRADE")
                    #conn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
        else:
            previousPrice = 0

        print("{0} Period: {1} {2}: {3} Moving Average: {4}".format(dataDate,period,pair,lastPairPrice,currentMovingAverage))

        prices.append(float(lastPairPrice))
        prices = prices[-lengthOfMA:]
        if (not startTime):
            time.sleep(int(period))


def getBalance():
    return {k: v for k, v in polo.returnBalances().items() if float(v) != 0}        
    
if __name__ == "__main__":
    main(sys.argv[1:])