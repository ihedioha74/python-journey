#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 20:39:14 2026

@author: emmanuel_uchenna_ihedioha
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def clean_load_data(filename):
    """Read a messy load CSV and return a cleaned DataFrame."""
    df = pd.read_csv(filename)

    # 1. remove exact duplicate rows
    df = df.drop_duplicates()

    # 2. standardize feeder labels to uppercase
    df["feeder"] = df["feeder"].str.upper()

    # 3. mark impossible load values as NaN
    df.loc[df["load_mw"] < 0, "load_mw"] = np.nan
    df.loc[df["load_mw"] > 500, "load_mw"] = np.nan

    # 4. drop rows with no valid load reading
    df = df.dropna(subset=["load_mw"])

    return df
print()
result = clean_load_data("messy_load.csv")
print(result)

messy2 = """timestamp,load_mw,feeder
2026-04-01 00:00,50,X
2026-04-01 01:00,,X
2026-04-01 02:00,-500,X
2026-04-01 03:00,52,x
2026-04-01 04:00,60,X
2026-04-01 04:00,60,X"""

with open("messy_load2.csv", "w") as f:
    f.write(messy2)

result2 = clean_load_data("messy_load2.csv")
print(result2)
print()
def summarize_load(df, title="Load Summary"):
    """Take a clean load DataFrame and plot average load per feeder."""
    averages = df.groupby("feeder")["load_mw"].mean()

    averages.plot(kind="bar", color="steelblue")
    plt.title(title)
    plt.xlabel("Feeder")
    plt.ylabel("Average Load (MW)")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()

    return averages
clean = clean_load_data("messy_load.csv")
summarize_load(clean, title="March Feeder Averages")