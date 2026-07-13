#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:40:18 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
load_mw = [42, 39, 37, 36, 38, 45, 61, 78, 85, 88, 90, 91,
           89, 87, 86, 88, 92, 96, 98, 95, 84, 70, 58, 48]

df = pd.DataFrame({
    "hour": range(24),      # 0, 1, 2, ... 23
    "load_mw": load_mw,
})
print(df)
print()
high_demand = df[df["load_mw"] > 80]
print(high_demand)
print()
low_demand_40mw = df[df["load_mw"] < 40]
high_demand_95mw = df[df["load_mw"] >= 95]
print(f"Hours corresponding to load less than 40MW\n {low_demand_40mw['hour']}")
print()
print(f"Hours corresponding to load greater than or equal 95MW\n {high_demand_95mw['hour']}")
print()
ranked = df.sort_values("load_mw", ascending=True)
print(ranked.head())      # .head() shows just the top 5 rows
print()
df["period"] = df["hour"].apply(lambda h: "night" if h < 6 or h >= 22 else "day")
print(df.head(8))
print()
print(df.groupby("period")["load_mw"].mean())
