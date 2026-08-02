#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:38:22 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
api.py — A FastAPI web service over the grid load database.

Turns the analysis into a callable SERVICE: other programs send HTTP requests
and receive JSON, without touching the database or Python code directly.
The "waiter" in front of the "kitchen" (SQL + load_report).

Run the server (from the activated venv):
    uvicorn api:app --reload
Then open the interactive docs at:
    http://127.0.0.1:8000/docs

Endpoints:
    GET /                      health check
    GET /summary?feeder=B      per-feeder summary (avg/peak/min/count)
    GET /feeders               list the distinct feeders available
"""
import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Grid Load API", version="1.0")

DB = "grid.db"


def query(sql, params=()):
    """Run a read-only query, always closing the connection (try/finally)."""
    conn = sqlite3.connect(DB)
    try:
        return pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()


@app.get("/")
def read_root():
    """Health check — confirms the service is running."""
    return {"message": "Grid load API is running"}


@app.get("/feeders")
def list_feeders():
    """List the distinct feeders present in the database."""
    df = query("SELECT DISTINCT feeder FROM readings ORDER BY feeder")
    return {"feeders": df["feeder"].tolist()}


@app.get("/summary")
def feeder_summary(feeder: str):
    """Per-feeder summary: average, peak, min load and reading count.

    404 if the feeder has no data (clear error, not an empty body).
    """
    df = query(
        "SELECT feeder, "
        "AVG(load_mw) AS avg_load, "
        "MAX(load_mw) AS peak_load, "
        "MIN(load_mw) AS min_load, "
        "COUNT(*) AS readings "
        "FROM readings WHERE feeder = ? GROUP BY feeder",
        params=(feeder,),
    )
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for feeder '{feeder}'")
    return df.to_dict(orient="records")[0]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)