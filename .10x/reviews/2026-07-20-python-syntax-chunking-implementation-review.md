Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Target: PR #69 at `360c6b9c666ccf432c082ac44d0a1400955ce3e9`
Verdict: pass

# Python Syntax Chunking Implementation Review

## Target

Independent adversarial review of PR #69 at reviewed head `360c6b9c666ccf432c082ac44d0a1400955ce3e9`, governed by `.10x/tickets/done/2026-07-19-implement-opt-in-python-syntax-chunking.md` and `.10x/specs/repo-python-syntax-chunking-experiment.md`.

## Findings

Independent review reached PASS with no blocker:

- the implementation is bounded to the three ratified arms, keeps the ordinary no-arm path unchanged, uses only standard-library `ast`/`tokenize`, and rejects incompatible metadata/card combinations before corpus generation;
- explicit `current-default` preserves the fixed 80-entry renderer plus generic split/overlap and fails closed if a selected code file loses its single common header or any expected generic source chunk;
- Python-aware arms preserve LF-coordinate source coverage, decorator and nested-owner boundaries, deterministic 80-line subdivision, exact treatment citations, sanitized whole-file fallback, and fail-closed unexpected-error behavior;
- focused tests cover the required coordinate, decorator, nesting, ownership, trivia, header, coverage, citation, fallback, default-parity, CLI, and written-plan paths, including acquisition-normalized CRLF and later-file control truncation;
- the reviewed evidence records sequential focused/full/ranking validation on CPython 3.11 and 3.13, distribution build success, passing hosted Python 3.11/Python 3.13/distribution checks, and a clean bounded source/test/record diff;
- same-commit local paired-plan evidence reports the selected files, commit, header/source rows, total rows, content bytes, multipliers, fallback counts, and zero remote calls/writes for all three arms;
- no dependency, lockfile, default, dataset, label, namespace, catalog, or applied-state change is present, and no C6 live operation or approval is implied.

## Verdict

PASS. C5 satisfies its implementation acceptance criteria and may close. The pass applies only to the reviewed PR #69 head and does not authorize C6 planning against the Buoy/pytest/Ruff pilot, any live apply or retrieval, namespace writes/deletes, catalog/default mutation, or promotion.

## Subsequent citation-contract correction

The PASS remains valid for C5's exact output-parity implementation. It did not establish that every control row has a parseable line-range component. The later pinned C6 Ruff corpus found 2,722 exactly ordinary-equivalent control rows across 170 paths without one; the user-ratified superseding spec now states that `current-default` preserves that exact existing behavior while treatment arms still require exact ranges. No C5 source/output change was required or made.

## Residual risk and attestation limit

The recorded paired plans cover only a bounded three-file local Buoy corpus, not the exact C6 Buoy/pytest/Ruff pilot forecast. Exact pilot repository commits/corpora, namespace names, selected-file and header/source row counts, storage multipliers, and write counts remain unreported, and exact write approval remains ungranted. Local artifacts, tests, diff inspection, and hosted checks cannot retroactively prove absence of every unlogged external action; the no-live-operation conclusion remains bounded by the tracked implementation, recorded procedure, and contemporaneous operator attestation. C6 retains durable ownership of both residuals and remains blocked.
