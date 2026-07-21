Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Relates-To: .10x/tickets/cancelled/2026-07-21-release-buoy-v0-4-1-through-main-automation.md

# Buoy v0.4.1 Preparation

## What was observed

Preparation began from exact `develop` commit `99f7685469571cec6f3a23f95801dcb649924059` in isolated branch/worktree `work/prepare-v0-4-1`. Project, module, and lock authorities agree on stable `0.4.1`. `CHANGELOG.md` has an empty Unreleased section, exactly one current `## [0.4.1] - pending` section, the ratified concise Changed entry, dated older releases, and comparison links from v0.4.0 to v0.4.1 and from v0.4.1 to HEAD.

Both complete locked supported-Python suites passed 534 tests. Deterministic double builds were byte-for-byte identical. Repository artifact inspection and a normal clean-wheel install proved exact metadata, inventory, command, help, entry-point, and bundled-tokenizer behavior.

## Procedure and results

### Release authorities and policy

- `uv lock` changed only the editable `buoy-search` lock entry from 0.4.0 to 0.4.1.
- A direct invocation of `validate_versions`, `validate_changelog`, and `validate_release_policy` passed for 0.4.1.
- `uv lock --check` passed.
- `scripts/release_automation.py validate` returned `0.4.1` on both Python versions.
- `git diff --check` passed.

### Locked source validation

Separate disposable environments were used:

- `UV_PROJECT_ENVIRONMENT=/tmp/buoy-v041-py311 uv sync --locked --python 3.11` used CPython 3.11.5. Release validation, frozen ranking validation, blocked C6 validation, and `python -m unittest discover -s tests -p 'test_*.py' -q` passed 534 tests in 57.646 seconds.
- `UV_PROJECT_ENVIRONMENT=/tmp/buoy-v041-py313 uv sync --locked --python 3.13` used CPython 3.13.0. The same validators and complete suite passed 534 tests in 67.921 seconds.
- Ranking validation retained 90 composite identities, 13 datasets/folds, 369 judgments, and dataset bundle `5a79f58aaca87a2d4f7cbec68fdcfbbcbf041131821587f8aba74a86daca99d9`.
- C6 validation retained forecast `d5199276c19ae89779287eaa90824ce1e1cc684a3f060899f02f65d976016243` with tokenizer readiness false and exact checkpoint `c3a1560e611114760909c110a118a3ce1a60f0527de08c769a85a20b263f4e0f`.

The first Python 3.11 full-suite attempt exposed two stale static assertions that still required project 0.4.0 and direct adjacency between Unreleased and the released 0.4.0 section. Those assertions were narrowly updated to require project 0.4.1 and the ratified pending section, Changed meaning, comparison links, and preserved dated 0.4.0 history. Both complete suites then passed. The suites emitted the two existing mocked temporary plan-artifact cleanup warnings and the existing lxml `strip_cdata` deprecation warning.

### Deterministic build and artifact inspection

With `SOURCE_DATE_EPOCH=1784668331` from the starting commit and `PYTHONHASHSEED=0`, `TZ=UTC`, and `LC_ALL=C`, `uv build` ran twice into separate disposable directories. `cmp`, SHA-256 lists, and generated artifact manifests matched exactly:

- `buoy_search-0.4.1-py3-none-any.whl`: `218f6e2093a3024805f35baeb849834f42e40b62a0a8a9809c858083b2af9a3d`
- `buoy_search-0.4.1.tar.gz`: `ac89c9a01a4bd02f9b66e02fa4c4fa8972bc08175bee5209d72a6c2f8d5ac8e6`

`scripts/release_automation.py artifacts`, `scripts/release_checks.py tag --tag v0.4.1`, and `scripts/release_checks.py assets` passed. The repository artifact validator proved exact names and metadata, exact `buoy = buoy_search.cli:main` entry point, required bundled tokenizer data, and absence of `.10x/**`, `turbo-search`, `turbo_search`, and `legacy_main` inventory.

### Clean wheel smoke

A fresh CPython 3.13 virtual environment normally installed only the built wheel as the requested direct artifact while resolving its declared dependencies. Assertions proved:

- `buoy --version` returned exactly `buoy 0.4.1`;
- `buoy --help` and `python -m buoy_search --help` both exited successfully;
- installed module and distribution versions were exactly 0.4.1;
- the distribution exposed exactly `buoy = buoy_search.cli:main`;
- loading the exact bundled tokenizer succeeded without model construction or inference;
- `exact_token_count(..., "Buoy release tokenizer smoke.")` returned exactly 9.

## What this supports

This supports the preparation-phase version, changelog, supported-Python, deterministic-build, artifact-inspection, and clean-wheel acceptance criteria for `.10x/tickets/cancelled/2026-07-21-release-buoy-v0-4-1-through-main-automation.md`.

## Limits and side effects

This evidence does not prove protected-branch integration, a future develop-to-main readiness run, main promotion, tag/Release publication, asset provenance, or final release state. Hosted exact-head CI is observed separately after the preparation pull request is opened. Disposable environments and artifacts were under `/tmp`; dependency resolution performed registry reads only. No main pull request, merge, tag, GitHub Release, package publication, workflow dispatch, release environment, branch protection, Turbopuffer/provider call, namespace operation, live retrieval/apply/eval, configuration, secret, or user-state mutation occurred.
