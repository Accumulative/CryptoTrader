#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:09:56 2018

@author: kieranburke
"""
import sys
sys.path.append("../Helpers")
sys.path.append("../Loggers")
sys.path.append("../Models")
import yaml
import pymysql
import datetime
from datehelper import DateHelper
from bottrade import BotTrade

class mysql_database(object):
    def __init__(self, parent):
        self.db_config = yaml.load(open('config.yml'))['mysql']
        self.parent = parent

    def connection(self):
        return pymysql.connect(host=self.db_config['host'], port=self.db_config['port'], user=self.db_config['username'], passwd=self.db_config['password'], db=self.db_config['database'])


    def getAllTrades(self):
        conn = self.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM trades")
        cur.close()
        conn.close()
        return cur

    def getAllOpenTrades(self):
        conn = self.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM trades where close_date is NULL")
        cur.close()
        conn.close()
        
        output = []
        for r in cur:
            trade = BotTrade(self.parent,0,0 if r[3] is None else float(r[3]), 0 if r[1] is None else float(r[1]), 0, 0, r[6], 0, 1)
            trade.externalId = r[0]
            output.append(trade);
        
        return output

    def getTradeById(self, id):
        result = ''
        try:
            conn = self.connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM trades where id={}".format(id))
            result = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return result

    def closeTrade(self, trade):
        conn = self.connection()
        cur = conn.cursor()
        sql = "UPDATE trades SET close_price='{}', close_date='{:%Y-%m-%d %H:%M:%S}' where id={}".format(trade.exitPrice, DateHelper.dt(trade.dateClosed), trade.externalId)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return cur 

    def createTrade(self, trade):
        result = ''
        try:
            conn = self.connection()
            cur = conn.cursor()
            sql = "INSERT INTO trades (open_date, open_price, amount, fee) VALUES ('{:%Y-%m-%d %H:%M:%S}', '{}', '{}', '{}');".format(DateHelper.dt(trade.dateOpened), trade.entryPrice, trade.volume, trade.fee)
            cur.execute(sql)
            conn.commit()
            sql = "SELECT LAST_INSERT_ID();"
            cur.execute(sql)
            result = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return result[0]
    
    def getStatistics(self):
        conn = self.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM statistics")
        cur.close()
        conn.close()
        
        data = {}
        for r in cur:
            data[r[1]] = float(r[2])
        
        return data
    
    def storeStatistics(self, stats):
        conn = self.connection()
        cur = conn.cursor()
        try:
            for key, val in stats.items():
                sql = """INSERT INTO statistics (name,value) 
                        VALUES ('{0}', '{1}') 
                            ON DUPLICATE KEY UPDATE value='{1}';          
                    """.format(key, val);
        
                cur.execute(sql)  
        finally:
            conn.commit()
            cur.close()
            conn.close()

    def getAllParameters(self):
        conn = self.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM parameters")
        cur.close()
        conn.close()
        
        data = {}
        for r in cur:
            data[r[1]] = str(r[2])
        
        return data
    
    def storeAllParameters(self, params):
        conn = self.connection()
        
        cur = conn.cursor()
        try:
            for key, val in params.items():
                sql = """INSERT INTO parameters (name,value,active) 
                        VALUES ('{0}', '{1}', 1) 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{1}';          
                    """.format(key, val);
        
                cur.execute(sql)  
        finally:
            conn.commit()
            cur.close()
            conn.close()

    def storePredictions(self, date, period, predictions):
        if len(predictions) > 0:
            conn = self.connection()
            cur = conn.cursor()
            try:
                for i in range(len(predictions[0])):
                    sql = """INSERT INTO predictions (value,type,pred_date) 
                            VALUES ('{0}', '{1}', '{2:%Y-%m-%d %H:%M:%S}') 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{0}';          
                        """.format(predictions[0][i], 0, DateHelper.round_to_hour(datetime.datetime.fromtimestamp(date + (i-2) * period))); # 0 is average
            
                    cur.execute(sql)  
                for i in range(len(predictions[1])):
                    sql = """INSERT INTO predictions (value,type,pred_date) 
                            VALUES ('{0}', '{1}', '{2:%Y-%m-%d %H:%M:%S}') 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{0}';          
                        """.format(predictions[1][i], 1, DateHelper.round_to_hour(datetime.datetime.fromtimestamp(date + (i-2) * period))); # 1 is min
            
                    cur.execute(sql)  
                for i in range(len(predictions[2])):
                    sql = """INSERT INTO predictions (value,type,pred_date) 
                            VALUES ('{0}', '{1}', '{2:%Y-%m-%d %H:%M:%S}') 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{0}';          
                        """.format(predictions[2][i], 2, DateHelper.round_to_hour(datetime.datetime.fromtimestamp(date + (i-2) * period))); # 2 is max
            
                    cur.execute(sql)  
            finally:
                conn.commit()
                cur.close()
                conn.close()