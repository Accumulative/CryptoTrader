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

class mysql_database(object):
    def __init__(self):
        db_config = yaml.load(open('config.yml'))['mysql']
        self.conn = pymysql.connect(host=db_config['host'], port=db_config['port'], user=db_config['username'], passwd=db_config['password'], db=db_config['database'])

    def getAllTrades(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM trades")
        cur.close()
        return cur

    def getTradeById(self, id):
        result = ''
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM trades where id={}".format(id))
            result = cur.fetchone()
        finally:
            cur.close()
        return result

    def closeTrade(self, trade):
        cur = self.conn.cursor()
        sql = "UPDATE trades SET close_price='{}', close_date='{:%Y-%m-%d %H:%M:%S}' where id={}".format(trade.exitPrice, trade.dateClosed, trade.externalId)
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        return cur 

    def createTrade(self, trade):
        result = ''
        try:
            cur = self.conn.cursor()
            sql = "INSERT INTO trades (open_date, open_price, buy) VALUES ('{:%Y-%m-%d %H:%M:%S}', '{}', '{}');"\
                .format(trade.dateOpened, trade.entryPrice, 1 if trade.volume >=0 else 0)
            cur.execute(sql)
            self.conn.commit()
            sql = "SELECT LAST_INSERT_ID();"
            cur.execute(sql)
            result = cur.fetchone()
        finally:
            cur.close()
        return result[0]
    
    def getAllParameters(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM parameters")
        cur.close()
        return cur
    
    def storeAllParameters(self, params):
        
        
        cur = self.conn.cursor()
        try:
            for key, val in params.items():
                sql = """INSERT INTO parameters (name,value,active) 
                        VALUES ('{0}', '{1}', 1) 
                            ON DUPLICATE KEY UPDATE value='{1}';          
                    """.format(key, val);
                print(sql)
        
                cur.execute(sql)  
        finally:
            self.conn.commit()
            cur.close()

    def closeConnection(self):
        self.conn.close()