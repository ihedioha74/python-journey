# Load Report Tool

A command-line tool for cleaning, analyzing, and reporting on electrical load data.
Built by an electrical power engineer learning Python — designed around real
power-systems concepts like peak demand, load factor, and per-feeder analysis.

## What It Does

Point it at a messy CSV of load readings and it will:

- **Clean** the data — remove duplicates, fix inconsistent feeder labels, and
  discard impossible values (negatives, sensor faults)
  
- **Analyze** each feeder — peak, minimum, and average demand, load factor,
  reading count, and the exact time each feeder peaked
  
- **Visualize** — a peak-vs-average bar chart per feeder

- **Report** — saves a cleaned CSV, a chart image, and a text summary,
  plus prints a headline result to the screen

## Requirements

- **Python 3** (tested with Anaconda)

- **pandas** — data loading, cleaning, and analysis

- **NumPy** — numerical operations

- **matplotlib** — charts

## Usage

Run a full report on a data file:

```
python load_report.py messy_meter_data.csv
```

Focus on a single feeder:

```
python load_report.py messy_meter_data.csv --feeder B
```

Only include readings at or above a threshold (MW):

```
python load_report.py messy_meter_data.csv --min-load 120
```

Combine filters — e.g. feeder D's heavy-load periods:

```
python load_report.py messy_meter_data.csv --feeder D --min-load 100
```

## About this project

This is a python programming journey of an Electrical Power Systems Engineer. 
I started from a zero level without a GitHub account. The goal of this project 
is to learn how to use python in solving any type of Electrical Power
Engineering problem. 

## Output

Each run saves three files to a `reports/` folder, named after the input and any filters applied:

- `<name>_cleaned.csv` — the cleaned dataset
- `<name>_chart.png` — a peak-vs-average bar chart
- `<name>_summary.txt` — the full per-feeder analysis
