Status: blocked
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
- 2026-07-21: Repaired both independent review findings against `3c882d4`: added executable clean-clone VCS development-install and exact-override artifact/install/module/CLI regression tests, and made the legacy checker require explicit exact dynamic-version authority plus generated-module agreement. Python 3.11 and 3.13 each passed 538 tests plus ranking/C6 validators; lock check passed. The first attempted parallel cross-version run was invalid because both commands replaced the same `.venv`; the required runs were repeated sequentially and passed. Evidence updated in `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`.
- 2026-07-21: Independent final rereview passed exact PR #99 head `75dd2023ac542a93430accf339b0eb04f032eed1` with no findings; both prior concerns are resolved. Review: `.10x/reviews/2026-07-21-tag-derived-package-versioning-final-review.md`.
- 2026-07-21: Hosted CI run `29886520116` passed at the same exact head: Python 3.11 in 2m9s, Python 3.13 in 1m52s, and Build distributions in 13s. Evidence: `.10x/evidence/2026-07-21-tag-derived-package-versioning-hosted-ci.md`.

## Acceptance mapping

- Dynamic metadata/generated module/ignore/import/lock: implementation diff plus configuration and lock assertions in `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`.
- Ordinary locked VCS development version: clean disposable install observation and durable regression in `tests/test_dynamic_version.py`, recorded in `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`.
- Exact deterministic 0.4.1 wheel/sdist/install/module/CLI: byte-identical local builds, archive/install smoke, and durable exact-override regression recorded in `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`.
- Complete Python 3.11/3.13 suites, validators, artifact inventory, clean smoke, tokenizer, links, hosted CI, and independent review: `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`, `.10x/evidence/2026-07-21-tag-derived-package-versioning-hosted-ci.md`, and `.10x/reviews/2026-07-21-tag-derived-package-versioning-final-review.md`.
- Frozen changelog through v0.4.0 and canonical future Releases guidance: `CHANGELOG.md` diff and contract assertions recorded in `.10x/evidence/2026-07-21-tag-derived-package-versioning.md`.

All behavioral acceptance criteria are supported. The ticket's evidence expectation also names protected integration; PR #99 is still open, so closure is not yet supported.

## Retrospective

The stale generated-version concern is now prevented by the fail-closed checker and executable regressions, which are the durable reusable safeguards. The invalid parallel shared-`.venv` attempt is recorded so future validation runs use isolated environments or sequential interpreter syncs. No additional knowledge or skill record is warranted: the active dynamic-version specification and focused tests already encode the reusable contract and procedure. Closure retrospective remains pending only for integration evidence.

## Blockers

Protected squash integration of PR #99 into `develop` and exact integrated-state evidence. No source repair or additional review is blocked.
