import os
import datetime

class BotLog(object):
    def __init__(self):
        folder = "Logs/" + datetime.datetime.now().strftime('%Y%m%d')
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.destinationLog = folder + "/output.html"
        self.destinationTrades = folder + "/trades.html"

    def log(self, m):
        with open(self.destinationLog, "a") as text_file:
            print("<p>{0}</p>".format(datetime.datetime.now().strftime('%H:%M:%S') + ": " +m), file=text_file)
        print(m)
        
    def logTrades(self, trades):
        with open(self.destinationTrades, "w") as text_file:
            print("""<table id="example" class="display" cellspacing="0" width="100%">
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
            for trade in trades:
                print("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}<td><td>{4}<td></td>{5}<td>{6:0.7f}</td><td>{7:0.4f}%</td></tr>".format(trade.dateOpened, trade.dateClosed, trade.status, trade.volume, trade.entryPrice, trade.exitPrice, 0 if trade.exitPrice == "" else float(trade.entryPrice - trade.exitPrice), 0 if trade.exitPrice == "" else (trade.entryPrice/trade.exitPrice-1)), file=text_file)
            print("""</tbody>
    </table>""", file=text_file)