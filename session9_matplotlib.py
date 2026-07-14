#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:48:34 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
import matplotlib.pyplot as plt 
load_mw = [42, 39, 37, 36, 38, 45, 61, 78, 85, 88, 90, 91,
           89, 87, 86, 88, 92, 96, 98, 95, 84, 70, 58, 48]
df = pd.DataFrame({"hour": range(24), "load_mw": load_mw})

peak = df["load_mw"].max()                          # Calculate the peak load
peak_hour = df["hour"][df["load_mw"].idxmax()]      # the hour where it occurs

plt.plot(df["hour"], df["load_mw"], marker="o", color="red")

plt.axhline(y=peak, color="gray", linestyle="--")   # horizontal dashed line at the peak

plt.annotate(f"Peak: {peak} MW at {peak_hour}h",    # the callout text
             xy=(peak_hour, peak),                   # the point it refers to
             xytext=(peak_hour - 9, peak - 4),       # where the text sits
             arrowprops={"arrowstyle": "->"})  # an arrow from text to point

low = df['load_mw'].min()                       #Calculates the minimum load
low_hour = df['hour'][df['load_mw'].idxmin()]   # the hour where it occurs
print(f"The minimum load of {low} MW occured at {low_hour} h")   #Prints the minimum load and the time it occured

plt.title("Daily Load Profile")
plt.xlabel("Hour of Day")
plt.ylabel("Load (MW)")
plt.grid(True)
plt.savefig("daily_load_profile.png", dpi=150, bbox_inches="tight")
plt.show()