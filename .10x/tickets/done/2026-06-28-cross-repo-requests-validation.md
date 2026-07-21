Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/evidence/2026-06-28-repo-index-hygiene-and-profile-validation.md

# Cross-Repo Requests Validation

## Scope

Validate repo-search defaults on a different public repository after the user selected `psf/requests` and approved a new namespace.

In scope:

- Plan `https://github.com/psf/requests` with current GitHub repo defaults.
- Apply to a new namespace only.
- Draft a small source-backed seed eval dataset for Requests.
- Run live evals against the new namespace.
- Compare whether repo defaults generalize beyond `turbo-search`.

Out of scope:

- Private repo support.
- Namespace deletion or stale deletion.
- Mutating any existing namespace.
- Proprietary model APIs.

## Acceptance criteria

- Uses a new namespace for Requests.
- Plan/apply evidence records files/chunks/rows and confirms no deletes.
- Eval dataset loads through the existing eval harness.
- Live eval reports Precision@5, NDCG@10, Recall@10, MRR@10, and composite score.
- Existing tests and `git diff --check` pass.

## Blockers

- None. User selected `psf/requests` and new namespace validation.

## Progress and notes

- 2026-06-28: Opened after user agreed that a different repo is better validation and selected `psf/requests` with a new namespace.
- 2026-06-28: Planned `psf/requests` at commit `4ed3d1b3204caa6806a36125a39589044a02e807`: 130 files discovered, 117 selected, 729 chunks, no turbopuffer calls.
- 2026-06-28: Applied new namespace `github-psf-requests-v1`: 729 embeddings generated, 729 rows upserted, no deletes.
- 2026-06-28: Added `src/turbo_search/data/requests_repo_search_seed_evals.json` and ran live evals. Cross-repo evidence showed `max` aggregation beats `capped_sum_3` as the safe universal repo default. Evidence: `.10x/evidence/2026-06-28-cross-repo-requests-validation.md`.

## Current State

Done. Requests validation is complete and changed the default decision back to repo `max` aggregation with capped aggregation opt-in.
