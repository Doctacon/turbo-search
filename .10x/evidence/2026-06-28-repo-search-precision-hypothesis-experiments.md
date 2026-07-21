Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-repo-search-precision-hypothesis-experiments.md, .10x/research/2026-06-28-repo-search-precision-state-of-art.md, .10x/evidence/2026-06-28-live-turbo-search-repo-index-and-eval.md

# Repo Search Precision Hypothesis Experiments

## What was observed

Executed the first three precision-improvement hypotheses sequentially against the applied live namespace `github-doctacon-turbo-search-v1` using retrieval-only turbopuffer calls and offline post-processing of retrieved hits.

No apply, delete, stale-delete, namespace-management, state mutation, or source-code mutation was performed.

Artifacts:

- Full JSON results: `autoresearch/runs/precision-hypothesis-experiments-20260628/results.json`
- Markdown report: `autoresearch/runs/precision-hypothesis-experiments-20260628/report.md`

## Procedure

Command shape:

```bash
OUT_DIR="autoresearch/runs/precision-hypothesis-experiments-20260628"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
uv run python - <<'PY'
# Live retrieval-only experiment runner.
# Loads src/turbo_search/data/turbo_search_repo_search_seed_evals.json.
# Retrieves pools from github-doctacon-turbo-search-v1.
# Scores offline transformations for H1/H2/H3.
PY
```

Retrieval pools:

```json
[
  {"pool_id": "rrf-top10-c100", "top_k": 10, "candidates": 100},
  {"pool_id": "rrf-top20-c100", "top_k": 20, "candidates": 100},
  {"pool_id": "rrf-top50-c100", "top_k": 50, "candidates": 100},
  {"pool_id": "rrf-top100-c100", "top_k": 100, "candidates": 100},
  {"pool_id": "rrf-top100-c200", "top_k": 100, "candidates": 200}
]
```

Experiment mode:

```json
{
  "mode": "live-retrieval-only-postprocess",
  "namespace": "github-doctacon-turbo-search-v1",
  "region": "gcp-us-central1",
  "embedding_model": "BAAI/bge-small-en-v1.5",
  "turbopuffer_api_calls": true,
  "live_writes_allowed": false,
  "namespace_management_allowed": false,
  "source_mutation_allowed": false,
  "state_mutation_allowed": false
}
```

## Baseline

Persisted live baseline and rerun matched:

```text
Precision@5: 0.300
repo_search_score: 59.967
NDCG@10: 0.612
Recall@10: 0.633
MRR@10: 0.708
passed: 10/10
```

## Hypothesis 1: collapse/diversify by `repo_path`

Variants:

| Variant | Precision@5 | ΔP@5 | Score | ΔScore | NDCG | Recall | MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `h1-collapse-first-rrf-top20-c100` | 0.460 | +0.160 | 69.450 | +9.483 | 0.699 | 0.783 | 0.717 |
| `h1-collapse-first-rrf-top50-c100` | 0.460 | +0.160 | 71.083 | +11.116 | 0.710 | 0.833 | 0.717 |
| `h1-collapse-first-rrf-top100-c100` | 0.460 | +0.160 | 72.209 | +12.242 | 0.719 | 0.867 | 0.717 |
| `h1-collapse-first-rrf-top100-c200` | 0.460 | +0.160 | 71.083 | +11.116 | 0.710 | 0.833 | 0.717 |

Consistency: positive and consistent. All four variants improved Precision@5 by +0.160. The best H1 variant improved six cases, left four unchanged, and made no case worse on Precision@5.

## Hypothesis 2: file-level aggregation/max-pooling

Best variants:

