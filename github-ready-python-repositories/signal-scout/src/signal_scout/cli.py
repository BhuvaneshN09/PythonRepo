from __future__ import annotations

import argparse
from pathlib import Path

from .profiler import profile_csv
from .report import render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Profile a CSV file and write a Markdown quality report.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--report", type=Path, default=Path("signal-scout-report.md"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    profile = profile_csv(args.csv_path)
    args.report.write_text(render_markdown(profile), encoding="utf-8")
    risky = ", ".join(profile.high_risk_columns) or "none"
    print(f"Profiled {profile.rows} rows across {len(profile.columns)} columns")
    print(f"High-risk columns: {risky}")
    print(f"Report written to {args.report}")
    return 0
