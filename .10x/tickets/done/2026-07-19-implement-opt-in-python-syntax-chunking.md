Status: done
Created: 2026-07-19
Updated: 2026-07-20
Parent: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md
Depends-On: .10x/tickets/done/2026-07-19-freeze-repo-ranking-experiment-contract.md

# C5: Implement Opt-In Python Syntax Chunking

## Outcome

Completed the exact ratified local-only Python syntax chunking implementation. Independent review passed PR #69 head `360c6b9c666ccf432c082ac44d0a1400955ce3e9`; the ordinary no-arm path remains unchanged, the three explicit arms are locally plan-capable, and no live operation, namespace/catalog/applied-state mutation, dataset/label/default change, or promotion occurred. C5 completion satisfies only C6's implementation dependency and grants no C6 planning, write, apply, retrieval, or promotion authority.

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

None for the closed C5 outcome. The seven-item contract is user-ratified and active, the implementation passed independent review, and C5 is done. C6's separate exact pilot-forecast and write-approval blockers are not C5 blockers.

## Explicit exclusions

Live retrieval or writes; namespace/catalog/default mutation; Tree-sitter; multilingual product support; repeating the completed global metadata experiment; public product promotion.

## References

- `.10x/specs/repo-python-syntax-chunking-experiment.md`
- `.10x/evidence/2026-07-20-python-syntax-chunking-contract-ratification.md`
- `.10x/evidence/2026-07-20-python-syntax-chunking-local-paired-plans.md`
- `.10x/evidence/2026-07-20-python-syntax-chunking-implementation-validation.md`
- `.10x/reviews/2026-07-20-python-syntax-chunking-contract-review.md`
- `.10x/reviews/2026-07-20-python-syntax-chunking-implementation-review.md`
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
- 2026-07-20: Implemented the three opt-in arms under the active contract with standard-library AST/tokenizer boundaries, isolated exact treatment chunks, unchanged explicit control/no-arm behavior, compatibility rejection, sanitized fallbacks, and fail-closed invariants. Added focused LF/decorator/nesting/ownership/trivia/80-line/header/citation/fallback/control/CLI/plan tests; focused/full suites and the frozen-contract validator pass locally on CPython 3.11 and 3.13, and PR #69 hosted Python 3.11/Python 3.13/distribution CI passed on the implementation commit. Recorded same-commit three-file paired local plan/count evidence in `.10x/evidence/2026-07-20-python-syntax-chunking-local-paired-plans.md` and local matrix/build evidence in `.10x/evidence/2026-07-20-python-syntax-chunking-implementation-validation.md`. C5 is active pending independent implementation review; C6 remains blocked and no model, credential, remote retrieval, namespace/catalog/state write, delete, default, dataset, or label change occurred.
- 2026-07-20: Repaired only PR #69 review blockers in commit `b5588aa48c8d916e8ff50eb3d77a2ab4403bd0dc`: explicit `current-default` now rejects any generic `--max-chunks` result that omits a selected code file's one header or any expected source chunk; acquisition-level CRLF/no-final-LF coverage and bounded end-to-end `plan --repo-chunking-arm` artifact coverage were added without changing the no-arm artifact contract. Focused 72-test and full 465-test suites plus the frozen-contract validator pass sequentially on CPython 3.11 and 3.13; distribution build and hosted run `29771927189` passed. C5 remains active for the required independent review; nothing was closed, merged, applied, or promoted.
- 2026-07-20: Independent review passed PR #69 head `360c6b9c666ccf432c082ac44d0a1400955ce3e9` with no blocker. Closed and moved C5 to `done`; mechanically repaired active references. This satisfies only C6's C5 dependency. The exact Buoy/pytest/Ruff pilot forecast/count checkpoint and separate namespace-write approval remain absent, so C6 remains blocked and no live plan/apply/retrieval or promotion occurred.

## Closure mapping

- **Active exact contract:** `.10x/specs/repo-python-syntax-chunking-experiment.md`, its ratification evidence, and contract review establish the unchanged three-arm, LF/AST/tokenizer/header/coverage/fallback/compatibility/safety authority.
- **Explicit opt-in and current-default parity:** `src/buoy_search/cli.py`, `src/buoy_search/github_repo.py`, and `src/buoy_search/repo_syntax_chunking.py`, exercised by `tests/test_cli.py`, `tests/test_github_repo.py`, and `tests/test_repo_syntax_chunking.py`, preserve the ordinary no-arm path and implement only explicit standard-library arms. Explicit `current-default` fails closed on an incomplete selected-file header/source sequence.
- **Treatment isolation and exact coverage:** focused tests prove metadata/card incompatibility, no downstream generic split/overlap for treatments, LF-vector adjacency/reconstruction, decorator and nested ownership, deterministic subdivision, header equality, exact treatment citations, and sanitized whole-file fallbacks.
- **Required runtime matrix and build:** `.10x/evidence/2026-07-20-python-syntax-chunking-implementation-validation.md` records focused/full/ranking passes on CPython 3.11 and 3.13, distribution build success, and passing hosted Python 3.11/Python 3.13/distribution checks.
- **Local paired plans:** `.10x/evidence/2026-07-20-python-syntax-chunking-local-paired-plans.md` binds all three arms to local Buoy commit `7b64aa12e473dd33bfd9c885aa0a07b54809c6cb`, the same three selected files, exact header/source/total rows and byte multipliers, zero fallbacks, and zero remote calls/writes.
- **Safety and unchanged defaults:** the implementation/evidence diff contains no dependency, lockfile, dataset, label, default, namespace, catalog, or applied-state mutation. Local generated artifacts and distribution outputs remained outside the repository.
- **Independent review:** `.10x/reviews/2026-07-20-python-syntax-chunking-implementation-review.md` records PASS at `360c6b9c666ccf432c082ac44d0a1400955ce3e9` and explicitly preserves C6's separate planning and write gates.

## Residual risk

The bounded three-file local paired plans are C5 implementation evidence, not the exact Buoy/pytest/Ruff C6 pilot forecast. Exact pilot commits/corpora, namespace names, selected-file and header/source row counts, storage multipliers, and write counts remain unreported, and no exact namespace-write approval exists. C6 owns these blockers and remains blocked. Tests, tracked artifacts, and review also cannot prove absence of every unlogged external action; the no-live-operation claim is bounded by the recorded procedure, diff, and contemporaneous attestation.

## Retrospective

Two closure-critical invariants required fail-closed tests rather than plausible equivalence: an explicit control must reject truncation anywhere in the complete selected-file sequence, and newline behavior must be tested through acquisition rather than only on already-normalized helper inputs. The final bounded CLI artifact test also demonstrates that unit-level chunk assertions are insufficient without one end-to-end written-plan path. These lessons are captured in the implementation tests, validation evidence, and review; no separate knowledge or skill record is warranted.
