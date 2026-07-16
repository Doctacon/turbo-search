Status: recorded
Created: 2026-07-15
Updated: 2026-07-15
Relates-To: .10x/tickets/done/2026-07-15-promote-develop-to-main-for-v0-3-0.md, .10x/tickets/2026-07-15-buoy-v0-3-0-release-plan.md

# Buoy v0.3.0 Main Promotion

## What was observed

After the independently authorized merge phase completed, exact remote refs were:

- `develop`: `5658fe4cc5c12b80d8fd64aa7963f5f1907133db`;
- `main`: `595d157177bd032c20cf6e6c0112ee6b43212a88`.

### Protected sync PR #23

GitHub reports PR #23 merged at `2026-07-16T21:50:43Z`:

- URL: `https://github.com/Doctacon/buoy-search/pull/23`;
- exact reviewed base: `1441c142dae2f501fd8d7306ab3bf1a9db1532d2`;
- exact reviewed head: `e32061ea33f4efe41cd4288e85083748fd0102fc`;
- merge commit: `5658fe4cc5c12b80d8fd64aa7963f5f1907133db`;
- ordered merge parents: base `1441c142dae2f501fd8d7306ab3bf1a9db1532d2`, then sync head `e32061ea33f4efe41cd4288e85083748fd0102fc`.

The sync head itself has exact parents release-prepared develop `1441c142dae2f501fd8d7306ab3bf1a9db1532d2` and prior main `1fa99431de85b9de435250f273919bf2d247d1fc`. Therefore the merged develop contains both exact histories.

PR #23's required checks all passed in run `29537212668`:

- Python 3.11: `https://github.com/Doctacon/buoy-search/actions/runs/29537212668/job/87751253365`;
- Python 3.13: `https://github.com/Doctacon/buoy-search/actions/runs/29537212668/job/87751253415`;
- Build distributions: `https://github.com/Doctacon/buoy-search/actions/runs/29537212668/job/87751374200`.

### Release PR #22

GitHub reports PR #22 merged at `2026-07-16T21:55:44Z`:

- URL: `https://github.com/Doctacon/buoy-search/pull/22`;
- exact base: prior main `1fa99431de85b9de435250f273919bf2d247d1fc`;
- exact fresh head: synced develop `5658fe4cc5c12b80d8fd64aa7963f5f1907133db`;
- release merge commit: `595d157177bd032c20cf6e6c0112ee6b43212a88`;
- ordered merge parents: prior main `1fa99431de85b9de435250f273919bf2d247d1fc`, then exact synced develop `5658fe4cc5c12b80d8fd64aa7963f5f1907133db`.

The strict-freshness pull-request CI at exact head `5658fe4` passed in run `29537511175`:

- Python 3.11: `https://github.com/Doctacon/buoy-search/actions/runs/29537511175/job/87752222280`;
- Python 3.13: `https://github.com/Doctacon/buoy-search/actions/runs/29537511175/job/87752222275`;
- Build distributions: `https://github.com/Doctacon/buoy-search/actions/runs/29537511175/job/87752317268`.

The exact synced develop push also passed run `29537509568` before the release merge.

### Tree and ancestry verification

The following commits all have identical tree `caee060f1df2d1d0025a7c566dcca30fffc304f6`:

- release-prepared develop `1441c142`;
- ancestry-only sync head `e32061ea`;
- protected develop merge `5658fe4c`;
- released main merge `595d1571`.

Exact-parent assertions, `merge-base --is-ancestor` checks for both prior main and release-prepared develop, `git diff --exit-code 1441c142..595d1571`, and `git diff --check` all passed. Project/module versions remained 0.3.0. Remote develop is an ancestor of remote main; `origin/main...origin/develop` divergence is one main-only merge commit and zero develop-only commits.

### Main push CI

The push to exact released main commit `595d157177bd032c20cf6e6c0112ee6b43212a88` completed successfully in CI run `29537732717`:

- run: `https://github.com/Doctacon/buoy-search/actions/runs/29537732717`;
- Python 3.11: `https://github.com/Doctacon/buoy-search/actions/runs/29537732717/job/87752884520` — success;
- Python 3.13: `https://github.com/Doctacon/buoy-search/actions/runs/29537732717/job/87752884538` — success;
- Build distributions: `https://github.com/Doctacon/buoy-search/actions/runs/29537732717/job/87752998132` — success.

No `v0.3.0` tag or GitHub Release existed during this post-merge record pass.

## Procedure

1. Fetched current origin develop/main and merged origin/develop into the records work branch with a merge commit, never rebase.
2. Read PR #23/#22 hosted metadata and exact merge commit IDs.
3. Verified each merge commit's ordered parents, trees, and ancestor relationships locally.
4. Compared the release merge tree byte-for-byte with release-prepared develop and ran diff hygiene checks.
5. Queried GitHub Actions workflow/check-run metadata for sync PR, fresh release PR head, develop push, and exact main push.
6. Verified remote branch ancestry/divergence and absent v0.3.0 tag/Release.
7. Changed, committed, and pushed only durable promotion records on the existing work branch; performed no protected-branch or release mutation.

## What this supports or challenges

This supports every technical and hosted acceptance claim for protected promotion of release-prepared develop into main with preserved ancestry and passing required checks. It supports unblocking the v0.3.0 tag/Release child only after parent durable review closes the still-active promotion ticket.

## External-side-effect boundary

This records already-completed PR merges. This record pass performed only Git fetches, read-only GitHub/API queries, and the explicitly requested commit/push to the existing records work branch. It did not mutate main/develop, merge a PR, create/push a tag, approve an environment, create a GitHub Release, publish to PyPI, change protection, expose credentials, or contact Turbopuffer.

## Limits

Independent durable review and ticket closure remain parent-owned. The successful main push CI proves the reviewed tree passed hosted checks; it does not itself create or verify v0.3.0 release artifacts, provenance, or publication.
