Status: recorded
Created: 2026-07-13
Updated: 2026-07-13
Relates-To: .10x/tickets/done/2026-07-12-live-dagster-throughput-benchmark.md, .10x/specs/approved-apply-throughput-measurement.md

# Live Dagster Approved-Apply Throughput Benchmark

## Raw artifacts

Sanitized raw plan, exact-plan preflight, and approved-apply JSON outputs are retained at `.10x/evidence/.storage/2026-07-13-live-dagster-throughput-benchmark-command-output.json`. They contain no credentials. The benchmark worker transcript is retained at `.pi-subagents/artifacts/outputs/413b46b7-9a8e-445e-ab24-034152afc675/worker/live-dagster-throughput-benchmark.md`.

## What was observed

A fresh local Dagster plan successfully crawled 1,164 pages and produced 25,322 chunks for the explicitly authorized new namespace `site-dagster-io-benchmark-v1`. It had no crawl errors, did not hit page/chunk limits, and required a first apply.

The inspected preflight was local-only (`turbopuffer_api_calls: false`) and projected 25,322 embeddings/upserts, zero stale rows, and no deletion.

One approved apply was then run with a 128-row write batch and a 64-item embedding computation batch. It completed successfully:

- rows upserted / embeddings generated: 25,322 / 25,322
- rows deleted: 0
- measured elapsed / embedding / write seconds: 707.575 / 521.829 / 165.997
- observed overall / embedding / write throughput: approximately 35.8 / 48.5 / 152.5 rows per second
- `state.duckdb` exists at `.turbo-search/state/dagster-io/site-dagster-io-benchmark-v1/state.duckdb` with 25,322 `applied_rows` and one `apply_runs` record
- the exact successful plan directory was automatically removed

## Procedure

1. Confirmed the new namespace had no existing local state and the planned artifact path was absent.
2. Ran local-only plan (wall time 241.34 seconds):

   ```text
   uv run turbo-search plan https://dagster.io/ \
     --out-dir artifacts/site-crawls/dagster-io-throughput-benchmark-plan \
     --namespace site-dagster-io-benchmark-v1 --json
   ```

3. Inspected `summary.json`, `plan.json`, `manifest.json`, and `chunks.jsonl`; confirmed the source, namespace, 25,322 records, empty errors, and no reached limit.
4. Ran local-only preflight (wall time 3.08 seconds) against the exact plan and namespace; confirmed it was a first apply, did not contact Turbopuffer, and omitted live timing.
5. Loaded `.env` only within a command subshell and ran exactly one approved apply (process wall time 715.02 seconds):

   ```text
   uv run turbo-search apply --approve \
     --plan artifacts/site-crawls/dagster-io-throughput-benchmark-plan/plan.json \
     --namespace site-dagster-io-benchmark-v1 \
     --batch-size 128 --embedding-batch-size 64 --json
   ```

6. Confirmed no stale delete occurred, the plan directory was removed, and the new namespace-local DuckDB ledger has 25,322 rows.

## What this supports or challenges

Supports that the new timing diagnostics separate the bottleneck for this workload: local embedding accounted for 75.9% of instrumented embedding-plus-write duration (521.829 of 687.826 seconds), while serial remote writes accounted for 24.1%. Embedding accounts for 73.7% of total elapsed time; the remaining elapsed time is setup/state/other overhead.

The benchmark changed only the authorized new namespace and used no delete/retry/retrieval operation.

## Limits

This is one benchmark run on the current host and service conditions. It compares informally with the prior user-observed ~15-minute 64/32 apply, but that prior run did not have stage timing and is not a controlled baseline. It does not establish the optimal next batch sizes or safe remote-write concurrency.
