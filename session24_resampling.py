#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:04:21 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
session24_resampling.py — Time-series resampling of load data.

Covers: datetime index, resample() with frequency aliases, the mean-vs-max
choice, groupby+resample per feeder, daily load factor, hour-of-day profile,
rolling averages, and the load duration curve.

Usage:  python session24_resampling.py
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILENAME = "messy_meter_data_v1.csv"
FEEDER = "B"


# ---------------------------------------------------------------- load & index
df = pd.read_csv(FILENAME)
df["feeder"] = df["feeder"].str.upper()
df = df.dropna(subset=["load_mw"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# the timestamp must be the INDEX, not just a column, for time-series tools
df = df.set_index("timestamp").sort_index()

print("First rows:")
print(df.head())
print("\nIndex type:", type(df.index).__name__, "| rows:", len(df))


# ------------------------------------------------- the trap: mixing feeders
# Valid arithmetic, meaningless physics: averages four separate circuits
# together, which corresponds to nothing measurable on the network.
daily_wrong = df["load_mw"].resample("D").mean().round(2)
print("\n--- WRONG: all feeders mixed together ---")
print(daily_wrong)


# ------------------------------------------------- mean vs max is a PHYSICAL choice
# .resample() only defines the buckets; the aggregation says how to collapse
# them. Resampling with .mean() and then taking a peak DESTROYS the peak.
one_feeder = df[df["feeder"] == FEEDER]["load_mw"]

print(f"\n--- Feeder {FEEDER}: daily mean vs daily max ---")
print(pd.DataFrame({
    "daily_mean": one_feeder.resample("D").mean().round(2),
    "daily_max": one_feeder.resample("D").max(),
}))


# ------------------------------------------------- correct: group first, then resample
daily = (df.groupby("feeder")["load_mw"]
           .resample("D")
           .agg(["max", "mean", "min"])
           .round(2))
daily["load_factor"] = (daily["mean"] / daily["max"]).round(3)

print("\n--- Daily summary per feeder ---")
print(daily)

# NOTE: period load factor < the average of daily load factors, always.
# The denominator (peak) only ratchets up over a longer window while the
# numerator (typical level) does not. "Load factor" is meaningless unless
# the period is stated.


# ------------------------------------------------- hour-of-day load profile
# A DatetimeIndex exposes .hour, .day, .dayofweek, .month directly.
by_hour = (df.groupby([df["feeder"], df.index.hour])["load_mw"]
             .mean()
             .unstack(level=0)
             .round(1))
by_hour.index.name = "hour"

print("\n--- Average load by hour of day ---")
print(by_hour)


# ------------------------------------------------- rolling average (smoothing)
# resample() REDUCES rows; rolling() keeps them all and smooths.
# First (window-1) values are NaN: not enough readings yet.
smoothed = one_feeder.rolling(window=8).mean().round(2)
print(f"\n--- Feeder {FEEDER}: 8-period rolling mean (first 12) ---")
print(smoothed.head(12))


# ------------------------------------------------- load duration curve
# Sort every reading descending: time leaves the x-axis, and what remains is
# how many intervals demand exceeded each level. Area = energy, shape = peakiness.
ldc = one_feeder.sort_values(ascending=False).reset_index(drop=True)

plt.figure(figsize=(8, 5))
plt.plot(ldc.values)
plt.xlabel("15-minute intervals (sorted, highest to lowest)")
plt.ylabel("Load (MW)")
plt.title(f"Load Duration Curve — Feeder {FEEDER}")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"reports/load_duration_curve_feeder_{FEEDER}.png", dpi=150)
plt.close()

print(f"\nSaved load_duration_curve_feeder_{FEEDER}.png")