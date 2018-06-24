#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:09:56 2018

@author: kieranburke
"""
import sys
sys.path.append("Helpers")
sys.path.append("../Loggers")
import yaml
import pymysql
import datetime
from datehelper import DateHelper

class mysql_database(object):
    def __init__(self):
        db_config = yaml.load(open('config.yml'))['mysql']
        self.conn = pymysql.connect(host=db_config['host'], port=db_config['port'], user=db_config['username'], passwd=db_config['password'], db=db_config['database'])

    def round_to_hour(self, dt):
        dt_start_of_hour = dt.replace(minute=0, second=0, microsecond=0)
        dt_half_hour = dt.replace(minute=30, second=0, microsecond=0)

        if dt >= dt_half_hour:
            # round up
            dt = dt_start_of_hour + datetime.timedelta(hours=1)
        else:
            # round down
            dt = dt_start_of_hour

        return dt

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
        sql = "UPDATE trades SET close_price='{}', close_date='{:%Y-%m-%d %H:%M:%S}' where id={}".format(trade.exitPrice, DateHelper.dt(trade.dateClosed), trade.externalId)
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        return cur 

    def createTrade(self, trade):
        result = ''
        try:
            cur = self.conn.cursor()
            sql = "INSERT INTO trades (open_date, open_price, amount) VALUES ('{:%Y-%m-%d %H:%M:%S}', '{}', '{}');".format(DateHelper.dt(trade.dateOpened), trade.entryPrice, trade.volume)
            cur.execute(sql)
            self.conn.commit()
            sql = "SELECT LAST_INSERT_ID();"
            cur.execute(sql)
            result = cur.fetchone()
        finally:
            cur.close()
        return result[0]
    
    def getStatistics(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM statistics")
        cur.close()
        return cur
    
    def storeStatistics(self, stats):
        cur = self.conn.cursor()
        try:
            for key, val in stats.items():
                sql = """INSERT INTO statistics (name,value) 
                        VALUES ('{0}', '{1}') 
                            ON DUPLICATE KEY UPDATE value='{1}';          
                    """.format(key, val);
        
                cur.execute(sql)  
        finally:
            self.conn.commit()
            cur.close()

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
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{1}';          
                    """.format(key, val);
        
                cur.execute(sql)  
        finally:
            self.conn.commit()
            cur.close()

    def storePredictions(self, date, period, predictions):
        if len(predictions) > 0:
            cur = self.conn.cursor()
            try:
                for i in range(len(predictions[0])):
                    sql = """INSERT INTO predictions (value,type,pred_date) 
                            VALUES ('{0}', '{1}', '{2:%Y-%m-%d %H:%M:%S}') 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{0}';          
                        """.format(predictions[0][i], 0, self.round_to_hour(datetime.datetime.fromtimestamp(date + (i-1) * period))); # 0 is average
            
                    cur.execute(sql)  
                for i in range(len(predictions[1])):
                    sql = """INSERT INTO predictions (value,type,pred_date) 
                            VALUES ('{0}', '{1}', '{2:%Y-%m-%d %H:%M:%S}') 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{0}';          
                        """.format(predictions[1][i], 1, self.round_to_hour(datetime.datetime.fromtimestamp(date + (i-1) * period))); # 1 is min
            
                    cur.execute(sql)  
                for i in range(len(predictions[2])):
                    sql = """INSERT INTO predictions (value,type,pred_date) 
                            VALUES ('{0}', '{1}', '{2:%Y-%m-%d %H:%M:%S}') 
                            ON DUPLICATE KEY UPDATE prev_val=value, value='{0}';          
                        """.format(predictions[2][i], 2, self.round_to_hour(datetime.datetime.fromtimestamp(date + (i-1) * period))); # 2 is max
            
                    cur.execute(sql)  
            finally:
                self.conn.commit()
                cur.close()


    def closeConnection(self):
        self.conn.close()