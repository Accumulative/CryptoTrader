#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:09:56 2018

@author: kieranburke
"""
import sys
sys.path.append("Loggers")
import yaml
import pymysql

class BotFunctions(object):
    def __init__(self):
        db_config = yaml.load(open('config.yml'))['mysql']
        self.conn = pymysql.connect(host=db_config['host'], port=db_config['port'], user=db_config['username'], passwd=db_config['password'], db=db_config['database'])

    def getAllTrades(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM trades")
        cur.close()
        return cur

    def getTradeById(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM trades where id={}".format(id))
        cur.close()
        return cur 

    def createTrade(self, trade):
        cur = self.conn.cursor()
        sql = "INSERT INTO trades (open_date, open_price, close_date, close_price, buy) VALUES ('{:%Y-%m-%d %H:%M:%S}', '{}', '{:%Y-%m-%d %H:%M:%S}', '{}', '{}')"\
            .format(trade.dateOpened, trade.entryPrice, trade.dateClosed, trade.exitPrice, 1 if trade.volume >=0 else 0)
        print(sql)
        cur.execute(sql)
        cur.close()
        return cur 

    def closeConnection(self):
        self.conn.close()