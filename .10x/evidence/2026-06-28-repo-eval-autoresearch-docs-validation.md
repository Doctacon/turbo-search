Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-eval-autoresearch-docs-validation.md

# Repo Eval Autoresearch Docs and Validation

## What was observed

Documented the composite repository search score, graded dataset format, seed dataset caveat, and one-shot config-only autoresearch command. Added a safe fixture-mode sample experiment and test coverage for it.

Changed files for this ticket:

- `README.md`
  - Added repository search eval documentation, the weighted composite formula, dataset location/format, seed-label caveat, safe sample command, and live-mode safety note.
- `docs/generic-site-rag-plan-apply.md`
  - Added repository composite eval and config autoresearch workflow notes to retrieval/eval validation docs.
- `autoresearch/program.md`
  - Added the checked-in fixture baseline experiment path and safe command shape.
- `autoresearch/experiments/repo-search-fixture-baseline.json`
  - Added fixture-mode-only experiment that uses ideal judged hits from the seed dataset and performs no credential reads or turbopuffer calls.
- `tests/test_autoresearch.py`
  - Added coverage that loads and runs the checked-in fixture experiment and asserts no turbopuffer calls plus a 100-point fixture score.
- `.10x/tickets/2026-06-28-repo-eval-autoresearch-docs-validation.md`
  - Updated progress, current state, and blockers.

Validation commands:

```bash
uv run python -m unittest tests.test_autoresearch tests.test_evals tests.test_cli tests.test_retriever
uv run python -m unittest discover tests
OUT=$(mktemp -d /tmp/turbo-search-autoresearch-fixture.XXXXXX)
uv run python -m turbo_search.autoresearch \
  --experiment autoresearch/experiments/repo-search-fixture-baseline.json \
  --out "$OUT" \
  --json | uv run python -c 'import json,sys; data=json.load(sys.stdin); print({"status": data["status"], "score": data["score"], "passed": data["eval"]["passed"], "total": data["eval"]["total"], "api_calls": data["eval"]["api_calls_occurred"]})'
find .turbo-search/state -maxdepth 4 -type f -name last-applied.json -print 2>/dev/null | sort | sed -n '1,80p'
```

Outputs:

```text
..........................................
----------------------------------------------------------------------
Ran 42 tests in 0.040s

OK
```

```text
.......................................................................................................................
----------------------------------------------------------------------
Ran 119 tests in 1.809s

OK
```

```text
{'status': 'passed', 'score': 100.00000000000001, 'passed': 10, 'total': 10, 'api_calls': False}
```

Applied-state namespace check output:

```text
.turbo-search/state/pi-dev/site-pi-dev-v1/last-applied.json
.turbo-search/state/sqlmesh-readthedocs-io/site-sqlmesh-readthedocs-io-v1/last-applied.json
.turbo-search/state/turbopuffer-com/site-turbopuffer-com-v1/last-applied.json
```

## Procedure

1. Read the executable ticket, governing spec, completed dependency tickets, docs, autoresearch program, runner, and seed dataset.
2. Added user-facing docs in README and workflow docs.
3. Added a checked-in fixture-mode sample experiment with no live behavior.
4. Added focused test coverage for the checked-in sample experiment.
5. Ran focused and full relevant tests.
6. Checked local applied-state namespaces and did not run live eval because no already-applied `turbo-search` GitHub repository namespace is present.

## What this supports or challenges

Supports the ticket acceptance criteria:

- README/docs explain composite score, dataset format, one-shot autoresearch command, and seed caveat.
- No CLI/help text was changed, so no CLI help drift was introduced.
- Focused and full relevant tests pass.
- Live eval validation was intentionally skipped because no already-applied `turbo-search` repo namespace is clearly present; live writes/namespaces are out of scope.
- Evidence maps acceptance criteria to commands and outputs without storing secrets.

## Limits

The fixture experiment validates metric/runner plumbing, not live retrieval quality. The seed dataset remains assistant-drafted and not human-approved ground truth. Live repository eval should be run only after a `turbo-search` GitHub repository namespace has been applied through the approved plan/apply workflow.
