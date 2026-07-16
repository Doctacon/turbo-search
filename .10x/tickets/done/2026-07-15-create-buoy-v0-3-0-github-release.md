Status: done
Created: 2026-07-15
Updated: 2026-07-16
Parent: .10x/tickets/2026-07-15-buoy-v0-3-0-release-plan.md
Depends-On: .10x/tickets/done/2026-07-15-promote-develop-to-main-for-v0-3-0.md

# Create Buoy v0.3.0 GitHub Release

## Scope

- Preflight reviewed main/version/CI, preserved v0.2.0/v0.2.1 history, absent v0.3.0 conflicts, and the existing release-environment approval gate.
- Create and push annotated `v0.3.0` from the exact reviewed main commit.
- Verify authoritative remote metadata reports object type `tag` and the expected peeled commit.
- Treat annotated-tag creation/push as the first external mutation. Then observe validation/build completion and the release environment wait; approve only the expected commit/version/artifacts. Approval gates provenance attestation and GitHub Release/assets creation, not the earlier tag push.
- Verify terminal workflow success, GitHub Release, wheel/sdist identities and digests, generated notes, and provenance attestation.
- Confirm no PyPI publication and record durable evidence/review.

## Acceptance criteria

- Existing tags/releases remain immutable and no v0.3.0 conflict exists before mutation.
- Annotated v0.3.0 points to exact reviewed main and remote object type is `tag`.
- Tag push occurs only after preflight and is recorded as an external mutation; the later environment approval gates attestation and GitHub Release/assets mutation, and only the expected run is approved.
- GitHub Release contains `buoy_search-0.3.0-py3-none-any.whl` and `buoy_search-0.3.0.tar.gz` with verifiable provenance.
- No PyPI, branch mutation, tag overwrite, source mutation, or Turbopuffer operation occurs.
- Independent review passes before closure.

## Explicit exclusions

Additional source changes, changelog final-link follow-up, PyPI, replacing tags/releases, branch protection, Turbopuffer.

## References

- `.10x/specs/buoy-ci-and-github-releases.md`
- `docs/releasing.md`
- `.10x/tickets/done/2026-07-14-create-buoy-v0-2-1-github-release.md`

## Evidence expectations

Preflight observations; tag object/peeled commit; workflow/run/job/deployment identity; approval boundary; release/assets/checksums/attestation; no-PyPI observation; independent review.

## Blockers

None. Main promotion completed and passed review.

## Progress and notes

- 2026-07-16: Strict preflight passed at exact reviewed main `595d157177bd032c20cf6e6c0112ee6b43212a88`: project/module/lock are 0.3.0; main push CI run `29537732717` passed; promotion evidence agrees; v0.2.0/v0.2.1 tag objects and v0.2.1 Release are preserved; v0.3.0 local/remote tag, Release, and workflow run are absent; PyPI returned 404; the `release` environment requires `Doctacon` review with self-review allowed; exact-main tag/assets dry checks and wheel/sdist metadata/content inspection passed. No external mutation had occurred at this checkpoint.

- 2026-07-16: Created/pushed exact annotated tag object `21a8d122151711a863dfb63d356baebbddca8d45`, verified its peel to reviewed main, and observed the single exact Release run `29538957482`. Validation/build passed before the run waited on exactly one `release` deployment; v0.3.0 Release was absent at that boundary.
- 2026-07-16: Approved only expected environment `18151168858` for exact run/commit after eligibility revalidation. Deployment `5481277630`, publication job `87756932412`, and the workflow completed successfully.
- 2026-07-16: Release `355388511` contains exactly the verified 0.3.0 wheel/sdist with matching downloaded/API digests and strict SLSA provenance. Isolated install behavior, prior immutable history, one-run uniqueness, no PyPI, and no Turbopuffer/branch/protection mutation passed. Evidence: `.10x/evidence/2026-07-16-buoy-v0-3-0-github-release.md`. Ticket remains active pending independent review.

- 2026-07-16: Corrected release chronology after review: preflight, tag push, hosted workflow approval/publication, verification, evidence recording, and commit occurred on July 16. Renamed temporal evidence and raw storage to `2026-07-16-*` and repaired references. Ticket creation and prior July 15 history remain unchanged; substantive IDs, hosted timestamps, digests, and claims are unchanged. Ticket remains active pending re-review.

- 2026-07-16: Two independent hosted-release audits passed after chronology was corrected in records. Review: `.10x/reviews/2026-07-16-buoy-v0-3-0-github-release-review.md`.

## Closure mapping

- Annotated tag: object `21a8d122151711a863dfb63d356baebbddca8d45`, exact reviewed main `595d157177bd032c20cf6e6c0112ee6b43212a88`.
- Workflow/approval: run `29538957482` passed; validation preceded environment wait/approval, which preceded attestation and Release creation.
- Release/assets: GitHub Release `355388511`; exact wheel/sdist identities, digests, metadata/content, generated notes, and SLSA provenance verified.
- Boundaries: prior history immutable, PyPI absent, no branch/source/tag overwrite or Turbopuffer operation.
- Review: pass with transient attestation-API availability recorded as residual risk.

## Retrospective

Release evidence chronology must use authoritative hosted event dates rather than the ticket's creation date. The release gate is two-stage: annotated-tag push is an external mutation, while the protected environment separately gates provenance and Release/assets publication.
