from __future__ import annotations

import re
from pathlib import Path

from .models import TargetBuild, TargetModule


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


def _parse_ship_header(line: str) -> tuple[str | None, int | None]:
    match = re.match(r"^\[(?P<ship>.+?)\]\s+\[(?P<grade>[+-]?\d+)\]\s*$", line.strip())
    if not match:
        return None, None

    ship_name = _normalize_optional(match.group("ship"))
    ship_grade = _normalize_int(match.group("grade"))
    return ship_name, ship_grade


def _parse_module_line(line: str) -> tuple[str, str, str | None, str, int | None] | None:
    match = re.match(
        r"^(?P<slot>[A-Za-z0-9]+)\s*:\s*(?P<class_name>\d+[A-Z])(?:/(?P<mount>[A-Z]))?\s+(?P<module_name>.+?)(?:\s+\[(?P<grade>[+-]?\d+)\])?\s*$",
        line.strip(),
    )
    if match is None:
        return None

    slot = match.group("slot")
    class_name = match.group("class_name")
    mount_type = match.group("mount")
    module_name = match.group("module_name").strip()
    grade = _normalize_int(match.group("grade"))
    return slot, class_name, mount_type, module_name, grade


def _parse_effect_line(line: str) -> tuple[str | None, int | None, list[str]]:
    raw_text = line.strip()
    if raw_text.startswith("*:") or raw_text.startswith("**:"):
        raw_text = raw_text[2:].strip()

    if not raw_text:
        return None, None, []

    comma_split = raw_text.split(", ", 1)
    if len(comma_split) == 2:
        engineering_part, experimental_part = comma_split
    else:
        engineering_part, experimental_part = raw_text, ""

    engineering_match = re.search(r"(?P<engineering>.*?)(?:\s+G(?P<grade>[1-5]))?(?:\s+100\.0%)?\s*$", engineering_part)
    engineering_name = None
    engineering_grade = None
    if engineering_match:
        engineering_name = _normalize_optional(engineering_match.group("engineering"))
        engineering_grade = _normalize_int(engineering_match.group("grade")) if engineering_match.group("grade") else None

    experimental_effects: list[str] = []
    if experimental_part:
        experimental_effects = [part.strip() for part in experimental_part.split(";") if part.strip()]

    return engineering_name, engineering_grade, experimental_effects


def parse_target_build_text(text: str) -> TargetBuild:
    ship_name: str | None = None
    ship_grade: int | None = None
    modules: list[TargetModule] = []
    summary: dict[str, str] = {}
    in_summary = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if line.startswith("---"):
            in_summary = True
            continue

        if in_summary:
            match = re.match(r"^(?P<label>[^:]+?)\s*:\s*(?P<value>.+)$", line.strip())
            if match:
                label = match.group("label").strip()
                value = match.group("value").strip()
                summary[label] = value
            continue

        if line.startswith("[") and "]" in line:
            ship_name, ship_grade = _parse_ship_header(line)
            continue

        parsed_module = _parse_module_line(line)
        if parsed_module is not None:
            slot, class_name, mount_type, module_name, grade = parsed_module
            modules.append(
                TargetModule(
                    slot=slot,
                    class_name=class_name,
                    mount_type=mount_type,
                    module_name=module_name,
                    grade=grade,
                    engineering=None,
                    engineering_grade=None,
                    experimental_effects=[],
                    effect_lines=[],
                )
            )
            continue

        if line.startswith("*:") or line.startswith("**:"):
            if not modules:
                continue
            effect_line = line[2:].strip()
            engineering_name, engineering_grade, experimental_effects = _parse_effect_line(effect_line)
            current = modules[-1]
            current.effect_lines.append(effect_line)
            if engineering_name:
                current.engineering = engineering_name
                current.engineering_grade = engineering_grade
            if experimental_effects:
                current.experimental_effects.extend(experimental_effects)
            modules[-1] = current
            continue

    return TargetBuild(ship_name=ship_name, ship_grade=ship_grade, modules=modules, summary=summary)


def load_target_build(path: str | Path) -> TargetBuild:
    target_path = Path(path)
    text = target_path.read_text(encoding="utf-8-sig")
    return parse_target_build_text(text)


def parse_target_build(path: str | Path) -> TargetBuild:
    return load_target_build(path)
