import os
import datetime
from datehelper import DateHelper

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
        self.destinationLog = folder + "/log.html"
        self.destinationTrades = folder + "/trades"
        self.destinationTrials = folder + "/trials"
        self.createFolders()
        
    def createFolders(self):
        
        folder = "Logs/" + datetime.datetime.now().strftime('%Y%m%d')
        self.destinationLog = folder + "/log.html"
        self.destinationTrades = folder + "/trades"
        self.destinationTrials = folder + "/trials"
        if not os.path.exists(self.destinationTrades):
            os.makedirs(self.destinationTrades)
        if not os.path.exists(self.destinationTrials):
            os.makedirs(self.destinationTrials)
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
        
    def consoleLog(self, m):
        print(m)
    
    def log(self, m, c = False):
        self.createFolders()
        with open(self.destinationLog, "a") as text_file:
            print("<p>{0}</p>".format(datetime.datetime.now().strftime('%H:%M:%S') + ": " +m), file=text_file)
        
        if c:
            self.consoleLog(m)
        
    def logTrades(self, trades, bal, trial):
        self.createFolders()
        self.consoleLog("Logging trades")
        with open(self.destinationTrades + "/" + str(trial) + ".html", "w") as text_file:
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
                    <th>ID</th>
                    <th>Open time</th>
                    <th>Close time</th>
                    <th>Status</th>
                    <th>Amount</th>
                    <th>Entry</th>
                    <th>Exit</th>
                    <th>Fee</th>
                    <th>Profit</th>
                    <th>Percentage</th>
                    <th>Reason</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th>ID</th>
                    <th>Open time</th>
                    <th>Close time</th>
                    <th>Status</th>
                    <th>Amount</th>
                    <th>Entry</th>
                    <th>Exit</th>
                    <th>Fee</th>
                    <th>Profit</th>
                    <th>Percentage</th>
                    <th>Reason</th>
                </tr>
            </tfoot>
            <tbody>
            <tr>""", file=text_file)
            sumProfit = 0
            trades.sort(key=lambda t: t.dateOpened)
            for trade in trades:
                currProfit = 0 if trade.exitPrice == "" else float(trade.exitPrice - trade.entryPrice)*trade.volume - trade.fee
                sumProfit += currProfit
                print("<tr><td>{8}</td><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{9}</td><td>{6:0.7f}</td><td>{7:0.4f}%</td><td>{10}</td></tr>".format(trade.dateOpened, trade.dateClosed, trade.status, trade.volume, trade.entryPrice, trade.exitPrice, currProfit, 0 if (trade.exitPrice == "" or currProfit == 0) else (100 *(currProfit)/(trade.entryPrice * trade.volume)), trade.id, trade.fee, trade.reason), file=text_file)
            print("<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>{0:0.7f}</td><td>{1:0.4f}%</td><td></td></tr>".format(sumProfit, sumProfit/bal), file=text_file)
            print("""</tbody>
            </table>
            <br/>
            <div align="right" >
            <button onclick="javascript:history.back()">Go back to index</button>
            </div>
            </body>
            </html>""", file=text_file)
    
    def logTrials(self, trialDetails, trialResults):
        self.consoleLog("Logging trials...")
        self.createFolders()
        name = "_".join(a[0]+"("+str(a[1])+"-"+str(a[2])+")" for a in trialDetails) + "_" + str(DateHelper.ut(datetime.datetime.now()))
        with open(self.destinationTrials  + "/" +  name + ".html", "w") as text_file:
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
            <h2 align="center">Monte Carlo results</h2>
                <table id="example" class="display" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th>ID</th>""" + \
            "".join("<th>{0}</th>".format(b[0]) for b in trialDetails) + \
                    """<th>Profit</th>
                        <th>Market</th>
                    
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th>ID</th>""" + \
            "".join("<th>{0}</th>".format(b[0]) for b in trialDetails) + \
                    """<th>Profit</th>
                        <th>Market</th>
                </tr>
            </tfoot>
            <tbody>
                <tr>""", file=text_file)
            
                     
            
            for res in sorted(trialResults, key=lambda prof: prof[2]):
                
                stringToWrite = "<td>{}</td>".format(res[0]) + \
                "".join("<td>{}</td>".format(c[1]) for c in res[:][1]) + \
                "<td>{}</td>".format(res[2]) + \
                "<td>{}</td>".format(res[3]) + \
                "</tr>"
                
                print(stringToWrite, file=text_file)
            print("""</tbody>
            </table>
            <br/>
            <div align="right" >
            <button onclick="javascript:history.back()">Go back to index</button>
            </div>
            </body>
            </html>""", file=text_file)
        
        