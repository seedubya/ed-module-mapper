from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleRecord:
    module_name: str
    class_name: str
    modification: str | None
    grade: int | None
    experimental_effect: str | None
    value: int | None
    location: str
