#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 20:42:38 2026

@author: emmanuel_uchenna_ihedioha
"""

#import pandas as pd
import matplotlib.pyplot as plt

# Panel 1 data: a day
hours = range(24)
load = [42, 39, 37, 36, 38, 45, 61, 78, 85, 88, 90, 91,
        89, 87, 86, 88, 92, 96, 98, 95, 84, 70, 58, 48]

# Panel 2 data: a year of monthly peaks
months = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]
peak = [120, 118, 105, 95, 88, 92, 98, 100, 90, 96, 110, 125]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1 — draw onto ax1
ax1.plot(hours, load, marker="o", color="red")
ax1.set_title("Daily Load Profile")
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("Load (MW)")
ax1.grid(True)

# Panel 2 — draw onto ax2
ax2.bar(months, peak)
ax2.set_title("Monthly Peak Demand")
ax2.set_xlabel("Month")
ax2.set_ylabel("Peak (MW)")
ax2.grid(True, axis="y")

plt.tight_layout()
plt.show()

#plotting a figure of 2x2

fig, axs = plt.subplots(2, 2, figsize=(14, 9))

# Top-left: daily load curve
axs[0, 0].plot(hours, load, marker="o", color="red")
axs[0, 0].set_title("Daily Load Profile")
axs[0, 0].set_ylabel("Load (MW)")

# Top-right: monthly peak bars
axs[0, 1].bar(months, peak)
axs[0, 1].set_title("Monthly Peak Demand")

# Bottom-left: a histogram — the DISTRIBUTION of hourly loads
axs[1, 0].hist(load, bins=8, color="green")
axs[1, 0].set_title("Distribution of Hourly Loads")
axs[1, 0].set_xlabel("Load (MW)")
axs[1, 0].set_ylabel("Count of hours")

# Bottom-right: leave empty for now, or add a note
axs[1, 1].axis("off")   # hide the unused panel

plt.tight_layout()
plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
plt.show()