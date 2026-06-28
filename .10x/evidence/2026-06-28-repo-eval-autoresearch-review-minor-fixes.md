Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-eval-autoresearch-docs-validation.md

# Repo Eval Autoresearch Review Minor Fixes

## What was observed

Addressed two minor reviewer findings without live calls or scope expansion.

Changed files:

- `src/turbo_search/evals.py`
  - Clamped per-case composite `repo_search_score` to the documented `0..100` range.
  - Clamped aggregate `repo_search_score` to the documented `0..100` range.
  - Added `path` and `repo_path` to `hit_summary` output.
- `src/turbo_search/autoresearch.py`
  - Rendered top-hit locators using `url`, then `repo_path`, then `path`, then `section_path`, avoiding `no locator` for path-only fixture hits.
- `tests/test_evals.py`
  - Added aggregate score clamping coverage.
  - Added hit summary path/repo_path coverage.
- `tests/test_autoresearch.py`
  - Added report assertion that path-only fixture hits render their path and do not render `no locator`.

Validation command:

```bash
uv run python -m unittest tests.test_autoresearch tests.test_evals tests.test_cli tests.test_retriever
```

Output:

```text
............................................
----------------------------------------------------------------------
Ran 44 tests in 0.042s

OK
```

## Procedure

1. Inspected the reviewer findings against `evals.py`, `autoresearch.py`, and focused tests.
2. Made targeted clamp and top-hit summary/report changes.
3. Added focused regression assertions.
4. Ran the requested focused unittest command.
5. Confirmed no staged files with `git diff --cached --name-only`.

## What this supports or challenges

Supports that the documented `repo_search_score` range is enforced for per-case and aggregate composite scores, and that path-only fixture hits now render useful locators in autoresearch reports.

## Limits

No live turbopuffer calls were run. Existing unrelated/uncommitted work in the repository was not staged or modified beyond the requested files/evidence.
