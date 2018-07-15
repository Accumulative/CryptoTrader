#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 22:26:46 2018

@author: kieran
"""

from mysql_database import mysql_database
from poloniex_functions import poloniex_functions
from ifttt import ifttt


class BotFunctions():
    def __init__(self):
        self.poloniex_conn = poloniex_functions()
        self.mysql_conn = mysql_database(self)
        self.ifttt_conn = ifttt()
        
