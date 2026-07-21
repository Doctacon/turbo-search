Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: PR #75 at `8e146e2106841a90402c8ecbb34ea4ff71dc595e`
Verdict: pass

# Experimental Buoy Baseline Preflight Repair Review

## Findings

Independent review confirmed:

- the canonical 12-file cache authority uses path-sorted compact `path`/`bytes`/`sha256` entries and reproduces the unchanged `5f783ebce23b6ac957d2741399b46e19502b1751acfd3c744b8c41103b138f35` pin without patched expectations;
- exact README hash, `license: mit`, and the Markdown-linked MIT statement are verified;
- immutable raw target/catalog schemas, distances, and returned card-row projections are captured before semantic normalization and emitted separately;
- target/card projections persist across later failures without evidence-only provider requests;
- successful and partial local commits reload persisted applied state and expose its exact hash;
- grant pins, fixed 26-slot/10-read/16-write budgets, 904 write-row and 1,817 returned-row ceilings, zero-delete boundary, and `max_retries=0` remain unchanged;
- exact-head Python 3.11, Python 3.13, focused/full tests, ranking validation, distribution build, and hosted checks pass;
- no live executor, credential, model, retained state, or provider resource was invoked.

## Verdict

Pass. The repair may integrate through a separate session. A fresh complete preflight may proceed only from the exact integrated `develop` commit; live invocation remains prohibited unless every existing preflight gate passes. Approval A remains unchanged and unspent.

## Residual risk

Remote compatibility and current local-state compatibility remain intentionally unobserved until the fresh preflight.
