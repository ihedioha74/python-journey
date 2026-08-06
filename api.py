#!/usr/bin/env python3
"""
Created on Sun Aug  2 18:38:22 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
api.py — A FastAPI web service over the grid load database.

Turns the analysis into a callable SERVICE: other programs send HTTP requests
and receive JSON, without touching the database or Python code directly.
The "waiter" in front of the "kitchen" (SQL + load_report).

Now AI-powered: /explain runs the summary, then asks Claude to interpret it —
the AI is just another layer of logic behind the same clean interface.

Run the server (from the activated venv):
    uvicorn api:app --reload
Then open the interactive docs at:
    http://127.0.0.1:8000/docs

Endpoints:
    GET /                      health check
    GET /feeders              list the distinct feeders available
    GET /summary?feeder=B      per-feeder summary (avg/peak/min/count)
    GET /explain?feeder=B      summary + a plain-language AI explanation
"""
import sqlite3

import pandas as pd
from anthropic import Anthropic
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Grid Load API", version="2.0")

DB = "grid.db"

# Anthropic client created ONCE at module level (reads ANTHROPIC_API_KEY from
# the environment), reused across all requests — not rebuilt per call.
claude = Anthropic()


def query(sql, params=()):
    """Run a read-only query, always closing the connection (try/finally)."""
    conn = sqlite3.connect(DB)
    try:
        return pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()


def get_summary(feeder):
    """Per-feeder summary as a dict, or None if the feeder has no data."""
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
        return None
    return df.to_dict(orient="records")[0]


def build_prompt(summary):
    """Turn the summary facts into a prompt for Claude."""
    return (
        "You are a power systems analyst. Explain this feeder's load profile "
        "in 2-3 sentences for a grid operator.\n\n"
        f"Feeder {summary['feeder']}: average load {summary['avg_load']:.1f} MW, "
        f"peak {summary['peak_load']:.1f} MW, minimum {summary['min_load']:.1f} MW, "
        f"across {summary['readings']} readings."
    )


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
    """Per-feeder summary: average, peak, min load and reading count."""
    summary = get_summary(feeder)
    if summary is None:
        raise HTTPException(status_code=404, detail=f"No data for feeder '{feeder}'")
    return summary


@app.get("/explain")
def explain_feeder(feeder: str):
    """Fetch the summary, then ask Claude to explain it in plain language."""
    summary = get_summary(feeder)
    if summary is None:
        raise HTTPException(status_code=404, detail=f"No data for feeder '{feeder}'")

    message = claude.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": build_prompt(summary)}],
    )
    return {"summary": summary, "explanation": message.content[0].text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
