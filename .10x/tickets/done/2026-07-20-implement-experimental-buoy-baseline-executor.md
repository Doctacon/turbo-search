Status: done
Created: 2026-07-20
Updated: 2026-07-20
Parent: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md
Depends-On: .10x/tickets/done/2026-07-19-freeze-repo-ranking-experiment-contract.md, .10x/tickets/done/2026-07-20-remove-buoy-internal-ranking-judgment.md

# Implement Fail-Closed Experimental Buoy Baseline Executor

## Outcome

Completed the smallest isolated executor that exactly satisfies `.10x/specs/experimental-buoy-baseline-executor.md`. Independent implementation review passed PR #70 head `f6cd38dba1bc7cf8fbcb542133ca264e6cb3d61c`. Live execution remains mechanically disabled by source-pinned Approval A grant constants set to `None`; Approval A and Approval B remain ungranted, C3 remains blocked, and no credential, model, provider, namespace, catalog, pending, or DuckDB domain-state operation occurred.

## Scope

- Add one explicitly experimental, non-default executor path for only the immutable Buoy baseline operation defined by the active specification. Do not route ordinary `apply`, retrieval, catalog, or public defaults through it.
- Reuse existing verified-plan, embedding-text, schema, card, pending, lock, and DuckDB state primitives where they preserve the contract; isolate stricter provider request interception/accounting and commit ordering rather than weakening shared production behavior.
- Validate every exact region/plan/artifact/source/model/cache/README/license/row/namespace/card/local-state value and all 903 unique intended row IDs before credential access. Set both offline environment controls before model import/construction.
- Construct every locked `turbopuffer==2.4.0` client with `max_retries=0` and reject any path that cannot prove SDK/wrapper retries, fallbacks, pagination, and repeated calls are disabled.
- Enforce the specification's exact preflight target/catalog reads, 15 fixed content batches, response/accounting contract, bounded target/card post-write reads, 26-attempt global ledger, per-operation ceilings, 904 write-row-position ceiling, 1,817 returned-row-position ceiling, and zero-delete invariant.
- Enforce exact response checks and commit order: no catalog mutation or local applied-state commit after content mismatch; no local commit/card-success claim after catalog mismatch; preserve the pending record and partial/indeterminate accounting; remove pending only after exact target and card verification plus local commit.
- Emit a secret-free evidence artifact that maps all 26 slots to attempted or unused and contains the exact accounting fields required by the active specification.
- Add deterministic focused tests using injected fakes and temporary local state only. Tests MUST NOT import/load/invoke the real embedding model, read `TURBOPUFFER_API_KEY`, construct a real provider client, make network calls, or touch the retained `/tmp` plan/state.

## Acceptance criteria

- Exact input/cache/license/ledger validation occurs before credential access, provider-client construction, or model construction and fails closed on every mismatch.
- All provider resources are mechanically attested `max_retries=0`; no retry, signature/schema fallback, pagination, cleanup delete, rollback delete, repeated call, or unused-slot reassignment is possible.
- The only allowed operation sequence and ceilings are encoded exactly: target metadata/optional empty probe; catalog metadata/two exact-card reads; `14 × 64 + 1 × 7` content upserts; target metadata/two `top_k=904` reads; at most one conditional card upsert; two `top_k=2` exact-card reads; 26 attempts, 904 write-row positions, 1,817 returned-row positions, and zero deletes.
- Accounting is appended before every fake physical attempt and finalized for success, failure, timeout, malformed response, and indeterminate outcome with exact/present markers for `rows_affected` and redacted billing, plus request/operation numbering and cumulative counters.
- Focused tests prove abort-before-write on ambiguous/non-empty/incompatible preflight; abort-before-card/local-commit on any content response or target verification mismatch; abort-before-local-commit/card-success on any card response or verification mismatch; exact success ordering; stable repeated-read requirements; pending retention on every partial failure; pending removal only after final verified commit; and secret/raw-request redaction.
- Successful simulated verification requires exactly 903 intended IDs and attributes, no 904th row, stable order, finite normalized-shape-compatible 384-dimensional vectors, exact schema/cosine distance, and one complete stable expected card revision.
- The evidence format maps every possible slot to attempted or unused, reports dollar cost as unknown absent authoritative pricing, and cannot claim success unless every contract invariant passes.
- Focused tests, the full existing test suite, static/type/lint checks used by the repository, and `git diff --check` pass. Independent implementation review records PASS before this ticket can close or Approval A can become eligible.

