Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-search-eval-autoresearch-plan.md, .10x/specs/repo-search-eval-autoresearch.md

# Repo Search Eval Autoresearch Final Validation

## What was observed

Validated the completed repo search composite eval and config-only autoresearch slice after reviewer fixes, including composite score clamping, path/repo_path report locators, and live retrieval repo_path normalization.

Final ticket status check showed all child tickets and the parent plan are `done`:

```text
.10x/tickets/2026-06-28-config-autoresearch-runner.md: Status: done
.10x/tickets/2026-06-28-graded-repo-eval-metric.md: Status: done
.10x/tickets/2026-06-28-repo-eval-autoresearch-docs-validation.md: Status: done
.10x/tickets/2026-06-28-repo-search-eval-autoresearch-plan.md: Status: done
.10x/tickets/2026-06-28-turbo-search-seed-repo-eval-dataset.md: Status: done
```

Focused validation command:

```bash
uv run python -m unittest tests.test_autoresearch tests.test_evals tests.test_cli tests.test_retriever
```

Output:

```text
............................................
----------------------------------------------------------------------
Ran 44 tests in 0.042s

OK
```

Full validation command:

```bash
uv run python -m unittest discover tests
```

Output:

```text
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 1.739s

OK
```

Whitespace validation:

```bash
git diff --check
```

Output: no errors.

Safe fixture experiment command:

```bash
uv run python -m turbo_search.autoresearch \
  --experiment autoresearch/experiments/repo-search-fixture-baseline.json \
  --out /tmp/turbo-search-final-fixture \
  --json
```

Summarized output:

```text
passed 100.0 10 10 False
```

Meaning: status passed, composite score 100.0, 10/10 cases passed, 10 total cases, no turbopuffer API calls.

## Procedure

1. Ran focused tests across autoresearch, eval, CLI, and retriever surfaces.
2. Ran the full unittest discovery suite.
3. Ran whitespace diff check.
4. Ran the checked-in fixture autoresearch experiment with temporary output.
5. Confirmed no live turbopuffer API call was made by fixture mode.

## What this supports or challenges

Supports parent-plan acceptance criteria:

- all child tickets are done;
- composite metric behavior is implemented and tested;
- the `turbo-search` seed dataset is present/loadable/tested;
- one-shot config-only autoresearch can run without source mutation and without live calls in fixture mode;
- no live eval was run because no already-applied `turbo-search` repository namespace exists locally and live writes/namespaces are out of scope.

## Limits

The fixture experiment validates evaluator/runner wiring, not live retrieval quality. Seed labels remain assistant-drafted and not human-approved ground truth. Live repository eval remains pending an approved/applied `turbo-search` GitHub repository namespace.
