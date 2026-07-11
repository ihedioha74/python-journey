#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 12:04:34 2026

@author: emmanuel_uchenna_ihedioha
"""

readings = []                            # an empty list to collect numbers

with open("load_data.txt", "r") as f:
    for line in f:
        clean = line.strip()             # remove the \n
        number = float(clean)            # convert text → number
        readings.append(number)          # add it to our list

print(readings)
print(type(readings[0]))                 # what type is the first item now?