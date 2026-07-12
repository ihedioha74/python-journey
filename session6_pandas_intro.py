#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 12:31:40 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
df = pd.read_csv("load_timeseries.csv")
print(df)
print(df.dtypes)
df["timestamp"] = pd.to_datetime(df["timestamp"])
print(df.dtypes)

print(df["timestamp"].dt.hour)        # pull the HOUR out of each timestamp
print(df["timestamp"].dt.day_name())  # what day of the week each reading falls on

df["load_kw"] = df["load_mw"] * 1000
print(df)