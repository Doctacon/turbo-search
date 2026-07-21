Status: active
Created: 2026-07-14
Updated: 2026-07-19

# Buoy Release Validation

## Purpose and scope

Define completion evidence for a code-level Buoy 0.4 candidate before external repository or registry mutation.

## Required validation

- Build wheel and source distribution from a clean temporary output directory and inspect package contents and metadata.
- Assert candidate project, module, lock, wheel, and sdist metadata consistently identify version 0.4.0.
- Inspect candidate wheel entry points and a clean isolated installation: `buoy`, `buoy_search`, and bundled data MUST work; the package MUST expose no `turbo-search` entry point, package-owned launcher, or dedicated `legacy_main` hook.
- In a second isolated environment, verify SHA-256 `048dba11df692a7efcd7ab7269fc2eec82f6b53e57573a3de113bbd051750bab` for the immutable released GitHub 0.3.0 wheel, prove both 0.3.0 launchers, normally upgrade that same environment to the candidate wheel, and prove 0.4.0 `buoy` works while installed metadata and the launcher directory contain no package-owned `turbo-search` launcher.
- Run primary CLI parser/help/version checks, including `buoy --help`, `buoy --version`, and `python -m buoy_search --help`, with outputs and exit codes unchanged except for the candidate version.
- In temporary directories, verify new `.buoy` defaults; legacy `.turbo-search` fallback; dual-root refusal; explicit-root override; existing DuckDB ledger loading; and old schema-supported plan preflight.
- Prove no compatibility validation copies, moves, deletes, re-embeds, or remotely mutates existing rows/namespaces. Package-manager removal of its own obsolete launcher during an isolated upgrade is the only deletion in this validation.
- Run fixture autoresearch and repository-search eval validation after module/path dataset changes.
- Run the complete test suite on Python 3.11 and 3.13, diff hygiene, local-link checks, distribution inventory, and independent review.
- Confirm no active source, tests, user docs, skills, package metadata, or open records incorrectly present `turbo-search` as the primary identity. Historical records, retained `.turbo-search` state compatibility, and explicit migration references are allowed.

## Release boundary

Passing this specification authorizes only the code-level 0.4 candidate artifact. It does not create or push a tag, create a GitHub Release, publish to PyPI, delete user-owned launchers, change remote Turbopuffer namespaces, or perform live retrieval/apply/evals. Those are separate external actions.
