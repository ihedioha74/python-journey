#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:05:51 2026

@author: emmanuel_uchenna_ihedioha
"""

def daily_load_summary(readings):
    peak = max(load_mw)
    low = min(load_mw)
    average = sum(load_mw) / len(load_mw)
    load_factor = (average / peak)*100

    print(f"Peak demand:    {peak} MW")
    print(f"Minimum demand: {low} MW")
    print(f"Average demand: {average:.2f} MW")
    print(f'Load Factor: {load_factor:.2f} %')

    for hour, value in enumerate(load_mw):
        if value == peak:
            print(f"Peak occurs at hour {hour}")
            
load_mw = [42, 39, 37, 36, 38, 45, 61, 78, 85, 88, 90, 91,
           89, 87, 86, 88, 92, 96, 98, 95, 84, 70, 58, 48]
daily_load_summary(load_mw)