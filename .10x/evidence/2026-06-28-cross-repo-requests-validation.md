Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-cross-repo-requests-validation.md, .10x/decisions/namespace-ranking-defaults.md

# Cross-Repo Requests Validation

## What was observed

Validated repo-search defaults on a different public repository selected by the user:

```text
https://github.com/psf/requests
```

New namespace:

```text
github-psf-requests-v1
```

Commit indexed:

```text
4ed3d1b3204caa6806a36125a39589044a02e807
```

Added eval dataset:

```text
src/turbo_search/data/requests_repo_search_seed_evals.json
```

The dataset has 10 assistant-drafted, source-backed cases covering top-level API helpers, Session flow, request/response models, adapters, auth, cookies, utilities, exceptions, structures, and hooks.

Safety:

- new namespace only;
- approved live upsert to the new namespace;
- no namespace deletion;
- no stale deletion;
- no mutation of existing namespaces;
- no proprietary model APIs.

## Procedure

Plan:

```bash
uv run turbo-search plan https://github.com/psf/requests \
  --out-dir artifacts/site-crawls/github-psf-requests-plan-20260628 \
  --namespace github-psf-requests-v1 \
  --json
```

Observed plan summary:

```text
files_discovered = 130
files_selected = 117
files_skipped_filtered = 2
files_skipped_oversize = 7
chunks_generated = 729
rows_to_upsert = 729
first_apply = true
turbopuffer_api_calls = false
```

Apply preflight and approved apply:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/github-psf-requests-plan-20260628/plan.json \
  --namespace github-psf-requests-v1 \
  --json

uv run turbo-search apply \
  --plan artifacts/site-crawls/github-psf-requests-plan-20260628/plan.json \
  --namespace github-psf-requests-v1 \
  --approve \
  --json
```

Observed approved apply:

```text
rows_to_upsert = 729
rows_upserted = 729
embeddings_generated = 729
stale_rows = 0
rows_deleted = 0
state_updated = true
```

Live evals:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/requests_repo_search_seed_evals.json \
  --namespace github-psf-requests-v1 \
  --top-k 10 \
  --candidates 200
```

Artifacts:

- `autoresearch/runs/cross-repo-requests-20260628/apply-preflight.json`
- `autoresearch/runs/cross-repo-requests-20260628/apply-approved.json`
- `autoresearch/runs/cross-repo-requests-20260628/eval-default.json`
- `autoresearch/runs/cross-repo-requests-20260628/eval-max.json`
- `autoresearch/runs/cross-repo-requests-20260628/eval-no-profile-capped.json`
- `autoresearch/runs/cross-repo-requests-20260628/summary.json`
- `autoresearch/runs/cross-repo-requests-20260628/report.md`
- `autoresearch/runs/default-max-after-cross-repo-20260628/summary.json`

Validation commands:

```bash
uv run python -m unittest discover tests
git diff --check
```

Observed:

```text
135 tests OK
git diff --check: no whitespace errors
```

## Results

| Variant | Profile | Aggregation | P@5 | Score | NDCG | Recall | MRR | Passed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| repo default after cross-repo decision | repo_code | max | 0.360 | 81.809 | 0.870 | 0.767 | 1.000 | 10/10 |
| no profile, capped | none | capped_sum_3 | 0.400 | 81.053 | 0.831 | 0.867 | 0.933 | 10/10 |
| repo_code capped | repo_code | capped_sum_3 | 0.320 | 78.229 | 0.822 | 0.800 | 0.920 | 10/10 |

## What this supports or challenges

Supports:

- A different public repo is useful validation; `turbo-search` is a noisy stress test because it contains project memory/eval/autoresearch artifacts.
- The `repo_code` path profile with max aggregation is safer as a universal repository default.
- Capped aggregation is useful as an opt-in repo-specific tuning knob, not as a cross-repo default.

Challenges:

- Requests Precision@5 is only `0.360` under the safe default. The strongest future hypothesis is not more fixed aggregation; it is path/symbol-aware ranking so exact modules like `hooks.py`, `structures.py`, `adapters.py`, and `utils.py` win targeted implementation queries without over-rewarding broad repeated chunks.

## Conclusion

Cross-repo validation reversed the universal default promotion for `capped_sum_3`. Repository defaults now use:

```text
file / repo_code / pool100 / max
```

`capped_sum_3` remains opt-in for repositories where repeated same-file evidence has been validated.
