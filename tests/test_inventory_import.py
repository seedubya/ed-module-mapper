from pathlib import Path

from ed_module_mapper.inventory import load_module_inventory


def test_load_module_inventory_reads_rows_and_normalizes_values():
    rows = load_module_inventory(Path(__file__).resolve().parents[1] / "data" / "example_data.csv")

    assert len(rows) > 0

    first = rows[0]
    assert first.module_name == "Auto Field-Maintenance Unit"
    assert first.class_name == "4A"
    assert first.modification is None
    assert first.grade is None
    assert first.experimental_effect is None
    assert first.value == 123456
    assert first.location == "Used on Throbbing Gristle [AX]"


def test_load_module_inventory_treats_unknown_as_blank():
    rows = load_module_inventory(Path(__file__).resolve().parents[1] / "data" / "example_data.csv")

    assert any(
        row.module_name == "Sirius AX Missile Rack [Fixed]"
        and row.experimental_effect is None
        for row in rows
    )
