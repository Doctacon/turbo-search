Status: done
Created: 2026-07-21
Updated: 2026-07-21

# Label-Driven Tag-Derived Release Automation

## Question

Can Buoy remove committed release-version/changelog preparation and make one labeled `develop -> main` PR auto-merge and publish safely with the current Hatch/uv/GitHub stack?

## Sources and methods

- Inspected open-source `hatch-vcs` at commit `dfec2c06defdb4648eb66f6aadf7b57453d732cd`:
  - build dependency/source configuration: https://github.com/ofek/hatch-vcs/blob/dfec2c06defdb4648eb66f6aadf7b57453d732cd/README.md#L28-L47
  - exact-version override: https://github.com/ofek/hatch-vcs/blob/dfec2c06defdb4648eb66f6aadf7b57453d732cd/README.md#L80-L83
  - generated version file: https://github.com/ofek/hatch-vcs/blob/dfec2c06defdb4648eb66f6aadf7b57453d732cd/README.md#L84-L119
  - editable-install caveat: https://github.com/ofek/hatch-vcs/blob/dfec2c06defdb4648eb66f6aadf7b57453d732cd/README.md#L121-L123
- Inspected GitHub's commit-associated pull-request API: https://docs.github.com/en/rest/commits/commits#list-pull-requests-associated-with-a-commit
- Queried current repository settings: canonical `Doctacon/buoy`, merge/squash/rebase enabled, `allow_auto_merge=false`, and no release labels.
- Queried released v0.4.0 main commit `c49dc0582bf3f06a16eafdcca0707d1e64e1c58d`; GitHub returned exactly merged PR #85 with base `main`, head `develop`, and exact matching `merge_commit_sha`.
- In disposable `/tmp/buoy-hatch-vcs-check`, cloned exact develop `5ce5c11553ac69a997b25567023b4765f5e780c8`; converted project version to dynamic Hatch VCS using pinned `hatch-vcs==0.5.0`; generated `src/buoy_search/_version.py`; ran `uv lock`, `uv sync --locked`, exact-version deterministic build input, and lock check after a new commit. No project worktree was mutated.

## Findings

- `hatch-vcs` officially supports Hatch's VCS version source and generated version file. `SETUPTOOLS_SCM_PRETEND_VERSION` is the supported primary exact-version override.
- Exact-project experiment succeeded:
  - `uv.lock` represented root `buoy-search` as dynamic editable source with no churned root version;
  - `uv sync --locked` installed a VCS development version (`0.4.1.dev70+g5ce5c1155...`);
  - `SETUPTOOLS_SCM_PRETEND_VERSION=0.4.1 uv build` produced exact `buoy_search-0.4.1` wheel/sdist;
  - `uv lock --check` remained valid after a new commit.
- The generated version file is refreshed only on install/build. Clean workflows must run locked sync/build before importing from source, and the generated file must not be tracked.
- GitHub can recover the exact merged release PR from the resulting merge commit. Main-push validation can require exactly one associated closed/merged PR with exact merge SHA, base `main`, head `develop`, same repository, and exactly one release label.
- GitHub auto-merge is available but disabled. It can be enabled at repository level; a no-checkout `pull_request_target` adapter can enable merge-commit auto-merge only for exact same-repository `develop -> main` PRs with one release label.
- Branch protection matches check-run job names. Release-readiness job names must themselves be the exact unique required contexts.

## Conclusion

The contract is technically feasible with the existing stack. The smallest safe design uses:

- one exact label: `release:patch`, `release:minor`, or `release:major`;
- highest valid stable annotated release tag reachable from base main as version authority;
- pinned `hatch-vcs==0.5.0` plus exact build override;
- frozen historical changelog and GitHub-generated future notes;
- no-checkout auto-merge adapter using merge method `MERGE`;
- main-push recovery of exact merged PR/label and verification of two-parent merge topology before any release mutation.

## Limits

The experiment did not publish, merge, tag, alter protection, create labels, enable auto-merge, access Turbopuffer, or mutate user/product state. Hosted implementation still requires exact tests and an end-to-end v0.4.1 proof.
