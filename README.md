# 📊 Bajeti AI — Kenya County Budget Tracker

> *Bajeti* (Swahili) = budget

AI-powered tool that tracks Kenya county government budgets, compares allocations vs actual spending, and explains what it means for citizens — in plain Swahili.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bajeti.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Matters

Kenya's 47 county governments receive billions in equitable share allocations annually. Citizens have a constitutional right to this information. Bajeti AI translates government budget data into Swahili explanations that any citizen can understand — what was promised, what was spent, and what wasn't done.

## Features

| Feature | Description |
|---------|-------------|
| 📥 Budget Data | Kenya Open Data API (opendata.go.ke) |
| 📊 Visual Analysis | Allocation vs spending charts per sector |
| 🤖 AI Explanation | Plain Swahili summary of budget performance |
| 🚨 Underspending | Flag sectors where funds were unused |
| 📱 Export | Share report via WhatsApp/SMS |

## Data Sources

- Kenya Open Data Portal (opendata.go.ke) — public domain
- Controller of Budget Kenya annual reports
- National Treasury county allocations

## Quickstart

```bash
git clone https://github.com/gabrielmahia/bajeti-ai
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer

Data from public sources. Not affiliated with any government entity. For civic education only.
