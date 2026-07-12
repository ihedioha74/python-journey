#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:54:31 2026

@author: emmanuel_uchenna_ihedioha
"""

import numpy as np
readings = np.array([
    [230, 12, 0.95],    # hour 0:  V,  I,  PF
    [228, 15, 0.93],    # hour 1
    [232, 18, 0.91],    # hour 2
    [229, 20, 0.90],    # hour 3
])

print(readings)
print(readings.shape)
print()
currents = readings[:, 1]      # column 1 this time
print(f"Current average: {currents.mean():.2f} A")
print(f"Current max:     {currents.max()} A")
print(f"Current std:     {currents.std():.2f} A")
print()
voltage = readings[:, 0]
average = voltage.mean()
peak = voltage.max()
variation = voltage.std()

print(f"Average Voltage: {average:.2f}")
print(f"Maximum Voltage: {peak}")
print(f"Standard Deviation of the Voltage: {variation:.2f}")