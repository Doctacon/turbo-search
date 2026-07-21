Status: done
Created: 2026-07-14
Updated: 2026-07-14
Parent: .10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md
Depends-On: None

# Add Buoy CI, Release Workflow, and Public Files

## Scope

Implement `.10x/specs/buoy-ci-and-github-releases.md` and `.10x/specs/buoy-public-project-surface.md`: pinned least-privilege workflows, truthful initial badges, changelog, contributing/security/releasing docs, package metadata, and automated workflow/static checks.

## Acceptance criteria

- CI/release workflows satisfy every trigger, permission, pinning, build/test, approval, attestation, GitHub-only, and reproducibility requirement.
- README stays within details-on-demand limits and displays only CI/license badges before release.
- Public files and package classifiers accurately reflect current behavior and support.
- Workflow/version/asset/no-PyPI assertions have focused tests or deterministic validation.
- Full suite, build, links, YAML/static checks, and independent security/technical/editorial review pass.

## Explicit exclusions

Commit/push, external environment configuration, tag/release creation, PyPI, branch protection, issue templates, dependency bots, Code of Conduct contact invention, and live Turbopuffer work.

## References

- `.10x/specs/buoy-ci-and-github-releases.md`
- `.10x/specs/buoy-public-project-surface.md`
- `.10x/research/2026-07-14-buoy-github-release-automation.md`

## Evidence expectations

Workflow inventory and pins, permission/trigger assertions, local commands, README/public-file validation, complete tests/build, and independent review.

## Progress and notes

- 2026-07-14: Parent execution authorized; assigned to one worker.
- 2026-07-14: Added pinned least-privilege CI/release workflows, side-effect-free release checks and seven tests, truthful CI/license badges, changelog/contribution/security/release docs, and package metadata. Focused tests pass on Python 3.11/3.13; full 233-test suites, lock/build/assets/metadata/links/SVG/diff checks pass. Evidence: `.10x/evidence/2026-07-14-buoy-ci-release-public-files.md`.
- 2026-07-14: Repaired review blockers by enforcing annotated tag objects before release mutation, adding lightweight/annotated regressions, pinning `hatchling==1.31.0`, strengthening approved-action identity/comment assertions, and keeping 0.2.0 changelog state pending without nonexistent release links. Focused 9 and full 235 tests plus build/assets/lock/diff checks pass.
- 2026-07-14: Final independent review passed. Review: `.10x/reviews/2026-07-14-buoy-ci-release-public-files-review.md`.

## Blockers

- None.
