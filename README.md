# Grid Load Intelligence — an AI-powered energy-data platform

A full-stack web application that ingests electrical grid load data, serves it through a
REST API, and uses a large language model to turn raw numbers into **plain-language
engineering analysis** — the kind of interpretation a power systems analyst would write.

Built end to end by an electrical power engineer: from the database and the cleaning
pipeline, through the API and the AI layer, to a deployed, public web dashboard.

---

## ▶️ Live demo

| | Link | What it is |
|---|---|---|
| **Dashboard** | https://python-journey-1.onrender.com | The visual app — pick a feeder, see the metrics, get an AI analysis |
| **API** | https://python-journey-gzrx.onrender.com | The REST backend serving data + AI over HTTP |
| **API docs** | https://python-journey-gzrx.onrender.com/docs | Interactive, auto-generated API documentation |

> ⏱️ **Note:** both services run on a free tier that sleeps after inactivity, so the
> first load may take 30–60 seconds to wake. After that it's fast.

**Try this:** open the dashboard, choose a feeder, and click **“Explain feeder …”**.
The written analysis you get back is generated live by Claude, from the feeder's real
statistics — including things like peak-to-average ratio, load factor, and voltage-regulation
implications.

---

## Why this project is different

Most data dashboards show you *numbers*. This one **explains what the numbers mean for
operating the grid.**

When it reports a feeder peaking at 154 MW against a 75 MW average, the AI layer doesn't
just restate that — it flags the 2:1 peak-to-average ratio, reasons about capacity reserves
and load management, and even notices when a suspiciously low minimum reading looks like a
*data-quality* issue rather than a real load. That's the difference between a chart and an
analyst.

This is deliberately built at the intersection of two skill sets that rarely sit together:

- **Power systems engineering** — the domain knowledge to know *which* numbers matter, what a
  load factor implies, and when a reading is physically implausible.
- **Software engineering** — the ability to actually ship it: a clean architecture, automated
  tests, and a live cloud deployment.

> **On the data:** the app runs on *representative demonstration data* modelled on real
> feeder load profiles — enough to exercise every feature end to end. The value on offer is
> the **architecture and analysis capability**, which transfers directly to a client's or
> employer's real measured data.

---

## Architecture

A cleanly decoupled three-layer system — each layer owns one job and talks only to its neighbour.

```
  ┌─────────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
  │   dashboard.py      │ ──▶ │       api.py         │ ──▶ │      grid.db      │
  │   (presentation)    │     │   (backend + AI)     │     │      (data)       │
  │                     │ ◀── │                      │ ◀── │                   │
  │  Streamlit UI       │     │  FastAPI + Claude    │     │  SQLite           │
  └─────────────────────┘     └──────────────────────┘     └───────────────────┘
     shows things             owns all logic &              stores & aggregates
     to a human               the AI analysis               (self-seeds on deploy)
```

- **`grid.db`** — SQLite store of cleaned load readings. On a fresh deploy it **provisions
  itself** from a committed seed, so the app stands up from nothing with no manual setup.
- **`api.py`** — a FastAPI service. Serves per-feeder summaries over HTTP and hosts the
  `/explain` endpoint, which runs a feeder's statistics through Claude and returns a written
  analysis. The single source of truth; every client comes through here.
- **`dashboard.py`** — a Streamlit frontend that owns no data or logic. It *asks* the API for
  every number and renders the result — metrics, an on-demand AI analysis, and a comparison chart.

The layers are independent: the database could be swapped for PostgreSQL, or the UI replaced
with a mobile app, without touching the others.

---

## Engineering practices

This is built like production software, not a throwaway script:

- **Automated tests** (`pytest`) covering the data-cleaning guarantees — case normalisation,
  out-of-range removal, duplicate handling, and correct error-raising.
- **Formatted & linted** with `black` and `ruff`, configured via `pyproject.toml`.
- **Secrets managed properly** — the AI API key is injected as an environment variable, never
  committed to the repository.
- **Self-provisioning data** — the deployed app builds its own database on startup, idempotently.
- **Environment-aware configuration** — the same code runs locally and in the cloud, switching
  behaviour via environment variables.
- **Version-controlled throughout** — every step committed, with a clear history.

---

## Tech stack

**Backend:** Python · FastAPI · SQLite · SQL
**Frontend:** Streamlit
**AI:** Anthropic Claude (via the Messages API)
**Data:** pandas · NumPy
**Quality:** pytest · black · ruff
**Deployment:** Render (two independent web services) · Git / GitHub

---

## Running it locally

```bash
# 1. clone and enter the project
git clone https://github.com/ihedioha74/python-journey.git
cd python-journey

# 2. create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux

# 3. install dependencies
pip install -r requirements.txt

# 4. set your Anthropic API key (for the AI endpoint)
export ANTHROPIC_API_KEY="sk-ant-..."

# 5. run the API (terminal 1)
uvicorn api:app --reload

# 6. run the dashboard (terminal 2)
streamlit run dashboard.py
```

The dashboard defaults to the local API. To point it at a different API, set `API_BASE`.

---

## About

I'm **Emmanuel Uchenna Ihedioha**, an electrical power engineer who builds software for
energy-data problems. This project reflects how I like to work: real engineering judgment,
made practical and shippable.

I'm open to opportunities — consulting or roles — where power-systems domain knowledge and
software delivery meet. Feel free to explore the live demo above, browse the code, or reach out.

📧 **ihedioha@gmail.com**  ·  💻 **[github.com/ihedioha74](https://github.com/ihedioha74)**
