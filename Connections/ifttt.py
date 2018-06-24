#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 22:26:46 2018

@author: kieran
"""
import yaml
import requests

class ifttt():
    def __init__(self): 
        self.config = yaml.load(open('config.yml'))['ifttt']
        
    
    def log(self, val1, val2, val3):
        print('ifttt', val1, val2, val3)
        data = {'value1': val1, 'value2': "{:0.4f}".format(val2), 'value3': "{:0.4f}".format(val3)}
        requests.post("https://maker.ifttt.com/trigger/stock_pos/with/key/"+self.config, data=data) 