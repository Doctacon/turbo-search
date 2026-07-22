Status: done
Created: 2026-07-22
Updated: 2026-07-22
Parent: .10x/tickets/done/2026-07-22-add-duckdb-document-relation-support.md
Depends-On: .10x/tickets/done/2026-07-22-implement-duckdb-relation-source.md

# Integrate database catalog, docs, and regression coverage

## Scope

Implement `.10x/specs/database-catalog-and-retrieval.md`; complete README and indexing documentation required by `.10x/specs/duckdb-document-relation-indexing.md`; extend focused catalog/retrieval/CLI tests; run all relevant regressions and the complete unittest discovery command; repair only regressions caused by this feature.

## Explicit exclusions

New source categories, changed existing namespace defaults, arbitrary metadata, upstream orchestration, unrelated cleanup, releases, pushes, and pull requests.

## Acceptance criteria

- Database catalog cards and strict `duckdb://` validation satisfy the spec without invalidating existing cards.
- `duckdb-` uses document/page defaults with all existing prefixes unchanged.
- README and `docs/indexing.md` document ownership boundary, SQL model, contract, command, read/apply safety, identities, table/view support, chunk multiplicity, and v1 non-goals.
- Focused tests and `uv run python -m unittest discover -s tests -p 'test_*.py'` complete with exact recorded results.

## Evidence expectations

Record commands, counts, failures, and limits. Update progress append-only.

## Progress and notes

- 2026-07-22: Opened from user-ratified specifications; awaits source implementation child.
- 2026-07-22: Dependency completed. Implemented strict database catalog cards and `duckdb://` kind/shape validation, deterministic DuckDB relation semantics, `duckdb-` document/page retrieval defaults, catalog registration previews, manual database card CLI support, README/indexing documentation, and focused regression coverage.
- 2026-07-22: Focused command `uv run python -m unittest tests.test_catalog tests.test_catalog_cli tests.test_retriever tests.test_duckdb_relation tests.test_duckdb_relation_cli` passed 67 tests. The first exact discovery run executed 550 tests and found two feature-caused regressions: the crawl parser no longer failed at argparse when `--base-url` was absent, and README exceeded its enforced 100-line limit. Restored the required crawl `--base-url` compatibility boundary and compacted README without removing the DuckDB contract.
- 2026-07-22: Final exact command `uv run python -m unittest discover -s tests -p 'test_*.py'` passed 550 tests in 62.506s with two expected best-effort plan cleanup warnings and one third-party lxml deprecation warning. Ticket remains active pending parent-owned review/evidence and closure.
- 2026-07-22: Repaired the independent catalog review finding: generated `duckdb://` semantics now require verified low-level `source_kind: duckdb_relation` and reject missing or contradictory kinds without changing manual card validation or non-database inference. Focused command `uv run python -m unittest tests.test_catalog tests.test_catalog_cli` passed 31 tests.
- 2026-07-22: Parent reran the exact full discovery command after all repairs: 560 tests passed in 63.285s. Evidence: `.10x/evidence/2026-07-22-duckdb-document-relation-validation.md`. Independent re-review passed: `.10x/reviews/2026-07-22-duckdb-document-relation-review.md`. Acceptance criteria are supported; closed.

## Blockers

None.
