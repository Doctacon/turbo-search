Status: done
Created: 2026-07-22
Updated: 2026-07-22
Parent: None
Depends-On: .10x/tickets/done/2026-07-22-add-duckdb-document-relation-support.md

# Validate public FineWeb DuckDB indexing

## Scope

Run a bounded end-to-end validation using a public FineWeb Parquet sample as upstream data. Outside the repository, materialize a small DuckDB `documents` table with `document_id`, `title`, and `content`; run Buoy plan from the feature worktree; inspect generated pages/plan/chunks for real content and path safety; delete the source database; then run saved-plan apply dry-run.

## Explicit exclusions

No live turbopuffer writes, no repository implementation changes, no dlt, no committed dataset/build artifacts, and no broad performance benchmark.

## Acceptance criteria

- Public data is successfully materialized into DuckDB without Buoy performing ingestion.
- Buoy plans at least one real document and chunk from the `documents` relation.
- Generated review artifacts contain public document content and do not contain the local database path.
- After source deletion, `apply --dry-run --plan` verifies successfully.
- Exact commands, counts, source URL, failures/workarounds, and limits are recorded as evidence.

## Progress and notes

- 2026-07-22: Opened from explicit user request for a public-dataset proof.
- 2026-07-22: Completed against the public FineWeb `sample/10BT/000_00000.parquet` shard using three upstream-materialized documents. Buoy generated three Markdown pages and four chunks with no source database path leakage. After deleting the source database, explicit saved-plan apply dry-run passed integrity verification with no credentials, embeddings, state mutation, or API calls. Exact commands, results, source URL, artifacts, workarounds, and limits are recorded in `.10x/evidence/2026-07-22-public-fineweb-duckdb-indexing.md`.

## Blockers

None.
