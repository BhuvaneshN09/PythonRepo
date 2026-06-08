from __future__ import annotations

import csv
import datetime as dt
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from statistics import median

RULES = {
    "groceries": ("grocery", "market", "metro"),
    "transport": ("transit", "uber", "train"),
    "software": ("cloud", "host", "github", "openai"),
    "coffee": ("coffee", "java", "cafe"),
}


@dataclass(frozen=True)
class Transaction:
    date: dt.date
    merchant: str
    amount: Decimal

    @property
    def month(self) -> str:
        return self.date.strftime("%Y-%m")


def load_transactions(path: str | Path) -> list[Transaction]:
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return [
            Transaction(
                date=dt.date.fromisoformat(row["date"]),
                merchant=row["merchant"].strip(),
                amount=Decimal(row["amount"]),
            )
            for row in reader
        ]


def categorize(merchant: str) -> str:
    normalized = merchant.lower()
    for category, needles in RULES.items():
        if any(needle in normalized for needle in needles):
            return category
    return "other"


def monthly_summary(transactions: list[Transaction]) -> dict[str, dict[str, Decimal]]:
    summary: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
    for transaction in transactions:
        summary[transaction.month][categorize(transaction.merchant)] += transaction.amount
    return {month: dict(categories) for month, categories in sorted(summary.items())}


def unusual_transactions(transactions: list[Transaction]) -> list[Transaction]:
    if len(transactions) < 4:
        return []
    amounts = [float(transaction.amount) for transaction in transactions]
    center = median(amounts)
    mad = median(abs(amount - center) for amount in amounts) or 1.0
    return [transaction for transaction in transactions if abs(float(transaction.amount) - center) / mad > 8]
