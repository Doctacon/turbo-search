Status: open
Created: 2026-07-19
Updated: 2026-07-20
Parent: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md
Depends-On: .10x/tickets/done/2026-07-19-freeze-repo-ranking-experiment-contract.md

# C5: Implement Opt-In Python Syntax Chunking

## Scope

Own a local-only, experiment-only Python syntax chunking implementation after an active focused specification defines exact behavior. Preserve the actual current default—fixed 80-entry repository sections followed by generic Markdown token splitting/overlap—and preserve existing `--repo-search-metadata` output/behavior.

The user ratified the complete seven-item syntax contract exactly as independently reviewed at PR #64 pre-ratification head `6f46ef9bb3b925400a6672e67f68dffc74f7872d`. `.10x/specs/repo-python-syntax-chunking-experiment.md` is active and settles the arm identifiers/control pairing, LF coordinates, AST/tokenizer decorator spans, breadcrumbs/ownership, treatment subdivision, common header, distinct control/treatment coverage and citations, fallback, compatibility, validation matrix, and local-only safety behavior. C5 has no unresolved semantic blocker and is executable within that authority.

## Ratified syntax-contract checkpoint

All seven numbered items in the active specification were confirmed unchanged on 2026-07-20. Provenance: `.10x/evidence/2026-07-20-python-syntax-chunking-contract-ratification.md`. Review: `.10x/reviews/2026-07-20-python-syntax-chunking-contract-review.md`.

## Acceptance criteria

- An active focused syntax experiment spec exists and this ticket contains no unresolved behavior.
- Implementation is explicit opt-in, local-plan-capable, standard-library-only unless a later decision says otherwise, and unchanged by default; `current-default` exactly reproduces the pre-C5 80-entry renderer plus generic token split/overlap.
- Each Python-aware arm is isolated from generic split/overlap and metadata/card treatments and is paired against `current-default` on the same commit/corpus.
- Tests cover every ratified LF/AST/tokenizer/header/boundary/fallback/coverage scenario, distinguish control originating-section citations from exact treatment final-chunk citations, and prove complete treatment source-order coverage with no unintended omission or duplication.
- Focused and full tests pass in the required CI matrix on CPython 3.11 and 3.13; one local runtime is not sufficient closure evidence.
- Local paired plans record commit, selected files, header/source chunks and rows, multipliers, and zero remote calls/writes.
- No namespace, catalog, applied state, dataset, label, or default changes occur.

## Stop conditions

- Implement only the exact active syntax contract; stop and return to shaping if implementation exposes a semantic gap or requires changing it.
- Stop if exact current-default parity, LF-coordinate treatment coverage, tokenizer-owned decorator spans, mandatory common-header parity, or the distinct control/treatment citation contracts cannot be implemented and tested.
- Do not add Tree-sitter or multilingual parser dependencies without a later explicit need and decision.
- Do not live-apply from this child.

## Evidence expectations

Ratification provenance, active focused spec, focused/full CPython 3.11/3.13 CI results, golden current-default parity, LF/AST/tokenizer/header coverage assertions, paired local plan/preflight summaries, diff review, and no-live-call proof.

## Blockers

None. The seven-item contract is user-ratified, independently reviewed, and active; C5 is open and executable with no unresolved semantics.

## Explicit exclusions

Live retrieval or writes; namespace/catalog/default mutation; Tree-sitter; multilingual product support; repeating the completed global metadata experiment; public product promotion.

## References

- `.10x/specs/repo-python-syntax-chunking-experiment.md`
- `.10x/evidence/2026-07-20-python-syntax-chunking-contract-ratification.md`
- `.10x/reviews/2026-07-20-python-syntax-chunking-contract-review.md`
- `.10x/research/2026-07-19-repo-search-heavy-ranking-experiment-decomposition.md`
- `.10x/research/2026-06-28-repo-search-precision-state-of-art.md`
- `.10x/research/2026-06-28-expanded-validation-ranking-hypotheses.md`
- `.10x/tickets/done/2026-06-28-repo-searchable-path-symbol-metadata.md`

## Progress and notes

- 2026-07-19: Opened blocked. Inspection found the hypothesis record-backed but the exact behavior insufficient for an active spec; no spec, source, tests, plans, or live operations were created.
- 2026-07-20: C1 closed. C5 remains blocked only on its separately required exact syntax-contract ratification and active focused spec; C1 closure authorized no implementation.
- 2026-07-20: Inspected the current 80-line repository renderer, regex metadata breadcrumbs, downstream token/overlap chunking, manifest citation fields, and CPython 3.11 AST spans. Drafted the exact seven-item recommended contract in `.10x/specs/repo-python-syntax-chunking-experiment.md`. No source, tests, plans, dependencies, model loads, live calls, writes, deletes, state, datasets, defaults, or parent-ticket content changed; C5 remains blocked.
- 2026-07-20: Repaired PR #64's record-contract blockers: the paired control is now the actual current renderer plus generic split/overlap; treatment coordinates are LF-only with standard-library tokenizer-owned decorator introducers/spans; treatment final-chunk coverage is separated from control originating-section citations; the identical non-source repository header is mandatory and counted explicitly; and validation requires focused/full CPython 3.11/3.13 CI. The spec remains draft and C5 remains blocked; no implementation, tests, dependencies, plans, live operations, defaults, or product behavior changed.
- 2026-07-20: Independent review passed PR #64 pre-ratification head `6f46ef9bb3b925400a6672e67f68dffc74f7872d`; the user then ratified all seven items exactly as reviewed. Activated the unchanged contract and moved C5 from blocked to open/executable with no unresolved semantics. No syntax source/tests, dependencies, local plans, model/credential access, live operations, writes/deletes, state, datasets, defaults, or product behavior changed.
