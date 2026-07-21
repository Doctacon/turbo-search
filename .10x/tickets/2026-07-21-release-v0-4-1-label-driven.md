Status: blocked
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: .10x/tickets/2026-07-21-configure-label-driven-release-hosting.md

# Release v0.4.1 Through Label-Driven Automation

## Scope

Use existing open PR #93 as the first end-to-end proof: after all implementation/configuration dependencies integrate to develop, add only `release:patch`; verify four exact passing readiness contexts, target 0.4.1, and final controller merge with immutable trailers; observe automatic main-push publication; verify exact tag/Release/assets/digests/provenance/generated notes/PyPI absence; record review and closure.

## Acceptance criteria

- PR #93 exact head equals current develop, base equals current main, and has one patch label.
- Target computes from valid v0.4.0 to v0.4.1; no static 0.4.1 preparation remains.
- Four exact readiness checks pass and the final readiness controller revalidates and merge-commits exact head/plan without manual merge or bypass.
- Main merge has exact two-parent topology and triggers one serialized release run.
- Annotated v0.4.1, non-draft/non-prerelease Release, exact wheel/sdist/downloaded digests, canonical `Doctacon/buoy` main-ref provenance, generated notes, and no PyPI pass.
- Any partial/mismatch stops without repair/retry/destruction.
- Independent final review and coherent parent closure pass.

## Explicit exclusions

Manual merge/tag/workflow/environment approval; version/changelog commit; squash/rebase; PyPI; Turbopuffer; force push; repair of partial release state; product changes.

## References

- `.10x/specs/develop-to-main-release-readiness.md`
- `.10x/specs/main-push-automatic-github-release.md`
- `.10x/tickets/2026-07-21-configure-label-driven-release-hosting.md`
- PR #93: `https://github.com/Doctacon/buoy/pull/93`

## Evidence expectations

Exact PR/labels/auto-merge/checks/merge; release run/logical state; tag object/peel; Release/assets/download hashes; attestations; PyPI absence; no-provider attestation; independent review.

## Blockers

Blocked on hosted configuration completion.
