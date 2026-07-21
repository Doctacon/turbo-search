Status: active
Created: 2026-07-21
Updated: 2026-07-21

# Label-Driven Main-Push Automatic GitHub Release

## Purpose and scope

Publish one deterministic stable GitHub Release automatically after a passing labeled `develop -> main` PR is merge-committed. No committed release version, changelog preparation, tag push, environment approval, PyPI, or Turbopuffer operation is involved.

This specification supersedes `.10x/specs/superseded/main-push-automatic-github-release-static-version.md` for future releases. Its deterministic build, least privilege, serialization, immutable exact-state, collision, final verification, v0.4 legacy, and portability guarantees remain.

## Trigger and merged-PR authority

The workflow triggers only on pushes to `main`, serialized repository-wide with `cancel-in-progress: false`.

Before mutation, exact `GITHUB_SHA` MUST:

- be a two-parent merge commit ordered `[prior main, exact develop head]`;
- resolve through GitHub's commit-associated-PR API to exactly one closed/merged same-repository PR with `merge_commit_sha=GITHUB_SHA`, base `main`, head `develop`, and merge method represented by that exact commit;
- have exactly one `release:patch|release:minor|release:major` label.

Any ambiguity, squash/rebase topology, different PR, missing/multiple label, or API mismatch fails before build publication or mutation.

## Version and notes

Using prior main as the base, derive the target version exactly as `.10x/specs/develop-to-main-release-readiness.md`. The recomputed base tag, label, and target MUST equal the readiness semantics.

Project metadata MUST be dynamic through pinned `hatch-vcs==0.5.0`; build and install validation use exact `SETUPTOOLS_SCM_PRETEND_VERSION=<target>`. Source checkouts may expose a PEP 440 VCS development version; published wheel/sdist and `buoy --version` MUST expose exact stable target SemVer.

`CHANGELOG.md` remains frozen history through v0.4.0. The GitHub Release uses generated notes over the exact previous-tag-to-current range.

## Validation and deterministic build

Read-only jobs use `contents: read`, `pull-requests: read`, and no secrets. They MUST:

1. validate merged PR/topology/label and tag authority;
2. validate dynamic metadata/frozen changelog/current repository policy;
3. run complete locked Python 3.11 and 3.13 validation;
4. build wheel/sdist exactly once with target override and deterministic environment;
5. verify exact names/metadata/inventory, clean install, CLI/help/version, and exact bundled tokenizer;
6. produce a hash-addressed immutable state plan from authoritative tag/Release/assets/provenance inspection.

The final publication job alone receives `contents: write`, `id-token: write`, `attestations: write`, and artifact-read permission. It installs nothing and executes no repository code.

## Exact state machine

For target `TAG=v<target>` and exact main `SHA`:

### Create

Only when tag ref and Release are both absent:

- REST-create annotated tag object `TAG`, message `Buoy <target>`, fixed GitHub Actions bot tagger, object `SHA` commit;
- REST-create `refs/tags/TAG` to that object;
- on ref 422, perform one full authoritative reinspection; exact complete becomes no-op, every partial/mismatch fails;
- attest exact wheel/sdist subject names/digests for repository `Doctacon/buoy`, workflow `release.yml`, source ref `refs/heads/main`, and exact `SHA`;
- REST-create non-draft/non-prerelease Release `Buoy <target>` with generated notes and exactly those two built assets;
- unconditionally reinspect tag/Release, download and hash both assets, and verify provenance before success.

### No-op

Only exact complete matching tag peel, Release identity, two asset names/digests, and provenance succeeds without mutation.

### Permanent fail

Every lightweight, tag-only, Release-only, partial asset, wrong peel/identity/digest/provenance, conflicting target, or repeated mutation state fails without completion, overwrite, move, deletion, cleanup, or retry repair.

## Legacy v0.4.0

The sole immutable legacy no-op remains exactly as recorded under repository `Doctacon/buoy-search`, source ref `refs/tags/v0.4.0`, commit `c49dc0582bf3f06a16eafdcca0707d1e64e1c58d`, exact two asset digests, workflow, tag, and Release identity. No future target may use either legacy repository or source-ref exception.

## Acceptance scenarios

- Merge-committed patch-labeled PR over v0.4.0 computes/publishes exact v0.4.1 automatically.
- Main SHA without exact merged PR/label/topology fails before mutation.
- Build metadata and installed CLI equal target despite dynamic source metadata.
- Existing exact complete target no-ops; every partial/mismatch permanently fails.
- Published assets have exact digests and canonical future provenance.

## Explicit exclusions

Static project/module/lock release version; committed pending changelog; squash/rebase main promotion; manual tag/workflow/environment approval; PyPI; Turbopuffer; destructive repair; force push; product changes.
