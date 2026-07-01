Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md, .10x/decisions/namespace-ranking-defaults.md

# Repo Module-Role Diversification Validation

## What was observed

Implemented a conservative scoring-only module-role diversification step inside the existing `repo_code` profile.

Behavior:

- applies after normal file-level scoring;
- preserves the top implementation hit;
- only acts when the top-5 window has no docs/tests companion;
- scans the next candidates and promotes at most one strong companion into slot 5;
- test companion evidence comes from exact query/source-stem matching such as `src/requests/utils.py` -> `tests/test_utils.py`;
- docs companion evidence comes from exact docs filename matches or strong query-token overlap with the retrieved docs chunk content;
- uses only existing retrieved fields, so it does not require schema changes, reindexing, namespace cleanup, or stale deletion.

No live writes, deletes, reindexing, or state mutation were performed for this validation.

## Procedure

Regression tests:

```bash
uv run python -m unittest tests.test_retriever
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
17 tests OK
139 tests OK
git diff --check: no whitespace errors
```

Live retrieval-only evals:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/turbo_search_repo_search_seed_evals.json \
  --namespace github-doctacon-turbo-search-v2-clean \
  --top-k 10 \
  --candidates 200 \
  --json

uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/requests_repo_search_seed_evals.json \
  --namespace github-psf-requests-v1 \
  --top-k 10 \
  --candidates 200 \
  --json
```

Artifacts:

- `autoresearch/runs/repo-role-diversification-20260628/turbo-default-role-diversification.json`
- `autoresearch/runs/repo-role-diversification-20260628/requests-default-role-diversification.json`
- `autoresearch/runs/repo-role-diversification-20260628/summary.json`
- `autoresearch/runs/repo-role-diversification-20260628/report.md`

## Results

Baseline is the previous repo default after path/symbol scoring: `file / repo_code / pool100 / max`.

| Corpus | Namespace | Score before | Score after | Δ score | P@5 before | P@5 after | Δ P@5 | NDCG@10 | Recall@10 | MRR@10 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| turbo-search | `github-doctacon-turbo-search-v2-clean` | 87.126 | 87.126 | +0.000 | 0.520 | 0.520 | +0.000 | 0.914 | 0.833 | 1.000 |
| psf/requests | `github-psf-requests-v1` | 82.547 | 84.093 | +1.546 | 0.400 | 0.420 | +0.020 | 0.889 | 0.800 | 1.000 |

## What this supports or challenges

Supports:

- The role-diversification rule improves the cross-repo aggregate without hurting `turbo-search`.
- Promoting a single docs/tests companion can improve Requests NDCG and Recall when the top implementation file is already correct but top-5 is crowded with adjacent implementation files.
- A conservative post-rank rule is safer than changing aggregation defaults because it does not displace rank 1 and acts only when the result window lacks a companion role.

Challenges / limits:

- The rule is still heuristic and validated on only two repository corpora.
- It cannot promote a relevant companion that never appears in the retrieval candidate pool, such as some adapter tests in the current Requests eval.
- The docs companion content match is based on retrieved chunk text, not full-file document structure.

## Conclusion

Promote module-role diversification as part of the universal `repo_code` default. The default shape remains:

```text
file / repo_code / pool100 / max
```

The `repo_code` profile now includes artifact demotion, tests boost, query-intent handling, path/symbol scoring, and single-companion role diversification.
