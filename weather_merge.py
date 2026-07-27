#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 21:29:58 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
weather_merge.py — Join temperature data to load data and measure the relationship.

Demonstrates: pandas merges (inner/left/outer), the `how` decision, aligning key
types before merging, and correlating two joined series.

Assumes load_report.py and load_data_2025.csv are alongside this file.
Usage:  python weather_merge.py
"""
import numpy as np
import pandas as pd
import load_report


def make_weather(year=2025, seed=1):
    """Daily average temperature: warm summers (peak ~day 200), cold winters."""
    dates = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    doy = dates.dayofyear
    # positive amplitude + summer peak location => high in July, low in January
    temp = 10 + 12 * np.cos((doy - 200) / 365 * 2 * np.pi)
    temp = temp + np.random.default_rng(seed).normal(0, 2, len(dates))
    return pd.DataFrame({"date": dates, "temp_c": temp.round(1)})


def load_vs_temperature(load_csv="load_data_2025.csv"):
    """Merge system daily load with daily temperature; return the joined frame."""
    clean = load_report.clean_load_data(load_csv)

    # daily average load per feeder, then averaged across feeders -> system load
    daily = load_report.analyze_load(clean, freq="D").reset_index()
    daily["date"] = pd.to_datetime(daily["timestamp"]).dt.date
    system = daily.groupby("date")["avg_mw"].mean().reset_index()

    # ALIGN KEY TYPES before merging: date-object won't match datetime
    system["date"] = pd.to_datetime(system["date"])
    weather = make_weather()

    n_before = len(system)
    merged = system.merge(weather, on="date", how="left")   # left: never drop a load day
    if len(merged) != n_before:                              # row-count safety check
        print(f"WARNING: row count changed {n_before} -> {len(merged)}")

    return merged


def main():
    merged = load_vs_temperature()
    corr = merged["avg_mw"].corr(merged["temp_c"])
    print(merged.head())
    print(f"\nRows: {len(merged)}")
    print(f"Load-temperature correlation: {corr:.3f}")
    print("Strong negative => cold drives high load (winter-peaking grid).")


if __name__ == "__main__":
    main()