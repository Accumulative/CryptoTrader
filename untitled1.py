#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 23:44:29 2017

@author: Kieran
"""
def erina():
    simEquations(7, 5, 3, 4, 37, 32)


def simEquations(oranges1, oranges2, apples1, apples2, fruit1, fruit2):
    
#    oranges1 + apples1 = fruit1
#   oranges2 + apples2 = fruit2

    newOranges1 = oranges1 * oranges2
    newApples1 = oranges2 * apples1
    newFruit1 = oranges2 * fruit1
    
    newOranges2 = newOranges1
    newApples2 = oranges1 * apples2
    newFruit2 = oranges1 * fruit2
    
#    print(newOranges1, newApples1, newFruit1, newOranges2, newApples2, newFruit2)
    
    newApples3 = newApples2 - newApples1
#    print (newApples3)
    newFruit3 = newFruit2 - newFruit1
#    print (newFruit3)
    apples = newFruit3/newApples3 
     
    oranges = (fruit1 - apples1 * apples )/ oranges1
    
    print (oranges,apples)

    

    