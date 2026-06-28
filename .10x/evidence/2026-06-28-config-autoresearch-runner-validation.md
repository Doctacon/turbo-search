Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-config-autoresearch-runner.md

# Config-only Autoresearch Runner Validation

## What was observed

Implemented the one-shot config-only repository search autoresearch runner.

Changed files for this ticket:

- `autoresearch/program.md`
  - Added the human-owned config-only repo search autoresearch program with editable surfaces, experiment format, one-iteration protocol, keep/discard guidance, and safety boundaries.
- `src/turbo_search/autoresearch.py`
  - Added `python -m turbo_search.autoresearch --experiment <json> --out <dir>` runner.
  - Added experiment validation for `experiment_id`, `question`, `hypothesis`, `dataset_path`, `config`, `retrieval_options`, mode, output path, and fixture hits.
  - Added fixture mode that scores supplied hits locally with no credential reads or turbopuffer calls.
  - Added live mode support only through existing retrieval/eval code; no apply/write/delete/state/namespace operations are present.
  - Added forbidden-field/command-token validation for code mutation, writes, applies, deletes, and namespace-management intent.
  - Writes `plan.json`, `result.json`, and `report.md` for exactly one experiment.
- `tests/test_autoresearch.py`
  - Added focused validation and fixture artifact generation tests.

Validation commands:

```bash
uv run python -m unittest tests.test_autoresearch tests.test_evals
uv run python -m py_compile src/turbo_search/autoresearch.py
uv run python -m unittest tests.test_autoresearch tests.test_evals tests.test_cli tests.test_retriever
```

Outputs:

```text
....................
----------------------------------------------------------------------
Ran 20 tests in 0.009s

OK
```

```text
.........................................
----------------------------------------------------------------------
Ran 41 tests in 0.036s

OK
```

## Procedure

1. Read the executable ticket, governing spec, current eval/retrieval/CLI code, eval tests, and both referenced autoresearch programs.
2. Implemented the runner as a module command rather than broad CLI integration to keep the diff narrow.
3. Reused existing graded eval scoring and live retrieval/eval paths.
4. Added local fixture scoring to validate runner artifacts without credentials or live turbopuffer calls.
5. Added tests for experiment validation, unsafe fields/commands, fixture artifact generation, module entry point, and live-mode fixture rejection.

## What this supports or challenges

Supports the ticket acceptance criteria:

- Human-owned `autoresearch/program.md` exists.
- One-shot runner reads one experiment and executes exactly one eval trial.
- Experiment definitions include hypothesis/question, dataset, namespace/config, retrieval options, and output path via `--out` or `output_path`.
- Runner writes structured JSON and Markdown artifacts.
- Fixture mode scores supplied hits without credentials/live calls.
- Live mode is retrieval-only through existing eval code.
- Unsafe mutation/write/delete/apply/namespace-management fields are rejected.
- Focused tests cover validation and dry-run artifact generation.

## Limits

No live turbopuffer calls were run for this ticket. The runner does not implement repeated looping, automatic promotion, code-mutating experiments, reranking, or query rewriting; those are explicit exclusions.
