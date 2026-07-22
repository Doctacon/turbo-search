Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Relates-To: .10x/tickets/2026-07-21-implement-tag-derived-package-versioning.md, .10x/specs/buoy-package-and-cli-identity.md, .10x/specs/buoy-release-validation.md

# Tag-Derived Package Versioning Candidate

## What was observed

On branch `work/implement-tag-derived-package-versioning` based on `develop` commit `429f499db1ce182b720833f9ee0ee659055bf1f9`, the candidate:

- replaces committed project/module version `0.4.1` with Hatch VCS dynamic metadata;
- pins `hatchling==1.31.0` and `hatch-vcs==0.5.0`;
- generates ignored `src/buoy_search/_version.py` and imports `buoy_search.__version__` from it;
- removes only the root `version = "0.4.1"` line from `uv.lock`, preserving the dynamic editable root;
- freezes `CHANGELOG.md` through v0.4.0 and points future notes to canonical `https://github.com/Doctacon/buoy/releases`;
- keeps the legacy side-effect-free release checker fail-closed while reading generated dynamic versions.

A clean disposable Git worktree with an isolated uv cache performed `uv sync --locked --python 3.11`, generated the ignored version module, and reported matching installed/module development version `0.4.1.dev71+g429f499db.d20260722`.

Python 3.11 and 3.13 each passed all 535 tests, the ranking validator, and the C6 validator. The ranking validator reported dataset bundle SHA-256 `5a79f58aaca87a2d4f7cbec68fdcfbbcbf041131821587f8aba74a86daca99d9`; C6 reported forecast `d5199276c19ae89779287eaa90824ce1e1cc684a3f060899f02f65d976016243` and the expected blocked tokenizer checkpoint `c3a1560e611114760909c110a118a3ce1a60f0527de08c769a85a20b263f4e0f`.

Two exact-version builds using `SETUPTOOLS_SCM_PRETEND_VERSION=0.4.1`, `SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD)`, `PYTHONHASHSEED=0`, `TZ=UTC`, and `LC_ALL=C` were byte-identical:

- `buoy_search-0.4.1-py3-none-any.whl`: `b9d2ba6486de1cd89c1ef4445c5ebefff52d9837c52b1cb7b17ef72c9dda85ec`
- `buoy_search-0.4.1.tar.gz`: `7e1d2e07cb05067c7514b59e31226f7ab3244e839b2f9c01820689f6a4950cc9`

Direct archive inspection found exact 0.4.1 filenames and metadata, generated `_version.py` in wheel and sdist, sole `buoy = buoy_search.cli:main` entry point, all 23 source data/tokenizer files, and no `.10x/`, `turbo_search`, `turbo-search`, or `legacy_main` inventory. A clean wheel-only virtual environment reported module, installed metadata, and `buoy --version` as 0.4.1; `buoy --help`, `python -m buoy_search --help`, representative imports, and exact tokenizer smoke (`9` tokens) passed.

## Procedure

Commands were run without GitHub, tag, Release, PyPI, Turbopuffer, provider, retrieval, apply, or eval side effects:

```text
uv lock
uv lock --check
uv sync --locked --python 3.13 --reinstall-package buoy-search
uv run --python 3.13 python scripts/validate_ranking_contract.py
uv run --python 3.13 python scripts/c6_syntax_forecast.py validate
uv run --python 3.13 python -m unittest discover -s tests -p 'test_*.py' -q
uv sync --locked --python 3.11 --reinstall-package buoy-search
uv run --python 3.11 python scripts/validate_ranking_contract.py
uv run --python 3.11 python scripts/c6_syntax_forecast.py validate
uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py' -q
SETUPTOOLS_SCM_PRETEND_VERSION=0.4.1 SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD) PYTHONHASHSEED=0 TZ=UTC LC_ALL=C uv build --out-dir /tmp/buoy-version-build-a
SETUPTOOLS_SCM_PRETEND_VERSION=0.4.1 SOURCE_DATE_EPOCH=$(git show -s --format=%ct HEAD) PYTHONHASHSEED=0 TZ=UTC LC_ALL=C uv build --out-dir /tmp/buoy-version-build-b
sha256sum /tmp/buoy-version-build-a/* /tmp/buoy-version-build-b/*
cmp <matching wheel pair>; cmp <matching sdist pair>
<direct zip/tar metadata, generated module, entry point, data, and forbidden-inventory assertions>
python3 -m venv /tmp/buoy-version-smoke
/tmp/buoy-version-smoke/bin/python -m pip install /tmp/buoy-version-build-a/*.whl
<installed metadata/module/CLI/help/import/tokenizer assertions>
```

The clean editable check used a detached disposable worktree at the same source commit, copied only the candidate diff into it, set an isolated temporary `UV_CACHE_DIR`, ran locked sync, asserted development version agreement, and removed that worktree.

## What this supports

This supports the ticket's dynamic metadata, generated module, lock, development version, exact override, deterministic artifact, inventory, clean-install, CLI, tokenizer, historical changelog, and local Python 3.11/3.13 validation criteria.

## Review-finding repair observation

The repair candidate adds three executable regressions in `tests/test_dynamic_version.py`:

- a disposable local Git clone is installed editable without an override and must report a PEP 440 development version containing the checked-out commit, with installed metadata, generated module, and `buoy --version` agreement;
- an exact `SETUPTOOLS_SCM_PRETEND_VERSION=0.4.1` build must produce the exact wheel/sdist filenames and metadata, exact generated modules in both archives, and an installed wheel whose metadata, module, and CLI all report 0.4.1;
- a temporary dynamic project proves the legacy checker rejects a missing override and a stale generated version that disagrees with the override, while accepting exact authority/module agreement.

The legacy checker now requires `SETUPTOOLS_SCM_PRETEND_VERSION` for dynamic projects and validates the generated module against it before either tag or asset validation. It no longer derives both sides of its comparison from one ignored generated file.

`uv lock --check` passed. Sequential Python 3.11 and Python 3.13 runs each passed all 538 tests, then the ranking and C6 validators with the same hashes recorded above. An initial parallel cross-version attempt was invalid because both commands replaced the same shared `.venv`; Python 3.11 nevertheless completed successfully, and Python 3.13 was then explicitly synced and rerun sequentially to a clean pass. No product, workflow, provider, GitHub, tag, Release, or publication behavior was mutated.

## Limits

- This local evidence does not itself prove hosted CI or independent review; those are recorded separately in `.10x/evidence/2026-07-21-tag-derived-package-versioning-hosted-ci.md` and `.10x/reviews/2026-07-21-tag-derived-package-versioning-final-review.md`.
- Hashes identify the pre-commit candidate built with the then-current HEAD timestamp. Any later source or commit-timestamp change requires a fresh deterministic pair for release authority.
- Existing readiness/main-push workflows and `scripts/release_automation.py` still encode the prior static release process; their replacement belongs to the plan's later executable children and was intentionally excluded here.
- The warnings emitted by two plan-cleanup negative tests and the lxml deprecation warning were pre-existing, non-failing test output.
