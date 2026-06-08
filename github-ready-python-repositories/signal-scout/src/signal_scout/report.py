from __future__ import annotations

from .profiler import DatasetProfile


def render_markdown(profile: DatasetProfile) -> str:
    lines = [
        "# Data Quality Report",
        "",
        f"Rows: **{profile.rows}**",
        f"Columns: **{len(profile.columns)}**",
        "",
        "| Column | Type | Missing | Unique | Examples | Warnings |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for column in profile.columns:
        examples = ", ".join(column.examples) or "-"
        warnings = "; ".join(column.warnings) or "-"
        lines.append(
            f"| {column.name} | {column.inferred_type} | {column.missing} | "
            f"{column.unique} | {examples} | {warnings} |"
        )
    lines.append("")
    return "\n".join(lines)