## Stop conditions

- Stop implementation and return to shaping if the locked SDK cannot expose or mechanically guarantee `max_retries=0`, bounded direct operations, exact response fields, or a no-pagination/no-fallback path without changing the ratified contract.
- Stop if current primitives cannot preserve the exact plan/card/pending/DuckDB commit order without widening the operation or weakening ordinary behavior.
- Do not simulate success by relaxing missing `rows_affected`, billing-presence markers, exact row/card comparisons, stable repeated reads, or any physical-attempt counter.
- Do not run the executor against retained artifacts or real local/remote state. Approval A is ungranted.

## Explicit exclusions

Any live execution; credential access; real model import/load/inference; provider or other network call; namespace/card/catalog/pending/DuckDB mutation outside temporary test directories; source corpus, dataset, judgment, default, dependency, or lockfile change; ordinary apply/retrieval behavior change; recrawl/replan; another namespace/card; delete; C3 retrieval; Approval A or B; promotion.

## Evidence expectations

Focused and full-test output; static inspection proving `max_retries=0` and no fallback/pagination/delete path; fake-call sequence and exact attempt-slot ledger for success and each failure phase; precondition-before-credential/model/provider proof; response-accounting/redaction fixtures; target/card stable-read and local-commit ordering evidence; changed-file/diff hygiene; independent review; explicit no-live/no-model/no-domain-write statement.

## References

- `.10x/specs/experimental-buoy-baseline-executor.md`
- `.10x/reviews/2026-07-20-experimental-buoy-baseline-executor-spec-review.md`
- `.10x/evidence/2026-07-20-experimental-buoy-baseline-executor-ratification.md`
- `.10x/evidence/2026-07-20-c3-buoy-baseline-approval-checkpoint.md`
- `.10x/tickets/2026-07-19-capture-current-repo-candidates-and-baselines.md`

## Blockers

None for the closed implementation outcome. Approval A remains ungranted and blocks every real credential/model/provider/domain-state operation. Approval B remains ungranted, and C3 remains separately blocked.

## Progress and notes

- 2026-07-20: Opened after the user ratified the independently reviewed PR #65 specification unchanged. No source/test implementation, credential read, model operation, provider call, or namespace/card/catalog/pending/DuckDB mutation occurred in this record turn. Approval A and Approval B remain ungranted; C3 remains blocked.
- 2026-07-20: Implemented the isolated non-default executor and 19 fake-backed tests. The executor fixes all 26 slots, enforces the exact request/write/read/delete ceilings and commit order, validates immutable plan/cache/model/row/card/state contracts before credential access, requires locked SDK `max_retries=0`, and preserves redacted partial accounting. CI-equivalent Python 3.11 and 3.13 suites each passed 465 tests; ranking validation, distribution build, and `git diff --check` passed. Evidence is recorded at `.10x/evidence/2026-07-20-experimental-buoy-baseline-executor-implementation.md`. No credential was read, model loaded, provider contacted, retained plan/state inspected, or namespace/catalog/pending/DuckDB domain state mutated. Ticket remains active pending independent implementation review; Approval A/B remain ungranted and no live execution is authorized.
- 2026-07-20: Repaired all reported independent-review blockers without adding a CLI or live invocation. Public live construction now accepts only durable paths, requires exact source-pinned Approval A record bytes/provenance, and is mechanically disabled because the grant pins remain `None`. Simulation is a separate fake-only identity and cannot report live/max-retry attestation. Live internally reloads the exact plan, rehashes the exact cache, constructs the pinned offline float32 normalized CLS model, literal-zero-retry SDK client, and integrity-bound pending/DuckDB effects. Accounting now enforces every slot's returned-row ceiling, exact write counts/IDs and object shapes, preserves attached exception response/metrics, and rejects missing distance/unknown schema keys. The focused matrix expanded to 28 tests including existing-card states, malformed accounting, local partial effects, every gate, and failures in all 26 slots. After incorporating current `origin/develop` (`687fe30`), CI-equivalent Python 3.11 and 3.13 runs each passed 493 tests; both ranking validations, distribution build, and diff hygiene passed. No credential/model/provider/domain-state/live operation occurred. PR #70 GitHub Actions run `29773872982` passed Python 3.11, Python 3.13, and distribution build on repair commit `54fb751`. Approval A/B remain ungranted and the ticket remains active pending independent review.
- 2026-07-20: Independent review passed PR #70 head `f6cd38dba1bc7cf8fbcb542133ca264e6cb3d61c` with no blocker. Current `origin/develop` remained incorporated at `687fe304a0ab2f2b2ba88c95b39eb04048104b7d`; final local Python 3.11 and 3.13 ranking/full-suite runs each passed 493 tests, the distribution build and diff hygiene passed, and exact-head hosted run `29774022595` passed all three CI jobs. Closed and moved this ticket to `done` without merging PR #70, setting either grant constant, reading a credential, loading a model, contacting a provider, or mutating domain state. Approval A/B remain ungranted and C3 remains blocked.

