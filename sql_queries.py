#!/usr/bin/env python3
"""
Created on Sun Aug  2 18:18:15 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
sql_queries.py — Sharper SQL: sorting, compound filters, top-N, and INSERT.

Reading (pd.read_sql):
  ORDER BY ... DESC/ASC     sort results
  WHERE a AND/OR b          compound filters
  ... LIMIT n               top-N when combined with ORDER BY
  COUNT(*)                  a computed fact, not raw data

Writing (cursor.execute + commit):
  INSERT with ? placeholders   parameterised — the safe way (no SQL injection)
  conn.commit()                changes are not permanent until committed
  a group of changes + one commit = a TRANSACTION (all-or-nothing)

Usage:  python sql_queries.py   (expects load_data_2025.csv + load_report.py)
"""
import sqlite3

import pandas as pd

import load_report

DB = "grid.db"
TABLE = "readings"


def load_full_dataset(csv, conn):
    """Clean the whole CSV and load it (clean on the way in). Returns row count."""
    clean = load_report.clean_load_data(csv)
    clean.to_sql(TABLE, conn, if_exists="replace", index=False)
    return pd.read_sql(f"SELECT COUNT(*) AS n FROM {TABLE}", conn)["n"][0]


def top_loads(conn, limit=10, above=120):
    """Top-N highest readings above a threshold — filter, sort, limit."""
    return pd.read_sql(
        f"SELECT timestamp, feeder, load_mw FROM {TABLE} "
        f"WHERE load_mw > {above} "
        f"ORDER BY load_mw DESC "
        f"LIMIT {limit}",
        conn,
    )


def feeder_above(conn, feeder, threshold):
    """Compound filter: one feeder's readings above a threshold."""
    return pd.read_sql(
        f"SELECT * FROM {TABLE} WHERE feeder = ? AND load_mw > ?",
        conn,
        params=(feeder, threshold),
    )


def insert_reading(conn, timestamp, feeder, load_mw):
    """Add ONE new reading — parameterised (?), then commit.

    ? placeholders are the safe way to pass values: never string-concatenate
    data into SQL (prevents SQL injection). commit() makes it permanent.
    """
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO {TABLE} (timestamp, feeder, load_mw) VALUES (?, ?, ?)",
        (timestamp, feeder, load_mw),
    )
    conn.commit()


def main():
    conn = sqlite3.connect(DB)
    try:
        n = load_full_dataset("load_data_2025.csv", conn)
        print(f"Rows in database: {n}")

        print("\nTop 10 readings above 120 MW:")
        print(top_loads(conn).to_string(index=False))

        hi_b = feeder_above(conn, "B", 130)
        print(f"\nFeeder B readings above 130 MW: {len(hi_b)} rows")

        insert_reading(conn, "2025-12-31 23:45:00", "B", 99.99)
        check = pd.read_sql(
            f"SELECT * FROM {TABLE} WHERE timestamp = '2025-12-31 23:45:00'", conn
        )
        print(f"\nAfter INSERT — rows at that timestamp: {len(check)}")
        print(check.to_string(index=False))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
