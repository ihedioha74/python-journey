#!/usr/bin/env python3
"""
Created on Tue Aug  4 19:15:09 2026

@author: emmanuel_uchenna_ihedioha
"""

# dashboard.py — Streamlit frontend for the Grid Load API.
#
# The frontend that only PRESENTS. It owns no data and no logic: every number
# comes from the FastAPI backend over HTTP, exactly like client.py — but the
# results drive widgets instead of print(). Three-layer architecture:
#
#     grid.db (data)  ->  api.py (backend/logic)  ->  dashboard.py (presentation)
#
# The AI explanation is fetched ON DEMAND (behind a button), because /explain
# calls Claude and takes a few seconds — fast numbers always, slow AI only when
# asked. That also means each /explain call is a real (billable) API request.
#
# Prerequisite: the API server must be running:  uvicorn api:app --reload
# Then run this app in another terminal:          streamlit run dashboard.py

import os

import requests
import pandas as pd
import streamlit as st

# The API base URL. Locally it defaults to your local server; when deployed,
# set API_BASE in the environment to the live API's public URL. Same code,
# both environments — no editing needed to switch.
BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000")

TIMEOUT = 5  # fast default for instant endpoints
AI_TIMEOUT = 30  # generous: /explain waits on Claude (seconds, not ms)


def get_json(path, params=None, timeout=TIMEOUT):
    """One place to call the API, with an operation-appropriate timeout and
    clear failure handling. The timeout MUST fit the work: 5s for SQL, longer
    for the AI call."""
    try:
        resp = requests.get(BASE + path, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot reach the API. Is the server running?  "
            "(uvicorn api:app --reload)"
        )
        st.stop()
    except requests.exceptions.ReadTimeout:
        st.error(
            "The request timed out. The AI analysis can take a while — "
            "please try again."
        )
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"API error: {e}")
        st.stop()


st.title("Grid Load Dashboard")
st.caption("Live data served by the FastAPI backend")

# 1. discover feeders from the API (no hardcoding)
feeders = get_json("/feeders")["feeders"]
feeder = st.selectbox("Choose a feeder:", feeders)

# 2. fetch that feeder's summary from the API (fast)
summary = get_json("/summary", params={"feeder": feeder})

# 3. present it — metric cards
col1, col2, col3 = st.columns(3)
col1.metric("Peak load", f"{summary['peak_load']:.1f} MW")
col2.metric("Average load", f"{summary['avg_load']:.1f} MW")
col3.metric("Readings", f"{summary['readings']:,}")

# 4. AI explanation — ON DEMAND (slow, billable), behind a button
st.subheader("AI analysis")
if st.button(f"Explain feeder {feeder}"):
    with st.spinner("Asking Claude to analyse this feeder..."):
        result = get_json("/explain", params={"feeder": feeder}, timeout=AI_TIMEOUT)
    st.write(result["explanation"])

# 5. compare all feeders at a glance — one call per feeder, then a chart
st.subheader("All feeders — peak vs average")
rows = [get_json("/summary", params={"feeder": f}) for f in feeders]
chart_df = pd.DataFrame(rows).set_index("feeder")[["peak_load", "avg_load"]]
st.bar_chart(chart_df)
