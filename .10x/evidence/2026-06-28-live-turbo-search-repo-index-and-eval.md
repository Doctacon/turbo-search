Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-live-turbo-search-repo-index-and-eval.md, .10x/specs/repo-search-eval-autoresearch.md

# Live turbo-search Repo Index and Eval

## What was observed

With user approval that live writes and namespaces are now in scope, applied the public `turbo-search` GitHub repository into turbopuffer and ran the live graded repository eval.

Target:

- Repository URL: `https://github.com/Doctacon/turbo-search`
- Namespace: `github-doctacon-turbo-search-v1`
- Region: `gcp-us-central1`
- Plan path: `artifacts/site-crawls/github-doctacon-turbo-search-plan-live/plan.json`
- Live eval result path: `autoresearch/runs/repo-search-live-baseline-20260628/result.json`
- Live eval report path: `autoresearch/runs/repo-search-live-baseline-20260628/report.md`

## Commands and outputs

### Plan

Command shape:

```bash
uv run turbo-search plan https://github.com/Doctacon/turbo-search \
  --out-dir artifacts/site-crawls/github-doctacon-turbo-search-plan-live \
  --namespace github-doctacon-turbo-search-v1 \
  --state-root .turbo-search \
  --json
```

Key output:

```json
{
  "source_kind": "github_repo",
  "namespace": "github-doctacon-turbo-search-v1",
  "site_id": "github-doctacon-turbo-search",
  "repo_full_name": "Doctacon/turbo-search",
  "commit_sha": "2b401d9b7d67ea5ade0faaf41516c86708b3df1b",
  "files_discovered": 32,
  "files_selected": 30,
  "chunks_generated": 432,
  "rows_to_upsert": 432,
  "turbopuffer_api_calls": false,
  "api_calls_occurred": false
}
```

### Apply preflight before approved apply

Command shape:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/github-doctacon-turbo-search-plan-live/plan.json \
  --namespace github-doctacon-turbo-search-v1 \
  --state-root .turbo-search \
  --json
```

Key output:

```json
{
  "approved": false,
  "artifact_verified": true,
  "rows_to_upsert": 432,
  "embeddings_to_generate": 432,
  "stale_rows": 0,
  "delete_stale": false,
  "turbopuffer_api_calls": false,
  "state_updated": false
}
```

### Approved apply

Command shape:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/github-doctacon-turbo-search-plan-live/plan.json \
  --namespace github-doctacon-turbo-search-v1 \
  --state-root .turbo-search \
  --approve \
  --json
```

Key output:

```json
{
  "approved": true,
  "artifact_verified": true,
  "rows_to_upsert": 432,
  "rows_upserted": 432,
  "embeddings_to_generate": 432,
  "embeddings_generated": 432,
  "stale_rows": 0,
  "delete_stale": false,
  "rows_deleted": 0,
  "turbopuffer_api_calls": true,
  "state_updated": true
}
```

### Post-apply preflight

Command shape:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/github-doctacon-turbo-search-plan-live/plan.json \
  --namespace github-doctacon-turbo-search-v1 \
  --state-root .turbo-search \
  --json
```

Key output:

```json
{
  "approved": false,
  "artifact_verified": true,
  "rows_to_upsert": 0,
  "chunks_to_embed": 0,
  "chunks_unchanged": 432,
  "pages_unchanged": 30,
  "stale_rows": 0,
  "state_first_apply": false,
  "turbopuffer_api_calls": false,
  "state_updated": false
}
```

### Live repo eval/autoresearch

Added live experiment definition:

- `autoresearch/experiments/repo-search-live-baseline.json`

Command shape:

```bash
uv run python -m turbo_search.autoresearch \
  --experiment autoresearch/experiments/repo-search-live-baseline.json \
  --out autoresearch/runs/repo-search-live-baseline-20260628 \
  --json
```

Key output:

```json
{
  "status": "passed",
  "score": 59.96699925637771,
  "namespace": "github-doctacon-turbo-search-v1",
  "passed": 10,
  "total": 10,
  "repo_metrics": {
    "ndcg_at_10": 0.6122787743583826,
    "recall_at_10": 0.6333333333333333,
    "mrr_at_10": 0.7083333333333333,
    "precision_at_5": 0.3,
    "repo_search_score": 59.96699925637771
  },
  "turbopuffer_api_calls": true
}
```

Lowest-scoring cases:

```text
apply-preflight-approved-safety: 29.78543058415277
evals-composite-metrics: 30.069620465147352
plan-command-local-only: 53.772348720692364
```

No cases failed the pass/fail threshold because each case retrieved at least one relevant judged file in top 10. The composite score remains moderate because ranking quality, recall, and precision were imperfect.

## Procedure

1. Created an active live-operation ticket after user authorization.
2. Planned the public GitHub repository with existing local-only plan workflow.
3. Verified apply preflight without credentials/live calls.
4. Ran approved apply with explicit `--approve`; no stale deletion was requested or run.
5. Ran a post-apply preflight confirming all 432 chunks are unchanged and no rows remain to upsert.
6. Added a live autoresearch experiment definition and ran retrieval-only live eval against the applied namespace.
7. Recorded key counts and scores without secret values.

## What this supports or challenges

Supports that:

- the namespace `github-doctacon-turbo-search-v1` now has the public GitHub repository corpus applied;
- approved apply embedded and upserted 432 rows and updated local state;
- post-apply preflight sees 432 unchanged chunks and 0 upserts;
- live repo eval is operational and returns a baseline composite score of approximately `59.967` over 10 seed cases.

Challenges/improvement signals:

- Top results often include generated docs and `.pi/skills` pages ahead of implementation files.
- Duplicate chunks from the same file can consume top-k slots.
- The seed labels are path-level and assistant-drafted, so score interpretation needs review/calibration.

## Limits

The indexed corpus came from the public GitHub remote at commit `2b401d9b7d67ea5ade0faaf41516c86708b3df1b`, not uncommitted local working-tree changes. No namespace deletion or stale deletion was run. No API key or secret value was recorded.
