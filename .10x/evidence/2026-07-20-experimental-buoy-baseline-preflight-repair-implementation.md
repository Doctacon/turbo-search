Status: recorded
Created: 2026-07-20
Updated: 2026-07-21
Relates-To: .10x/tickets/2026-07-20-source-pin-and-execute-experimental-buoy-baseline.md, .10x/evidence/2026-07-20-experimental-buoy-baseline-repair-ratification.md, .10x/reviews/2026-07-20-experimental-buoy-baseline-step-2-preflight-review.md, .10x/specs/experimental-buoy-baseline-executor.md

# Experimental Buoy Baseline Preflight Repair Implementation Evidence

## What was implemented

The bounded repair changes only `src/buoy_search/experimental_baseline.py`, its deterministic fake-backed tests, this evidence, and append-only ticket progress:

- cache validation now hashes path-sorted compact UTF-8 JSON entries with exactly `path`, `bytes`, and `sha256`, preserving the approved `5f783ebce23b6ac957d2741399b46e19502b1751acfd3c744b8c41103b138f35` pin and all cache bytes; the 1,430-byte canonical 12-entry authority is checked in at `.10x/evidence/.storage/2026-07-20-bge-small-en-v1.5-cache-manifest.json`, whose bytes themselves hash to that pin;
- the existing exact README hash and `license: mit` front matter remain mandatory, while the license statement check now recognizes the README's Markdown-linked `MIT License` text;
- fixed-ledger reads retain secret-free immutable hashes of the raw sanitized target/card rows, not parsed `NamespaceCard` values, plus raw provider-observed schema/distance projections before validation normalization or default injection; successful and later failed runs preserve those facts without another request;
- successful or partially completed local commits reload the applied state and retain its exact hash in public evidence.

The Approval A grant bytes, approval text, source pins, model/cache/README pins, identities, 26 fixed slots, budgets, `max_retries=0`, zero-delete boundary, retry/fallback/pagination behavior, commit order, CLI/default paths, dependencies, and lockfile remain unchanged.

## Deterministic tests

`tests/test_experimental_baseline.py` now proves:

- the checked-in actual 12-file path/byte/SHA authority is path-sorted, totals 267,599,430 bytes, contains only the three authorized fields, is already in canonical compact serialization, and hashes directly and through the production serializer to the unchanged approved pin without patching an expected hash or README;
- the exact Markdown-linked MIT sentence recognizer is covered directly while the production cache attestation continues to require the pinned README hash and front matter;
- complete success retains both stable 903-row raw target projections, both stable raw post-write card projections (including a provider-only `$dist` field), raw schemas/distances without injected defaults, and the reloaded committed applied-state hash; every projection hash is compared with the corresponding fake's raw returned row;
- a deterministic final-card-read failure retains both already-validated raw target projections and the first raw card projection, performs no local state commit/reload, keeps later evidence absent rather than inferring it, and proves provider query counts did not increase for evidence.

The focused module passes 32 tests. After incorporating current `develop` commit `f85136659f7d9094f180b7da397c589d6f178ee8`, the complete suite passes 507 tests on each supported CI interpreter.

## Procedure and validation output

1. `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest tests.test_experimental_baseline -q` — passed, 32 tests.
2. `uv sync --locked --python 3.11` — passed with the existing lock, including `turbopuffer==2.4.0`.
3. `PYTHONDONTWRITEBYTECODE=1 uv run python scripts/validate_ranking_contract.py` under Python 3.11 — passed: 13 datasets, 90 composite identities, 369 judgments; Buoy remains `pending_baseline_approval`.
4. `PYTHONDONTWRITEBYTECODE=1 uv run python scripts/c6_syntax_forecast.py validate` under Python 3.11 — passed the current CI forecast check after incorporating `develop`.
5. `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -p 'test_*.py' -q` under Python 3.11 — passed, 507 tests.
6. `uv sync --locked --python 3.13` — passed with the existing lock.
7. The same ranking-contract and C6 forecast commands under Python 3.13 — passed with the same frozen hashes/counts and Buoy still pending baseline approval.
8. The same full unittest discovery under Python 3.13 — passed, 507 tests.
9. `uv build --out-dir /tmp/buoy-baseline-repair-build-dist` — passed; built the wheel and source distribution outside the repository.
10. `git diff --check` — passed.
11. A standard-library/import-only assertion checked the exact Approval A record/text/provenance pins, unchanged cache/README pins, and exact 26-slot/10-read/16-write/904-write-row/1,817-returned-row ceilings — passed.
12. Direct standard-library inspection of the checked-in cache authority confirmed 1,430 canonical bytes, 12 entries, 267,599,430 resolved bytes, and SHA-256 `5f783ebce23b6ac957d2741399b46e19502b1751acfd3c744b8c41103b138f35` — passed.

The full suite emitted two existing temporary plan-cleanup warning lines per interpreter and still passed. The warnings concern suite-created temporary directories, not retained baseline state.

## No-live attestation

No live entry point was invoked. Validation did not read a credential, import or load a model, construct a real provider client, make a provider request, or read/mutate retained plan, namespace, catalog, pending, or DuckDB state. One bounded read-only inspection of the existing live cache resolved the actual 12 path/byte/SHA entries used to check in the compact authority; it read bytes only for hashing and did not import, construct, or load the model. Executor behavior tests use simulation-only provider/model/local-effect fakes. There were no deletes, retries, fallbacks, pagination calls, other namespaces, ordinary-path/default changes, dependency changes, or lockfile changes.

Approval A remains exact and unspent; Approval B remains ungranted; C3 remains blocked. This evidence does not establish remote compatibility or authorize invocation. Independent implementation review, hosted CI, protected integration, and a fresh complete preflight remain required.

## Limits

This is implementation evidence, not independent review or integration evidence. Provider behavior, remote state, real cache compatibility, and model runtime remain unobserved. The owning ticket remains active pending independent review and integration.
