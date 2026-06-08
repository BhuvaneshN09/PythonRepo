# Receipt Radar

Receipt Radar is a small command-line expense analyzer. It categorizes transactions with transparent rules, summarizes monthly spend, and flags unusual transactions without sending data anywhere.

## Features

- Rule-based transaction categorization
- Monthly category summaries
- Simple anomaly detection using median absolute deviation
- CSV-first workflow with sample data and tests

## Quick start

```bash
python -m pip install -e .
receipt-radar examples/transactions.csv
```

## Development

```bash
python -m pytest
```
