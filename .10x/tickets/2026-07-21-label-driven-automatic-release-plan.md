Status: open
Created: 2026-07-21
Updated: 2026-07-21
Parent: None
Depends-On: None

# Label-Driven Automatic Release Plan

## Outcome

Replace static version/changelog release preparation with one labeled `develop -> main` PR that automatically merge-commits after four passing checks and automatically publishes a deterministic GitHub Release.

## Child sequence

1. `.10x/tickets/2026-07-21-implement-tag-derived-package-versioning.md`
2. `.10x/tickets/2026-07-21-implement-label-driven-release-readiness.md`
3. `.10x/tickets/2026-07-21-implement-label-driven-main-push-release.md`
4. `.10x/tickets/2026-07-21-configure-label-driven-release-hosting.md`
5. `.10x/tickets/2026-07-21-release-v0-4-1-label-driven.md`

Children are sequential because they overlap release metadata/tooling and hosted behavior. This parent is not executable.

## Aggregate acceptance criteria

- Dynamic Hatch VCS package versioning works with locked uv, source/editable development versions, exact release override, deterministic artifacts, clean installs, and current identity.
- One exact release label determines target SemVer from authoritative stable tag history.
- Four uniquely named readiness checks validate exact prospective merge and target artifacts.
- Safe no-checkout final readiness job merge-commits only exact same-repository release PRs after all four checks, embedding immutable plan trailers.
- Main-push workflow recovers the exact merged PR/label/topology and publishes through the immutable exact-state machine.
- Three release labels are configured; protection remains exact; mutable queued auto-merge remains unnecessary.
- Current PR #93 becomes the first patch-labeled proof and publishes exact v0.4.1 automatically.
- No committed version bump, pending changelog, manual merge/tag/workflow/environment approval, PyPI, Turbopuffer, force push, destructive repair, or product behavior change occurs.

## References

- `.10x/decisions/label-driven-tag-derived-automatic-releases.md`
- `.10x/specs/buoy-package-and-cli-identity.md`
- `.10x/specs/buoy-release-validation.md`
- `.10x/specs/develop-to-main-release-readiness.md`
- `.10x/specs/main-push-automatic-github-release.md`
- `.10x/specs/protected-github-branches.md`
- `.10x/research/2026-07-21-label-driven-tag-derived-release-automation.md`

## Progress and notes

- 2026-07-21: User explicitly authorized exactly one release label, tag-derived versions through open-source hatch-vcs, frozen historical changelog with GitHub-generated future notes, merge commits, automatic merge, and PR #93 as first v0.4.1 proof. Compatibility research passed without project mutation.

## Blockers

None.
