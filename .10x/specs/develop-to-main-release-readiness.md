Status: active
Created: 2026-07-21
Updated: 2026-07-21

# Label-Driven Develop-to-Main Release Readiness

## Purpose and scope

Make one same-repository `develop -> main` PR the complete release-control surface: one explicit SemVer label, four deterministic checks, merge-commit auto-merge, and no version/changelog preparation.

This specification supersedes `.10x/specs/superseded/develop-to-main-release-readiness-static-version.md` for future releases while retaining its protected prospective-merge, test, distribution, no-provider, and portability guarantees.

## PR and label contract

The workflow MUST trigger only for pull requests targeting `main`. The PR MUST be non-draft with exact head `Doctacon/buoy:develop` and base `Doctacon/buoy:main`.

Exactly one label MUST exist from:

- `release:patch`
- `release:minor`
- `release:major`

Missing or multiple release labels fail. Other non-release labels are allowed. Labeled/unlabeled/synchronize/reopen events rerun readiness.

## Version derivation

Let `B` be the highest stable `vMAJOR.MINOR.PATCH` annotated tag whose exact complete GitHub Release/provenance state is valid and whose peeled commit is reachable from current base main. Any higher stable tag that is lightweight, partial, mismatched, or not base-reachable fails closed instead of being ignored.

The target version increments `B` using the exact release label:

- patch: `M.m.(p+1)`
- minor: `M.(m+1).0`
- major: `(M+1).0.0`

Core identifiers MUST have no leading zeros. The target annotated tag and Release MUST both be absent.

## Prospective merge validation

GitHub's exact prospective merge commit MUST be checked out and have ordered parents `[current base main, exact head develop]`. Its tree is the candidate.

Policy MUST verify:

- exact repository/branches/parents;
- exact one-label version plan and base-tag authority;
- dynamic project version metadata uses pinned `hatch-vcs==0.5.0` and no committed static project/module/lock release version;
- `CHANGELOG.md` is frozen history through v0.4.0 with future notes delegated to canonical GitHub Releases;
- canonical repository `Doctacon/buoy`, exact legacy v0.4 exception, no PyPI/Turbopuffer release behavior;
- target tag/Release absence and no partial state.

## Required checks

The workflow MUST emit these exact GitHub Actions check-run job names, each app-bound under ID 15368:

1. `Release readiness / Policy`
2. `Release readiness / Python 3.11`
3. `Release readiness / Python 3.13`
4. `Release readiness / Distribution`

Main protection requires exactly those contexts with `strict=false`. Missing/skipped/cancelled/stale/failed checks block merge.

Python jobs independently use locked dependencies, validate frozen ranking/C6 contracts, and run the complete suite without secrets, model/provider/live retrieval/apply/eval, or mutation.

Distribution builds once with `SETUPTOOLS_SCM_PRETEND_VERSION=<target>` plus deterministic `SOURCE_DATE_EPOCH`, `PYTHONHASHSEED=0`, `TZ=UTC`, and `LC_ALL=C`. It verifies exact target-version wheel/sdist names and metadata, clean install, CLI/help/version, bundled tokenizer, inventory, and absence of internal/legacy artifacts.

## Automatic merge adapter

A separate `pull_request_target` workflow MAY enable auto-merge only when all exact PR/repository/label predicates above hold. It MUST:

- never check out or execute PR code;
- use only GitHub metadata and native `gh`/GraphQL;
- request merge method `MERGE`;
- use least permissions needed for pull-request/contents merge control;
- make no branch, tag, Release, package, provider, or configuration mutation beyond enabling auto-merge for that exact PR.

Repository setting `allow_auto_merge` MUST be true. Normal branch protection remains the merge boundary. Human manual merging remains allowed only with merge method `MERGE` and passing checks.

## Acceptance scenarios

- Exact patch label over released v0.4.0 computes 0.4.1, checks pass, and merge-commit auto-merge waits for protection.
- Minor/major labels reset lower identifiers correctly.
- Missing/multiple labels, draft/cross-repo/wrong branches, ambiguous tag authority, existing/partial target, wrong dynamic metadata, wrong job names, or failed validation block without mutation.
- Adding/removing a release label reruns and cannot merge while invalid.
- Auto-merge adapter never checks out untrusted code.

## Explicit exclusions

Committed release-version bump; pending changelog sections; squash/rebase release merge; tag/Release creation during PR checks; PyPI; Turbopuffer; force push; environment approval; manual workflow dispatch; recurring ancestry bridge; product behavior changes.
