#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 03:36:14 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
polars_operations.py — Everyday polars: joins, window functions, dynamic resampling.

The polars versions of operations learned earlier in pandas:
  * join        — Session 27's merge (merge -> join; same on=/how=)
  * .over()     — window function: per-group value kept on EVERY row (annotate,
                  not collapse) — no clean pandas one-liner equivalent
  * group_by_dynamic — Session 24's time resampling (resample -> group_by_dynamic)

Assumes grid_data_large.csv alongside (from generate_grid_data.py).
Usage:  python polars_operations.py
"""
import polars as pl


def build_metadata(n_feeders=30):
    """A small per-feeder lookup table to join against (region + voltage)."""
    feeders = [f"F{i:02d}" for i in range(n_feeders)]
    regions = ["Nord", "Süd", "Ost", "West"]
    return pl.DataFrame({
        "feeder": feeders,
        "region": [regions[i % 4] for i in range(n_feeders)],   # cycle via modulo
        "voltage_kv": [[10, 20][i % 2] for i in range(n_feeders)],
    })


def demo_join(df, metadata):
    """Attach metadata to every load row. how='left' keeps all load rows."""
    joined = df.join(metadata, on="feeder", how="left")
    assert joined.height == df.height, "row count changed — duplicate keys?"
    return joined


def demo_window(joined):
    """.over('feeder'): each row keeps its own reading AND its feeder's average,
    so deviation-from-baseline is a single expression. Foundation of anomaly work."""
    return joined.with_columns(
        pl.col("load_mw").mean().over("feeder").alias("feeder_avg"),
    ).with_columns(
        (pl.col("load_mw") - pl.col("feeder_avg")).round(2).alias("deviation"),
    )


def demo_dynamic(df):
    """Daily peak & mean per feeder — group first, then resample (Session 24)."""
    ts = df.with_columns(pl.col("timestamp").str.to_datetime()).sort("timestamp")
    return (
        ts.group_by_dynamic("timestamp", every="1d", group_by="feeder")
          .agg([
              pl.col("load_mw").mean().alias("avg_mw"),
              pl.col("load_mw").max().alias("peak_mw"),
          ])
    )


def main():
    df = pl.read_csv("grid_data_large.csv")
    metadata = build_metadata()

    joined = demo_join(df, metadata)
    print("Joined:", joined.height, "rows,", joined.width, "columns")

    dev = demo_window(joined)
    print("\nBiggest deviations from each feeder's own baseline:")
    print(dev.sort("deviation", descending=True)
             .select(["timestamp", "feeder", "load_mw", "feeder_avg", "deviation"])
             .head())

    daily = demo_dynamic(df)
    print(f"\nDaily rollup: {daily.height:,} rows")
    print(daily.head())


if __name__ == "__main__":
    main()