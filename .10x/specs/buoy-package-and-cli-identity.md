Status: active
Created: 2026-07-14
Updated: 2026-07-19

# Buoy Package and CLI Identity

## Purpose and scope

Define the code and distribution identity for Buoy through the 0.4 release.

## Behavior

- Project metadata MUST use display name `Buoy`, distribution name `buoy-search`, current release version `0.4.0`, and Apache-2.0 licensing with a root `LICENSE` file.
- Implementation code MUST live under `src/buoy_search`; internal imports, tests, mocks, module commands, bundled data paths, reports, and build configuration MUST use `buoy_search`.
- The sole product console script MUST be `buoy = buoy_search.cli:main`; CLI help and version output MUST identify `buoy`.
- Version 0.4 MUST NOT expose a `turbo-search` console entry point or a dedicated `buoy_search.cli:legacy_main` hook.
- `python -m buoy_search` and `python -m buoy_search.autoresearch` MUST work. `turbo_search` Python imports/module execution remain an intentional clean break and MUST be documented in the migration guide.
- User agents, generated runner identifiers, self-referential eval questions, expected source paths, fixture names, and active user-facing error text MUST use the new identity.
- Existing semantic identifiers unrelated to branding—including source namespaces, plan IDs, apply IDs, deterministic remote `ts_*` row IDs, and intermediate `jf_*` chunk IDs—MUST NOT change solely for the rebrand.
- The wheel/sdist MUST contain `buoy_search` and required bundled datasets, and MUST NOT contain the old implementation package.

## Compatibility

- Scripts migrate from the removed `turbo-search` console entry point by replacing only the executable name with `buoy`; arguments and primary CLI behavior remain unchanged.
- Package installation and upgrade validation concerns package-owned launchers only. Buoy does not delete user-created aliases, copied launchers, wrappers, caches, or other files outside package-manager ownership.
- No Python import shim is provided.
- Existing plan and state compatibility is governed separately by `.10x/specs/buoy-local-compatibility.md`.
- Deprecated environment-alias removal is governed separately by `.10x/specs/buoy-v0-4-environment-alias-removal.md`.

## Acceptance scenarios

- A clean 0.4 install can run `buoy --version`, `buoy --help`, and `python -m buoy_search --help`, and has no package-owned `turbo-search` launcher.
- A normal same-environment upgrade from the immutable released 0.3.0 wheel keeps `buoy` working and removes the old package-owned `turbo-search` launcher.
- Importing representative modules from `buoy_search` succeeds; importing `turbo_search` is not part of the supported contract.
- Package build inspection finds the new module/data and no old implementation module, `turbo-search` entry point, or dedicated legacy hook.

## Explicit exclusions

GitHub repository mutation, PyPI publication, remote namespace changes, live Turbopuffer calls, arbitrary user-owned launcher cleanup, state-root compatibility removal, and environment-alias implementation.
