#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 21:56:29 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
session29_multiindex.py — Working with multi-index (hierarchical) DataFrames.

A reference for the selection, reshaping, and flattening patterns that come up
whenever you group by more than one key (as analyze_load(df, freq=...) does).

Key rules, up front:
  * Build a multi-index by grouping on several keys: groupby(["feeder", ...]).
  * Each row is identified by a TUPLE of level values, e.g. ("A", "2025-07-31").
  * .loc matches the OUTER level; use .xs(value, level="name") for any INNER level.
  * One row selected -> Series; many rows -> DataFrame.
  * merge works on COLUMNS, not index levels -> reset_index() before merging.

Assumes load_report.py and load_data_2025.csv are alongside this file.
Usage:  python session29_multiindex.py
"""
import pandas as pd
import load_report


def build_monthly():
    """A two-level (feeder, timestamp) summary — the multi-index we explore."""
    clean = load_report.clean_load_data("load_data_2025.csv")
    return load_report.analyze_load(clean, freq="ME")


def demo_selection(monthly):
    """Selecting from a multi-index: outer level, exact row, inner level."""
    # all of feeder A's months — .loc on the OUTER level (drops that level)
    feeder_a = monthly.loc["A"]                     # -> DataFrame (12 rows)

    # one exact (feeder, month) row — pin BOTH levels with a tuple
    a_july = monthly.loc[("A", "2025-07-31")]       # -> Series (one row)

    # all feeders for one month — INNER level, so .loc fails; use .xs
    july_all = monthly.xs("2025-07-31", level="timestamp")   # -> DataFrame (4 rows)

    return feeder_a, a_july, july_all


def demo_reshape(monthly):
    """Swapping which level is outer, and flattening for merge/export."""
    # put timestamp outer, feeder inner — now .loc[date] gives all feeders
    swapped = monthly.swaplevel().sort_index()      # sort so the new outer groups

    # drop the hierarchy: levels become ordinary columns (needed for merge/CSV)
    flat = monthly.reset_index()

    return swapped, flat


def main():
    monthly = build_monthly()
    print("=== multi-index summary (head) ===")
    print(monthly.head(6))
    print("\nindex levels:", monthly.index.names)

    feeder_a, a_july, july_all = demo_selection(monthly)
    print("\n=== monthly.loc['A'] — outer level, all A's months ===")
    print(feeder_a.head(3))
    print("\n=== monthly.loc[('A','2025-07-31')] — one row -> Series ===")
    print(a_july)
    print("\n=== monthly.xs('2025-07-31', level='timestamp') — inner level, all feeders ===")
    print(july_all)

    swapped, flat = demo_reshape(monthly)
    print("\n=== swaplevel().sort_index() — timestamp now outer ===")
    print(swapped.head(4))
    print("\n=== reset_index() — flat, ready to merge/export ===")
    print("columns:", flat.columns.tolist())


if __name__ == "__main__":
    main()