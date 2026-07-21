Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/2026-07-20-implement-deterministic-token-budget-source-subdivision.md, .10x/specs/deterministic-treatment-token-budget-subdivision.md, .10x/tickets/2026-07-20-shape-prose-token-budget-compatibility.md, .10x/tickets/2026-07-19-evaluate-python-syntax-chunking.md

# Deterministic Token-Budget Source Subdivision Implementation Evidence

## What was implemented

The two opt-in Python-aware treatment arms now load only a bundled tokenizer-only copy of the exact four pinned BGE tokenizer files at revision `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`. Local planning verifies `transformers==5.12.1`, exact `BertTokenizer` implementation, revision-directory identity, canonical tokenizer-file identity `9c7beccadaa552c323907a895ad9ab188d8b75763022403f72c5d91085334f3b`, and model maximum 512 before processing plan rows. The loader forces offline/no-implicit-token/no-telemetry environment settings, constructs no model, and calls the tokenizer with special tokens enabled and truncation/padding disabled.

`process_syntax_repo_corpus` now renders every candidate through the same production `MarkdownChunk` renderer used for emission and counts its complete `embedding_text`. For each existing `SourceRange`, it tests every candidate end at every cursor, chooses the farthest feasible end, and never crosses the parent. Every child inherits the exact parent breadcrumb tuple; AST/fixed/fallback ownership and LF source payload remain from the parent `SourceChunking`. Compatible parents remain one unchanged source row. Final source indexes are consecutive and existing semantic plan-row identity remains derived from canonical URL, section path, and content.

A complete rendered one-line source payload above 512 raises a sanitized repository/arm/path/line/count/checkpoint diagnostic before any plan object or plan/manifest/chunks artifact can be returned. Unchanged headers and prose are not subdivided; each independently fails when its complete existing final payload is above 512. This deliberately preserves the separate prose blocker.

## Tests added or updated

- `tests/test_treatment_token_budget.py` pins offline tokenizer file/class/max identity and three complete-payload golden counts; verifies exact tokenizer call options; mutation-tests package, revision, file set, implementation, and maximum drift; proves exhaustive selection across a non-monotone failure seam; checks 200 deterministic randomized maximality/coverage cases; and proves an exact 513-token one-line payload is unsplittable.
- `tests/test_github_repo.py` adds end-to-end golden source boundaries `1-19/20-37/38-55/56-73/74-80`, exact counts `506/501/501/501/215`, citations, breadcrumb copying, reconstruction, stable chunk and semantic row identities, sanitized 513-token complete-plan failure without artifacts, and independent unchanged header/prose failure gates.
- Existing syntax, GitHub repository, CLI, plan-artifact, control/no-arm, metadata/card, fallback, and full-suite tests remained passing.

## Validation observed

1. `uv run --python 3.11 python -m unittest discover -s tests` — 516 tests passed in 74.134 seconds.
2. `uv run --python 3.13 python -m unittest discover -s tests` — 516 tests passed in 67.970 seconds.
3. On both CPython 3.11 and 3.13, `scripts/validate_ranking_contract.py` reproduced the same dataset/inventory/source-manifest identities.
4. On both CPython 3.11 and 3.13, `scripts/c6_syntax_forecast.py validate` reproduced blocked readiness `false`, forecast identity `d5199276c19ae89779287eaa90824ce1e1cc684a3f060899f02f65d976016243`, and tokenizer checkpoint `c3a1560e611114760909c110a118a3ce1a60f0527de08c769a85a20b263f4e0f`.
5. `uv build --out-dir /tmp/buoy-token-subdivision-dist` built the sdist and wheel; bounded wheel inspection proved all four offline tokenizer files are packaged. No repository `dist/` artifact was created.
6. `git diff --check` and `python -m compileall -q src tests scripts` passed.

The 3.11 and 3.13 runs execute the same exact golden boundary/count/citation/identity assertions, so their passing results establish runtime parity for the pinned fixtures.

## PR #79 exact-file-set repair validation

