#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 14:18:08 2017

@author: Kieran
"""

class Person(object):
    def __init__(self, name, age, match):
        self.Name = name
        self.Age = age
        self.Loves = ""
        self.Match = match
    
    
    
kieran = Person("Kieran Burke", 23,"Very")
erina = Person("Erina Kitao", 23, "Well")

kieran.Loves = erina
erina.Loves = kieran

