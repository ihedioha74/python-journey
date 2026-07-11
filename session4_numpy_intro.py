#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 21:59:44 2026

@author: emmanuel_uchenna_ihedioha
"""

import numpy as np
currents = np.array([12, 15, 18, 20, 22, 25])   # amperes
R = 8  # ohms

P = (currents**2*R)/1000

print(f'Power: {P} kW')
print(f"Total power:   {P.sum():.3f} kW")
print(f"Average power: {P.mean():.3f} kW")
print(f"Max power:     {P.max():.3f} kW")
print(f"Min power:     {P.min():.3f} kW")
print(f"Std deviation: {P.std():.3f} kW")