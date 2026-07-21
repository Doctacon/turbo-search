Status: recorded
Created: 2026-07-14
Updated: 2026-07-14
Target: current Buoy codebase
Verdict: concerns

# Buoy Performance and UX Codebase Review

## Target

Current `main` source, tests, docs, workflows, active records, and retained Dagster benchmark evidence.

## Findings

### 1. Execute opt-in float16 embedding inference

Embedding consumed 521.829 of 707.575 seconds (73.7%) in the 25,322-row Dagster apply. Existing M2 Pro microbenchmarks measured MPS float16 batch 32 at 76.8 rows/s versus float32 at 61.9 rows/s, about 24% higher throughput with minimum sampled cosine similarity 0.99976. This is already owned by `.10x/tickets/done/2026-07-13-float16-embedding-inference.md`; no duplicate ticket is needed.

### 2. Remove duplicate plan processing and add stage timing

Each source path already runs `process_corpus`, then `_run_plan` runs it again. `_run_plan` also constructs complete plan artifacts twice, including chunk JSONL serialization. The Dagster plan took 241.34 seconds, but current timing cannot attribute crawl versus duplicated parse/chunk/artifact work. Owner: `.10x/tickets/done/2026-07-14-single-pass-plan-and-stage-timing.md`.

### 3. Make plan → approval → live retrieval handoff explicit

Live retrieval silently falls back to the built-in Scrapling demo namespace when neither CLI nor environment supplies one. Default text preflight also omits the automatically selected plan/source and several fields the indexing guide says users should review. Require an operator-sourced namespace for live retrieval, emit a copy-ready retrieval command, and make preflight text decision-complete while retaining JSON as the automation contract. Owner: `.10x/tickets/done/2026-07-14-explicit-plan-to-retrieval-handoff.md`.

## Verdict

The codebase has strong remote-write/state safety and meaningful tests. Highest leverage comes from improving the measured embedding bottleneck, eliminating certain duplicated planning work, and preventing successful-but-wrong operator actions. Broad module splitting, retriever micro-optimization, DuckDB tuning, and speculative remote-write concurrency are not currently evidence-backed priorities.

## Residual risk

Performance evidence is one Apple M2 Pro and one large Dagster workload. Plan stages and live retrieval latency remain unmeasured; claims beyond the observed numbers require new benchmarks.
