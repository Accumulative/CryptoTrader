
from botfunctions import BotFunctions
from botlog import BotLog
#import time

class BotAccount(object):
    def __init__(self, functions):
        self.output = BotLog()
        self.output.log("Getting balance data...")
        self.functions = functions
        self.data = self.__updateBalance()

    def getBalance(self):
        return self.data 
    
    def createBalancePage(self):
        with open("balance.html", "w") as text_file:
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
        <h1>BALANCE</h1><table id="example" class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
                <th>Pair</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
                <th>Pair</th>
                <th>Amount</th>
            </tr>
        </tfoot>
        <tbody>
            <tr>""", file=text_file)
            for k, v in self.data.items():
                print("<tr><td>{0}</td><td>{1}</td></tr>".format(k, v), file=text_file)
            print("""</tbody>
    </table>
    <br/>
    <div align="right" >
    <button onclick="javascript:history.back()">Go back to index</button>
    </div>
    </body>
    </html>""", file=text_file)
                    
    def __updateBalance(self):
        # return self.functions.getBalance()
        return {'BTC_XMR':50,'BTC_LTC':20} 