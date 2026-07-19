Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-promote-repo-search-file-level-ranking.md, .10x/evidence/2026-06-28-repo-search-precision-hypothesis-experiments.md

# Repo Search File Ranking Promotion Validation

## What was observed

After user ratified `Change defaults`, implemented default repository-aware final ranking for retrieval/evals:

- default `candidates`: `200`;
- default `ranking_mode`: `file`;
- default `ranking_profile`: `repo_code`;
- default `ranking_pool`: `100`.

The default file ranking groups repository hits by `repo_path`, keeps one representative chunk per file, and applies the gentle `repo_code` multiplier that demotes repository process/docs paths after fusion. Generic website rows without `repo_path` remain chunk-keyed and are not collapsed accidentally. Users can inspect old raw chunk order with `--ranking-mode chunk --ranking-profile none`.

Changed files:

- `src/turbo_search/retriever.py`
- `src/turbo_search/cli.py`
- `src/turbo_search/evals.py`
- `src/turbo_search/autoresearch.py`
- `tests/test_retriever.py`
- `tests/test_cli.py`
- `README.md`
- `docs/generic-site-rag-plan-apply.md`

## Validation commands

### Unit/full test validation

```bash
uv run python -m unittest tests.test_retriever tests.test_cli tests.test_autoresearch tests.test_evals
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
46 tests OK
123 tests OK
git diff --check: no whitespace errors
```

### Dry-run retrieval plan validation

Command shape:

```bash
uv run turbo-search retrieve "Where is apply preflight implemented?" \
  --dry-run \
  --namespace github-doctacon-turbo-search-v1 \
  --json
```

Key output:

```json
{
  "top_k": 5,
  "candidates": 200,
  "ranking_mode": "file",
  "ranking_profile": "repo_code",
  "ranking_pool": 100,
  "turbopuffer_api_calls": false
}
```

### Live eval validation on existing baseline namespace

Command shape:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/turbo_search_repo_search_seed_evals.json \
  --namespace github-doctacon-turbo-search-v1 \
  --top-k 10 \
  --json > autoresearch/runs/repo-search-default-file-ranking-20260628/result.json
```

Key output:

```json
{
  "passed": 10,
  "total": 10,
  "ranking_mode": "file",
  "ranking_profile": "repo_code",
  "ranking_pool": 100,
  "top_k": 10,
  "candidates": 200,
  "repo_metrics": {
    "ndcg_at_10": 0.9197228411018873,
    "recall_at_10": 0.8333333333333334,
    "mrr_at_10": 1.0,
    "precision_at_5": 0.5,
    "repo_search_score": 87.25142292727048
  }
}
```

Compared with the prior persisted live baseline from `.10x/evidence/2026-06-28-live-turbo-search-repo-index-and-eval.md`:

```text
Precision@5: 0.300 -> 0.500
repo_search_score: 59.967 -> 87.251
NDCG@10: 0.612 -> 0.920
Recall@10: 0.633 -> 0.833
MRR@10: 0.708 -> 1.000
passed: 10/10 -> 10/10
```

## H9 config grid

Ran 21 live retrieval-only config variants over candidates, ranking pool, ranking mode, and profile.

Artifacts:

- `autoresearch/runs/repo-search-h9-config-grid-20260628/results.json`
- `autoresearch/runs/repo-search-h9-config-grid-20260628/report.md`

Best rows:

```text
file-repo-code-c200-pool100: P@5 0.500, score 87.251
file-repo-code-c200-pool150: P@5 0.500, score 87.251
file-repo-code-c400-pool100: P@5 0.500, score 87.251
file-repo-code-c400-pool150: P@5 0.500, score 87.251
file-repo-code-c100-pool100: P@5 0.500, score 86.621
```

This supports `candidates=200`, `ranking_pool=100` as a reasonable default; larger candidate/pool values did not improve this seed dataset.

## H4 index hygiene experiments

Created new namespaces only; the current baseline namespace `github-doctacon-turbo-search-v1` was not mutated or deleted.

### No-process namespace

Namespace: `github-doctacon-turbo-search-v1-no-process`

Plan command shape:

```bash
uv run turbo-search plan https://github.com/Doctacon/turbo-search \
  --out-dir artifacts/site-crawls/github-doctacon-turbo-search-plan-no-process-20260628 \
  --namespace github-doctacon-turbo-search-v1-no-process \
  --state-root .turbo-search \
  --exclude-path '.pi/**' \
  --exclude-path '.10x/**' \
  --exclude-path '.loom/**' \
  --exclude-path '.claude/**' \
  --exclude-path '.cursor/**' \
  --exclude-path 'artifacts/**' \
  --exclude-path 'autoresearch/runs/**' \
  --json
