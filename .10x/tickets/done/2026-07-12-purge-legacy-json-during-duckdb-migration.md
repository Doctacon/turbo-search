Status: done
Created: 2026-07-12
Updated: 2026-07-18
Parent: None
Depends-On: .10x/tickets/done/2026-07-12-compact-duckdb-applied-state-plan.md

# Purge Legacy JSON During DuckDB Migration

## Scope

Supersede archive-and-reset legacy-state migration with delete-and-reset migration. Remove existing `legacy-json/` state artifacts that originated from the superseded behavior.

## Acceptance criteria

- On first state access with `last-applied.json` and no `state.duckdb`, delete the JSON and create an empty DuckDB ledger.
- Do not create or retain `legacy-json/` during migration.
- Safely remove existing `legacy-json/` state artifacts without touching `state.duckdb`, active lock files, plan artifacts, credentials, or Turbopuffer.
- Update user-facing docs and project skill from archive/reset to delete/reset behavior.
- Add regression coverage proving the JSON is deleted, active state is first apply, and no archive remains.

## Explicit exclusions

- Plan-artifact GC/retention.
- Remote namespace/data operations.
- Importing legacy rows or enabling Quack.

## References

- `.10x/specs/compact-duckdb-applied-state.md`
- `.10x/decisions/superseded/duckdb-applied-state-concurrency-and-retention.md`
- `.10x/tickets/done/2026-07-12-local-artifact-retention-and-legacy-state-gc.md`

## Evidence expectations

Targeted migration tests, full suite result, a local-only cleanup report with deleted-path/count summary excluding content, and a review.

## Progress and notes

- 2026-07-12: Opened after the operator explicitly superseded archive behavior and directed legacy JSON deletion.
- 2026-07-12: Implementation authorized; assigned to a single worker.
- 2026-07-12: Replaced archive-and-reset with delete-and-reset migration, updated state tests/docs/project skill, and ran a local-only existing-archive cleanup pass (0 matching directories found). Evidence: `.10x/evidence/2026-07-12-purge-legacy-json-during-duckdb-migration.md`. Focused tests: 39 passed; full suite: 186 passed.
- 2026-07-13: Review found destructive migration ordering. The migration now atomically installs a valid empty temporary DuckDB ledger before deleting legacy JSON; mocked initialization failure leaves JSON intact and no partial database. Focused tests: 13 passed; full suite: 187 passed.
- 2026-07-13: Independent re-review passed.

## Blockers

- None.