Review found that the original canonical identity hashed only the four expected paths and did not reject extra directory entries. The repaired identity path now sorts and enumerates the snapshot directory before hashing, requires its names to equal the exact four-file tuple, requires every entry to be a regular non-symlink file, and only then reads bytes or permits `BertTokenizer.from_pretrained` to run.

A recognized `added_tokens.json` mutation demonstrates the blocker concretely: direct unguarded local loading changes exact tokenization of the pinned test payload from 4 tokens to 3, while both guarded identity calculation and loading reject the snapshot with a file-set identity mismatch before `from_pretrained`. Mutations also reject an unrelated regular file, a subdirectory, and an expected-name symlink. The committed snapshot still computes identity `9c7beccadaa552c323907a895ad9ab188d8b75763022403f72c5d91085334f3b`, retains all prior golden counts and subdivision semantics, and builds into a wheel with exactly the same four tokenizer entries.

Post-repair validation observed:

1. Focused `tests.test_treatment_token_budget tests.test_github_repo` — 33 tests passed on each of CPython 3.11 and 3.13.
2. Full discovery — 518 tests passed on CPython 3.11 in 59.499 seconds and CPython 3.13 in 52.330 seconds.
3. Locked sync plus `scripts/validate_ranking_contract.py` passed on both runtimes with identical dataset/inventory/source-manifest identities.
4. `scripts/c6_syntax_forecast.py validate` passed on both runtimes with unchanged blocked readiness `false`, forecast identity `d5199276c19ae89779287eaa90824ce1e1cc684a3f060899f02f65d976016243`, and tokenizer checkpoint `c3a1560e611114760909c110a118a3ce1a60f0527de08c769a85a20b263f4e0f`.
5. `uv build --out-dir /tmp/buoy-pr79-exact-file-set-dist` passed, and bounded wheel inspection found exactly the four committed tokenizer files.
6. `git diff --check` passed. Preserved forecast JSON, compressed tokenizer report, and validator hashes remain `4f40e8630438e1c1c2dead10c9587711652f695cab458a1f3efff68942ecb2bd`, `7adb1d6e05b2ce9f24ab69468758b867d6d7871221ba5d014090b3088e8fb808`, and `0c3c0dd5d9cda426f4018a5a42a0ef1c759e535dcd1771552839c3a13dac45f8` respectively.
7. Hosted GitHub Actions run `29799849205` passed at repair commit `77016562cac82d34142cf64f03b17c33f0ca75af`: Python 3.11 in 2m03s, Python 3.13 in 1m36s, and distribution build in 12s.

## Preserved C6 checkpoint and local regeneration boundary

The existing local planning flow automatically applies the source subdivision before `MarkdownChunk`/plan finalization. Therefore a separately authorized local C6 forecast regeneration can reuse the existing pinned source acquisition and plan-generation mechanics, then run `scripts/c6_syntax_forecast.py generate-preflight` against the regenerated plan roots. No model is needed for either stage. This implementation task did not run that mutating regeneration because the active ticket explicitly excludes it and the unchanged 366 prose rows must still fail.

Preserved whole-file SHA-256 values after implementation remained:

- forecast JSON: `4f40e8630438e1c1c2dead10c9587711652f695cab458a1f3efff68942ecb2bd`;
- compressed tokenizer report: `7adb1d6e05b2ce9f24ab69468758b867d6d7871221ba5d014090b3088e8fb808`; and
- `scripts/c6_syntax_forecast.py`: `0c3c0dd5d9cda426f4018a5a42a0ef1c759e535dcd1771552839c3a13dac45f8`.

The blocked prose ticket `.10x/tickets/2026-07-20-shape-prose-token-budget-compatibility.md` remains `blocked`. The implementation ticket remains `active` pending independent review. C6 remains blocked and no regenerated forecast identity, count, namespace candidate, or approval is claimed.

## Safety and limits

No dependency or lockfile changed. No embedding model file was bundled, loaded, constructed, or inferred. No credential was read; no provider, retrieval, namespace, catalog, applied-state, default, dataset, delete, evaluation, promotion, or live C6 operation occurred. The exact all-corpus post-subdivision counts and pytest/Ruff individually unsplittable-line counts remain unknown until the separately authorized local regeneration and review.
