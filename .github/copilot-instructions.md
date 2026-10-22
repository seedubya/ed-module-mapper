# Copilot Instructions

## Non-negotiable rules

- **If an `AGENTS.md` file is present (repo root or any parent directory of the files you're editing), read it and follow its instructions.** It defines the issue-tracking workflow and session-completion requirements and takes precedence over ad-hoc task management.
- **Never commit `config.env`** or any file containing real API keys, credentials, or secrets.
- **Every code change must include the relevant doc updates in the same commit.** Do not commit code without updating docs.
- **Preserve the monorepo layout**: Do not flatten or reorganize.

---

## Documentation files that must stay in sync

These files must be reviewed and updated whenever their relevant layer changes:

| File | Update when… |
|---|---|
| `README.md` | Any layer changes: new routes, new services, new ingestion sources, new env vars, changed ports, changed directory layout |
| `CLAUDE.md` | Tech stack changes, new routers/services added to backend, agents/ directory changes, key convention changes |
| `config.example.env` | Any env var is added, removed, or renamed |
| `docs/ARCHITECTURE.md` | Data flow changes, new components, new storage layers, new agent types |
| `docs/DEBUGGING.md` | New failure modes, new config knobs referenced in troubleshooting, new services that could break |
| `docs/PERFORMANCE.md` | New indexes, new caching layers, new batching strategies, new tuning knobs |
| `backend/README.md` | New routers added to `backend/app/api/routers/`, router prefix changes, new services in `backend/app/services/`, dependency changes |
| `frontend/README.md` | New/removed components in `frontend/components/`, new/removed hooks in `frontend/hooks/`, new/removed files in `frontend/services/` or `frontend/store/`, package.json dependency changes |
| `agents/README.md` | Any change to what lives in `agents/` vs `backend/app/services/` |
| `database/README.md` | Schema changes in `database/schema.sql`, new tables, index changes |

---

## What to check for each type of change

### Adding a backend router or service
2. Update `README.md` — API endpoints section and/or Architecture section.
3. Update `CLAUDE.md` — routers list in Directory Structure.
4. If the service has new config, update `config.example.env` and `README.md` env vars table.

### Adding or moving frontend files
1. If a new component directory is added under `frontend/components/`, add it to the structure section in `frontend/README.md`.
2. If a new hook is added under `frontend/hooks/`, add it to the hooks list in `frontend/README.md`.
3. If files move between `frontend/lib/` ↔ `frontend/services/` ↔ `frontend/store/`, update all path references in `frontend/README.md`.
4. If a package is added or removed from `package.json`, update the dependencies section in `frontend/README.md`.

### Moving agent logic between `agents/` and `backend/app/services/`
1. Update `agents/README.md` — the overview must accurately state where the logic lives.
2. Update `README.md` — Architecture section component descriptions.
3. Update `CLAUDE.md` — directory structure and services list.

### Adding a new ingestion source
1. Add a row to the Data Providers table in `README.md`.
2. Add an entry to `docs/ARCHITECTURE.md`.
3. Add any new env vars to `config.example.env`.

### Adding or renaming env vars
1. Update `config.example.env` (authoritative template).
2. Update any env var tables or examples in `README.md`, `backend/README.md`, `agents/README.md`, `frontend/README.md` that reference those vars.

### Changing directory or file structure
1. Update the directory tree in `README.md`.
2. Update the directory tree in `CLAUDE.md`.
3. Search all `*.md` files for the old path and update every reference.

---

## Dependency / library swaps

When a library is replaced (e.g. swapping a mapping or state-management library):
1. `grep -r "<old-library-name>" --include="*.md"` across the whole repo.
2. Update every result before committing.
3. Update the tech stack table in `CLAUDE.md` and `frontend/README.md` (or relevant layer README).
