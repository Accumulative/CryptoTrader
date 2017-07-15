import os
import datetime

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)

class BotLog(object):
    def __init__(self):
        folder = "Logs/" + datetime.datetime.now().strftime('%Y%m%d')
        if not os.path.exists(folder):
            os.makedirs(folder)
            with open(folder + "/output.html","w") as text_file:
                print("""<!DOCTYPE html>
<html>
<body>
<style type="text/css">
.inline { 
display: inline-block; 
margin-left:120px
}


</style>
<div class="inline" >
<h2>Output ("""+folder+""")</h2>
</div>
<div class="inline">
    <button onclick="javascript:history.back()">Go back to index</button>
    </div>
<div class="inline">
    <input type="button" value="Refresh Page" onClick="window.location.reload()">
    </div>

<iframe height="500" width="800" src="log.html">
  <p>Your browser does not support iframes.</p>
</iframe>
    
</body>
</html>""", file=text_file)
        self.destinationLog = folder + "/log.html"
        self.destinationTrades = folder + "/trades.html"
        
    def consoleLog(self, m):
        print(m)
    
    def log(self, m):
        with open(self.destinationLog, "a") as text_file:
            print("<p>{0}</p>".format(datetime.datetime.now().strftime('%H:%M:%S') + ": " +m), file=text_file)
        self.consoleLog(m)
        
    def logTrades(self, trades):
        self.consoleLog("Logging trades")
        with open(self.destinationTrades, "w") as text_file:
            print("""<!DOCTYPE html>
        <html>
        <head>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        
        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        
        tr:nth-child(even) {
            background-color: #dddddd;
        }
        </style>
        </head>
        <body>
        <h2 align="center">Trades</h2>
            <table id="example" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Open time</th>
                <th>Close time</th>
                <th>Status</th>
                <th>Amount</th>
                <th>Entry</th>
                <th>Exit</th>
                <th>Profit</th>
                <th>Percentage</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
                <th>Open time</th>
                <th>Close time</th>
                <th>Status</th>
                <th>Amount</th>
                <th>Entry</th>
                <th>Exit</th>
                <th>Profit</th>
                <th>Percentage</th>
            </tr>
        </tfoot>
        <tbody>
            <tr>""", file=text_file)
            sumProfit = 0
            for trade in trades:
                sumProfit += 0 if trade.exitPrice == "" else float(trade.entryPrice - trade.exitPrice)*trade.volume
                print("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6:0.7f}</td><td>{7:0.4f}%</td></tr>".format(trade.dateOpened, trade.dateClosed, trade.status, trade.volume, trade.entryPrice, trade.exitPrice, 0 if trade.exitPrice == "" else float(trade.entryPrice - trade.exitPrice)*trade.volume, 0 if trade.exitPrice == "" else (trade.entryPrice/trade.exitPrice-1)), file=text_file)
            print("<tr><td></td><td></td><td></td><td></td><td></td><td></td><td>{0:0.7f}</td><td>{1:0.4f}%</td></tr>".format(sumProfit, sumProfit/5000), file=text_file)
            print("""</tbody>
    </table>
    <br/>
    <div align="right" >
    <button onclick="javascript:history.back()">Go back to index</button>
    </div>
    </body>
    </html>""", file=text_file)