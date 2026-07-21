Status: superseded
Created: 2026-07-12
Updated: 2026-07-18

# DuckDB Applied-State Concurrency and Retention

Superseded by `.10x/decisions/duckdb-only-applied-state-hard-cutover.md`.

## Context

`turbo-search` requires compact local state for incremental Turbopuffer applies and independent concurrent applies to different namespaces. The prior decision selected one embedded DuckDB file per `(site_id, namespace)`, compact apply summaries, and fail-fast same-namespace locking.

The operator now explicitly requires that legacy JSON state be deleted rather than archived after DuckDB migration. The renewed Turbopuffer account has no matching namespaces, so importing legacy rows would incorrectly suppress necessary upserts; retaining the legacy JSON locally is not required.

## Decision

Use embedded DuckDB, not Quack, for applied state. Each `(site_id, namespace)` owns:

```text
.turbo-search/state/<site-id>/<namespace>/state.duckdb
```

Keep one current row ledger and lightweight `apply_runs` summaries indefinitely; do not retain full row snapshots.

Approved apply must take a non-blocking exclusive lock scoped to `(site_id, namespace)`. A contending same-namespace apply fails before remote mutation; different namespaces may apply concurrently.

When a legacy `last-applied.json` is encountered during migration, delete it and initialize the DuckDB ledger empty. Do not archive or import legacy row data. Existing `legacy-json/` artifacts from the superseded migration behavior are also cleanup candidates and must not be treated as active state.

## Alternatives considered

- **Archive legacy JSON:** superseded by explicit operator direction to delete it; it retains local bloat without supporting the new remote account.
- **Import legacy rows:** rejected because the current remote account has no matching rows.
- **One shared DuckDB file:** rejected because independent namespaces would contend on one writer boundary.
- **DuckDB Quack:** rejected for local, different-namespace parallelism; it adds service, token, and beta-protocol operations without making remote writes and local state one transaction.
- **Same-namespace parallel applies:** rejected because remote and local mutations cannot form one distributed transaction.

## Consequences

- Legacy JSON is intentionally unrecoverable after migration; the next approved apply is a full re-upsert for that namespace.
- Existing `legacy-json/` directories become eligible for local cleanup.
- The project needs a corrective migration ticket because the current implementation archives rather than deletes legacy JSON.
- Plan-artifact retention remains a separate unratified cleanup policy.

## Supersedes

`.10x/decisions/superseded/duckdb-applied-state-concurrency.md`
