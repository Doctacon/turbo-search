Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-website-page-level-ranking.md, .10x/evidence/2026-06-28-local-reranker-repo-and-site-validation.md

# Website Page-Level Ranking Validation

## What was observed

Implemented an experiment-first `page` ranking mode for retrieval/evals:

```bash
--ranking-mode page --ranking-profile none
```

Behavior:

- `ranking_mode=page` groups non-repository website chunks by canonical URL, stripping fragments and trailing slashes.
- Repository rows still group by `repo_path`, even when `ranking_mode=page`, so repo file-level behavior does not regress.
- Defaults were not changed. Default remains `ranking_mode=file`, `ranking_profile=repo_code`.

Changed files:

- `src/turbo_search/retriever.py`
- `src/turbo_search/cli.py`
- `tests/test_retriever.py`
- `README.md`
- `docs/generic-site-rag-plan-apply.md`

## Validation commands

```bash
uv run python -m unittest tests.test_retriever tests.test_cli tests.test_autoresearch tests.test_evals
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
50 tests OK
127 tests OK
git diff --check: no whitespace errors
```

## Live eval experiment

Artifact:

- `autoresearch/runs/website-page-ranking-20260628/results.json`
- `autoresearch/runs/website-page-ranking-20260628/report.md`

Command shape:

```bash
uv run python - <<'PY'
# Live retrieval-only grid over site-turbopuffer-com-v1 and github-doctacon-turbo-search-v1.
# Variants: default file, raw chunk, page ranking with pools 20/50/100/150,
# c100/c200/c400, and repo_code profile smoke.
PY
```

No live writes, deletes, stale deletes, namespace management, or state mutation were run.

## turbopuffer.com website results

Baseline default on `site-turbopuffer-com-v1`:

```text
Precision@5: 0.200
repo_search_score: 59.734
NDCG@10: 0.681
Recall@10: 0.483
MRR@10: 0.708
```

Best page-ranking variants:

| Variant | Precision@5 | ΔP@5 | Score | ΔScore | NDCG | Recall | MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `page-none-pool20` | 0.270 | +0.070 | 65.279 | +5.545 | 0.727 | 0.567 | 0.750 |
| `page-none-c400-pool100` | 0.220 | +0.020 | 67.594 | +7.860 | 0.742 | 0.667 | 0.750 |
| `page-none-c100-pool100` | 0.200 | +0.000 | 68.646 | +8.912 | 0.747 | 0.717 | 0.750 |
| `page-none-pool100` | 0.200 | +0.000 | 67.415 | +7.680 | 0.742 | 0.667 | 0.750 |

Interpretation:

- Page-level ranking consistently improved website composite score.
- `page-none-pool20` gave the best Precision@5 improvement.
- Larger pools improved recall/composite more than Precision@5.
- This supports page ranking as an experimental website option, not yet a default.

## Repo regression check

Baseline default on `github-doctacon-turbo-search-v1`:

```text
Precision@5: 0.500
repo_search_score: 87.251
NDCG@10: 0.920
Recall@10: 0.833
MRR@10: 1.000
```

Repo check:

```text
page-repo-code-pool100: Precision@5 0.500, score 87.251
```

`ranking_mode=page` with `repo_code` profile matched the repo default because repository rows continue grouping by `repo_path`. Raw chunk order remains worse:

```text
chunk-raw: Precision@5 0.300, score 59.967
```

## What this supports or challenges

Supports:

- URL/page-level deduplication is useful for website namespaces.
- Website and repository ranking should have separate grouping identities: `url` for pages, `repo_path` for repo files.
- Page ranking should stay opt-in for now because the best Precision@5 and best composite score used different pool/candidate settings.

Challenges:

- The `turbopuffer.com` website eval labels are assistant-drafted and small.
- Page ranking improved website metrics but does not yet establish one obvious default setting for all websites.

## Recommended next action

Keep `--ranking-mode page` as an experimental option. Next, run it on at least one more website namespace or expand/human-review website labels before making page ranking the website default.

## Limits

The experiment used live retrieval-only calls. No namespace writes/deletes or proprietary model APIs were used. The existing repo default behavior was preserved.
