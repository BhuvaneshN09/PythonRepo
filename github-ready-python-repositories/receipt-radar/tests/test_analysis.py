from decimal import Decimal
from pathlib import Path

from receipt_radar import categorize, load_transactions, monthly_summary, unusual_transactions


def test_categorizes_merchants() -> None:
    assert categorize("Metro Grocery") == "groceries"
    assert categorize("CloudHost") == "software"
    assert categorize("Unknown Shop") == "other"


def test_monthly_summary_totals_by_category() -> None:
    transactions = load_transactions(Path("examples/transactions.csv"))
    summary = monthly_summary(transactions)

    assert summary["2026-01"]["groceries"] == Decimal("117.52")
    assert summary["2026-01"]["software"] == Decimal("318.00")


def test_detects_unusual_transaction() -> None:
    transactions = load_transactions(Path("examples/transactions.csv"))
    unusual = unusual_transactions(transactions)

    assert [transaction.merchant for transaction in unusual] == ["CloudHost"]
