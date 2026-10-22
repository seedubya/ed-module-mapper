from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModuleRecord:
    module_name: str
    class_name: str
    modification: str | None
    grade: int | None
    experimental_effect: str | None
    value: int | None
    location: str


@dataclass
class TargetModule:
    slot: str
    class_name: str
    mount_type: str | None = None
    module_name: str = ""
    grade: int | None = None
    engineering: str | None = None
    engineering_grade: int | None = None
    experimental_effects: list[str] = field(default_factory=list)
    effect_lines: list[str] = field(default_factory=list)


@dataclass
class TargetBuild:
    ship_name: str | None
    ship_grade: int | None
    modules: list[TargetModule]
    summary: dict[str, str] = field(default_factory=dict)
