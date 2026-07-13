#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:07:14 2026

@author: emmanuel_uchenna_ihedioha
"""

import pandas as pd
load_mw = [42, 39, 37, 36, 38, 45, 61, 78, 85, 88, 90, 91,
           89, 87, 86, 88, 92, 96, 98, 95, 84, 70, 58, 48]
df = pd.DataFrame({"hour": range(24), "load_mw": load_mw})

peak = df['load_mw'].max()
df['load_pu'] = df['load_mw'].apply(lambda x: x / peak)

def maintenance_flag(mw):
    if mw < 45:
        return 'Ok to service'
    else:
        return 'Do not service'


df['maintenance'] = df['load_mw'].apply(maintenance_flag)
print(df.head(10))