#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 21:19:16 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
pivot_and_copies.py — Reshaping with pivot tables, and the SettingWithCopyWarning.

Covers: long vs wide data, pivot_table (index/columns/values/aggfunc/margins),
pivot_table vs groupby+unstack, and views-vs-copies (why filter-then-modify warns).

Assumes load_report.py and load_data_2025.csv are alongside this file.
Usage:  python pivot_and_copies.py
"""
import pandas as pd
import load_report


def monthly_grid(clean, aggfunc="mean"):
    """Reshape 15-min readings into a month x feeder grid in one pivot_table call.

    aggfunc="mean" -> average load per cell; "max" -> monthly peak per cell.
    """
    clean = clean.copy()
    clean["month"] = pd.to_datetime(clean["timestamp"]).dt.month
    return clean.pivot_table(
        index="month", columns="feeder", values="load_mw", aggfunc=aggfunc
    ).round(1)


def flag_high_load(clean, month, threshold=100):
    """Return an INDEPENDENT January-only frame with a 'high load' flag.

    The explicit .copy() removes the view/copy ambiguity that triggers
    SettingWithCopyWarning when you filter-then-modify.
    """
    clean = clean.copy()
    clean["month"] = pd.to_datetime(clean["timestamp"]).dt.month
    subset = clean[clean["month"] == month].copy()      # <-- the fix
    subset["flag"] = subset["load_mw"] > threshold
    return subset


def main():
    clean = load_report.clean_load_data("load_data_2025.csv")

    print("=== Monthly AVERAGE load (MW) ===")
    print(monthly_grid(clean, "mean"))

    print("\n=== Monthly PEAK load (MW) ===")
    print(monthly_grid(clean, "max"))

    jan = flag_high_load(clean, month=1, threshold=100)
    print(f"\nJanuary readings above 100 MW: {jan['flag'].sum()}")


if __name__ == "__main__":
    main()