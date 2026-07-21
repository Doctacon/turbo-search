Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: PR #76 at commit `581d9ec79ed5426dbc174e0373805c674d79184c`
Verdict: pass

# Deterministic Token-Budget Subdivision Contract Review

## Target and method

Independent adversarial review of PR #76 pre-ratification head `581d9ec79ed5426dbc174e0373805c674d79184c` against `origin/develop` at `f851366`. The review inspected the complete focused draft, its shaping ticket and evidence, the active Python syntax contract, the blocked C6 ticket and preserved tokenizer checkpoint, the current source-range/rendering/identity boundaries cited by the draft, the record-only diff, and hosted checks.

This review covers only the exact source-only subdivision contract and whether it is precise enough to activate and hand to one bounded implementation ticket. It does not review an implementation, regenerated plans, prose behavior, namespaces, or writes because none exists in PR #76.

## Findings

- The tokenizer decision is exact and fail closed: immutable BGE revision, tokenizer-file identity, locked implementation, maximum 512, special tokens enabled, and truncation/padding disabled. Every decision counts the complete production-rendered embedding payload rather than source text alone.
- Exhaustive farthest-feasible prefixes are deterministic without assuming token-count monotonicity. Children remain inside one existing treatment parent, retain its exact breadcrumb/fallback/ownership semantics, and cover the parent’s LF physical lines exactly once with payload-accurate citations.
- The one-line failure boundary is complete and sanitized: one over-limit rendered physical line aborts the complete repository/arm plan with no truncation, fallback, omission, source disclosure, or partial artifact.
- Identity and order are specified through existing semantic row identity, consecutive final indexes, stable parent/file/header/prose order, and mandatory regeneration of affected artifact/count/namespace identities rather than projections from the obsolete plan.
- Isolation is explicit: common headers, prose, `current-default`, ordinary no-arm, metadata/cards, and generic split/overlap behavior remain unchanged; no model construction/inference or live surface is authorized.
- The exact checkpoint decomposition is internally consistent: 20,926 incompatible source plan rows plus 366 incompatible unchanged prose plan rows equals 21,292. The source-only contract does not claim to resolve prose.
- The 366 prose plan rows remain an independent fail-closed C6 stop and require a separate blocked shaping owner. Activating this source contract and opening its implementation ticket cannot make C6 executable or approval-ready.
- The downstream implementation and validation requirements cover tokenizer identity/options, exact overhead, non-monotone selection, coverage, composition, one-line/headers/prose failure, identity/order, isolation, CPython 3.11/3.13 parity, and no-live-operation safety.
- PR #76’s hosted Python 3.11, Python 3.13, and distribution-build checks passed on the reviewed head. The diff contains records only; no source, tests, plans, preserved forecast artifacts, validator, dependency, lockfile, namespace, or live state changed.

### Blockers

None for exact contract ratification, activation, and creation of one bounded source-only implementation ticket. Prose behavior remains unresolved by design and must not be inferred into that ticket. C6 remains blocked.

## Verdict

PASS. The focused source-only contract at `581d9ec79ed5426dbc174e0373805c674d79184c` may be activated without changing its tokenizer, payload, boundary, coverage, citation, breadcrumb/ownership, failure, identity/order, isolation, regeneration, or safety semantics. One bounded implementation ticket may be opened from that active authority.

This pass does not authorize prose subdivision, source/test implementation in the ratification turn, forecast or artifact regeneration, model construction/inference, credentials/provider access, namespace/catalog/applied-state/default operations, retrieval, deletes, evaluation, promotion, or C6 writes.

## Exact reviewed user checkpoint

The exact confirm-or-correct checkpoint is the block under `## User-legible confirm-or-correct checkpoint` in `.10x/specs/deterministic-treatment-token-budget-subdivision.md` at reviewed commit `581d9ec79ed5426dbc174e0373805c674d79184c`. Ratification must preserve it unchanged and must explicitly acknowledge that the 366 incompatible prose plan rows remain a separate fail-closed C6 blocker.

## Residual risk

No source implementation or focused/full CPython runtime validation exists. Pinned pytest and Ruff sources were unavailable for the shaping probe, so all-corpus individually unsplittable-line counts remain unknown. Exact final plan/artifact identities and row/storage/write counts cannot exist before implementation and separately authorized regeneration. The unchanged 366 prose plan rows independently prevent tokenizer-ready C6 plans.
