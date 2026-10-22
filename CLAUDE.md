# CLAUDE.md

## Project overview

ED Module Mapper is a planning tool for Elite Dangerous players who want to compare their owned modules to a target build or engineering requirement list.

The product is intended to answer a single question quickly and clearly: what is still missing before a ship reaches its desired configuration?

## Project status

This repository is currently a lightweight project foundation. The application architecture, module data model, and build logic are still being defined, but the project direction is clear: build a tool that helps players reason about upgrades and requirements in a structured way.

## Core goals

- compare a player’s current modules with a target module set
- highlight missing, incompatible, or under-spec modules
- support build planning by ship, role, and engineering goals
- keep the interface simple enough to use during active gameplay

## Planned repository layout

The project is expected to grow into a small monorepo with separated frontend, backend, and data concerns:

```text
ed_module_mapper/  initial Python package for CSV ingestion and module normalization
frontend/          user interface for inventory and build planning
backend/           API and business logic for comparison rules
data/              module catalog and build metadata, including example inventory CSVs
docs/              architecture notes and product documentation
scripts/           project automation and setup scripts
tests/             validation and scenario-based checks
```

## Current implementation snapshot

The repository now contains the first concrete system in place for handling the owned-module CSV:

- CSV rows are read from `data/example_data.csv`
- blank and `[Unknown]` values are normalized to `None`
- module values are captured as a structured record with a `class_name`, `grade`, `value`, and `location`
- parsing is covered by tests under `tests/`

## Documentation expectations

When new project components are introduced, keep the documentation in sync:

- update the root README when the project scope, architecture, or workflow changes
- document new data sources, rules, or inventory concepts in the project docs
- keep contributor-facing notes aligned with the repo’s actual structure
- maintain a clear separation between product intent and implementation details

## Product principles

- prioritize player clarity over technical complexity
- keep the module comparison logic explicit and easy to validate
- treat the target build and owned inventory as the source of truth for planning
- prefer incremental, testable features over broad speculative work

## Recommended next steps

1. define the module schema and required attributes
2. choose the build comparison rules and edge cases
3. prototype the build planner UI and result presentation
4. add realistic sample data for validating output
5. iterate the workflow around actual player needs

## Working conventions

- keep documentation honest about what is implemented and what is planned
- document assumptions early, especially around module metadata or game rules
- prefer minimal, maintainable architecture while the project is still small
- avoid broad feature work before the build-planning model is stable

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->
## Beads issue tracker

This project uses `bd` for issue tracking. Run `bd prime` for workflow details and session guidance.

### Quick reference

```bash
bd ready
bd show <id>
bd update <id> --claim
bd close <id>
```

### Rules

- use `bd` for all task tracking in this repository
- keep issue status current as work progresses
- do not treat the issue tracker as a substitute for project documentation

## Session completion

When a work session ends, finish the required repo workflow before considering the task complete.

1. File or update any remaining work items.
2. Run the relevant quality checks for the work performed.
3. Close or update the related issue status.
4. Push the branch and confirm it is up to date with the remote.
5. Clean up local state and verify the final result.
<!-- END BEADS INTEGRATION -->
