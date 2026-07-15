#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 21:04:09 2026

@author: emmanuel_uchenna_ihedioha
"""

import numpy as np

# Fake raw data: 3 readings per month, to show grouping
raw = pd.DataFrame({
    "month": ["Jan","Jan","Jan","Feb","Feb","Feb","Mar","Mar","Mar"],
    "load_mw": [118, 120, 115, 110, 118, 112, 100, 105, 98],
})
print(raw)
monthly_peak = raw.groupby("month")["load_mw"].max()
print(monthly_peak)

plt.bar(monthly_peak.index, monthly_peak.values)
plt.title("Monthly Peak from Raw Data")
plt.xlabel("Month")
plt.ylabel("Peak Demand (MW)")
plt.grid(True, axis="y")
plt.show()
print()
monthly_average = raw.groupby("month")["load_mw"].mean()
print(monthly_average)

plt.bar(monthly_average.index, monthly_average.values, color = 'purple')
plt.title("Monthly Average from Raw Data")
plt.xlabel("Month")
plt.ylabel("Average Demand (MW)")
plt.grid(True, axis="y")
plt.show()