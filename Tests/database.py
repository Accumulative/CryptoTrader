import sys
sys.path.append("Connections")
sys.path.append("Models")
from mysql_database import BotFunctions
from bottrade import BotTrade
from datetime import datetime
import mysql_database
hey = mysql_database.BotFunctions()
trade = BotTrade(1, datetime.now(), 5, 645, 2, 0.1, 10, 20)
trade.externalId = hey.createTrade(trade)
trade.close(datetime.now(), 700, 'reason')
hey.closeTrade(trade)
print(hey.getTradeById(trade.externalId))