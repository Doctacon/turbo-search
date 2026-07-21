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
- Exact-project experiment configuration replaced static project version with `dynamic = ["version"]`, pinned build requirements `hatchling==1.31.0` plus `hatch-vcs==0.5.0`, configured `[tool.hatch.version] source = "vcs"`, configured the VCS hook version file `src/buoy_search/_version.py`, and imported `__version__` from that generated module.
- Commands were `uv lock`, `uv sync --locked`, installed-version import, `SETUPTOOLS_SCM_PRETEND_VERSION=0.4.1 SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD) PYTHONHASHSEED=0 TZ=UTC LC_ALL=C uv build --out-dir dist`, a new local test commit, then `uv lock --check`.
- Exact-project experiment succeeded:
  - lock diff removed only root `version = "0.4.1"`; root remained `{ editable = "." }`;
  - `uv sync --locked` installed VCS development version `0.4.1.dev70+g5ce5c1155.d20260721`;
  - exact build produced wheel SHA-256 `366444fbac08c2a2fa87e438efff7b3bb391d3a6129d148b8e58a64ba7ca238b` and sdist SHA-256 `5433fc2f7a1a545ca7de218db5c261b1a164154c7ffeb099d7a77f80ff2464ef` with exact 0.4.1 names;
  - `uv lock --check` remained valid after a new commit;
  - generated `_version.py` was untracked, confirming the required ignore/build lifecycle.
- The generated version file is refreshed only on install/build. Clean workflows must run locked sync/build before importing from source, and the generated file must not be tracked.
- GitHub can recover the exact merged release PR from the resulting merge commit. Main-push validation can require exactly one associated closed/merged PR with exact merge SHA, base `main`, head `develop`, same repository, and exactly one release label.
- GitHub native queued auto-merge is available but disabled. Review found mutable-label and concurrent-event authority risks in using queued auto-merge. A safer design is a final no-checkout job in the readiness workflow: after all four jobs pass, refetch exact current metadata, recompute the plan, and immediately merge with `gh pr merge --merge --match-head-commit`, embedding immutable plan trailers.
- Branch protection matches check-run job names. Release-readiness job names must themselves be the exact unique required contexts.

## Conclusion

The contract is technically feasible with the existing stack. The smallest safe design uses:

- one exact label: `release:patch`, `release:minor`, or `release:major`;
- highest valid stable annotated release tag reachable from base main as version authority;
- pinned `hatch-vcs==0.5.0` plus exact build override;
- frozen historical changelog and GitHub-generated future notes;
- no-checkout final merge controller using method `MERGE`, exact head matching, current metadata reinspection, and immutable plan trailers;
- main-push recovery of exact merged PR plus immutable trailer authority and verification of two-parent merge topology before any release mutation.

## Limits

The experiment did not publish, merge, tag, alter protection, create labels, enable auto-merge, access Turbopuffer, or mutate user/product state. Hosted implementation still requires exact tests and an end-to-end v0.4.1 proof.
