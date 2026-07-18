#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:54:56 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
load_report.py — Clean a load CSV and print a feeder summary.
Usage:  python load_report.py <filename>
"""
import sys
import pandas as pd
import numpy as np


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


def summarize(df):
    """Print average load per feeder."""
    averages = df.groupby("feeder")["load_mw"].mean()
    print("\nAverage load per feeder (MW):")
    print(averages.round(2))
    return averages


def main():
    """The program's entry point — orchestrates the whole job."""
    if len(sys.argv) < 2:
        print("Usage: python load_report.py <filename>")
        return

    filename = sys.argv[1]
    print(f"Processing '{filename}'...")

    clean = clean_load_data(filename)
    print(f"Cleaned data: {clean.shape[0]} rows remaining.")
    summarize(clean)
    print("\nDone.")


if __name__ == "__main__":
    main()