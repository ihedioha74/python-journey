#!/usr/bin/env python3
"""
Created on Sat Aug  1 02:01:18 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
polars_lazy_benchmark.py — Eager vs lazy, CSV vs Parquet, at scale.

Demonstrates the two independent speedups that stack for large tabular work:
  1. lazy polars (scan_csv + .collect) over eager pandas — filter/column
     pushdown means most of the file is never read.
  2. Parquet over CSV — binary, columnar, compressed: far smaller and far
     faster to scan, and projection pushdown becomes physical.

Rule of thumb: lazy polars + Parquet is the standard for data you query
repeatedly at scale. At small scale (~100k rows) it isn't worth the ceremony.

Requires generate_grid_data.py alongside. Writes ~1.4 GB CSV + ~0.1 GB Parquet.
Usage:  python polars_lazy_benchmark.py
"""
import os
import time

import pandas as pd
import polars as pl

import generate_grid_data

CSV = "grid_data_huge.csv"
PARQUET = "grid_data_huge.parquet"
FEEDER = "F00"


def build_files():
    """Generate the ~47M-row dataset once, saved as both CSV and Parquet."""
    huge = generate_grid_data.generate_grid_data(
        n_feeders=30, years=(2023, 2024, 2025), freq_min=1
    )
    huge.to_csv(CSV, index=False)
    huge.to_parquet(PARQUET)
    print(f"Rows: {len(huge):,}")
    print(f"CSV:     {os.path.getsize(CSV)/1e9:.2f} GB")
    print(f"Parquet: {os.path.getsize(PARQUET)/1e9:.2f} GB")
    del huge


def bench():
    """Time the same per-feeder mean three ways."""
    # 1. eager pandas from CSV
    t0 = time.time()
    pdf = pd.read_csv(CSV)
    _ = pdf[pdf["feeder"] == FEEDER]["load_mw"].mean()
    print(f"pandas + CSV:      {time.time()-t0:5.1f} s")
    del pdf

    # 2. lazy polars from CSV
    t0 = time.time()
    _ = (
        pl.scan_csv(CSV)
        .filter(pl.col("feeder") == FEEDER)
        .select(pl.col("load_mw").mean())
        .collect()
    )
    print(f"polars + CSV:      {time.time()-t0:5.1f} s")

    # 3. lazy polars from Parquet
    t0 = time.time()
    _ = (
        pl.scan_parquet(PARQUET)
        .filter(pl.col("feeder") == FEEDER)
        .select(pl.col("load_mw").mean())
        .collect()
    )
    print(f"polars + Parquet:  {time.time()-t0:5.1f} s")


def main():
    if not (os.path.exists(CSV) and os.path.exists(PARQUET)):
        build_files()
    bench()


if __name__ == "__main__":
    main()
