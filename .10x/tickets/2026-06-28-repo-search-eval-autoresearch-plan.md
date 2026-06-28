Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: None
Depends-On: None

# Repo Search Eval Autoresearch Plan

## Scope

Coordinate the first implementation slice for repository search quality measurement and config-only autoresearch.

The slice is governed by `.10x/specs/repo-search-eval-autoresearch.md` and includes:

1. graded composite metrics for repository retrieval;
2. an initial drafted `turbo-search` repo eval dataset;
3. a one-shot config-only autoresearch runner/program scaffold;
4. docs and validation.

## Child tickets

- `.10x/tickets/2026-06-28-graded-repo-eval-metric.md`
- `.10x/tickets/2026-06-28-turbo-search-seed-repo-eval-dataset.md`
- `.10x/tickets/2026-06-28-config-autoresearch-runner.md`
- `.10x/tickets/2026-06-28-repo-eval-autoresearch-docs-validation.md`

## Acceptance criteria

- All child tickets are done or explicitly cancelled with rationale.
- Composite metric behavior is implemented and covered by tests.
- The initial `turbo-search` eval dataset is present and loadable.
- Config-only one-shot autoresearch can run without source mutation in dry-run/test mode.
- Live eval validation, if run, is retrieval-only and records evidence without secrets.

## Evidence expectations

- Test command output for focused and full relevant tests.
- If live eval-only validation is run, evidence with command shape, namespace, counts, and score but no secrets.
- Final summary mapping child acceptance to evidence.

## References

- Governing spec: `.10x/specs/repo-search-eval-autoresearch.md`
- Existing eval harness: `src/turbo_search/evals.py`
- Existing retrieval client: `src/turbo_search/retriever.py`
- Current CLI eval command: `src/turbo_search/cli.py`
- Inspired by: `https://github.com/karpathy/autoresearch`
- Inspired by: `https://github.com/z3z1ma/10x/tree/main/autoresearch`

## Progress and notes

- 2026-06-28: User selected `turbo-search` as first repo target, authorized assistant-drafted graded labels, allowed live eval-only validation, and chose metric + runner as first implementation slice.
- 2026-06-28: Completed child `.10x/tickets/2026-06-28-graded-repo-eval-metric.md`; evidence: `.10x/evidence/2026-06-28-graded-repo-eval-metric-validation.md`.
- 2026-06-28: Completed child `.10x/tickets/2026-06-28-turbo-search-seed-repo-eval-dataset.md`; evidence: `.10x/evidence/2026-06-28-turbo-search-seed-repo-eval-dataset-validation.md`.
- 2026-06-28: Completed child `.10x/tickets/2026-06-28-config-autoresearch-runner.md`; evidence: `.10x/evidence/2026-06-28-config-autoresearch-runner-validation.md`.
- 2026-06-28: Completed child `.10x/tickets/2026-06-28-repo-eval-autoresearch-docs-validation.md`; evidence: `.10x/evidence/2026-06-28-repo-eval-autoresearch-docs-validation.md`.
- 2026-06-28: Reviewer found no initial blockers; two minor findings were fixed. Follow-up review surfaced and verified a live `repo_path` normalization blocker fix. Review: `.10x/reviews/2026-06-28-repo-eval-autoresearch-review.md`; fix evidence: `.10x/evidence/2026-06-28-repo-eval-autoresearch-review-minor-fixes.md`, `.10x/evidence/2026-06-28-live-retrieval-repo-path-normalization-validation.md`.
- 2026-06-28: Final validation passed after follow-up fix: `uv run python -m unittest tests.test_autoresearch tests.test_evals tests.test_cli tests.test_retriever` ran 44 tests OK; `uv run python -m unittest discover tests` ran 121 tests OK; `git diff --check` reported no whitespace errors; fixture experiment returned `passed 100.0 10 10 False`. Evidence: `.10x/evidence/2026-06-28-repo-search-eval-autoresearch-final-validation.md`.
- 2026-06-28: After user expanded scope to live writes/namespaces, completed live index and eval follow-up in `.10x/tickets/2026-06-28-live-turbo-search-repo-index-and-eval.md`; evidence: `.10x/evidence/2026-06-28-live-turbo-search-repo-index-and-eval.md`.

## Current State

Done. The first implementation slice is complete: graded repo search metrics, seed `turbo-search` dataset, one-shot config-only autoresearch runner/program, fixture sample, docs, tests, evidence, and review are in place.

## Blockers

- None. Live repository-quality validation was completed after explicit user authorization for writes/namespaces.
