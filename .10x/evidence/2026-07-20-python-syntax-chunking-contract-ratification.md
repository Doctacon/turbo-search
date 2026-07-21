Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/specs/repo-python-syntax-chunking-experiment.md, .10x/tickets/done/2026-07-19-implement-opt-in-python-syntax-chunking.md, .10x/tickets/2026-07-19-evaluate-python-syntax-chunking.md, .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md, .10x/reviews/2026-07-20-python-syntax-chunking-contract-review.md

# Python Syntax Chunking Contract Ratification

## What was observed

PR #64 pre-ratification head `6f46ef9bb3b925400a6672e67f68dffc74f7872d` contains the complete seven-item Python syntax chunking contract. Independent review recorded PASS with no unresolved semantics in `.10x/reviews/2026-07-20-python-syntax-chunking-contract-review.md`.

The user explicitly ratified all seven items exactly as reviewed on 2026-07-20. The ratification activates `.10x/specs/repo-python-syntax-chunking-experiment.md` without changing its three arms, current-default pairing, LF-coordinate model, AST/tokenizer decorator spans, breadcrumb/ownership rules, treatment subdivision, common header, distinct control/treatment coverage and citations, fallback behavior, compatibility, CI matrix, or local-only safety contract.

The syntax-contract checkpoint is therefore satisfied. C5 moved from `blocked` to `open` and is executable with no unresolved semantics. C6 remains `blocked` on C5 completion, required focused/full CPython 3.11/3.13 CI, exact passing paired local plans with namespace/row/storage/write counts, and separate exact write approval.

## Procedure

1. Reviewed the exact contract at PR #64 commit `6f46ef9bb3b925400a6672e67f68dffc74f7872d`; findings and PASS are recorded in `.10x/reviews/2026-07-20-python-syntax-chunking-contract-review.md`.
2. Recorded the user's exact ratification of all seven numbered items.
3. Changed the specification status from `draft` to `active` and replaced only obsolete proposal/activation-gate prose; the reviewed behavioral and acceptance contract was preserved.
4. Changed C5 from `blocked` to `open`, removed its satisfied semantic blockers, and recorded that it is executable only under the active contract.
5. Kept C6 `blocked` and made its remaining C5/local-plan/write-approval blockers explicit.
6. Incorporated current `origin/develop` through commit `420f4aef4bc7fd0886f5547bfdd76e92b358fd5c`, including merged PR #62, before ratification edits.

## What this supports

This supports treating the exact reviewed syntax contract as active authority and assigning bounded C5 implementation without another semantic checkpoint. It also supports keeping C6 blocked until C5 produces passing implementation evidence and exact local plans and the user separately approves the reported writes.

## Safety observation

This ratification turn changed records only. It did not implement syntax source/tests, add dependencies, generate local plans, load a model, read credentials, call GitHub for acquisition, contact a retrieval/provider service, create/write/delete a namespace, mutate catalog/applied state, change datasets or labels, change defaults, or promote product behavior.

## Limits and residual risk

No syntax implementation, focused/full syntax validation, paired local plan, row/storage forecast, namespace identity, write approval, live evaluation, or promotion evidence exists yet. C5 remains open rather than done. C6 and all live/write behavior remain blocked.
