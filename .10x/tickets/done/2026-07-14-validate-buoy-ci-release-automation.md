Status: done
Created: 2026-07-14
Updated: 2026-07-14
Parent: .10x/tickets/done/2026-07-14-buoy-public-ci-release-plan.md
Depends-On: .10x/tickets/done/2026-07-14-add-buoy-ci-release-and-public-files.md

# Validate Buoy CI and Release Automation

## Scope

Adversarially validate and repair only integration defects in the completed public-project/workflow child before any commit, push, tag, environment, or release mutation.

## Acceptance criteria

- Workflow YAML parses and static assertions prove exact triggers, minimal permissions, SHA pins, matrix, locked install, full tests, build-once behavior, environment gate, version check, artifact attestation, and no PyPI path.
- Local execution of all portable CI/release preflight commands passes.
- A dry harness proves `v0.2.0` matching and rejects mismatched tags/releases without creating refs or releases.
- Built wheel/sdist, README badges, changelog, public docs, package metadata, links, SVG, tests, and diff hygiene pass.
- Independent adversarial review maps every governing criterion to evidence.

## Explicit exclusions

Git mutation, GitHub configuration, workflow dispatch, tag/release creation, PyPI, branch protection, and live operations.

## References

- `.10x/specs/buoy-ci-and-github-releases.md`
- `.10x/specs/buoy-public-project-surface.md`
- `.10x/tickets/done/2026-07-14-add-buoy-ci-release-and-public-files.md`

## Evidence expectations

Raw YAML/static reports, command outputs, negative version tests, package inventories, full suite/build, and independent review.

## Progress and notes

- 2026-07-14: Dependency closed; assigned to validator/repair worker.
- 2026-07-14: Adversarial local/static integration validation found no repair requirement. Workflow triggers/permissions/pins/matrix/build-once/gate/attestation/no-PyPI assertions pass; negative tag/asset harnesses pass; exact wheel/sdist and public surface validate; sequential Python 3.11 and 3.13 full suites each pass 235 tests. Evidence: `.10x/evidence/2026-07-14-buoy-ci-release-integration-validation.md`; raw: `.10x/evidence/.storage/2026-07-14-buoy-ci-release-integration-validation.json`.
- 2026-07-14: Initial review found evidence insufficiency only. Re-ran and retained raw focused/full test, build, positive/negative tag/asset, annotated-tag, lock/diff/index outputs plus complete wheel/sdist inventories and metadata. No implementation or external state changed.
- 2026-07-14: Final independent review passed. Review: `.10x/reviews/2026-07-14-validate-buoy-ci-release-automation-review.md`.

## Blockers

- None.
