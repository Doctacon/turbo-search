Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/2026-07-20-implement-experimental-buoy-baseline-executor.md, .10x/specs/experimental-buoy-baseline-executor.md

# Experimental Buoy Baseline Executor Implementation Evidence

## What was observed

The bounded implementation adds only `src/buoy_search/experimental_baseline.py` and its focused fake-backed tests in `tests/test_experimental_baseline.py`. It is an explicitly non-default module with no CLI, ordinary apply, retrieval, catalog, or default routing integration.

Static inspection and focused tests establish:

- immutable region, plan, artifact, source, namespace, 903-row, model revision/precision/dimensions/pooling/normalization, cache manifest, README/license, generated card, and local applied-state values are checked under an injected plan-bound lock before credential access;
- both offline environment controls are set before the injected preparation/model boundary;
- the locked provider factory checks `turbopuffer==2.4.0` and constructs exactly one client with the literal `max_retries=0`; executor resources must attest wrapper retries, fallbacks, and pagination are disabled;
- a simulation/live gate rejects non-simulated execution without separately granted Approval A and rejects a simulation that claims Approval A;
- the physical ledger contains exactly 26 non-reassignable slots, with the target empty probe as the only conditionally unused slot, and enforces at most 10 reads, 16 writes, 26 physical attempts, 904 attempted write-row positions, 1,817 returned-row positions, and zero deletes;
- the only content write shape is `14 × 64 + 1 × 7`; successful writes require exact `rows_affected`, and the catalog write additionally requires its exact affected ID;
- accounting is created before each fake physical call and retains status, requested rows or `top_k`, exact/present `rows_affected`, returned-row count, redacted/present billing, hashed/present provider request identity, affected IDs, operation/global numbering, and cumulative counters across success, malformed response, timeout, and indeterminate outcomes;
- target absence must be unambiguous; otherwise exact normalized schema/cosine compatibility and a bounded empty probe are required. Catalog metadata and two exact-card reads must be compatible and stable before pending creation or content writes;
- two exact 903-row strong reads, including stable provider order, attributes, finite normalized 384-dimensional vectors, and no 904th row, precede the one conditional card write;
- two exact stable card reads precede local state commit, and pending removal follows local commit. Every tested partial content/target/card failure retains pending state, performs no retry or delete, and blocks the prohibited later commit;
- evidence maps all 26 slots to attempted or unused and reports dollar cost as unknown.

## Procedure and validation output

1. `uv sync --locked --python 3.11` — passed with locked dependencies, including `turbopuffer==2.4.0`.
2. `PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ranking_contract.py` under Python 3.11 — passed; 13 datasets, 90 composite identities, 369 judgments; Buoy remained in `pending_baseline_approval`.
3. `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q` under Python 3.11 — passed, 465 tests.
4. `uv sync --locked --python 3.13` — passed with locked dependencies.
5. The same ranking-contract command under Python 3.13 — passed with identical frozen hashes/counts and Buoy still pending baseline approval.
6. The same full unittest discovery under Python 3.13 — passed, 465 tests.
7. `uv build --out-dir /tmp/buoy-baseline-build-dist` — passed; built wheel and source distribution outside the repository.
8. Incorporated current `origin/develop` commit `3e6005c` and repeated both interpreter suites, ranking validation, build, and diff hygiene successfully on that target state.
9. `git diff --check` — passed.
10. Static source scan found no executor delete operation, retry loop, pagination loop, fallback call, credential-environment read, or sentence-transformer import. The only SDK constructor is `turbopuffer.Turbopuffer(api_key=api_key, region=region, max_retries=0)`.

The full suite emitted two existing temporary plan-cleanup warning lines per interpreter and still completed successfully; no executor test touched retained plan/state paths.

## What this supports

This supports independent implementation review of the bounded executor and tests. It does not support ticket closure, Approval A, Approval B, a live/model/provider operation, or Buoy baseline compatibility. The ticket remains active pending the required independent review.

## Limits and no-live attestation

Validation used only injected in-memory provider/model fakes and injected local-effect callbacks. It did not read `TURBOPUFFER_API_KEY`, import/load/invoke the real embedding model, inspect the retained `/tmp` plan or state, construct a real provider client, make a network call, or mutate a namespace, routing catalog, pending record, DuckDB applied state, project default, dependency, or lockfile. No delete was attempted. Approval A and Approval B remain ungranted; no live execution or merge occurred.
