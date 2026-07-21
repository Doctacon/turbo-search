Status: recorded
Created: 2026-07-14
Updated: 2026-07-14
Relates-To: .10x/tickets/done/2026-07-13-float16-embedding-inference.md, .10x/specs/embedding-inference-precision.md

# Float16 Embedding Inference Validation

## Observed behavior

- Plans record `embedding_precision`; float32 remains default. Apply derives effective precision from the verified plan, so a valid ambient retrieval precision cannot override it. Invalid/conflicting ambient configuration is still rejected during general runtime configuration loading.
- Existing plans without the field verify as float32 with their original artifact-hash shape.
- Float16 changes embedding identity and triggers re-upsert while preserving deterministic `ts_*` row IDs and namespace.
- Retrieval/evals/autoresearch accept CLI/environment precision and expose it in dry-run/result output.
- Float16 calls `.half()` only after Sentence Transformers selects CUDA or Apple MPS; CPU selection fails before encoding with a user-friendly error.
- Apply timing/summary reports effective precision. No write/order/locking/delete/state behavior changed.

## Local no-live benchmark

Raw metrics: `.10x/evidence/.storage/2026-07-14-float16-embedding-parity-benchmark.json`.

On Apple M2 Pro / 16 GB / PyTorch MPS, 1,024 real Iceberg plan chunks at encoder batch 32 produced:

- minimum float32/float16 normalized-vector cosine: 0.999756;
- mean cosine: 1.000156 (minor floating-point overshoot);
- exact top-10 identity for query “How does Apache Iceberg handle table metadata and snapshots?”: true;
- three-run median float32: 15.838s / 64.66 rows/s;
- three-run median float16: 15.855s / 64.58 rows/s.

Parity acceptance passed, but this repeated benchmark did **not** reproduce the earlier ~24% throughput improvement. Float16 remains opt-in; no default-performance claim is supported.

## Validation

```text
Focused config/chunker/plan/apply/retrieval/eval/autoresearch/CLI tests
Ran 146 tests; OK

PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q
Ran 242 tests; OK

uv build --out-dir /tmp/buoy-float16-build-final
Built buoy_search-0.2.1 wheel and sdist

git diff --check
OK

Post-review repair validation:
Focused CLI/retrieval/autoresearch/plan tests: 86 tests; OK
Full suite: 246 tests; OK
Built buoy_search-0.2.1 wheel and sdist; git diff --check and empty staged diff passed
```

Post-review regressions prove live retrieval plus dry/live eval text precision, float32-state to float16-plan re-upsert with stable `ts_*` row ID, float16 query embedder construction through `HybridRetriever.from_config`, and invalid fixture autoresearch precision rejection.

No credentials, Turbopuffer calls, live retrieval/evals, namespace changes, or remote mutations occurred.

## Limits

MPS throughput was variable across earlier and current runs. Numerical and one-query top-10 parity do not establish universal retrieval equivalence. CUDA was unit-tested by device classification, not benchmarked on this host.
