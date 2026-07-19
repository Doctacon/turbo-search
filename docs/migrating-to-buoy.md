# Migrating from turbo-search to Buoy

Buoy 0.2 changes the product, package, import, command, and default state-root names without renaming existing plans, rows, or remote namespaces.

## Command and Python package

Use `buoy` for new commands:

```bash
uv run buoy --help
```

Buoy 0.4 removes the deprecated `turbo-search` console entry point. Update scripts and commands by replacing only the executable name `turbo-search` with `buoy`; arguments, parser behavior, output, and exit codes are unchanged by this removal. Package upgrades remove the package-owned launcher, but Buoy does not delete user-created shell aliases, copied launchers, wrappers, or caches.

Python imports make a clean break: replace `turbo_search` with `buoy_search`. There is no old import shim.

```bash
uv run python -m buoy_search --help
uv run python -m buoy_search.autoresearch --help
```

## Environment variables

Use `BUOY_EMBEDDING_MODEL` instead of `TURBO_SEARCH_EMBEDDING_MODEL`. Through 0.3, the old model and precision variables are accepted with warnings only when their corresponding `BUOY_*` variables are absent; they are scheduled for removal in 0.4. If an old and new variable are both set differently, Buoy stops rather than guessing.

Turbopuffer credentials and region remain unchanged:

```text
TURBOPUFFER_API_KEY
TURBOPUFFER_REGION
```

`TURBOPUFFER_NAMESPACE` is ignored by retrieval after the remote-catalog cutover. Use repeatable CLI `--namespace` for the sole explicit routing bypass; with no CLI namespace, authenticated remote routing is the default. Plain automatic and explicit retrieval now execute live. Scripts that relied on plain retrieval as a preview must add `--dry-run` (or compatibility alias `--plan`); existing `--live` scripts continue to execute live because the flag remains an accepted no-op. `--live` conflicts with preview flags. Legacy `--auto-route` remains accepted as a compatibility no-op. Local catalog path options and `BUOY_CATALOG_PATH` are removed.

## Local state

New projects default to `.buoy/`. Existing state is never copied, moved, merged, or deleted automatically.

- Only `.buoy` exists, or neither root exists: Buoy uses `.buoy`.
- Only `.turbo-search` exists: Buoy uses it in place and warns.
- Both exist: Buoy stops and asks you to choose with `--state-root`.
- Explicit `--state-root`: that path always wins.

This prevents two local DuckDB ledgers from silently diverging.

## Existing plans and remote data

Schema-supported plans that record `.turbo-search` paths remain valid when that root is selected. The rebrand does not change artifact hashes, deterministic row IDs, existing Turbopuffer namespace names, or applied state history. It does not trigger re-embedding or remote writes by itself.

The GitHub repository and package registry are separate release operations; this guide does not imply either external rename or publication has occurred.

## Legacy local catalog migration

Use `buoy catalog migrate-local --source PATH` to preview an authenticated migration into fixed remote `buoy-routing-catalog-v1`, then add `--approve` only after reviewing classifications and affected IDs. Migration never changes or deletes its source. The exact legacy catalog is deleted only later by the cutover operator after remote and integrated behavior are verified; other `.buoy` state remains untouched.
