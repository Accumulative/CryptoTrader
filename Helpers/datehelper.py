# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:42:11 2017

@author: Kieran
"""

import calendar
import datetime

class DateHelper(object):
    def dt(u): return datetime.datetime.utcfromtimestamp(u)
    def ut(d): return calendar.timegm(d.timetuple())