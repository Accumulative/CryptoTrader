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
    
    def round_to_hour(dt):
        dt_start_of_hour = dt.replace(minute=0, second=0, microsecond=0)
        dt_half_hour = dt.replace(minute=30, second=0, microsecond=0)

        if dt >= dt_half_hour:
            # round up
            dt = dt_start_of_hour + datetime.timedelta(hours=1)
        else:
            # round down
            dt = dt_start_of_hour

        return dt