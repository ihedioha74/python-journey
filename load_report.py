#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:54:56 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
load_report.py — Clean a load CSV and save a full report.
Usage:  python load_report.py <filename>
Outputs (into the 'reports' folder): cleaned CSV, chart PNG, text summary.
"""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def make_output_name(input_filename, suffix, new_ext=None):
    """Turn 'march.csv' + '_cleaned' into 'march_cleaned.csv' (optionally new extension)."""
    base = os.path.splitext(os.path.basename(input_filename))[0]
    ext = new_ext if new_ext else os.path.splitext(input_filename)[1]
    return base + suffix + ext


def clean_load_data(filename):
    """Read a messy load CSV and return a cleaned DataFrame."""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find '{filename}'. Check the name and path.")

    required = ["load_mw", "feeder"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"File '{filename}' is missing required column(s): {missing}")

    df = df.drop_duplicates()
    df["feeder"] = df["feeder"].str.upper()
    df.loc[df["load_mw"] < 0, "load_mw"] = np.nan
    df.loc[df["load_mw"] > 500, "load_mw"] = np.nan
    df = df.dropna(subset=["load_mw"])
    return df

def analyze_load(df):
    """Compute a per-feeder summary: peak, min, mean, count, load factor, time of peak."""
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    summary = df.groupby("feeder")["load_mw"].agg(["max", "min", "mean", "count"])
    summary["load_factor"] = (summary["mean"] / summary["max"]).round(3)
    summary = summary.round(2)
    peak_times = df.loc[df.groupby("feeder")["load_mw"].idxmax()].set_index("feeder")["timestamp"]
    summary["peak_time"] = peak_times
    summary = summary.rename(columns={
        "max": "peak_mw", "min": "min_mw", "mean": "avg_mw", "count": "readings",
    })
    return summary


def save_report(df, input_filename, output_dir="reports"):
    """Save a cleaned CSV, a chart PNG, and a rich text summary into output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    summary = analyze_load(df)

    # 1. cleaned CSV
    csv_path = os.path.join(output_dir, make_output_name(input_filename, "_cleaned"))
    df.to_csv(csv_path, index=False)

    # 2. chart PNG — peak vs average per feeder
    png_path = os.path.join(output_dir, make_output_name(input_filename, "_chart", ".png"))
    summary[["peak_mw", "avg_mw"]].plot(kind="bar")
    plt.title("Peak vs Average Load per Feeder")
    plt.ylabel("Load (MW)")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close()

    # 3. rich text summary
    txt_path = os.path.join(output_dir, make_output_name(input_filename, "_summary", ".txt"))
    with open(txt_path, "w") as f:
        f.write(f"Load Report for {input_filename}\n")
        f.write(f"Rows after cleaning: {len(df)}\n\n")
        f.write("Per-feeder summary:\n")
        f.write(summary.to_string())
    return csv_path, png_path, txt_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python load_report.py <filename>")
        return

    filename = sys.argv[1]
    print(f"Processing '{filename}'...")
    clean = clean_load_data(filename)
    print(f"Cleaned data: {clean.shape[0]} rows remaining.")

    csv_path, png_path, txt_path = save_report(clean, filename)
    print("Saved:")
    print(f"  {csv_path}")
    print(f"  {png_path}")
    print(f"  {txt_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()