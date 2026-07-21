Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: .10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md
Depends-On: .10x/tickets/done/2026-06-28-graded-repo-eval-metric.md, .10x/tickets/done/2026-06-28-turbo-search-seed-repo-eval-dataset.md, .10x/tickets/done/2026-06-28-config-autoresearch-runner.md

# Repo Eval Autoresearch Docs and Validation

## Scope

Document and validate the first repo search composite eval and config-only autoresearch workflow.

## Acceptance criteria

- README or docs explain the composite score, dataset format, and one-shot autoresearch command.
- CLI/help text, if changed, accurately states dry-run vs live behavior.
- Focused and full relevant tests pass.
- Optional live eval-only validation is run only against an already-applied namespace and records no secrets.
- Evidence maps acceptance criteria to test/live outputs.

## Explicit exclusions

- Live writes/deletes/namespaces.
- Treating seed eval labels as final ground truth without user review.

## Evidence expectations

- `unittest` output.
- If live eval is run: command shape, namespace, total cases, component metrics, composite score, and limits.

## References

- `.10x/specs/repo-search-eval-autoresearch.md`
- `.10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md`

## Progress and notes

- 2026-06-28: Added README documentation for the composite repo search score, graded dataset format, seed dataset caveat, fixture sample command, and live-mode safety boundary.
- 2026-06-28: Added workflow docs for repository composite evals and config-only one-shot autoresearch.
- 2026-06-28: Added `autoresearch/experiments/repo-search-fixture-baseline.json`, a safe fixture-mode-only sample experiment.
- 2026-06-28: Updated `autoresearch/program.md` to point at the checked-in fixture baseline command.
- 2026-06-28: Added `tests/test_autoresearch.py` coverage that runs the checked-in fixture experiment without live calls.
- 2026-06-28: Ran focused tests: `uv run python -m unittest tests.test_autoresearch tests.test_evals tests.test_cli tests.test_retriever` passed, 42 tests.
- 2026-06-28: Ran full tests: `uv run python -m unittest discover tests` passed, 119 tests.
- 2026-06-28: Ran the sample fixture experiment; result passed with score 100.00000000000001, 10/10 cases, `api_calls: False`.
- 2026-06-28: Checked local applied-state namespaces; no already-applied `turbo-search` GitHub repository namespace was present, so live eval validation was not run.
- 2026-06-28: Validation recorded in `.10x/evidence/2026-06-28-repo-eval-autoresearch-docs-validation.md`.

## Current State

Done. Documentation, safe sample experiment, focused sample test coverage, and local validation are complete.

## Blockers

- None for docs/local validation.
- Live repository eval remains pending until a `turbo-search` GitHub repository namespace is applied through the approved plan/apply workflow; live writes/namespaces are out of scope for this ticket.
