Status: active
Created: 2026-07-21
Updated: 2026-07-21
Parent: .10x/tickets/2026-07-21-label-driven-automatic-release-plan.md
Depends-On: None

# Implement Tag-Derived Package Versioning

## Scope

Implement `.10x/specs/buoy-package-and-cli-identity.md` and the package/frozen-changelog portions of `.10x/specs/buoy-release-validation.md`: pinned hatch-vcs dynamic metadata, generated untracked version module, stable uv lock, development/release version tests, exact override builds, and CHANGELOG frozen through v0.4.0 with canonical GitHub Releases guidance. Remove committed 0.4.1 version/pending preparation without changing dependencies beyond build metadata or product behavior.

## Acceptance criteria

- Dynamic metadata, generated module, ignore rules, imports, and lock satisfy the active spec.
- Ordinary locked install reports valid VCS development version.
- Exact override 0.4.1 produces matching deterministic wheel/sdist/installed/CLI versions.
- Complete Python 3.11/3.13 suites, artifact inventory, clean smoke, tokenizer, links, and independent review pass.
- Historical changelog through v0.4.0 remains; future notes point to canonical Releases.

## Explicit exclusions

Workflow/branch/label/auto-merge changes; main/tag/Release/PyPI/Turbopuffer/product mutation.

## References

- `.10x/specs/buoy-package-and-cli-identity.md`
- `.10x/specs/buoy-release-validation.md`
- `.10x/research/2026-07-21-label-driven-tag-derived-release-automation.md`

## Evidence expectations

Exact diff; lock before/after; development/exact versions; deterministic hashes; full suites; clean install; review; protected integration.

## Progress and notes

- 2026-07-21: Implemented pinned Hatch VCS dynamic metadata, ignored generated `src/buoy_search/_version.py`, generated-version import, dynamic editable lock, frozen-through-v0.4.0 changelog guidance, and dynamic-aware fail-closed legacy release checks on `work/implement-tag-derived-package-versioning`. Updated focused tests for PEP 440 development CLI versions and the complete dynamic metadata/lock/changelog contract.
- 2026-07-21: Local validation passed: clean isolated locked editable install reported matching development version `0.4.1.dev71+g429f499db.d20260722`; Python 3.11 and 3.13 each passed 535 tests plus ranking and C6 validators; two exact 0.4.1 builds were byte-identical; archive inventory, clean wheel install, CLI/help/import, and tokenizer smoke passed. Evidence: `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`. Independent review and hosted CI remain integration-side because this bounded execution did not push or mutate GitHub.

## Blockers

None.
