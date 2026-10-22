from __future__ import annotations

import csv
from pathlib import Path

from .models import ModuleRecord


def _normalize_optional(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    if cleaned == "" or cleaned == "[Unknown]":
        return None
    return cleaned


def _normalize_int(value: str | None) -> int | None:
    if value is None:
        return None

    cleaned = value.strip()
    if cleaned in {"", "[Unknown]"}:
        return None

    return int(cleaned.replace(",", ""))


def load_module_inventory(csv_path: str | Path) -> list[ModuleRecord]:
    path = Path(csv_path)

    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        rows: list[ModuleRecord] = []

        for row in reader:
            raw_grade = row.get("Grade")
            rows.append(
                ModuleRecord(
                    module_name=row.get("Module", "").strip(),
                    class_name=row.get("Class", "").strip(),
                    modification=_normalize_optional(row.get("Modification")),
                    grade=_normalize_int(raw_grade) if raw_grade not in (None, "") else None,
                    experimental_effect=_normalize_optional(row.get("Exp. effect")),
                    value=_normalize_int(row.get("Value")),
                    location=row.get("Location", "").strip(),
                )
            )

    return rows


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Load ED Module Mapper inventory CSV files.")
    parser.add_argument("csv_path", type=Path, help="Path to the module inventory CSV file")
    args = parser.parse_args()

    records = load_module_inventory(args.csv_path)
    print(f"Loaded {len(records)} module records from {args.csv_path}")


if __name__ == "__main__":
    main()
