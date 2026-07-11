#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 20:00:39 2026

@author: emmanuel_uchenna_ihedioha
"""

timestamps = []
loads = []

with open("load_timeseries.csv", "r") as f:
    header = f.readline()          # read & discard the first line (the header)
    for line in f:
        clean = line.strip()
        parts = clean.split(",")
        timestamps.append(parts[0])          # keep timestamp as text (for now)
        loads.append(float(parts[1]))        # convert load to a real number