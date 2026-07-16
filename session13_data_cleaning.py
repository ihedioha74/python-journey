#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 22:03:26 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
import numpy as np
messy = """timestamp,load_mw,feeder
2026-03-01 00:00,42,A
2026-03-01 01:00,,A
2026-03-01 02:00,37,A
2026-03-01 03:00,36,A
2026-03-01 04:00,-999,A
2026-03-01 05:00,45,A
2026-03-01 00:00,55,B
2026-03-01 01:00,58,B
2026-03-01 01:00,58,B
2026-03-01 03:00,999,B
2026-03-01 04:00,66,B
2026-03-01 05:00,70,b"""

with open("messy_load.csv", "w") as f:
    f.write(messy)
print("Messy file written.")
print()
df = pd.read_csv("messy_load.csv")
print(df)
print()
print(df.dtypes)
print()
print(df.shape)
print()
df = df.drop_duplicates()
print(df)
print(df.shape)
print()
df["feeder"] = df["feeder"].str.upper()
print(df)
print()
df.loc[df["load_mw"] < 0, "load_mw"] = np.nan      # kill negatives
df.loc[df["load_mw"] > 500, "load_mw"] = np.nan    # kill the wild outlier
print(df)
print()
# Option A — drop rows with any NaN in load_mw
clean_dropped = df.dropna(subset=["load_mw"])
print("After dropping:", clean_dropped.shape)

# Option B — fill NaN with each feeder's average load
df["load_filled"] = df.groupby("feeder")["load_mw"].transform(lambda s: s.fillna(s.mean()))
print(df)

print()
print(df.groupby("feeder")["load_mw"].mean())