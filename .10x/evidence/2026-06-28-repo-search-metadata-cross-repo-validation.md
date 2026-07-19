Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-repo-search-metadata-cross-repo-validation.md, .10x/tickets/2026-06-28-repo-searchable-path-symbol-metadata.md, .10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md

# Repo Search Metadata Cross-Repo Validation

## What was observed

After explicit user approval, metadata-only repository indexing was live-applied and evaluated on the older repo validation basket:

- `doctacon/turbo-search` -> `github-doctacon-turbo-search-v3-metadata`
- `psf/requests` -> `github-psf-requests-v2-metadata`
- `pallets/click` -> `github-pallets-click-v2-metadata`

This used `--repo-search-metadata` with the default 51200-byte repo file cap. No oversize flag was used. No stale deletion or namespace deletion was run.

Prior pytest/Typer metadata-only results from `.10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md` were included for the full five-repo no-regression readout.

## Procedure

Plan/apply pattern:

```bash
uv run turbo-search plan https://github.com/<owner>/<repo> \
  --namespace <new-metadata-namespace> \
  --out-dir artifacts/site-crawls/<repo>-metadata-plan-20260628 \
  --repo-search-metadata \
  --json

uv run turbo-search apply --plan artifacts/site-crawls/<repo>-metadata-plan-20260628/plan.json \
  --namespace <new-metadata-namespace> \
  --approve --json
```

Eval pattern:

```bash
uv run turbo-search evals --live --dataset <repo-seed-dataset> \
  --namespace <namespace> --top-k 10 --candidates 200 --json
```

Artifacts:

- `autoresearch/runs/repo-search-metadata-cross-repo-20260628/metadata-cross-repo-summary.json`
- `autoresearch/runs/repo-search-metadata-cross-repo-20260628/metadata-cross-repo-report.md`
- plan/apply/eval JSON files under `autoresearch/runs/repo-search-metadata-cross-repo-20260628/`

## Apply counts

| Repo | Metadata namespace | Rows | Embeddings | Deleted |
|---|---|---:|---:|---:|
| turbo-search | `github-doctacon-turbo-search-v3-metadata` | 662 | 662 | 0 |
| requests | `github-psf-requests-v2-metadata` | 768 | 768 | 0 |
| click | `github-pallets-click-v2-metadata` | 1362 | 1362 | 0 |

## Eval results

| Repo | Baseline score | Metadata score | Δ score | Baseline P@5 | Metadata P@5 | Δ P@5 | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| turbo-search | 87.760 | 85.568 | -2.193 | 0.540 | 0.540 | +0.000 | regression |
| requests | 84.426 | 84.000 | -0.426 | 0.420 | 0.440 | +0.020 | regression |
| click | 72.474 | 73.141 | +0.667 | 0.400 | 0.420 | +0.020 | pass |
| pytest | 84.742 | 85.971 | +1.229 | 0.640 | 0.700 | +0.060 | pass |
| Typer | 59.423 | 62.062 | +2.639 | 0.380 | 0.440 | +0.060 | pass |

Averages across the five repo basket:

- Score: `77.765 -> 78.148` (`+0.383`)
- P@5: `0.476 -> 0.508` (`+0.032`)

## Regression drivers

Turbo-search regressions were concentrated in a few cases despite unchanged P@5:

| Case | Baseline score | Metadata score | Δ | Note |
|---|---:|---:|---:|---|
| `repo-file-selection-corpus` | 77.02 | 66.55 | -10.47 | MRR dropped `1.0 -> 0.5`. |
| `chunking-code-and-markdown` | 84.41 | 80.89 | -3.52 | P@5 and MRR unchanged; NDCG/recall shift. |
| `evals-composite-metrics` | 75.76 | 59.48 | -16.28 | MRR dropped `1.0 -> 0.5`. |

Requests had smaller mixed movement:

| Case | Baseline score | Metadata score | Δ | Note |
|---|---:|---:|---:|---|
| `session-request-send-flow` | 93.02 | 88.74 | -4.29 | P@5 and MRR unchanged; NDCG/recall shift. |
| `utilities-proxies-netrc-encoding-uri` | 76.61 | 80.12 | +3.51 | P@5 improved `0.2 -> 0.4`. |

## What this supports or challenges

Supports:

- Metadata-only indexing improves average score and average P@5 across the five-repo basket.
- Metadata-only improves three of five repos: pytest, Typer, and Click.

Challenges:

- Metadata-only fails the no-regression promotion policy because turbo-search and Requests regress by composite score.
- The effect is not simple precision improvement: P@5 improves or stays flat on the older basket, while composite score can drop because MRR/NDCG/recall change.

## Conclusion

Do not promote `--repo-search-metadata` to a default planner behavior yet. Keep it opt-in. The next metadata work, if pursued, should be ranking/embedding placement rather than simply enabling the metadata preamble everywhere; the existing owner is `.10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md`.
