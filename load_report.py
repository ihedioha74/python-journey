#!/usr/bin/env python3
"""
Created on Sat Jul 18 09:54:56 2026

@author: emmanuel_uchenna_ihedioha
"""

"""
load_report.py — Clean a load CSV and save a full report.
Usage:  python load_report.py <filename>
Outputs (into the 'reports' folder): cleaned CSV, chart PNG, text summary.
"""
import argparse
import os

import anthropic
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_output_name(input_filename, suffix, new_ext=None):
    """Turn 'march.csv' + '_cleaned' into 'march_cleaned.csv' (optionally new extension)."""
    base = os.path.splitext(os.path.basename(input_filename))[0]
    ext = new_ext if new_ext else os.path.splitext(input_filename)[1]
    return base + suffix + ext


def clean_load_data(filename):
    """Read a messy load CSV and return a cleaned DataFrame."""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find '{filename}'. Check the name and path."
        )

    required = ["load_mw", "feeder"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"File '{filename}' is missing required column(s): {missing}")

    df = df.drop_duplicates()
    df["feeder"] = df["feeder"].str.upper()
    df.loc[df["load_mw"] < 0.1, "load_mw"] = (
        np.nan
    )  # implausibly low (< 100 kW) → fault
    df.loc[df["load_mw"] > 500, "load_mw"] = np.nan  # implausibly high → fault
    df = df.dropna(subset=["load_mw"])
    return df


def analyze_load(df, freq=None):
    """Per-feeder load summary: peak, min, avg, load factor, reading count, peak time.

    freq=None  → one row per feeder (whole period, as before).
    freq="ME"  → one row per feeder per month (or "D" daily, "W" weekly, etc.).
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # choose the grouping: feeder alone, or feeder + time bucket
    if freq is None:
        grouper = df.groupby("feeder")["load_mw"]
    else:
        df = df.set_index("timestamp").sort_index()
        grouper = df.groupby(["feeder", pd.Grouper(freq=freq)])["load_mw"]

    summary = grouper.agg(["max", "min", "mean", "count"])
    summary["load_factor"] = (summary["mean"] / summary["max"]).round(3)
    summary = summary.round(2)
    summary = summary.rename(
        columns={
            "max": "peak_mw",
            "min": "min_mw",
            "mean": "avg_mw",
            "count": "readings",
        }
    )
    return summary


def print_headline(summary):
    """Print the single most important finding to the screen."""
    # which feeder has the highest peak, and what is it?
    top_feeder = summary["peak_mw"].idxmax()
    top_peak = summary.loc[top_feeder, "peak_mw"]
    top_lf = summary.loc[top_feeder, "load_factor"]

    print("\n" + "=" * 50)
    print(f"  HEADLINE: Highest peak is {top_peak} MW on feeder {top_feeder}")
    print(f"            (load factor {top_lf})")
    print("=" * 50)


def save_report(df, summary, input_filename, output_dir="reports", filter_suffix=""):
    """Save a cleaned CSV, chart PNG, and text summary, with an optional filter suffix in the names."""
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(
        output_dir, make_output_name(input_filename, filter_suffix + "_cleaned")
    )
    df.to_csv(csv_path, index=False)

    png_path = os.path.join(
        output_dir, make_output_name(input_filename, filter_suffix + "_chart", ".png")
    )
    summary[["peak_mw", "avg_mw"]].plot(kind="bar")
    plt.title("Peak vs Average Load per Feeder")
    plt.ylabel("Load (MW)")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close()

    txt_path = os.path.join(
        output_dir, make_output_name(input_filename, filter_suffix + "_summary", ".txt")
    )
    with open(txt_path, "w") as f:
        f.write(f"Load Report for {input_filename}\n")
        f.write(f"Rows after cleaning/filtering: {len(df)}\n\n")
        f.write("Per-feeder summary:\n")
        f.write(summary.to_string())

    return csv_path, png_path, txt_path


def build_prompt(summary):
    """Turn a per-feeder summary table into a prompt for an AI to explain."""
    table_text = summary.to_string()
    prompt = f"""You are an expert power systems analyst. Below is a per-feeder \
electrical load summary (values in MW, load_factor is average/peak).

{table_text}

In 3-4 sentences of plain, professional language, explain what this data reveals \
about the feeders. Identify which feeder is most concerning and why, and mention \
the load factor's practical meaning. Do not just restate the numbers — interpret them."""
    return prompt


def explain_load(summary, use_real_api=False):
    """Generate a plain-language interpretation of a load summary.
    use_real_api=False returns a mock; True calls the Anthropic API."""
    prompt = build_prompt(summary)

    if use_real_api:
        # create a client — it automatically reads ANTHROPIC_API_KEY from the environment
        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return message.content[0].text
    else:
        return (
            "[AI-generated insight — mock mode]\n"
            "This interpretation is a placeholder. Once the Anthropic API key is "
            "configured, this section will contain a live, data-specific analysis "
            "written by Claude based on the summary above."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Clean a load CSV and produce a per-feeder report."
    )
    parser.add_argument("filename", help="the load CSV to process")
    parser.add_argument("--feeder", help="focus on a single feeder (e.g. B)")
    parser.add_argument(
        "--min-load", type=float, help="only include readings at or above this MW value"
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="add an AI-generated plain-language interpretation",
    )
    parser.add_argument(
        "--period",
        default=None,
        help="resample analysis by period: D (daily), W (weekly), ME (monthly)",
    )
    args = parser.parse_args()

    print(f"Processing '{args.filename}'...")
    clean = clean_load_data(args.filename)

    # apply optional filters
    if args.feeder:
        clean = clean[clean["feeder"] == args.feeder.upper()]
        print(f"Filtered to feeder {args.feeder.upper()}: {len(clean)} rows.")

    if args.min_load is not None:
        clean = clean[clean["load_mw"] >= args.min_load]
        print(f"Filtered to load >= {args.min_load} MW: {len(clean)} rows.")

    if clean.empty:
        print("No data left after filtering. Nothing to report.")
        return

    suffix_parts = []
    if args.feeder:
        suffix_parts.append(f"_feeder_{args.feeder.upper()}")
    if args.min_load is not None:
        suffix_parts.append(f"_min{int(args.min_load)}")
    filter_suffix = "".join(suffix_parts)
    print(f"Analyzing {clean.shape[0]} rows.")
    # print the headline result to the screen
    summary = analyze_load(clean, freq=args.period)
    if args.period is None:
        print_headline(summary)
    save_report(clean, summary, args.filename, filter_suffix=filter_suffix)

    if args.explain:
        print("\n--- Interpretation ---")
        print(explain_load(summary, use_real_api=True))

    # print(f"Analyzing {clean.shape[0]} rows.")
    csv_path, png_path, txt_path = save_report(
        clean, summary, args.filename, filter_suffix=filter_suffix
    )

    print("Saved:")
    print(f"  {csv_path}")
    print(f"  {png_path}")
    print(f"  {txt_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
