Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: PR #70 at `f6cd38dba1bc7cf8fbcb542133ca264e6cb3d61c`
Verdict: pass

# Experimental Buoy Baseline Executor Implementation Review

## Target

Independent adversarial review of PR #70 at reviewed head `f6cd38dba1bc7cf8fbcb542133ca264e6cb3d61c`, governed by `.10x/specs/experimental-buoy-baseline-executor.md` and `.10x/tickets/done/2026-07-20-implement-experimental-buoy-baseline-executor.md`.

## Findings

Independent review reached PASS with no blocker:

- the implementation is isolated in a non-default module with no CLI, ordinary apply, retrieval, catalog, or default route;
- the live entry point accepts only four durable keyword-only paths and remains mechanically unavailable because `APPROVAL_A_GRANTED_RECORD_SHA256` and `APPROVAL_A_GRANTED_PROVENANCE` are source-pinned to `None`; a caller cannot inject a model, provider, local effects, approval boolean, or attestation;
- the separate simulation entry point requires simulation-only provider identity and cannot report live SDK or zero-retry attestation;
- live execution revalidates the exact plan, source, artifact, namespace, row identities, empty local state, immutable cache revision/manifest/README/license, and prepared rows/card/state before credential access; both offline controls precede the internally constructed pinned float32 normalized 384-dimensional CLS model;
- the locked `turbopuffer==2.4.0` client is internally constructed with literal `max_retries=0`, exposes only direct metadata/query/write operations, and contains no retry, schema/signature fallback, pagination, delete, cleanup-delete, or rollback-delete path;
- the ledger fixes all 26 non-reassignable slots, 10 reads, 16 writes, 904 write-row positions, 1,817 returned-row positions, and zero deletes, with accounting installed before every physical call and malformed/attached exception accounting preserved in redacted evidence;
- exact write counts and affected IDs, response object shapes, schema/distance, stable target/card reads, 903 intended row identities/attributes/vectors, card revision, pending retention, and local commit ordering fail closed;
- the 28 focused fake-backed tests include exact success, absent/verified-empty target states, existing-card states, immutable and plan gates, malformed accounting, timeout/indeterminate outcomes, local partial effects, and forced failure in every one of the 26 slots without retry or reassignment;
- CI-equivalent Python 3.11 and 3.13 ranking/full-suite runs each passed 493 tests, distribution build and diff hygiene passed, and PR #70 hosted run `29774022595` passed Python 3.11, Python 3.13, and Build distributions at the reviewed head;
- no dependency, lockfile, ordinary behavior, dataset, label, default, namespace, catalog, pending, or DuckDB domain-state change is present beyond the bounded executor and the optional timestamp accepted by the existing pending-confirmation primitive.

## Verdict

PASS. The bounded implementation satisfies its ticket and may close. This pass applies only to PR #70 head `f6cd38dba1bc7cf8fbcb542133ca264e6cb3d61c`. It does not grant Approval A or Approval B, authorize a credential read, model load/inference, provider call, baseline operation, domain-state mutation, C3 retrieval, promotion, merge, or default change.

## Residual risk and attestation limit

No real SDK resource, remote namespace/card/account response, billing object, model runtime, retained `/tmp` plan/cache, or domain state was exercised by this review. Those remain future-operation facts that only a separately granted Approval A and its required post-run evidence could establish. The exact Approval A grant would require a later reviewed source change to pin durable grant-record bytes and provenance; both pins remain `None`. C3 remains blocked on separately granted Approval A, compatible-baseline evidence, and separately granted Approval B.
