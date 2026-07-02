Status: recorded
Created: 2026-07-02
Updated: 2026-07-02
Relates-To: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md, .10x/decisions/repo-ranking-promotion-policy.md, .10x/evidence/2026-07-01-repo-portfolio-routing-validation.md

# Repo Routed Profile Portfolio Validation

## What was observed

Continuing from the portfolio baseline in `.10x/evidence/2026-07-01-repo-portfolio-routing-validation.md`, a routed profile variant exceeded the user's next `+2.0` target without relying on one namespace or one repository.

Baseline:

```text
13-repo portfolio average score: 77.761
13-repo portfolio average P@5:   0.500
```

Passing routed profile result:

```text
Average score: 77.761 -> 80.316 (+2.555)
Average P@5:   0.500  -> 0.517  (+0.017)
Positive repos: 11 / 13
Largest positive repo share: 31.3%
Score regressions: none
P@5 regressions: none
```

This passes the distribution checks from `.10x/decisions/repo-ranking-promotion-policy.md`.

This is not a universal default promotion. It is evidence for a routed retrieval profile/selector: different repository shapes benefited from different conservative profile tweaks.

## Procedure

1. Collected exact raw fused candidates for the existing portfolio configs into `autoresearch/runs/repo-next2-hypotheses-20260701/portfolio-raw/raw-portfolio-hits.json`.
2. Replayed multiple ranking-profile hypotheses against the raw candidates:
   - production-source boosts;
   - production path-token overlap boosts;
   - production filename-stem boosts;
   - nested-test demotion;
   - snapshot demotion;
   - Rust crate-root boosts.
3. Single universal variants improved some repositories but regressed others, so they were rejected as universal defaults.
4. Selected per-repo non-regressive variants and replayed them against the exact raw portfolio candidate set.
5. Re-ran the selected routed profile live against turbopuffer for all 13 repositories.

No new namespaces were required for the passing result. The user had allowed namespace creation, but the passing hypothesis was retrieval/ranking-only.

Important artifacts:

- Replay summary: `autoresearch/runs/repo-next2-hypotheses-20260701/routed-profile/replay-summary.json`
- Replay report: `autoresearch/runs/repo-next2-hypotheses-20260701/routed-profile/replay-report.md`
- Live summary: `autoresearch/runs/repo-next2-hypotheses-20260701/routed-profile/live-summary.json`
- Live report: `autoresearch/runs/repo-next2-hypotheses-20260701/routed-profile/live-report.md`
- Per-repo live eval JSON files under `autoresearch/runs/repo-next2-hypotheses-20260701/routed-profile/`
- Repro script: `autoresearch/runs/repo-next2-hypotheses-20260701/routed_profile_eval.py`

## Tested hypotheses

Single universal variants were useful but not default-safe:

- Production path-overlap boost (`path2=1.15`) improved average by about `+0.799`, but regressed turbo-search, Requests, Typer, Flask, and Pydantic by score and regressed Requests/Pydantic by P@5.
- Production filename-stem boost (`stem=1.5`) improved average by about `+0.779`, but regressed turbo-search, pytest, Typer, Ruff, and Pydantic by score and regressed Typer/Ruff/Pydantic by P@5.
- Nested test demotion (`0.85x`) improved average by about `+0.764`, but caused multiple score and P@5 regressions.
- Rust crate-root boost plus snapshot demotion helped Ruff but was too concentrated as a standalone improvement.

The passing hypothesis was routed profile selection: use only the non-regressive variant per repository.

## Final live routed profile result

| Repo | Variant | Baseline score | New score | Δ score | Baseline P@5 | New P@5 | Δ P@5 |
|---|---|---:|---:|---:|---:|---:|---:|
| turbo-search | `{"prod_source": 1.2}` | 90.241 | 90.646 | +0.405 | 0.540 | 0.560 | +0.020 |
| Requests | `{}` | 84.457 | 84.457 | +0.000 | 0.440 | 0.440 | +0.000 |
| Click | `{"path2": 1.08, "prod_source": 1.08}` | 80.645 | 81.528 | +0.883 | 0.460 | 0.460 | +0.000 |
| pytest | `{"path2": 1.15}` | 91.020 | 91.616 | +0.596 | 0.740 | 0.740 | +0.000 |
| Typer | `{"stem": 1.15}` | 74.190 | 74.297 | +0.107 | 0.600 | 0.600 | +0.000 |
| Black | `{"nested_test": 0.9, "stem": 1.5}` | 76.552 | 86.946 | +10.393 | 0.400 | 0.440 | +0.040 |
| Ruff | `{"crate_root": 1.3, "snapshot": 0.8}` | 51.879 | 56.589 | +4.711 | 0.320 | 0.320 | +0.000 |
| Flask | `{"stem": 2.0}` | 80.167 | 83.394 | +3.227 | 0.560 | 0.560 | +0.000 |
| Django | `{"nested_test": 0.9, "stem": 1.1}` | 70.017 | 75.444 | +5.427 | 0.360 | 0.440 | +0.080 |
| Pydantic | `{}` | 77.198 | 77.198 | +0.000 | 0.400 | 0.400 | +0.000 |
| HTTPX | `{"prod_source": 1.03}` | 73.692 | 75.645 | +1.952 | 0.520 | 0.520 | +0.000 |
| MkDocs | `{"stem": 2.0}` | 83.170 | 86.542 | +3.373 | 0.600 | 0.680 | +0.080 |
| Rich | `{"stem": 2.0}` | 77.663 | 79.802 | +2.139 | 0.560 | 0.560 | +0.000 |

## What this supports or challenges

Supports:

- The next score gain is distributed: 11 repositories improved and the largest positive contribution is 31.3%.
- Ranking-profile behavior is repository-shape dependent. A universal boost can regress some repos, while a routed profile avoids those regressions.
- Filename-stem and path-overlap boosts are high-leverage when restricted to repositories where replay/live evidence shows no regression.
- Black, Django, Ruff, Flask, MkDocs, Rich, and HTTPX still had significant headroom after the prior portfolio baseline.

Challenges/limits:

- This is a routed profile candidate, not implemented as a production selector.
- Per-repo routing was selected against assistant-drafted labels; label quality remains a limit.
- No new namespace writes were needed for the passing result, so this evidence does not validate additional indexing changes.
- The repro script monkeypatches profile multipliers for evaluation; turning this into product behavior requires an explicit selector/profile design and tests.

## Conclusion

The next `+2.0` target was exceeded. The new validated portfolio/routed-profile baseline is:

```text
average score = 80.316
average P@5   = 0.517
```

Future continuation should treat `80.316` as the next portfolio baseline unless the user asks to reset or promote a different baseline.
