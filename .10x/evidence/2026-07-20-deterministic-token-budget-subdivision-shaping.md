Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/2026-07-20-shape-deterministic-token-budget-subdivision.md, .10x/specs/deterministic-treatment-token-budget-subdivision.md, .10x/tickets/2026-07-19-evaluate-python-syntax-chunking.md

# Deterministic Token-Budget Subdivision Shaping Evidence

## What was observed

The preserved exact tokenizer-only report remains checkpoint `c3a1560e611114760909c110a118a3ce1a60f0527de08c769a85a20b263f4e0f`. It pins `BAAI/bge-small-en-v1.5@5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`, tokenizer-files identity `9c7beccadaa552c323907a895ad9ab188d8b75763022403f72c5d91085334f3b`, `model_max_length=512`, `add_special_tokens=true`, and `truncation=false`. Its exact result remains 21,292 incompatible treatment plan rows across 4,162 paths, maximum 12,785 tokens.

Read-only decomposition of the report's existing `incompatible_rows` found:

| Repository / arm | Source rows >512 | Prose rows >512 | Total |
|---|---:|---:|---:|
| Buoy / fixed breadcrumbs | 232 | 0 | 232 |
| Buoy / AST | 123 | 0 | 123 |
| pytest / fixed breadcrumbs | 689 | 9 | 698 |
| pytest / AST | 199 | 9 | 208 |
| Ruff / fixed breadcrumbs | 10,047 | 174 | 10,221 |
| Ruff / AST | 9,636 | 174 | 9,810 |
| **Total** | **20,926** | **366** | **21,292** |

The source rows represent 11,427 unique `(repository,row_id)` values across 4,111 repository-qualified paths and 4,105 distinct unqualified `repo_path` strings. Six source path strings occur in more than one repository. The prose rows represent 183 unique `(repository,row_id)` values across 57 paths; each is repeated in both treatment plans because the prose path is unchanged. Source and prose path strings are disjoint, so `4,105 + 57` matches the report's exact 4,162-path-string union. This disproves any claim that physical-source-line subdivision alone can clear the preserved C6 checkpoint. `.10x/specs/deterministic-treatment-token-budget-subdivision.md` therefore leaves prose behavior unchanged and records all 366 plan rows as an independent fail-closed blocker.

Current source establishes the exact rendered accounting boundary:

- `src/buoy_search/repo_syntax_chunking.py` produces ordered, adjacent, at-most-80-line `SourceRange` values and exact LF payload slices;
- `src/buoy_search/github_repo.py` renders optional `Symbol breadcrumbs`, a whole-file-safe fence/language, exact source payload, and `Lines S-E` section path;
- `src/buoy_search/chunker.py` renders embedding text as nonempty `Title:`, `Section:`, and content parts joined by double LF; and
- `src/buoy_search/plan_artifacts.py` derives semantic row identity from site/canonical URL/section/content rather than chunk index.

The draft consequently counts the complete final embedding payload for every candidate end and chooses the farthest exactly feasible prefix inside each existing parent range. It does not assume token-count monotonicity, cross active fixed/ownership boundaries, recompute breadcrumbs, or change source coordinates.

### Read-only individually unsplittable-line probe

The Buoy pinned source commit `fcb7abbe1652d2eab4ee23816b6d992d893603ac` was present in the local git object database. A read-only tokenizer-only probe inspected all 46 selected Buoy code files (the other 11 of 57 selected files are Markdown/prose) from that exact commit, verified every inspected text SHA-256 against the preserved selected-file checkpoint, ran the active treatment range construction, inherited each parent range's exact breadcrumb tuple, rendered every individual physical line with its exact candidate title/section/fence/language/special-token overhead, and used the pinned offline tokenizer with no truncation.

Observed candidate one-line failures in Buoy:

| Arm | Individually over-limit line instances | Paths | Maximum one-line rendered tokens |
|---|---:|---:|---:|
| `fixed-80-python-breadcrumbs` | 0 | 0 | N/A |
| `python-ast` | 0 | 0 | N/A |

This is a bounded shaping observation, not an all-corpus forecast. The pinned pytest and Ruff commits and original exact plan roots were not present locally, and the preserved token report intentionally contains row identities/counts rather than source content. No network fetch was permitted or attempted. Their individually unsplittable-line counts remain unknown until a separately authorized regeneration has exact pinned local sources/plans. The draft fails closed rather than treating the Buoy zero as evidence for pytest/Ruff.

## Procedure

1. Ran the required branch/status and worktree inspection.
2. Read the shaping ticket, active syntax specification, blocked C6 ticket, preserved forecast narrative/machine checkpoint/token report, C6 validator, and current renderer/range/embedding/row-identity source.
3. Read the gzip token report with the standard library and counted existing incompatible entries by repository, arm, and row class. No artifact was rewritten.
4. Reused the already-cached exact tokenizer snapshot in offline mode through the existing locked environment. Constructed only `BertTokenizer`; no embedding model was constructed and no inference ran.
5. Read Buoy source blobs from the local git object database at the pinned commit, verified source hashes, and printed aggregate one-line compatibility counts to stdout. No source checkout, plan, report, cache, or project artifact was created.
6. Drafted one inactive focused specification and updated only shaping/C6 records. No source, tests, active specification, preserved forecast/token artifact, validator, namespace, state, dataset, or default changed.

## Preserved-artifact attestation

Before record edits, whole-file SHA-256 values were:

- forecast JSON: `4f40e8630438e1c1c2dead10c9587711652f695cab458a1f3efff68942ecb2bd`;
- compressed tokenizer report: `7adb1d6e05b2ce9f24ab69468758b867d6d7871221ba5d014090b3088e8fb808`; and
- `scripts/c6_syntax_forecast.py`: `0c3c0dd5d9cda426f4018a5a42a0ef1c759e535dcd1771552839c3a13dac45f8`.

Post-edit validation MUST reproduce these exact hashes and the existing validator's blocked-checkpoint output. The embedded forecast hash remains `d5199276c19ae89779287eaa90824ce1e1cc684a3f060899f02f65d976016243`; the compressed file's whole-file hash is distinct from the embedded canonical checkpoint by design.

## What this supports or challenges

This supports exhaustive farthest-feasible physical-line prefixes as a small deterministic post-range mechanism: active parents contain at most 80 lines, complete overhead can be rendered exactly, and exact treatment coverage/citations/ownership can be retained without generic splitting or truncation.

It challenges treating the requested mechanism as a complete C6 fix. Exactly 366 incompatible plan rows are on the unchanged prose path and have no treatment `SourceRange` contract. Inventing prose subdivision would widen this shaping scope and change active prose behavior. They remain explicitly unresolved and keep C6 blocked.

## Validation boundary and residual risk

This is record-only shaping evidence. It does not prove implementation correctness, all-corpus unsplittable-line absence, final row/storage counts, package behavior on both CI runtimes, or namespace readiness. The proposed algorithm, inherited-breadcrumb rule, complete-plan failure scope, and source-only boundary remain unratified. Independent review and explicit confirm-or-correct ratification are required before active-spec or implementation work.

No model/dependency download or install, model construction/inference, credential/provider access, namespace/retrieval/catalog/applied-state/default operation, delete, evaluation, promotion, active-spec/source/test/CI/forecast/token-report/validator mutation, or live plan/apply occurred.
