Status: active
Created: 2026-07-19
Updated: 2026-07-19

# Buoy 0.4 Internal Record Artifact Exclusion

## Purpose and scope

Keep Buoy's internal `.10x/**` project records durable in the source repository while excluding them from every Buoy 0.4 wheel and source distribution. This packaging boundary prevents record-only evidence updates from changing an otherwise identical candidate artifact.

This specification governs only the repository-root `.10x` directory and all of its descendants.

## Behavior

- The repository-root `.10x` directory and all `.10x/**` records MUST remain in the repository.
- Buoy 0.4 wheel and sdist builds MUST exclude every repository-root `.10x/**` path.
- The packaging change MUST exclude only `.10x/**`. It MUST NOT introduce another exclusion.
- Runtime and packaged application code, bundled package data, and user documentation MUST remain unchanged by this packaging change.
- Wheel and sdist inventories MUST contain zero `.10x` entries. For the sdist, this assertion applies after removing the archive's single top-level distribution directory from each member path.
- Under controlled deterministic build conditions, adding only a record beneath `.10x/**` MUST NOT change either the wheel or sdist. Corresponding archives MUST be byte-for-byte identical and have equal SHA-256 digests.

## Controlled determinism procedure

The comparison MUST use the same source content outside `.10x/**`, interpreter, platform, locked build dependencies, build command, fixed `SOURCE_DATE_EPOCH`, environment, and fresh temporary output directories. Build once, add only one record beneath `.10x/**`, then build again. Record both complete inventories, byte comparisons, and SHA-256 digests for the corresponding wheel and sdist.

The record-only delta used for this proof MUST remain internal evidence; it MUST NOT alter runtime/package code, bundled package data, tests, user documentation, or build configuration between the two compared builds.

## Aggregate validation

After the exclusion is implemented, aggregate validation MUST:

- inspect the wheel and sdist inventories and prove zero `.10x` entries;
- complete the controlled deterministic comparison above;
- rerun the candidate clean-wheel installation and the digest-verified released-0.3.0-to-candidate-0.4.0 same-environment upgrade procedure governed by `.10x/specs/superseded/buoy-v0-4-release-validation.md`;
- reconfirm candidate metadata, primary-launcher continuity, and removal of the package-owned `turbo-search` launcher.

## Acceptance scenarios

### Repository records are retained but not distributed

Given the repository contains `.10x/**` records,
when the Buoy 0.4 wheel and sdist are built,
then the repository records remain present in the source tree,
and neither artifact inventory contains a `.10x` member.

### Record-only evidence cannot perturb artifacts

Given controlled deterministic build conditions and a completed baseline build,
when the only source-tree delta is one added record beneath `.10x/**`,
then the rebuilt wheel is byte-for-byte identical to the baseline wheel,
and the rebuilt sdist is byte-for-byte identical to the baseline sdist,
and each corresponding SHA-256 digest is equal.

### No packaging scope expansion

Given the `.10x/**` exclusion is implemented,
when the implementation diff and artifact inventories are reviewed,
then no other exclusion was introduced,
and runtime/package code, bundled package data, and user documentation are unchanged.

## Explicit exclusions

Removing or relocating repository records; excluding any path other than `.10x/**`; runtime or CLI behavior changes; package-data changes; user-documentation changes; compatibility changes beyond the already governed Buoy 0.4 removals; publication to a package registry; Git tag creation; GitHub Release creation; release publication.
