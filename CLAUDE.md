# CLAUDE.md

## Project Overview

**ED Module Mapper** is a mapping tool for engineering and building ships in Elite Dangerous. It will examine the modules you own, versus the requirements list and provide a detailed plan of how to achieve the required build.

## Tech Stack

| Layer | Technology |
|---|---|

## Directory Structure

```
frontend/        Next.js app (app/, components/, services/, hooks/, store/, styles/)
backend/         FastAPI app
  main.py        Entry point — routers, startup/shutdown hooks
  app/
    api/routers/ HTTP route handlers:
                   events, llm, correlation, anomalies, investigation, report,
                   auth, health, observability, realtime
    core/        Config (settings loaded from config.env)
    db/          DuckDB connection (connection, events, ingest_buffer, query_cache, retention), MinIO client
    observability/ Metrics, tracing, alerting, structured logging
    queue/       Async queue (Redis or in-memory), LLM queue, investigation queue, workers
    schemas/     Pydantic models
    security/    Authentication (JWT/API key), rate limiting, audit logging
    services/    Business logic:
                   event_service, llm_service, ollama_client, realtime,
                   spatial_correlation, negative_space_anomaly,
                   analyst_service, investigation_service, report_generator
agents/          Placeholder — standalone agent processes not yet implemented;
                 agent logic lives in backend/app/services/
ingestion/       Data pipelines
  ais/           Maritime AIS (port 8081)
  celestrak/     Satellite TLE (port 8082)
  opensky/       Aircraft (OpenSky Network)
database/        DuckDB schema (schema.sql) and init script (init.py)
prompts/         LLM prompt templates
docker/          Dockerfiles (frontend, backend, agents) + Prometheus config and Grafana dashboards
scripts/         setup.sh, start.sh, start-local.sh, seed.sh
tests/           Integration and E2E test suite
docs/            Architecture docs
config.example.env   Authoritative config template — keep in sync
config.env           Local secrets — NEVER commit
```

## Guardrails

- **Never commit `config.env`** or any file containing real API keys, credentials, or secrets. `config.example.env` is the authoritative template.
- **Every code change requires doc updates in the same commit.** Review the table below and update every affected file.

### Doc sync checklist

| What changed | Files to update |
|---|---|
| New/removed/renamed backend router | `backend/README.md` architecture diagram · `README.md` API section · `CLAUDE.md` routers list |
| New/removed service in `backend/app/services/` | `CLAUDE.md` services list · `README.md` architecture section |
| New/moved file in `frontend/` | `frontend/README.md` project structure · fix all path references in that file |
| New/removed frontend package | `frontend/README.md` dependencies section |
| Agent logic moved between `agents/` and `backend/app/services/` | `agents/README.md` overview · `README.md` architecture · `CLAUDE.md` directory structure |
| New/removed/renamed env var | `config.example.env` · any README or doc that shows that var |
| New ingestion source | `README.md` data providers table · `docs/ARCHITECTURE.md` · `config.example.env` |
| Changed service port or URL | `README.md` service URLs table · `CLAUDE.md` service URLs · `docs/DEBUGGING.md` |
| New failure mode or tuning knob | `docs/DEBUGGING.md` and/or `docs/PERFORMANCE.md` |
| Top-level directory added or removed | `README.md` directory structure · `CLAUDE.md` directory structure |

- **Dependency/library swaps require a full doc sweep**: run `grep -r "<old-library>" --include="*.md"` across the repo and update every hit before committing.
- **Preserve monorepo structure**: `frontend/`, `backend/`, `agents/`, `database/`, `ingestion/`, `scripts/`, `tests/`. Do not flatten or reorganize directories.
- **Document new services/agents**: Any new ingestion pipeline, agent type, or data source needs an entry in README's data providers table and architecture section.

## Development Workflow

1. `cp config.example.env config.env` then fill in secrets.
2. **All services**: `docker-compose up -d`
3. **Backend only** (local): `cd backend && uvicorn main:app --reload --port 8000`
4. **Frontend only** (local): `cd frontend && npm install && npm run dev`
5. **Ingestion** (local): `source .venv/bin/activate && pip install -r ingestion/requirements.txt && python ingestion/ais/main.py`

Service URLs:
- Frontend: http://localhost:3000
- Backend API / Swagger: http://localhost:8000/docs
- MinIO console: http://localhost:9001
- AIS realtime webhook: http://localhost:8081
- Satellite realtime webhook: http://localhost:8082

## Key Conventions

- All spatial data uses **EPSG:4326 (WGS84)** by default; SRID is always explicit in storage.
- All events normalize to the standard schema: `id`, `timestamp`, `geometry` (GeoJSON), `source`, `event_type`, `properties`, `tags`, `srid`, `agent_flags`.
- Backend responses for spatial queries use **GeoJSON FeatureCollection** format.
- LLM analysis returns structured JSON (anomaly type, confidence, reasoning, recommendations).
- All logs are structured JSON.
- PRs target the `develop` branch; `main` is the stable branch.

## Configuration Notes

- Settings are loaded from `config.env` via `backend/app/core/config.py` (Pydantic settings).
- LLM queue is toggled by `LLM_QUEUE_ENABLED`; workers default to 2.
- Event queue defaults to Redis (`EVENT_QUEUE_TYPE=redis`); falls back to in-memory if Redis is unavailable.
- `CORS_ALLOWED_ORIGINS` is comma-separated; `*` disables CORS restrictions.

## Memory Directives
When you learn an important project fact, decision, or user preference that should persist across sessions, invoke the `memorygraph` tool to store it. Capture entities and relationships so future sessions can recall the context without re-deriving it from scratch.


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
