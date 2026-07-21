Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md, .10x/evidence/2026-06-28-cross-corpus-live-apply.md, .10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md, .10x/decisions/namespace-ranking-defaults.md

# Cross-Corpus Live Retrieval Evals

## What was observed

After explicit user approval, live retrieval-only evals were run against the four expanded validation basket namespaces:

- `github-pytest-dev-pytest-v1`
- `github-fastapi-typer-v1`
- `site-ruff-docs-v1`
- `site-typer-docs-v1`

No writes, deletes, apply, stale cleanup, namespace deletion, or state mutation occurred during these evals.

## Procedure

Repository variants:

```bash
uv run turbo-search evals --live --dataset <repo dataset> --namespace <repo namespace> --top-k 10 --candidates 200 --json
uv run turbo-search evals --live --dataset <repo dataset> --namespace <repo namespace> --top-k 10 --candidates 200 --ranking-mode file --ranking-profile repo-code --ranking-pool 100 --ranking-aggregation max --json
uv run turbo-search evals --live --dataset <repo dataset> --namespace <repo namespace> --top-k 10 --candidates 200 --ranking-mode file --ranking-profile repo-code --ranking-pool 100 --ranking-aggregation capped-sum-3 --json
uv run turbo-search evals --live --dataset <repo dataset> --namespace <repo namespace> --top-k 10 --candidates 200 --ranking-mode chunk --ranking-profile none --json
```

Website variants:

```bash
uv run turbo-search evals --live --dataset <site dataset> --namespace <site namespace> --top-k 10 --candidates 200 --json
uv run turbo-search evals --live --dataset <site dataset> --namespace <site namespace> --top-k 10 --candidates 200 --ranking-mode chunk --ranking-profile none --json
uv run turbo-search evals --live --dataset <site dataset> --namespace <site namespace> --top-k 10 --candidates 200 --ranking-mode page --ranking-profile none --ranking-pool 20 --ranking-aggregation capped-sum-3 --json
```

Artifacts:

- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/pytest-default.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/pytest-max.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/pytest-capped.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/pytest-chunk.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-repo-default.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-repo-max.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-repo-capped.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-repo-chunk.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/ruff-docs-default.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/ruff-docs-capped.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/ruff-docs-chunk.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-docs-default.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-docs-capped.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/typer-docs-chunk.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/summary.json`
- `autoresearch/runs/cross-corpus-validation-basket-20260628/live-evals/report.md`

## Results

| Target | Variant | Mode | Aggregation | P@5 | Score | Delta score vs default | Recall | NDCG | MRR | Passed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| pytest repo | current default | file/repo_code/pool100 | adaptive_sum_3 | 0.640 | 84.742 | +0.000 | 0.807 | 0.858 | 1.000 | 10/10 |
| pytest repo | repo file max | file/repo_code/pool100 | max | 0.640 | 83.585 | -1.158 | 0.807 | 0.837 | 1.000 | 10/10 |
| pytest repo | capped_sum_3 | file/repo_code/pool100 | capped_sum_3 | 0.740 | 88.278 | +3.536 | 0.884 | 0.876 | 1.000 | 10/10 |
| pytest repo | raw chunk | chunk/none | adaptive_sum_3 ignored | 0.440 | 61.885 | -22.857 | 0.607 | 0.579 | 0.900 | 10/10 |
| Typer repo | current default | file/repo_code/pool100 | adaptive_sum_3 | 0.380 | 59.423 | +0.000 | 0.527 | 0.587 | 0.853 | 10/10 |
| Typer repo | repo file max | file/repo_code/pool100 | max | 0.400 | 56.139 | -3.284 | 0.493 | 0.545 | 0.820 | 10/10 |
| Typer repo | capped_sum_3 | file/repo_code/pool100 | capped_sum_3 | 0.360 | 52.663 | -6.760 | 0.450 | 0.500 | 0.839 | 10/10 |
| Typer repo | raw chunk | chunk/none | adaptive_sum_3 ignored | 0.200 | 31.151 | -28.272 | 0.293 | 0.264 | 0.583 | 7/10 |
| Ruff docs | current default | page/none/pool20 | max | 0.577 | 87.691 | +0.000 | 0.867 | 0.902 | 1.000 | 10/10 |
| Ruff docs | capped_sum_3 | page/none/pool20 | capped_sum_3 | 0.577 | 89.225 | +1.534 | 0.867 | 0.930 | 1.000 | 10/10 |
| Ruff docs | raw chunk | chunk/none | max ignored | 0.420 | 83.799 | -3.892 | 0.833 | 0.872 | 1.000 | 10/10 |
| Typer docs | current default | page/none/pool20 | max | 0.493 | 73.690 | +0.000 | 0.625 | 0.764 | 0.950 | 10/10 |
| Typer docs | capped_sum_3 | page/none/pool20 | capped_sum_3 | 0.513 | 74.540 | +0.850 | 0.625 | 0.776 | 0.950 | 10/10 |
| Typer docs | raw chunk | chunk/none | max ignored | 0.360 | 72.549 | -1.141 | 0.660 | 0.759 | 0.933 | 10/10 |

Averages on the new basket:

| Group | Variant | Avg P@5 | Avg score |
|---|---|---:|---:|
| new repos | current default | 0.510 | 72.083 |
| new repos | repo file max | 0.520 | 69.862 |
| new repos | capped_sum_3 | 0.550 | 70.470 |
| new repos | raw chunk | 0.320 | 46.518 |
| new sites | current default | 0.535 | 80.691 |
| new sites | capped_sum_3 | 0.545 | 81.883 |
| new sites | raw chunk | 0.390 | 78.174 |

## What this supports or challenges

Supports:

- The current repo default `file / repo_code / pool100 / adaptive_sum_3` generalizes better than strict `max` on both new repo targets and remains much better than raw chunk retrieval.
- Full repo `capped_sum_3` still fails the no-regression policy: it improves pytest but materially regresses Typer repo.
- The current website default `page / none / pool20 / max` beats raw chunk retrieval on both new site targets.
- Website `page / none / pool20 / capped_sum_3` improved both new site seed datasets versus current max aggregation.

Challenges / limits:

- Seed labels remain assistant-drafted and not human-approved.
- The Typer repo score is lower than prior repo corpora. Part of this may be caused by the current 50 KiB repository file cap skipping central files such as `typer/main.py` and `typer/params.py`; see `.10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md`.
- Website capped aggregation looks stronger after the new Ruff/Typer site data, but previous Pi-site evidence showed a tiny score regression for capped at pool 20 (`88.398 -> 88.204`) while P@5 was unchanged. Under the selected no-regression policy, this evidence alone does not justify changing the website default.

## Conclusion

Keep current defaults unchanged:

```text
repo/general = file / repo_code / pool100 / adaptive_sum_3
site-* = page / none / pool20 / max
```

The expanded basket strengthens confidence in the repo default and raw-chunk avoidance. It also reopens website capped aggregation as a promising candidate, but not enough to promote under the selected no-regression policy without resolving or accepting the prior Pi-site capped-score regression.
