#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 22:26:46 2018

@author: kieran
"""

import requests

class ifttt():
    def __init__(self):
        pass
        
    def log(val1, val2, val3):
        print('ifttt', val1, val2, val3)
        data = {'value1': str(val1), 'value2': str(val2), 'value3': str(val3)}
        requests.post("https://maker.ifttt.com/trigger/stock_pos/with/key/secret", data=data) 