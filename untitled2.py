#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 01:02:25 2017

@author: Kieran
"""

from random import randint

colours = ['black','red','yellow','brown','orange','white','green','purple']

#code = input("What is your code? ").split(" ")



count = 0

def guess():
    
    picks = []
    colourpick = []
    for i in range(4):
        pick = randint(0, len(colours)-1)
        picks.append(pick)
        colourpick.append(colours[pick])
    
    return colourpick

compOneGuess = guess()
compTwoGuess = guess()
     
computerOne = guess()
computerTwo = guess()

print(computerOne, computerTwo)

while compOneGuess != computerTwo and compTwoGuess != computerOne:
    count += 1
    
    compOneGuess = guess()
    compTwoGuess = guess()
    print(count, compOneGuess, compTwoGuess)
    
if compOneGuess == computerTwo:
    print("Computer one won!")
else:
    print("Computer two won!")