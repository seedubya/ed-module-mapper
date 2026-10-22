# ED Module Mapper

A planning tool for Elite Dangerous players who want to compare their current ship loadouts against a target build or engineering requirement set.

## Overview

ED Module Mapper is designed to answer a simple but important question: what do I still need to reach my intended build?

The project will help players:

- compare owned modules against a selected build plan
- identify missing, incompatible, or under-spec items
- track progression across multiple ship builds
- reason about engineering and module requirements in one place

## Current status

This repository is currently in the early planning and documentation stage. The codebase is intentionally minimal while the product direction, data model, and feature scope are being defined.

The immediate goal is to establish a clear project foundation for:

- module metadata and inventory modeling
- build requirement definitions
- comparison and recommendation logic
- a user-facing dashboard for build planning

## Planned workflow

1. Define a target ship or role.
2. Load owned modules or import inventory data.
3. Match those modules against required build constraints.
4. Highlight missing modules, engineering gaps, and upgrade priorities.
5. Produce a practical plan for reaching the target configuration.

## Target use cases

- checking whether a current ship build satisfies a known requirement list
- planning a new engineering route for a specific ship loadout
- comparing different module combinations before committing to upgrades
- tracking long-term progression across multiple builds

## Repository structure

At the moment, the repository is intentionally lightweight and serves as the foundation for the project:

- `README.md` — project overview and goals
- `CLAUDE.md` — contributor notes and project conventions
- `AGENTS.md` — repo workflow and issue-tracking instructions
- `docs/module-selection-rules.md` — product rules for selecting owned modules
- `LICENSE` — project licensing information

## Current implementation

The repository now includes the first concrete parsing layer for both owned inventory and the target ship build format.

- `ed_module_mapper/models.py` defines the core `ModuleRecord`, `TargetModule`, and `TargetBuild` data models
- `ed_module_mapper/inventory.py` loads rows from the owned-module CSV and normalizes blanks and `[Unknown]` values to `None`
- `ed_module_mapper/target_build.py` parses the target-build text format in `data/example_input.txt`
- mount type is tracked explicitly (`G`, `F`, or `T`) for hardpoints instead of being hidden inside the class string
- `data/example_data.csv` and `data/example_input.txt` are the canonical sample datasets for development and validation

### CSV import usage

```bash
python -m ed_module_mapper data/example_data.csv
```

This returns a count of parsed module records and establishes the baseline for later build comparison logic.

### Target build parsing usage

```bash
python - <<'PY'
from ed_module_mapper.target_build import load_target_build
build = load_target_build('data/example_input.txt')
print(build.ship_name, build.ship_grade, len(build.modules))
PY
```

This parses a target build such as `[Federal Corvette] [+5]` and its associated hardpoints, utility mounts, and summary stats.

## Planned architecture

The final application is expected to include:

- a frontend for inventory input, build selection, and result summaries
- a backend API for requirement checks and comparison logic
- a data layer storing module definitions and build metadata
- validation and reporting utilities for planning output

## Contribution guidelines

- keep documentation aligned with the actual project direction
- document any new data sources, rules, or build logic clearly
- prefer explicit, player-focused terminology over generic platform language
- treat the module comparison rules as a source of truth for the application

## Roadmap

The project will evolve in stages:

- define the module data model and required attributes
- implement inventory comparison logic using the
  [module selection rules](docs/module-selection-rules.md)
- add build requirement definitions and prioritization rules
- ship a user interface for exploring missing upgrades
- validate the planner against realistic loadout scenarios

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
