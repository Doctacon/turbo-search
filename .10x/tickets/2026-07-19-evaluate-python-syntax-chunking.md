Status: blocked
Created: 2026-07-19
Updated: 2026-07-20
Parent: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md
Depends-On: .10x/tickets/2026-07-19-implement-opt-in-python-syntax-chunking.md

# C6: Evaluate Python Syntax Chunking

## Scope

After C5 has an active ratified spec, passing required CI, and exact paired plan counts, evaluate only the specified `current-default`, fixed/breadcrumb, and syntax arms on Buoy, pytest, and Ruff. `current-default` MUST be the actual unchanged 80-entry repository renderer followed by current generic Markdown token split/overlap; pair each isolated Python-aware treatment against it on identical source commits/corpora. Use new namespaces and zero deletes.

## Acceptance criteria

- C5 is complete, focused/full CPython 3.11/3.13 CI is passing, and exact per-arm namespace names, commits, header/source row counts, storage multipliers, and write counts are reported before approval.
- The `current-default` control is proven identical to the ordinary pre-C5 no-arm pipeline; each Python-aware treatment is isolated from generic split/overlap and metadata/card treatments and paired against that control on the same selected corpus.
- Every apply targets a new namespace; no stale or namespace delete occurs; baseline namespaces, catalog, defaults, and local applied state outside the new namespaces remain unchanged.
- Live eval after approved applies is retrieval-only.
- Primary metrics match C4. Also report chunk-count multiplier, mean/p95 chunk tokens, symbol-boundary coverage, and fallback rate by language.
- The three-repo no-regression/positive-average/two-improving-repo rule is only an experiment escalation gate. Stop an arm at the pilot if it fails that gate, exceeds an approved chunk/storage bound, or gains only from the already-completed global metadata preamble. Passing permits only a request for separately approved full-basket experimentation; it is not promotion authority.
- Full-basket expansion requires a separate exact ten-repo forecast and approval; only the full-basket keep gate is governed by the active distribution policy.
- Passing means promotion-candidate evidence only; fixed-line behavior remains the default.

## Approval gate

Blocked until C5 local plans can fill this exact checkpoint:

> Approve up to `<rows>/<new namespaces>/<estimated writes and storage multiplier>` for the ratified Buoy/pytest/Ruff `current-default` control and its paired isolated Python-aware arms on the reported identical commits/corpora, with zero deletes and no catalog/default change?

Past namespace approvals do not authorize these writes. Approval covers only the exact planned commits/arms/counts.

## Stop conditions

- Stop before any live operation without exact approval.
- Stop on commit/corpus mismatch, unapproved/exceeded rows or storage, a failed pilot gate, fallback/coverage behavior that violates the active spec, or any need to delete/mutate a baseline namespace.
- Do not add Tree-sitter unless the Python experiment first passes and a later multilingual need is explicitly ratified.
- Stop before full expansion until its exact incremental forecast is separately approved.

## Evidence expectations

Approval provenance; required CPython 3.11/3.13 CI; paired control/treatment plan and apply summaries; exact header/source rows and writes/deletes; per-arm metrics/resources/fallbacks; retrieval-only proof; review; explicit no-promotion conclusion.

## Blockers

- C5 is open/executable but not complete; its required focused/full CPython 3.11/3.13 CI and exact paired local plans do not yet exist.
- C5 local plans have not yet reported the exact per-arm namespace names, commits, header/source row counts, storage multipliers, and write counts needed for the approval checkpoint.
- No exact syntax namespace-write approval exists.

## Explicit exclusions

Source implementation; behavior shaping; Tree-sitter; baseline mutation/deletion; catalog/default changes; automatic promotion.

## References

- `.10x/specs/repo-python-syntax-chunking-experiment.md`
- `.10x/research/2026-07-19-repo-search-heavy-ranking-experiment-decomposition.md`
- `.10x/tickets/2026-07-19-implement-opt-in-python-syntax-chunking.md`
- `.10x/decisions/repo-ranking-promotion-policy.md`

## Progress and notes

- 2026-07-19: Opened blocked. No namespace names/counts, write budget, live call, or promotion was ratified.
- 2026-07-20: Clarified that the three-repo rule is an experiment escalation gate only, not active promotion policy.
- 2026-07-20: Reconciled C6 with the parent paired-default rule: the required control is the actual unchanged current renderer plus generic split/overlap, and each isolated Python-aware arm must be paired against it on the same corpus. C6 remains blocked on C5 and exact write approval.
- 2026-07-20: The exact seven-item C5 contract is now independently reviewed, user-ratified unchanged, and active. C6 remains blocked on C5 completion, passing exact paired local plans with namespace/row/storage/write counts, and separate exact write approval; no plan, namespace, live operation, or write was authorized.
