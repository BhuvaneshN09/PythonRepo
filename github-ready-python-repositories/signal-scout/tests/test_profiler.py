from pathlib import Path

from signal_scout import profile_csv
from signal_scout.report import render_markdown


def test_profile_finds_quality_warnings() -> None:
    profile = profile_csv(Path("examples/customers.csv"))

    assert profile.rows == 8
    assert "spend_usd" in profile.high_risk_columns
    assert "signup_date" in profile.high_risk_columns


def test_report_contains_column_summary() -> None:
    profile = profile_csv(Path("examples/customers.csv"))
    report = render_markdown(profile)

    assert "| spend_usd | number | 1 |" in report
    assert "possible numeric outlier" in report