## Closure mapping

- **Exact active contract and identity gates:** `.10x/specs/experimental-buoy-baseline-executor.md`, its ratification evidence, and `src/buoy_search/experimental_baseline.py` bind the one region/plan/artifact/source/namespace/model/revision/cache/license/903-row operation and fail before credential access on mismatch.
- **No live authority:** `APPROVAL_A_GRANTED_RECORD_SHA256` and `APPROVAL_A_GRANTED_PROVENANCE` remain source-pinned to `None`; the four-path live entry point cannot accept caller-supplied authority, model, provider, effects, or attestation. The executor grants neither Approval A nor Approval B.
- **Offline model and zero-retry provider boundary:** live construction sets both offline controls before internally loading the pinned float32 normalized 384-dimensional CLS model, rehashes the immutable cache at the model boundary, and internally constructs locked `turbopuffer==2.4.0` with literal `max_retries=0` and direct non-paginating operations.
- **Fixed operation and accounting limits:** the implementation fixes 26 non-reassignable slots, 10 reads, 16 writes, 904 write-row positions, 1,817 returned-row positions, and zero deletes; accounting precedes physical calls and preserves redacted exact/present markers for success, failure, malformed, timeout, and indeterminate responses.
- **Verification and commit order:** two exact stable 903-row target reads precede the one conditional card write; two exact stable card reads precede the 903-row local commit; partial failures retain/re-observe pending, card, and local-state effects without retry, fallback, rollback, or cleanup delete.
- **Focused and full validation:** `tests/test_experimental_baseline.py` contains 28 fake-backed tests covering exact success, both allowed target states, existing-card states, every immutable/plan gate, malformed accounting, local partial effects, and every one of the 26 failure slots. `.10x/evidence/2026-07-20-experimental-buoy-baseline-executor-implementation.md` records Python 3.11/3.13 ranking and 493-test passes, build success, exact-head hosted CI, diff hygiene, and the no-live attestation.
- **Independent review:** `.10x/reviews/2026-07-20-experimental-buoy-baseline-executor-implementation-review.md` records PASS at `f6cd38dba1bc7cf8fbcb542133ca264e6cb3d61c` and explicitly preserves Approval A/B and C3 as separate blocked authority.

## Residual risk

No real model, SDK resource, remote namespace/card/account response, billing object, retained `/tmp` artifact, or domain state was exercised. These are future-operation facts, not implementation gaps: C3 durably owns the remaining Approval A, compatible-baseline evidence, and Approval B blockers and remains blocked.

## Retrospective

A callable experimental executor is not safely isolated merely because it lacks a CLI: live authority, model/provider/effect construction, retry identity, and post-write evidence must also be non-injectable and source-pinned. Separating fake-only simulation identity from the durable-path live entry point, installing accounting before every physical attempt, and re-observing local partial effects make the fail-closed boundary mechanically reviewable. The focused tests and review preserve these lessons; no separate knowledge or skill record is warranted.
