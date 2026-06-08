# Signal Scout

Signal Scout is a zero-dependency CSV profiling CLI for quick data quality checks. It scans a dataset, infers column types, highlights missing values, detects numeric outliers, and writes a clean Markdown report you can share in an issue, pull request, or portfolio walkthrough.

## Why it is useful

- Works with only the Python standard library
- Produces human-readable reports for messy CSV files
- Includes deterministic tests and sample data
- Ships as an installable CLI package

## Quick start

```bash
python -m pip install -e .
signal-scout examples/customers.csv --report report.md
```

## Example output

```text
Profiled 8 rows across 5 columns
High-risk columns: spend_usd, signup_date
Report written to report.md
```

## Development

```bash
python -m pytest
python -m signal_scout examples/customers.csv --report report.md
```
