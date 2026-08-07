#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 19:46:18 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
make_seed.py — one-off: extract a small, representative slice of grid.db
into grid_seed.csv, the committed demo data the deployed app builds from.

Run once locally:  python make_seed.py
"""
import sqlite3
import pandas as pd

DB = "grid.db"
OUT = "grid_seed.csv"
# one month keeps the file small while still showing all feeders and a
# realistic daily/weekly load shape.
START = "2025-01-01"
END = "2025-02-01"

conn = sqlite3.connect(DB)
try:
    df = pd.read_sql(
        "SELECT timestamp, load_mw, feeder FROM readings "
        "WHERE timestamp >= ? AND timestamp < ? ORDER BY timestamp, feeder",
        conn,
        params=(START, END),
    )
finally:
    conn.close()

# downsample to hourly to keep the committed seed lightweight: take readings
# on the hour only. (Delete this line to keep full 15-minute resolution.)
df = df[df["timestamp"].str.endswith("00:00")]

df.to_csv(OUT, index=False)
print(f"Wrote {OUT}: {len(df)} rows, feeders {sorted(df['feeder'].unique())}")