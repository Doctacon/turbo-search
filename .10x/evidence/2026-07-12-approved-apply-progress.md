Status: recorded
Created: 2026-07-12
Updated: 2026-07-12
Relates-To: .10x/tickets/done/2026-07-12-approved-apply-progress.md

# Approved Apply Progress Validation

## What was observed

- Interactive `apply --approve` now reuses the existing one-line stderr renderer for verification, namespace-lock acquisition, embedding/upserting preparation, each successful batch, local-state commit, and successful-plan cleanup.
- Batch updates report completed/total batches and rows only after the batch's Turbopuffer write succeeds.
- `--no-progress`, `--json`, and non-TTY stderr suppress progress; JSON stdout remains parseable and unchanged.
- Preflight shows verification only and does not invoke the embedding/upsert progress path.
- Progress callbacks and stderr writes are best-effort: their failures cannot interrupt an approved apply after remote upsert, prevent the DuckDB state commit, or replace an underlying upsert failure. If stderr itself is unavailable while reporting an approved-apply failure, the command still returns 2 rather than raising and masking that failure.

## Procedure

1. Added mocked approved-apply tests using two one-row batches and a TTY-like stderr stream.
2. Verified each phase and batch counter appears on one terminal line with no newline output.
3. Verified suppression for JSON, explicit `--no-progress`, and non-TTY stderr.
4. Simulated a failing progress callback after each apply phase, including after successful upserts; verified the state still commits.
5. Simulated a TTY stderr write failure; verified approved apply still completes and saves state.
6. Verified a failing callback does not replace a genuine upsert error.
7. Simulated both a failing TTY stderr stream and a failing upsert; verified `main()` returns 2 without raising.
8. Ran focused and complete unit suites plus whitespace/index checks.

## Results

```text
PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest tests.test_apply_cli tests.test_cli -q
Ran 58 tests in 2.078s
OK

PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q
Ran 202 tests in 6.860s
OK

git diff --check
OK

git diff --cached --quiet
no staged files
```

The suite prints an expected cleanup-boundary warning from an existing cleanup regression; it does not indicate a failure.

## What this supports or challenges

Supports the ticket contract without altering JSON output, remote write sequencing, lock behavior, state commit, or cleanup decisions. It resolves the review findings that display failures could leave successfully written remote rows without committed local state or that a broken stderr stream could mask an approved-apply error.

## Limits

Mocked batch writes validate renderer integration and counters, not real embedding or Turbopuffer latency. No live apply was run.
