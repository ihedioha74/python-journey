#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 21:49:53 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
client.py — A Python client for the Grid Load API (Session 38's api.py).

The mirror of the server: FastAPI *receives* requests, the requests library
*sends* them. Two separate programs talking over HTTP — no browser, no human.
This is how the Streamlit app, an ML model, or any program will reach the API.

Prerequisite: the server must be running in another terminal:
    uvicorn api:app --reload

Usage:  python client.py
"""
import requests

BASE = "http://127.0.0.1:8000"
TIMEOUT = 5   # seconds — never wait forever for a server that may be down


def get_json(path, params=None):
    """GET a path and return parsed JSON, raising a clear error on failure."""
    resp = requests.get(BASE + path, params=params, timeout=TIMEOUT)
    resp.raise_for_status()          # turn HTTP 4xx/5xx into an exception
    return resp.json()


def list_feeders():
    """Ask the API which feeders exist (discovery before querying)."""
    return get_json("/feeders")["feeders"]


def feeder_summary(feeder):
    """Fetch one feeder's summary as a dict."""
    return get_json("/summary", params={"feeder": feeder})


def main():
    try:
        # 1. health check
        print("Health:", get_json("/"))

        # 2. discover feeders, then summarise each
        feeders = list_feeders()
        print("Feeders available:", feeders)

        print("\nPer-feeder summary (fetched over HTTP):")
        for f in feeders:
            s = feeder_summary(f)
            print(f"  {f}: peak {s['peak_load']:.1f} MW, "
                  f"avg {s['avg_load']:.1f} MW, {s['readings']} readings")

    except requests.exceptions.ConnectionError:
        print("ERROR: could not reach the API. Is the server running?")
        print("Start it with:  uvicorn api:app --reload")
    except requests.exceptions.HTTPError as e:
        print(f"API returned an error: {e}")


if __name__ == "__main__":
    main()