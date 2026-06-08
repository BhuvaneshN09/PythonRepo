from __future__ import annotations

import csv
import datetime as dt
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Iterable


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    inferred_type: str
    missing: int
    unique: int
    examples: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class DatasetProfile:
    rows: int
    columns: tuple[ColumnProfile, ...]

    @property
    def high_risk_columns(self) -> tuple[str, ...]:
        return tuple(column.name for column in self.columns if column.warnings)


def profile_csv(path: str | Path) -> DatasetProfile:
    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    columns = tuple(_profile_column(name, [row.get(name, "") for row in rows]) for name in reader.fieldnames or [])
    return DatasetProfile(rows=len(rows), columns=columns)


def _profile_column(name: str, values: Iterable[str]) -> ColumnProfile:
    cleaned = [value.strip() for value in values]
    present = [value for value in cleaned if value]
    missing = len(cleaned) - len(present)
    inferred_type = _infer_type(present)
    warnings = list(_quality_warnings(name, cleaned, inferred_type))
    examples = tuple(value for value, _ in Counter(present).most_common(3))
    return ColumnProfile(
        name=name,
        inferred_type=inferred_type,
        missing=missing,
        unique=len(set(present)),
        examples=examples,
        warnings=tuple(warnings),
    )


def _infer_type(values: list[str]) -> str:
    if not values:
        return "empty"
    checks = (("integer", _is_int), ("number", _is_float), ("date", _is_date))
    for label, check in checks:
        if sum(1 for value in values if check(value)) / len(values) >= 0.8:
            return label
    return "text"


def _quality_warnings(name: str, values: list[str], inferred_type: str) -> Iterable[str]:
    present = [value for value in values if value]
    if values and (len(values) - len(present)) / len(values) >= 0.15:
        yield "missing values above 15%"
    if inferred_type in {"integer", "number"}:
        numbers = [float(value) for value in present if _is_float(value)]
        if _has_outlier(numbers):
            yield "possible numeric outlier"
    if "date" in name.lower() and any(value and not _is_date(value) for value in values):
        yield "date-like column has invalid dates"


def _has_outlier(numbers: list[float]) -> bool:
    if len(numbers) < 4:
        return False
    center = median(numbers)
    deviations = [abs(value - center) for value in numbers]
    mad = median(deviations) or 1.0
    return any(abs(value - center) / mad > 12 for value in numbers)


def _is_int(value: str) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    return True


def _is_float(value: str) -> bool:
    try:
        number = float(value)
    except ValueError:
        return False
    return math.isfinite(number)


def _is_date(value: str) -> bool:
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True

