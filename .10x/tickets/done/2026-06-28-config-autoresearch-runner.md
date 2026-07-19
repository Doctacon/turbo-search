Status: done
Created: 2026-06-28
Updated: 2026-06-28
Parent: .10x/tickets/done/2026-06-28-repo-search-eval-autoresearch-plan.md
Depends-On: .10x/tickets/done/2026-06-28-graded-repo-eval-metric.md

# Config-only Autoresearch Runner

## Scope

Implement the first one-shot config-only autoresearch surface for repository search evals.

The runner should be inspired by `karpathy/autoresearch` and `z3z1ma/10x/autoresearch`, but scoped to this project:

- human-owned program document;
- fixed evaluator;
- one registered experiment per run;
- one metric and component metrics;
- raw artifacts and report output;
- no source-code mutation during trials.

## Acceptance criteria

- A human-owned `autoresearch/program.md` or equivalent describes the config-only loop, editable surfaces, safety limits, and keep/discard protocol.
- A one-shot runner command or module can read an experiment definition and execute exactly one eval trial.
- Experiment definitions include hypothesis, namespace/config, dataset path, retrieval options, and output path.
- Runner writes structured JSON and a readable Markdown report.
- Runner has a dry-run/test path that does not require credentials or live turbopuffer calls.
- Runner refuses or ignores experiment fields that would imply source-code mutation or live writes/deletes.
- Tests cover experiment validation and dry-run artifact generation.

## Explicit exclusions

- Infinite loop daemon.
- Code-mutating retrieval experiments.
- Automatic promotion of configs.
- Live apply/write/delete operations.

## Evidence expectations

- Focused test output for runner validation.
- Sample dry-run artifact path and contents summarized in evidence.

## References

- `.10x/specs/repo-search-eval-autoresearch.md`
- `/tmp/pi-github-repos/karpathy/autoresearch/program.md`
- `/tmp/pi-github-repos/z3z1ma/10x@main/autoresearch/README.md`
- `/tmp/pi-github-repos/z3z1ma/10x@main/autoresearch/program.md`

## Progress and notes

- 2026-06-28: Added `autoresearch/program.md` as the human-owned config-only repo search eval loop program.
- 2026-06-28: Added `src/turbo_search/autoresearch.py` with `python -m turbo_search.autoresearch --experiment <json> --out <dir>` one-shot runner.
- 2026-06-28: Implemented experiment validation for required scientific/config fields, fixture/live modes, retrieval options, and forbidden mutation/write/delete/apply/namespace-management fields.
- 2026-06-28: Implemented fixture mode that scores supplied hits locally with no credential reads or turbopuffer calls.
- 2026-06-28: Implemented live mode only through existing retrieval/eval code; no live validation was run in this ticket.
- 2026-06-28: Runner writes `plan.json`, `result.json`, and `report.md`.
- 2026-06-28: Added `tests/test_autoresearch.py` covering experiment validation, unsafe fields/commands, fixture artifact generation, module entry point, and live-mode fixture rejection.
- 2026-06-28: Validation recorded in `.10x/evidence/2026-06-28-config-autoresearch-runner-validation.md`.

## Current State

Done. The config-only one-shot autoresearch runner and human-owned program scaffold are implemented and focused tests pass.

## Blockers

- None.
