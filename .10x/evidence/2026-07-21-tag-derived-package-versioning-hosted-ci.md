Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Relates-To: .10x/tickets/cancelled/2026-07-21-implement-tag-derived-package-versioning.md, .10x/reviews/2026-07-21-tag-derived-package-versioning-final-review.md

# Tag-Derived Package Versioning Hosted CI

## What was observed

GitHub PR #99 (`https://github.com/Doctacon/buoy/pull/99`) reported exact head `75dd2023ac542a93430accf339b0eb04f032eed1`. GitHub Actions run `29886520116` completed all jobs successfully:

- Python 3.11: pass in 2m9s, job `88818084531`;
- Python 3.13: pass in 1m52s, job `88818084523`;
- Build distributions: pass in 13s, job `88818356866`.

PR #99 remained open and was not merged while this evidence was recorded.

## Procedure

The hosted state was read with:

```text
gh pr view 99 --json headRefOid,statusCheckRollup,state,url
```

The returned head SHA was compared with local branch HEAD. Each check run reported `status: COMPLETED` and `conclusion: SUCCESS` under workflow `CI`.

## What this supports

This supports the ticket's exact-head hosted Python 3.11, Python 3.13, and distribution-build validation requirements. Together with `.10x/evidence/2026-07-21-tag-derived-package-versioning.md` and `.10x/reviews/2026-07-21-tag-derived-package-versioning-final-review.md`, it supports every implementation and review acceptance criterion before integration.

## Limits

The run proves only the checked PR head. It does not prove protected integration into `develop`, post-integration push CI, or behavior owned by later label-driven release tickets. No merge, tag, Release, registry, provider, or hosted configuration mutation was performed.
