#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 19:27:23 2026

@author: emmanuel_uchenna_ihedioha
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import load_report

st.title("Load Report Tool")
st.write("Upload a meter data CSV to clean, analyse, and visualise it.")

uploaded = st.file_uploader("Choose a CSV file", type="csv")

if uploaded is not None:
    clean = load_report.clean_load_data(uploaded)
    st.success(f"Cleaned data: {len(clean)} rows remaining.")

    summary = load_report.analyze_load(clean)

    st.subheader("Per-feeder summary")
    st.dataframe(summary)

    # headline metrics
    top_feeder = summary["peak_mw"].idxmax()
    col1, col2 = st.columns(2)
    col1.metric("Highest peak", f"{summary.loc[top_feeder, 'peak_mw']} MW", f"Feeder {top_feeder}")
    col2.metric("Load factor", f"{summary.loc[top_feeder, 'load_factor']}")

    # chart
    st.subheader("Peak vs average load")
    fig, ax = plt.subplots()
    summary[["peak_mw", "avg_mw"]].plot(kind="bar", ax=ax)
    ax.set_ylabel("Load (MW)")
    ax.grid(True, axis="y")
    st.pyplot(fig)

    # AI interpretation, opt-in
    st.subheader("AI interpretation")
    if st.button("Generate interpretation"):
        with st.spinner("Asking Claude..."):
            insight = load_report.explain_load(summary, use_real_api=True)
        st.write(insight)