```

Plan key output:

```json
{
  "files_discovered": 32,
  "files_selected": 28,
  "files_skipped_filtered": 3,
  "files_skipped_oversize": 1,
  "chunks_generated": 415,
  "rows_to_upsert": 415,
  "turbopuffer_api_calls": false
}
```

Approved apply key output:

```json
{
  "approved": true,
  "artifact_verified": true,
  "rows_to_upsert": 415,
  "rows_upserted": 415,
  "embeddings_generated": 415,
  "stale_rows": 0,
  "rows_deleted": 0,
  "state_updated": true,
  "turbopuffer_api_calls": true
}
```

Live eval artifact: `autoresearch/runs/repo-search-no-process-index-20260628/result.json`

```json
{
  "precision_at_5": 0.5,
  "repo_search_score": 84.99598013606897,
  "ndcg_at_10": 0.8923511539891328,
  "recall_at_10": 0.8333333333333334,
  "mrr_at_10": 0.95,
  "passed": "10/10"
}
```

### Src/tests-only namespace

Namespace: `github-doctacon-turbo-search-v1-src-tests`

Plan command shape:

```bash
uv run turbo-search plan https://github.com/Doctacon/turbo-search \
  --out-dir artifacts/site-crawls/github-doctacon-turbo-search-plan-src-tests-20260628 \
  --namespace github-doctacon-turbo-search-v1-src-tests \
  --state-root .turbo-search \
  --include-path 'src/**' \
  --include-path 'tests/**' \
  --json
```

Plan key output:

```json
{
  "files_discovered": 32,
  "files_selected": 24,
  "files_skipped_filtered": 8,
  "files_skipped_oversize": 0,
  "chunks_generated": 394,
  "rows_to_upsert": 394,
  "turbopuffer_api_calls": false
}
```

Approved apply key output:

```json
{
  "approved": true,
  "artifact_verified": true,
  "rows_to_upsert": 394,
  "rows_upserted": 394,
  "embeddings_generated": 394,
  "stale_rows": 0,
  "rows_deleted": 0,
  "state_updated": true,
  "turbopuffer_api_calls": true
}
```

Live eval artifact: `autoresearch/runs/repo-search-src-tests-index-20260628/result.json`

```json
{
  "precision_at_5": 0.5,
  "repo_search_score": 81.6987955646263,
  "ndcg_at_10": 0.8642205254174474,
  "recall_at_10": 0.7833333333333333,
  "mrr_at_10": 0.9,
  "passed": "10/10"
}
```

## What this supports or challenges

Supports:

- Promoting file-level ranking plus gentle repo-code profiling improves live eval quality substantially on the existing baseline namespace.
- H9 tuning confirms `candidates=200` and `ranking_pool=100` are sufficient for the best observed seed score; larger values did not improve quality.
- H4 corpus hygiene can maintain `Precision@5 = 0.500`, but removing process/docs from the corpus did not beat the ranking-only default on this dataset.

Challenges:

- Strict corpus hygiene/source-only indexing can reduce recall and composite score because some docs/README results are legitimately relevant in the seed labels.
- The seed dataset remains assistant-drafted and small, so this validates direction but not production-grade generality.

## Limits

Live writes occurred only for new experiment namespaces `github-doctacon-turbo-search-v1-no-process` and `github-doctacon-turbo-search-v1-src-tests`. No namespace deletion, stale deletion, or baseline namespace mutation was run. No proprietary model APIs were used. No secrets were recorded.
