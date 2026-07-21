Status: open
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-buoy-v0-4-0-release-plan.md
Depends-On: .10x/tickets/2026-07-21-validate-buoy-v0-4-0-release-candidate.md

# Promote Develop to Main for v0.4.0

## Scope

- Verify release-ready `develop`, current `main`, branch protection, PR #80, exact divergence, and no conflicting release operation.
- Create a dedicated ancestry-sync branch from exact release-ready `develop`, merge exact current `main` with a merge commit, and prove the resulting tree is content-identical to release-ready `develop` except for this ticket's already-reviewed release records where applicable.
- Open the ancestry-only sync PR to `develop`; require strict freshness, all three checks, exact-parent/tree evidence, and independent review; merge using a merge commit only.
- Revalidate updated `develop` and PR #80, require all checks and independent complete release-diff review, then merge PR #80 to `main` with a merge commit only.
- Verify exact parents/ancestry/tree and passing `main` push CI.

## Acceptance criteria

- Current `main` ancestry reaches `develop` through a protected PR without direct push, squash, rebase, force push, or protection change.
- The sync merge introduces no content from stale `main` over release-ready develop.
- PR #80 contains the exact reviewed release candidate, is clean/current, and passes Python 3.11, Python 3.13, and Build distributions.
- PR #80 merges with a merge commit whose parents preserve prior main and exact synced develop.
- Resulting `main` tree equals reviewed release-ready develop and main push CI passes.
- Durable evidence and independent review pass; no tag/Release/PyPI/Turbopuffer operation occurs.

## Explicit exclusions

Candidate source changes after review; tag or Release creation; publication; branch protection changes; direct push; squash/rebase; Turbopuffer.

## References

- `.10x/specs/protected-github-branches.md`
- `.10x/decisions/protected-development-and-github-release-governance.md`
- PR #80: `https://github.com/Doctacon/buoy-search/pull/80`
- `.10x/tickets/done/2026-07-15-promote-develop-to-main-for-v0-3-0.md`

## Evidence expectations

Exact pre/post refs, divergence, sync commit parents/tree, PR/check URLs, merge methods and parents, reviewed candidate tree identity, main push CI, independent review, and explicit no-publication/no-product-state boundary.

## Blockers

Blocked on completed candidate validation and review.

## Progress and notes

- 2026-07-21: Opened after PR #80 reported conflicts between `main` `820b8ab` and `develop` `ce262d4`. The established protected ancestry-only sync mechanism is record-backed from v0.3.0. No branch, PR, ancestry, tag, release, or product state changed.
