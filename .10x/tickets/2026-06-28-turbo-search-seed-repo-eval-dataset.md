Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: .10x/tickets/2026-06-28-repo-search-eval-autoresearch-plan.md
Depends-On: .10x/tickets/2026-06-28-graded-repo-eval-metric.md

# turbo-search Seed Repo Eval Dataset

## Scope

Draft the first graded repository-search eval dataset for the `turbo-search` repository.

The dataset should cover representative user questions for this codebase, including at least:

- GitHub repository ingestion flow;
- plan/apply safety and local-only behavior;
- retrieval command behavior;
- chunking/artifact generation;
- eval/autoresearch behavior once available.

## Acceptance criteria

- Dataset file exists under `src/turbo_search/data/` or another documented data path.
- Dataset contains at least 8 graded cases.
- Each case has at least one grade-3 judgment and at least one additional grade-1/2 supporting or contrast judgment where useful.
- Judgments use `repo_path` for source files in this repo and include reasons.
- Dataset loads through the graded eval loader and is covered by tests.
- Dataset is explicitly marked as seed/draft in documentation or comments if the format permits.

## Explicit exclusions

- Treating this seed dataset as final human-approved ground truth.
- Live GitHub/turbopuffer calls.

## Evidence expectations

- Tests showing the dataset loads and has valid graded judgments.

## References

- `.10x/specs/repo-search-eval-autoresearch.md`
- Current source files under `src/turbo_search/`
- Current tests under `tests/`

## Progress and notes

- 2026-06-28: Added `src/turbo_search/data/turbo_search_repo_search_seed_evals.json` with seed/draft metadata and 10 graded eval cases for the `turbo-search` repository.
- 2026-06-28: Covered GitHub repository ingestion, plan/apply safety and local-only behavior, retrieval command behavior, chunking/artifact generation, and eval/autoresearch behavior.
- 2026-06-28: Added tests in `tests/test_evals.py` for dataset loading, draft metadata, minimum case count, required coverage areas, graded judgment shape, reasons, and repo path existence.
- 2026-06-28: Validation recorded in `.10x/evidence/2026-06-28-turbo-search-seed-repo-eval-dataset-validation.md`.

## Current State

Done. The seed dataset is implemented, explicitly marked as draft/not human-approved, loadable through the graded eval loader, and covered by focused tests.

## Blockers

- None.
