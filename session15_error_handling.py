#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 21:47:06 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
import numpy as np
def clean_load_data(filename):
    """Read a messy load CSV and return a cleaned DataFrame."""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find '{filename}'. Please check the name and path."
        )

    # validate the file has the columns we need
    required = ["load_mw", "feeder"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"File '{filename}' is missing required column(s): {missing}"
        )

    df = df.drop_duplicates()
    df["feeder"] = df["feeder"].str.upper()
    df.loc[df["load_mw"] < 0, "load_mw"] = np.nan
    df.loc[df["load_mw"] > 500, "load_mw"] = np.nan
    df = df.dropna(subset=["load_mw"])
    return df

