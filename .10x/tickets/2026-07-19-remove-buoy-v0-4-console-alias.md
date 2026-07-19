Status: active
Created: 2026-07-19
Updated: 2026-07-19
Parent: .10x/tickets/2026-07-19-buoy-v0-4-compatibility-removal-plan.md
Depends-On: None

# Remove Buoy 0.4 Console Alias

## Scope

Implement `.10x/specs/buoy-v0-4-console-alias-removal.md` as one bounded 0.4.0 package cutover:

- remove the `turbo-search` script entry from `pyproject.toml`;
- delete the dedicated `buoy_search.cli:legacy_main` hook and alias-only tests/imports;
- set coherent candidate 0.4.0 package/module/lock metadata required to build and identify the candidate wheel;
- replace legacy-presence validation with wheel metadata, clean-install, and same-environment released-0.3.0-to-candidate-0.4.0 upgrade validation;
- update only console-command migration, changelog, package identity, and release-validation text affected by this removal.

## Acceptance criteria

- Source and built metadata expose `buoy = buoy_search.cli:main` and no `turbo-search` entry point; `legacy_main` is absent.
- `buoy --help`, `buoy --version`, `python -m buoy_search --help`, parser behavior, outputs, exit codes, direct-command defaults, and safety gates remain unchanged except the reported 0.4.0 version.
- Candidate package/module/lock metadata consistently identifies 0.4.0 without tagging, publishing, or creating a release.
- A fresh isolated candidate-wheel install has `buoy` and no package-owned `turbo-search` launcher.
- A second isolated environment installs the released GitHub 0.3.0 wheel only after verifying SHA-256 `048dba11df692a7efcd7ab7269fc2eec82f6b53e57573a3de113bbd051750bab`, proves both 0.3 launchers, upgrades that same environment normally to the candidate wheel, then proves 0.4.0 `buoy` works and package metadata plus launcher-directory inspection find no `turbo-search`.
- Focused CLI/package/release tests, complete Python 3.11/3.13 suites, wheel/sdist build and inventory, migration-reference checks, independent review, and hosted checks pass.
- Console migration guidance says only to replace the executable name and does not promise deletion of user-owned launchers.
- No retained compatibility, state/data, remote behavior, or environment-alias behavior changes.

## Validation and evidence expectations

Record exact changed files, artifact paths/hashes/versions, 0.3 URL and digest verification, isolated install/upgrade commands, installed entry points and launcher listings before/after, primary CLI outputs, focused/full tests, distribution inventory, hosted run identities, and an explicit no-state/no-remote/no-publication attestation. Evidence must distinguish clean-install absence from same-environment upgrade deletion.

## Dependencies and parallelism

No child execution dependency. Work may proceed in parallel with `.10x/tickets/2026-07-19-remove-buoy-v0-4-environment-aliases.md`, but the two reviewed diffs and coherent 0.4.0 metadata must be assembled into one aggregate candidate before integration to `develop`.

## Blockers

None.

## Explicit exclusions

Environment-alias runtime/config changes; removal of any other compatibility; arbitrary user-owned launcher cleanup; unrelated parser refactoring; state/data migration; remote operations; PyPI publication; Git tag/GitHub Release creation; stale skill-reference correction.

## References

- `.10x/tickets/2026-07-19-buoy-v0-4-compatibility-removal-plan.md`
- `.10x/specs/buoy-v0-4-console-alias-removal.md`
- `.10x/specs/buoy-v0-4-environment-alias-removal.md`
- `.10x/decisions/buoy-product-identity-and-compatibility-v0-3.md`
- `.10x/evidence/2026-07-16-buoy-v0-3-0-github-release.md`

## Progress and notes

- 2026-07-19: Opened from the ratified active console-removal specification. No implementation performed.
- 2026-07-19: Began bounded implementation on `work/remove-v0-4-console-alias` from `develop` commit `31b355a`; read the governing plan, both active 0.4 compatibility specs, identity/local/precision/release-validation specs, compatibility inventory research, shaping reviews, and immutable v0.3.0 release evidence before changing source.
