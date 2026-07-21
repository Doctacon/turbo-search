Status: recorded
Created: 2026-07-12
Updated: 2026-07-12
Relates-To: .10x/tickets/done/2026-07-12-approved-apply-throughput-measurement.md, .10x/specs/approved-apply-throughput-measurement.md

# Approved Apply Throughput Measurement Validation

## What was observed

- `apply --approve` retains the 64-row default `--batch-size` for serial Turbopuffer writes and adds a positive `--embedding-batch-size` option with default 32.
- The selected embedding batch size is passed to each local `SentenceTransformer.encode` invocation independently of the write batch size.
- Each successful write-batch progress update includes cumulative elapsed, embedding, and write seconds plus rows and batches completed.
- Approved summaries add a `timing` object with elapsed, embedding, and write seconds and both effective batch sizes. Preflight summaries omit it and continue not to construct model/writer instances.
- Timing and progress remain diagnostic; writes, state persistence, locking, and cleanup remain serial and unchanged.

## Procedure

1. Added an argument/default/positive-validation test for the two batch controls.
2. Added a controlled monotonic-clock apply test using two one-row write batches, verifying independent encoder batch size propagation, cumulative embedding/write timings, and final timing summary.
3. Extended approved JSON/text summary coverage and preflight coverage.
4. Ran focused CLI/apply tests, the complete suite, and whitespace/index checks.
5. After independent review, injected a monotonic-clock failure immediately after successful remote upsert and verified the local state still commits.
6. Ran a controlled delete-only apply and verified its successful delete duration contributes to cumulative write timing and emits post-success timing progress.

## Results

```text
PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest tests.test_apply_cli tests.test_cli -q
Ran 62 tests
OK

PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q
Ran 206 tests
OK

git diff --check
OK

git diff --cached --quiet
no staged files
```

Both test commands print one expected existing plan-cleanup-boundary warning; the suite exits successfully.

## What this supports or challenges

Supports the governing specification's measurement and independent-batch-control contract without live apply, concurrency, retry, model, state, or remote-protocol changes. It also supports the review-required safety property that timing observation failures cannot prevent state commit or mask an apply outcome, and that stale deletes count toward remote write timing.

## Limits

The timing values are deterministic mock observations; no live embedding, service latency, hardware throughput, or Turbopuffer payload limit was benchmarked.
