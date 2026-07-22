Status: done
Created: 2026-07-22
Updated: 2026-07-22
Parent: None
Depends-On: .10x/tickets/done/2026-07-22-add-duckdb-document-relation-support.md

# Clarify external-backed DuckDB views

## Scope

Make the read-only DuckDB relation boundary practical for daily use: document that supported relations must be self-contained in the database because external access and extension loading are disabled, and convert failures from external-backed views into an actionable concise error that recommends materializing the final relation into the database upstream.

## Explicit exclusions

Do not enable external access or extension loading, weaken the plan/crawl safety boundary, add arbitrary SQL, or add metadata mapping.

## Acceptance criteria

- README and indexing documentation distinguish ordinary in-database views from views that read external files/databases or require extensions.
- Planning an external-backed view fails clearly and recommends materializing a table/relation upstream.
- Existing missing-relation and malformed-source errors remain actionable.
- Focused tests and the full suite pass.

## Evidence expectations

Record exact commands/results and independent review. Update progress append-only.

## Progress and notes

- 2026-07-22: Opened from explicit user authorization before merge.
- 2026-07-22: Added narrow classification of DuckDB's external-filesystem and external-extension security diagnostics so external-backed views recommend upstream in-database materialization while unrelated DuckDB errors retain their original diagnostics. Documented the self-contained relation boundary in README and indexing guidance. Added adapter and CLI regressions, including missing-relation diagnostic preservation. Focused tests passed: `uv run python -m unittest tests.test_duckdb_relation tests.test_duckdb_relation_cli` (19 tests). Full discovery passed: `uv run python -m unittest discover -s tests -p 'test_*.py'` (561 tests). Ticket remains open for parent evidence/review and closure.
- 2026-07-22: Repaired review finding by requiring DuckDB `PermissionException` in addition to the exact security marker before rewriting an error as an external dependency failure. Added a self-contained-view regression proving an unrelated `ConversionException` containing the filesystem marker retains its original diagnostic, plus synthetic `PermissionException` coverage for the extension marker without enabling or installing an extension. Focused tests passed: `uv run python -m unittest tests.test_duckdb_relation tests.test_duckdb_relation_cli` (21 tests), and the three classification regressions passed independently with verbose output. `git diff --check` passed. Optional targeted Ruff validation could not run because Ruff is not installed in the environment.
- 2026-07-22: Parent evidence `.10x/evidence/2026-07-22-external-backed-view-guidance-validation.md` and passing review `.10x/reviews/2026-07-22-external-backed-view-guidance-review.md` support all acceptance criteria. Closed pending aggregate branch integration validation.

## Blockers

None.
