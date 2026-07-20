Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/2026-07-20-implement-experimental-buoy-baseline-executor.md, .10x/specs/experimental-buoy-baseline-executor.md

# Experimental Buoy Baseline Executor Implementation Evidence

## What was observed

The repaired bounded implementation remains an explicitly non-default module with no CLI, ordinary apply, retrieval, catalog, or default routing integration. The only adjacent primitive change lets the existing pending confirmation accept an optional exact timestamp; ordinary callers retain the prior default.

Static inspection and 28 focused fake-backed tests establish:

- the public live entry point accepts only four keyword-only durable paths. It has no caller callback, boolean, attestation, prepared model, provider, or local-effect parameter;
- live is mechanically disabled while Approval A is ungranted. A future reviewed source change must pin the exact durable grant bytes and exact message provenance in addition to the record containing the full Approval A text/hash, grant state, actor, timestamp, and provenance;
- the separately named simulation entry point carries simulation-only provider identity, reports `execution_mode=simulation`, never reports live SDK/max-retry attestation, and cannot enter the live constructor path;
- live reloads and rehashes the exact plan/artifact under the fixed namespace lock, hashes the full immutable model cache twice at the model boundary, sets both offline controls before imports, and internally constructs the exact revision's tokenizer/model for float32 normalized 384-dimensional CLS output;
- live internally constructs the locked `turbopuffer==2.4.0` client with literal `max_retries=0`, direct non-paginating resources, fixed namespaces, and no retry/fallback loop; it also constructs pending/DuckDB effects internally from existing integrity-bound primitives;
- the physical ledger contains exactly 26 non-reassignable slots: 10 reads, 16 writes, 904 attempted write-row positions, 1,817 returned-row positions, and zero provider deletes. Every metadata/write slot has a returned-row ceiling of zero;
- every write requires exact integer nonnegative `rows_affected`, the exact batch/card count, and the exact ordered affected IDs. Billing, request identity, and metrics object shapes are validated and redacted; parseable response/metrics attached to exceptions are preserved;
- target and catalog metadata require exact schemas and explicit `cosine_distance`; missing distance, unknown config keys, extra attributes, unstable/duplicate cards, nonempty targets, and incompatible existing cards fail closed before writes;
- two exact stable 903-row reads precede the card write; two exact stable card reads precede the local commit. Local partial create/commit/cleanup failures are re-observed from durable effects so evidence does not erase a completed partial effect;
- the matrix covers compatible/incompatible/duplicate existing cards, malformed response/accounting shapes, attached error accounting, local partial failures, immutable/cache/model gates, and a forced failure in each of all 26 slots with no reassignment, retry, or later attempt.

## Procedure and validation output

1. `uv sync --locked --python 3.11` — passed with locked dependencies, including `turbopuffer==2.4.0`.
2. `PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ranking_contract.py` under Python 3.11 — passed; 13 datasets, 90 composite identities, 369 judgments; Buoy remained in `pending_baseline_approval`.
3. `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q` under Python 3.11 — passed, 493 tests.
4. `uv sync --locked --python 3.13` — passed with locked dependencies.
5. The same ranking-contract command under Python 3.13 — passed with identical frozen hashes/counts and Buoy still pending baseline approval.
6. The same full unittest discovery under Python 3.13 — passed, 493 tests.
7. `uv build --out-dir /tmp/buoy-baseline-build-dist` — passed; built wheel and source distribution outside the repository.
8. `git diff --check` — passed.
9. Static inspection confirms 26 slots, 10 reads, 16 writes, 904 write positions, 1,817 returned-row ceilings, no executor delete method, no retry/fallback/pagination loop, literal `max_retries=0`, exact offline revision construction, no live CLI import, and source-pinned Approval A grant constants intentionally `None`.

The full suite emitted two existing temporary plan-cleanup warning lines per interpreter and still completed successfully; no executor test touched retained plan/state paths.

## What this supports

This supports independent implementation review of the bounded executor and tests. It does not support ticket closure, Approval A, Approval B, a live/model/provider operation, or Buoy baseline compatibility. The ticket remains active pending the required independent review.

## Limits and no-live attestation

Validation used only the separately named simulation path with in-memory provider/model/local-effect fakes and temporary approval-record files. It did not read `TURBOPUFFER_API_KEY`, import/load/invoke the real embedding model, inspect the retained `/tmp` plan or state, construct a real provider client, make a network call, or mutate a namespace, routing catalog, pending record, DuckDB applied state, project default, dependency, or lockfile. No provider delete was attempted. Approval A is source-pinned as ungranted; Approval B remains ungranted; no live execution or merge occurred. The ticket remains active for the required independent review and CI on the pushed repair.
