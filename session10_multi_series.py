#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:28:54 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
import matplotlib.pyplot as plt 
weekday = [42, 39, 37, 36, 38, 45, 61, 78, 85, 88, 90, 91,
           89, 87, 86, 88, 92, 96, 98, 95, 84, 70, 58, 48]

weekend = [40, 38, 36, 35, 35, 37, 42, 50, 58, 66, 72, 75,
           76, 75, 73, 72, 74, 78, 80, 77, 70, 62, 54, 46]

df = pd.DataFrame({
    "hour": range(24),
    "weekday": weekday,
    "weekend": weekend,
})
print(df.head())

df["difference"] = df["weekday"] - df["weekend"]
print(df[["hour", "weekday", "weekend", "difference"]])

max_gap_hour = df["difference"].idxmax()
max_gap = df["difference"].max()
print(f"Largest gap: {max_gap} MW at hour {max_gap_hour}")

plt.plot(df["hour"], df["weekday"], marker="o", label="Weekday")
plt.plot(df["hour"], df["weekend"], marker="s", label="Weekend")
plt.plot(df["hour"], df["difference"], marker="^", label="Difference", linestyle="--")

plt.title("Weekday vs Weekend Load, with Difference")
plt.xlabel("Hour of Day")
plt.ylabel("Load (MW)")
plt.legend()
plt.grid(True)
plt.savefig("weekday_weekend_comparison.png", dpi=150, bbox_inches="tight")
plt.show()

