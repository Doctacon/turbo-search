Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: PR #64 at commit `6f46ef9bb3b925400a6672e67f68dffc74f7872d`
Verdict: pass

# Python Syntax Chunking Contract Review

## Target and method

Independent adversarial review of PR #64 pre-ratification head `6f46ef9bb3b925400a6672e67f68dffc74f7872d`. The review inspected the complete draft specification, C5/C6 tickets, parent paired-default authority, current repository renderer and generic split/citation boundaries recorded in the spec, required CPython matrix, and record-only diff scope.

This review concerns only whether the exact seven-item contract is sufficiently precise for ratification and bounded C5 implementation. It does not review syntax source/tests, local plans, namespaces, experiment results, or promotion because none exists in this change.

## Findings

- The three arms are exact and non-overlapping. `current-default` is the actual unchanged fixed-80-entry renderer plus generic 300-token/up-to-two-sentence overlap path, and both Python-aware treatments must pair against it on the same commit/corpus.
- The treatment coordinate model is deterministic: one-based LF-only physical rows after universal-newline acquisition, no terminal-LF row, form-feed retained within a row, and fail-closed post-acquisition bare carriage returns.
- Standard-library `ast` and `tokenize` are sufficient and exclusively authorized. Symbol kinds, Python 3.11 grammar, decorator introducer matching, complete multiline decorator ownership, count/coordinate invariants, and unexpected-failure behavior are explicit.
- Fixed-window breadcrumbs, innermost AST ownership, module ownership, nested carving, forward-except-at-EOF trivia attachment, deterministic 80-line subdivision, zero overlap, and no generic treatment split leave no unresolved boundary choice.
- The identical per-file non-source header is required in all arms and counted separately. Treatment final chunks have exact LF-vector coverage and payload-accurate `Lines S-E` citations; the control correctly retains only originating-section citations and must prove exact pre-C5 parity.
- Parse and non-Python fallbacks are whole-file, isolated fixed/no-breadcrumb treatments with explicit sanitized counts. Unexpected tokenizer, coordinate, and runtime failures stop rather than silently downgrade.
- Default, metadata/card compatibility, local-only safety, standard-library-only dependencies, focused/full CPython 3.11/3.13 CI, and no-live-operation boundaries are explicit. C6 retains separate plan and write approval gates.

No blockers or unresolved semantics were found in the reviewed seven-item contract.

## Verdict

PASS. The specification at `6f46ef9bb3b925400a6672e67f68dffc74f7872d` is precise enough to activate unchanged after explicit user ratification and to make C5 open/executable. This pass does not authorize syntax implementation in the ratification record turn, C6 execution, local-plan inference, model or credential access, live operations, namespace writes/deletes, catalog/default changes, or promotion.

## Residual risk

- The contract has not been implemented or validated against focused/full CPython 3.11/3.13 syntax tests.
- Exact paired local plan rows, namespace names, storage multipliers, and write counts do not exist; C6 therefore remains blocked.
- If C5 implementation exposes a semantic gap, it must stop and return to shaping rather than revise this active contract silently.