| Variant | Precision@5 | ΔP@5 | Score | ΔScore | NDCG | Recall | MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `h2-file-sum-rrf-top50-c100` | 0.500 | +0.200 | 82.066 | +22.099 | 0.839 | 0.833 | 0.950 |
| `h2-file-sum-rrf-top100-c100` | 0.500 | +0.200 | 83.195 | +23.228 | 0.852 | 0.867 | 0.933 |
| `h2-file-sum-rrf-top100-c200` | 0.500 | +0.200 | 77.439 | +17.472 | 0.775 | 0.867 | 0.833 |
| `h2-file-top3-mean-rrf-top100-c100` | 0.480 | +0.180 | 78.439 | +18.472 | 0.796 | 0.867 | 0.833 |
| `h2-file-max-log-count-rrf-top100-c100` | 0.460 | +0.160 | 82.327 | +22.360 | 0.844 | 0.867 | 0.933 |

Consistency: positive. Sum aggregation over file chunks was strongest and consistent across three retrieval pools, reaching Precision@5 0.500 each time. The best H2 variant improved seven cases, left three unchanged, and made no case worse on Precision@5.

## Hypothesis 3: source-first/profile reranking

Best variants:

| Variant | Precision@5 | ΔP@5 | Score | ΔScore | NDCG | Recall | MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| `h3-demote-process-docs-rrf-top100-c200` | 0.500 | +0.200 | 87.251 | +27.284 | 0.920 | 0.833 | 1.000 |
| `h3-src-tests-first-fill-rrf-top100-c200` | 0.500 | +0.200 | 87.180 | +27.213 | 0.924 | 0.817 | 1.000 |
| `h3-demote-process-docs-rrf-top100-c100` | 0.500 | +0.200 | 86.621 | +26.654 | 0.917 | 0.808 | 1.000 |
| `h3-src-tests-first-fill-rrf-top100-c100` | 0.500 | +0.200 | 86.005 | +26.038 | 0.915 | 0.783 | 1.000 |
| `h3-src-tests-boost-rrf-top100-c100` | 0.480 | +0.180 | 85.933 | +25.966 | 0.918 | 0.783 | 1.000 |

Consistency: positive, especially for gentle demotion/source-first-fill profiles. Source-heavy/src-only variants improved Precision@5 but lost recall compared with gentler profiles, so they are less attractive as defaults.

## Overall findings

Ranked best variants across all hypotheses:

```text
1. h3-demote-process-docs-rrf-top100-c200: P@5 0.500, score 87.251
2. h3-src-tests-first-fill-rrf-top100-c200: P@5 0.500, score 87.180
3. h3-demote-process-docs-rrf-top100-c100: P@5 0.500, score 86.621
4. h3-src-tests-first-fill-rrf-top100-c100: P@5 0.500, score 86.005
5. h2-file-sum-rrf-top100-c100: P@5 0.500, score 83.195
```

All three hypotheses improved Precision@5 consistently over the baseline. The strongest pattern was cumulative: retrieve a deeper candidate pool, aggregate/diversify by file path, then apply a gentle source-first profile that demotes process/docs noise without completely removing docs.

## What this supports or challenges

Supports:

- Duplicate chunks are a major precision problem.
- File-level aggregation is better aligned with path-level repository evals than raw chunk ranking.
- Gentle source-first profiles improve ranking quality more than strict source-only filtering.
- `candidates=100` and `candidates=200` both improved, suggesting the effect is not a one-pool fluke.

Challenges/cautions:

- These are offline post-processing experiments over live retrieval output, not production retrieval behavior.
- The seed eval has only 10 assistant-drafted path-level cases; results are directionally useful but not human-approved ground truth.
- Strict source-only/source-heavy profiles improved Precision@5 but can reduce recall, especially where README/docs are legitimately judged relevant.

## Recommended promotion path

1. Promote `repo_path` collapse/file-level aggregation as an experimental retrieval option first.
2. Add a configurable gentle path-profile mode rather than hardcoding `src/` only.
3. Re-run on a larger, human-reviewed dataset before making source-first behavior the default.

## Limits

No production source changes were made for this experiment ticket. The experiment did not test rerankers or alternate embedding models. It did not run live writes, deletes, or namespace-management operations.
