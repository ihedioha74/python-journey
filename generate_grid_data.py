#!/usr/bin/env python3
"""
Created on Thu Jul 30 20:32:59 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
generate_grid_data.py — Physically-coherent grid load data, parameterised to scale.

Extends the Session 25 single-year generator with knobs for the number of
feeders, the set of years, and the time resolution, so the same code produces
anything from a 140k-row toy to a multi-million-row stress test.

Physics (per Session 25), now scaled PROPORTIONALLY to each feeder's base load
so small and large feeders swing realistically:
    load = base
         + daily     (±35% of base, cosine peaking at 19:00)
         + weekly    (weekends -12% of base, weekdays +5%)
         + seasonal  (±25% of base, cosine peaking ~1 Jan — winter-peaking grid)
         + noise     (Gaussian, 8% of base)

Per-feeder base loads are drawn right-skewed (lognormal) across ~20-120 MW:
most feeders modest, a few large — the shape of a real substation region.

Output: grid_data_large.csv   Usage: python generate_grid_data.py
"""
import numpy as np
import pandas as pd


def generate_grid_data(n_feeders=30, years=(2023, 2024, 2025), freq_min=15, seed=42):
    """Return a long DataFrame (timestamp, feeder, load_mw) at the requested scale."""
    rng = np.random.default_rng(seed)

    # per-feeder base loads: right-skewed 20-120 MW
    feeders = [f"F{i:02d}" for i in range(n_feeders)]
    raw = rng.lognormal(0.0, 0.5, n_feeders)
    bases = 20 + (raw - raw.min()) / (raw.max() - raw.min()) * 100

    # time backbone across all requested years, at the requested resolution
    parts = [
        pd.date_range(f"{y}-01-01", f"{y}-12-31 23:59", freq=f"{freq_min}min")
        for y in years
    ]
    timestamps = pd.DatetimeIndex(np.concatenate(parts))

    # cartesian product: every feeder reports at every timestamp
    idx = pd.MultiIndex.from_product(
        [timestamps, feeders], names=["timestamp", "feeder"]
    )
    df = idx.to_frame(index=False)

    # time components
    hour = df["timestamp"].dt.hour + df["timestamp"].dt.minute / 60
    dow = df["timestamp"].dt.dayofweek
    doy = df["timestamp"].dt.dayofyear

    # layers — each PROPORTIONAL to the feeder's own base
    base = df["feeder"].map(dict(zip(feeders, bases)))
    daily = 0.35 * base * np.cos((hour - 19) / 24 * 2 * np.pi)
    weekly = np.where(dow >= 5, -0.12 * base, 0.05 * base)
    seasonal = 0.25 * base * np.cos((doy - 1) / 365 * 2 * np.pi)
    noise = rng.normal(0, 0.08 * base, len(df))

    df["load_mw"] = (base + daily + weekly + seasonal + noise).round(2)
    return df


def main():
    df = generate_grid_data()  # defaults: 30 feeders x 3 years x 15-min ~ 3.16M rows
    out = "grid_data_large.csv"
    df.to_csv(out, index=False)
    print(f"Saved {out} — {len(df):,} rows")
    print(df.groupby("feeder")["load_mw"].mean().round(1).head())


if __name__ == "__main__":
    main()
