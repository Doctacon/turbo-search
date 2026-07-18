Status: recorded
Created: 2026-07-18
Updated: 2026-07-18
Target: commits `2bbd525`, `59e2def`, and `8e8f602`
Verdict: pass

# Remote Routing Backend Review

## Findings

Initial review rejected the inert backend for pre-write target validation gaps, unbounded cyclic pagination, arbitrary-vector safe rebase, single-read accept-remote validation, insufficient independent schema fixtures, ambiguous zero-eligible handling, and provider payload exposure.

Repairs now:

- reject cross-region, reserved-target, duplicate-target, and duplicate-ID mutations before provider writes;
- bound namespace/card pagination and reject repeated cursors/signatures and non-advancing data;
- preserve exact base projection when semantics are unchanged and recompute changed manual semantics through an injected projector;
- validate first-apply manual races under the same exact source/retrieval constraints;
- require two identical valid strong-read cards at the exact operator-approved revision;
- distinguish management snapshots from routing reads that require an eligible card;
- test all 29 remote attributes against an independent literal schema fixture;
- suppress provider exception chaining so formatted tracebacks cannot expose credentials, vectors, or response bodies.

The final focused suite passed 23 tests. Existing catalog/pending/routing compatibility passed 59 tests. Prior implementation evidence records 382 full tests passing on Python 3.11 and 3.13, plus successful distribution builds. Hosted CI remains the final integration gate.

## Verdict

Pass. The module remains inert: no public CLI, apply, retrieval, documentation, credential, network, or local catalog behavior is wired or changed.

## Residual risk

Provider behavior is validated against installed SDK 2.4.0 request/response contracts and fakes, not live state. The atomic cutover ticket owns fail-closed hosted preflight and all authorized live mutations.
