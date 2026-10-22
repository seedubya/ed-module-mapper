from pathlib import Path

from ed_module_mapper.target_build import load_target_build


EXAMPLE_INPUT = Path(__file__).resolve().parents[1] / "data" / "example_input.txt"


def test_load_target_build_parses_ship_header_and_first_module():
    build = load_target_build(EXAMPLE_INPUT)

    assert build.ship_name == "Federal Corvette"
    assert build.ship_grade == 5
    assert len(build.modules) > 0

    first = build.modules[0]
    assert first.slot == "H"
    assert first.class_name == "4E"
    assert first.mount_type == "G"
    assert first.module_name == "Burst Laser"
    assert first.grade == 3
    assert first.effect_lines[0].startswith("Efficient")


def test_load_target_build_parses_summary_metrics():
    build = load_target_build(EXAMPLE_INPUT)

    assert build.summary["Mass"] == "1,775.60 T empty"
    assert build.summary["Fuel"] == "32 T"
    assert build.summary["Price"] == "820,186,500 Cr"


def test_load_target_build_handles_varied_module_types():
    build = load_target_build(EXAMPLE_INPUT)

    assert any(module.slot == "BH" and module.module_name == "Reactive Surface Composite" for module in build.modules)
    assert any(module.slot == "PP" and module.module_name == "Power Plant" for module in build.modules)
    assert any(module.slot == "7" and module.module_name == "Bi-Weave Shield Generator" for module in build.modules)
