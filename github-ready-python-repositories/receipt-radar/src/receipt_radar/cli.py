from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import load_transactions, monthly_summary, unusual_transactions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze expenses from a transaction CSV.")
    parser.add_argument("csv_path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    transactions = load_transactions(args.csv_path)
    summary = monthly_summary(transactions)
    print("Monthly spend")
    for month, categories in summary.items():
        print(f"\n{month}")
        for category, amount in sorted(categories.items()):
            print(f"  {category:<10} ${amount:>8}")
    unusual = unusual_transactions(transactions)
    if unusual:
        print("\nUnusual transactions")
        for transaction in unusual:
            print(f"  {transaction.date} {transaction.merchant}: ${transaction.amount}")
    return 0
