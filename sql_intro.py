#!/usr/bin/env python3
"""
Created on Sun Aug  2 02:04:51 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
sql_intro.py — Storing and querying load data with SQLite.

The shift from analysis to backend: a CSV is re-read and re-parsed in full on
every run; a database stores data in queryable form and returns only what you
ask for. SQLite is a complete SQL database in a single file, built into Python.

Architectural principle proven here: CLEAN ONCE, ON THE WAY IN. The database is
only as clean as what you put in it, so cleaning belongs upstream of storage —
not repeated in every query. Then every query inherits trustworthy data.

Usage:  python sql_intro.py   (expects load_data_2025.csv + load_report.py)
"""
import sqlite3

import pandas as pd

import load_report

DB = "grid.db"
TABLE = "readings"


def load_clean_to_db(csv, conn, n=1000):
    """Clean the CSV FIRST, then write it to the database (clean on the way in)."""
    clean = load_report.clean_load_data(csv).head(n)
    clean.to_sql(TABLE, conn, if_exists="replace", index=False)
    return len(clean)


def show_schema(conn):
    """Inspect the database's own structure — never query blind."""
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)[
        "name"
    ].tolist()
    schema = pd.read_sql(f"PRAGMA table_info({TABLE})", conn)
    return tables, schema[["name", "type"]]


def summary_by_feeder(conn):
    """Per-feeder average and peak — the analyze_load summary, in one SQL line."""
    return pd.read_sql(
        f"SELECT feeder, "
        f"AVG(load_mw) AS avg_load, "
        f"MAX(load_mw) AS peak_load "
        f"FROM {TABLE} GROUP BY feeder",
        conn,
    )


def main():
    conn = sqlite3.connect(DB)
    try:
        n = load_clean_to_db("load_data_2025.csv", conn)
        print(f"Loaded {n} cleaned rows into '{TABLE}'")

        tables, cols = show_schema(conn)
        print("\nTables:", tables)
        print("Columns:")
        print(cols.to_string(index=False))

        print("\nPer-feeder summary (clean — four feeders):")
        print(summary_by_feeder(conn).to_string(index=False))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
