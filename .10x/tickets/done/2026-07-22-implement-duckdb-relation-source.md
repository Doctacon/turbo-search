Status: done
Created: 2026-07-22
Updated: 2026-07-22
Parent: .10x/tickets/done/2026-07-22-add-duckdb-document-relation-support.md
Depends-On: None

# Implement DuckDB relation source

## Scope

Implement `.10x/specs/duckdb-document-relation-indexing.md` in the existing architecture: dataclass source model/union, strict identity helpers, read-only adapter, deterministic batched scan, Markdown materialization, shared `process_corpus()` handoff, plan/crawl CLI arguments and dispatch, compatible summaries, and focused source/CLI/plan-boundary tests.

## Explicit exclusions

Catalog/retrieval changes, final docs, arbitrary SQL/metadata, upstream orchestration, custom chunking/apply, plan schema bumps, and unrelated refactors.

## Acceptance criteria

- Table and view acquisition; canonical and mapped columns; title detection/fallback.
- Strict path, identifier, relation/column, ID, and content validation with actionable failures.
- Stable logical URI/page identity independent of path/order/content hash; no path leakage.
- Empty rows counted; caps applied and reported; bounded deterministic scanning.
- Plan/crawl remain local-only and use existing corpus/plan machinery.
- Saved plan dry-run verifies after source deletion.
- Focused tests cover the source contract and relevant CLI boundary.

## Evidence expectations

Record exact focused test commands/results and inspect artifacts for path absence. Update progress append-only.

## Progress and notes

- 2026-07-22: Opened from user-ratified specification.
- 2026-07-22: Execution started after source inspection. Ratified the exact identity boundary: source IDs match `^[a-z0-9]+(?:-[a-z0-9]+)*$`; relation components and columns match `^[A-Za-z_][A-Za-z0-9_]*$`.
- 2026-07-22: Implemented the bounded read-only DuckDB relation adapter, stable logical identity and Markdown materialization, shared `process_corpus()` handoff, plan/crawl CLI dispatch and summaries, and saved-plan dry-run independence from the source file. Added focused source and CLI/plan-boundary tests. An initial focused run exposed two test expectation/fixture issues; both were corrected before final validation.
- 2026-07-22: Final focused regression command passed: `uv run python -m unittest tests.test_duckdb_relation tests.test_duckdb_relation_cli tests.test_cli tests.test_crawler tests.test_apply_cli` (154 tests, OK; two pre-existing best-effort cleanup warnings). `uv run python -m py_compile src/buoy_search/duckdb_relation.py src/buoy_search/crawler.py src/buoy_search/cli.py src/buoy_search/apply.py tests/test_duckdb_relation.py tests/test_duckdb_relation_cli.py`, `git diff --check`, and the no-staged-files check also passed. Ticket remains active pending parent-owned evidence/review and closure.
- 2026-07-22: Independent review findings were repaired: connection-time DuckDB sandbox settings, UTC-stable ID conversion, escaped scalar fidelity, and expanded contract tests. Focused repair suites passed 23 and 224 tests. Parent-recorded evidence is `.10x/evidence/2026-07-22-duckdb-document-relation-validation.md`; passing re-review is `.10x/reviews/2026-07-22-duckdb-document-relation-review.md`. Acceptance criteria are supported; closed.
- 2026-07-22: Reopened after independent review failed the source child. Bounded repair scope is DuckDB external/extension lockdown before relation access, UTC-stable text conversion, generated frontmatter scalar fidelity, and missing source-boundary regressions; catalog semantics remain excluded.
- 2026-07-22: Repaired the review blockers. The relation connection now applies `enable_external_access=false`, `autoinstall_known_extensions=false`, `autoload_known_extensions=false`, and `allow_community_extensions=false` at connect time, then sets UTC before any relation query. The shared scalar parser now decodes generated JSON-compatible double-quoted values so quotes and backslashes round-trip. Added persisted external-view denial, TIMESTAMPTZ host-timezone stability, scalar fidelity, absent-title fallback, invalid mapped columns, byte/mtime immutability, and identity-change regressions.
- 2026-07-22: Focused repair command `uv run python -m unittest tests.test_duckdb_relation tests.test_duckdb_relation_cli tests.test_chunker -v` passed 23 tests. Expanded regression command `uv run python -m unittest tests.test_duckdb_relation tests.test_duckdb_relation_cli tests.test_chunker tests.test_cli tests.test_crawler tests.test_apply_cli tests.test_catalog tests.test_catalog_cli tests.test_retriever` passed 224 tests in 7.547s with two pre-existing best-effort plan-cleanup warnings. Ticket remains active for fresh independent re-review.

## Blockers

None.
