Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/done/2026-07-19-implement-opt-in-python-syntax-chunking.md, .10x/specs/repo-python-syntax-chunking-experiment.md

# Python Syntax Chunking Local Paired Plans

## What was observed

The three ratified arms produced deterministic in-memory local plan artifacts over the same three-file Python corpus from local Buoy commit `7b64aa12e473dd33bfd9c885aa0a07b54809c6cb`. The selected files were exactly:

- `src/buoy_search/chunker.py`
- `src/buoy_search/plan_artifacts.py`
- `tests/test_chunker.py`

| Arm | Planned namespace | Header rows | Source rows | Total rows | Content bytes | Row multiplier | Content-byte multiplier | Python parse fallbacks | Non-Python fallbacks |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `current-default` | `github-doctacon-buoy-search-c5-current-default` | 3 | 57 | 60 | 48,789 | 1.000000 | 1.000000 | 0 | 0 |
| `fixed-80-python-breadcrumbs` | `github-doctacon-buoy-search-c5-fixed-80-python-breadcrumbs` | 3 | 19 | 22 | 50,162 | 0.366667 | 1.028142 | 0 | 0 |
| `python-ast` | `github-doctacon-buoy-search-c5-python-ast` | 3 | 89 | 92 | 52,378 | 1.533333 | 1.073562 | 0 | 0 |

Deterministic artifact identities were:

- `current-default`: `plan_25c28c3358c561c6`, artifact hash `25c28c3358c561c60794363da44106b39ac7f74b46ae0afd45ef6b7bd07d2823`
- `fixed-80-python-breadcrumbs`: `plan_a8177494fafa5c79`, artifact hash `a8177494fafa5c7943e324ab7deb38315ffaa96eb647865b88939c0a869ec0d9`
- `python-ast`: `plan_9dee35a31517d1d1`, artifact hash `9dee35a31517d1d14bf978037f688352f51174fa5f8e39a74a46d2064265fc6f`

Every arm recorded zero remote calls, credential reads, model loads, live writes, deletes, and state updates.

## Procedure

1. Constructed a `GitHubRepoAcquisition` directly from the existing local worktree and its current `git rev-parse HEAD`; no clone, GitHub API request, or other network acquisition occurred.
2. Used the same exact include-path tuple and commit for all arms.
3. Generated each corpus only under a temporary directory outside the project.
4. Ran the unchanged generic processor for `current-default`, including the common-header invariant/count check.
5. Ran the isolated syntax processor for each Python-aware arm with fixed `target_tokens=300`, `overlap_sentences=2`, and a nonbinding `100000` row cap.
6. Built plan artifacts in memory with separate proposed namespace names. `write_plan_artifacts` was not called.
7. Counted manifest rows and UTF-8 content bytes, then calculated treatment multipliers against the paired control.
8. The temporary directory and generated pages were deleted automatically at command exit.

## What this supports

This supports that all three arms can be locally planned against one identical commit/corpus, that every selected code file contributes one independently counted common header row, that treatment/control row counts and payload multipliers are reviewable, and that the C5 implementation itself requires no model, credential, remote service, namespace write, delete, or state mutation.

## Limits

This is bounded C5 implementation/preflight evidence over a representative three-file local Python corpus. It is not the C6 Buoy/pytest/Ruff pilot forecast, does not authorize any proposed namespace, does not prove model storage or provider billing, and does not approve an apply. C5 independent review and required CI are complete, but C6 remains blocked on exact pilot-repository namespace/commit/corpus/file/header/source/total-row/storage/write forecasts and separate exact write approval. No namespace, catalog, applied state, default, dataset, or label was changed.
