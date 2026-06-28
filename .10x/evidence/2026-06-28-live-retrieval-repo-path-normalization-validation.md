Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/specs/repo-search-eval-autoresearch.md

# Live Retrieval repo_path Normalization Validation

## What was observed

Fixed the reviewer blocker where live retrieval eval reports could emit an empty `repo_path` even when turbopuffer rows contained a `repo_path` attribute.

Changed files:

- `src/turbo_search/retriever.py`
  - Added `repo_path` to `RETRIEVAL_ATTRIBUTES` so live ANN/BM25 subqueries request it from turbopuffer rows.
  - Added `repo_path` to `SearchHit` and `SearchHit.to_dict()`.
  - Updated `row_to_hit()` to preserve normalized row `repo_path` attributes in `SearchHit`.
- `tests/test_retriever.py`
  - Updated the live-retriever normalization fixture to include `repo_path` in returned row attributes.
  - Asserted `result.hits[0].repo_path`, serialized hit `repo_path`, and `hit_summary(SearchHit(...))["repo_path"]` all preserve the repo path.

Validation command:

```bash
uv run python -m unittest tests.test_retriever tests.test_evals tests.test_autoresearch tests.test_cli
```

Output:

```text
............................................
----------------------------------------------------------------------
Ran 44 tests in 0.087s

OK
```

Staging check:

```bash
git diff --cached --name-only
```

Output: no staged files.

## Procedure

1. Inspected `src/turbo_search/retriever.py`, `src/turbo_search/evals.py`, `tests/test_retriever.py`, and relevant eval tests.
2. Added repo-path retrieval and preservation through the live retrieval normalization path.
3. Added focused assertions in the existing live retriever test.
4. Ran the requested focused test command; no live turbopuffer calls were made.
5. Confirmed no staged files.

## What this supports or challenges

Supports that live retrieval reports can now carry repository file identity from turbopuffer rows through `SearchHit`, serialized retrieval output, and eval hit summaries.

## Limits

No live turbopuffer retrieval was run. The test uses a mocked namespace response that mirrors turbopuffer row attributes.
