
from poloniex import Poloniex
from botlog import BotLog

class BotAccount(object):
    def __init__(self):
        self.output = BotLog()
        
        self.conn = Poloniex('key','secret')

        self.output.log("Getting balance data...")
        self.data = self.__updateBalance()
        

    def getBalance(self):
        return self.data 
    
    def createBalancePage(self):
        with open("balance.html", "w") as text_file:
            print("""<h1>BALANCE</h1><table id="example" class="display" cellspacing="0" width="100%">
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
    </table>""", file=text_file)
                    
    def __updateBalance(self):
        return {'BTC_XMR':50,'BTC_LTC':20}#{k: v for k, v in self.conn.returnBalances().items() if float(v) != 0}