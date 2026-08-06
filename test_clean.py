#!/usr/bin/env python3
"""
Created on Wed Aug  5 20:10:58 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
test_clean.py — Automated tests for clean_load_data (pytest).

Encodes the guarantees of the cleaning pipeline as permanent, runnable checks —
the behaviours previously verified by hand (Sessions 13, 26, 36), now automatic.
Every test follows Arrange-Act-Assert.

Run (through the venv's pytest, not Anaconda's):
    python -m pytest test_clean.py -v
"""
import pandas as pd
import pytest

import load_report


@pytest.fixture
def write_csv(tmp_path):
    """Write a DataFrame to a temp CSV and return its path.

    tmp_path is a pytest-provided temp directory, unique per test and cleaned
    up automatically — no _test_input.csv litter in the project folder.
    """

    def _write(df):
        path = tmp_path / "input.csv"
        df.to_csv(path, index=False)
        return str(path)

    return _write


def test_uppercases_feeder_names(write_csv):
    csv = write_csv(
        pd.DataFrame(
            {
                "timestamp": ["2025-01-01 00:00:00", "2025-01-01 00:15:00"],
                "load_mw": [50.0, 60.0],
                "feeder": ["a", "B"],
            }
        )
    )
    result = load_report.clean_load_data(csv)
    assert set(result["feeder"]) == {"A", "B"}


def test_removes_out_of_range_loads(write_csv):
    csv = write_csv(
        pd.DataFrame(
            {
                "timestamp": ["2025-01-01 00:00:00"] * 4,
                "load_mw": [50.0, 0.05, 600.0, 80.0],  # 0.05 too low, 600 too high
                "feeder": ["A", "A", "A", "A"],
            }
        )
    )
    result = load_report.clean_load_data(csv)
    assert len(result) == 2
    assert result["load_mw"].min() >= 0.1
    assert result["load_mw"].max() <= 500


def test_drops_duplicate_rows(write_csv):
    csv = write_csv(
        pd.DataFrame(
            {
                "timestamp": ["2025-01-01 00:00:00", "2025-01-01 00:00:00"],
                "load_mw": [50.0, 50.0],
                "feeder": ["A", "A"],
            }
        )
    )
    result = load_report.clean_load_data(csv)
    assert len(result) == 1


def test_missing_file_raises(write_csv):
    """clean_load_data should raise FileNotFoundError for a missing file."""
    with pytest.raises(FileNotFoundError):
        load_report.clean_load_data("does_not_exist.csv")
