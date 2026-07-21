Status: open
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-buoy-v0-4-0-release-plan.md
Depends-On: .10x/tickets/2026-07-21-promote-develop-to-main-for-v0-4-0.md

# Create Buoy v0.4.0 GitHub Release

## Scope

- Preflight exact reviewed main/version/CI, immutable prior tags/releases, absent v0.4.0 conflicts, release environment approval, dry tag/assets checks, and no PyPI publication.
- Create and push annotated `v0.4.0` from the exact reviewed main commit only.
- Verify authoritative remote metadata reports an annotated tag object peeled to that main commit.
- Observe the unique workflow through validation/build and the protected `release` environment wait; approve only the expected run/commit/version/artifacts.
- Verify successful Release publication, exact wheel/sdist identities and digests, generated notes, and provenance attestation.
- Record complete evidence and obtain independent review.

## Acceptance criteria

- No v0.4.0 tag, release, or conflicting workflow exists before mutation.
- Annotated v0.4.0 points to exact reviewed main and remote object type is `tag`.
- Validation/build pass before environment approval; approval targets only the expected deployment.
- Release contains exactly the expected 0.4.0 wheel/sdist with verified digests and provenance.
- No PyPI, branch/source mutation, tag overwrite, release replacement, Turbopuffer operation, or user-state mutation occurs.
- Evidence and independent review pass before closure.

## Explicit exclusions

Source/changelog finalization; PyPI; deleting/replacing tags or releases; branch protection; Turbopuffer.

## References

- `.10x/specs/buoy-ci-and-github-releases.md`
- `docs/releasing.md`
- `.10x/tickets/done/2026-07-15-create-buoy-v0-3-0-github-release.md`

## Evidence expectations

Exact main/tag object/peeled commit; preflight state; workflow/run/jobs/artifacts/deployment/approval identity and chronology; release ID/URL/assets/digests; provenance; no-PyPI observation; review.

## Blockers

Blocked on completed main promotion and exact-main CI.

## Progress and notes

- 2026-07-21: Read-only planning preflight found no local/remote `v0.4.0` tag or GitHub Release and found the `release` environment configured with required reviewer `Doctacon`, self-review allowed. No tag, workflow, deployment, release, or publication was created.
