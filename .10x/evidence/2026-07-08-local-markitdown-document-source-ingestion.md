Status: recorded
Created: 2026-07-08
Updated: 2026-07-08
Relates-To: .10x/tickets/done/2026-07-08-local-markitdown-document-source-ingestion.md, .10x/specs/local-markitdown-document-source-ingestion.md

# Local MarkItDown Document Source Ingestion Evidence

## What was observed

Implementation added MarkItDown-backed local document ingestion for the ratified extension allowlist while preserving existing PDF identity and plan/apply guardrails.

Key observed behaviors:

- Supported non-PDF local files route through the local document path and use `file-<ext>-<filename-slug>-<sha16>-v1` namespaces.
- PDFs still use `pdf-<filename-slug>-<sha16>-v1` and `pdf://...` synthetic URLs.
- Local document summaries and artifacts include filename, extension, SHA-256 hash, source ID, and source kind.
- Generated artifacts avoid the absolute source filepath.
- Plan/crawl remain local-only with no turbopuffer API calls.

## Procedure and results

### Compile and full test suite

Command:

```bash
uv run python -m compileall -q src tests && uv run --with pytest python -m pytest
```

Result:

```text
collected 179 items
...
179 passed in 3.61s
```

### Targeted local document/source tests

Command:

```bash
uv run --with pytest python -m pytest tests/test_crawler.py tests/test_plan_artifacts.py tests/test_cli.py
```

Result:

```text
collected 83 items
83 passed in 0.97s
```

### Local-only real MarkItDown smoke plan

Fixture:

```text
/tmp/turbo-search-local-file-smoke/Smoke Data.csv
```

Command:

```bash
uv run turbo-search plan \
  /tmp/turbo-search-local-file-smoke/Smoke\ Data.csv \
  --out-dir /tmp/turbo-search-local-file-smoke/plan \
  --state-root /tmp/turbo-search-local-file-smoke/state \
  --json \
  --no-progress
```

Observed summary subset:

```json
{
  "api_calls_occurred": false,
  "chunks_generated": 1,
  "credentials_required": false,
  "documents_converted": 1,
  "namespace": "file-csv-smoke-data-31d9ad0744b7200d-v1",
  "source_kind": "local_file",
  "turbopuffer_api_calls": false
}
```

Artifact privacy check:

```bash
rg -F "/tmp/turbo-search-local-file-smoke/Smoke Data.csv" /tmp/turbo-search-local-file-smoke/plan
```

Result:

```text
absolute source path absent from plan artifacts
```

### Lock and diff hygiene

Commands:

```bash
uv lock --check
git diff --check
git diff --stat
```

Results:

```text
Resolved 127 packages in 8ms
```

`git diff --check` produced no whitespace errors.

Diff stat at evidence time:

```text
 README.md                           |  23 ++-
 docs/generic-site-rag-plan-apply.md |  18 +-
 pyproject.toml                      |   2 +-
 src/turbo_search/cli.py             |  43 +++--
 src/turbo_search/crawler.py         | 342 +++++++++++++++++++++++++++++-------
 src/turbo_search/plan_artifacts.py  |   8 +
 src/turbo_search/retriever.py       |   2 +-
 tests/test_cli.py                   | 134 ++++++++++++++
 tests/test_crawler.py               |  91 ++++++++++
 tests/test_plan_artifacts.py        |  58 ++++++
 uv.lock                             | 187 +++++++++++++++++++-
 11 files changed, 810 insertions(+), 98 deletions(-)
```

## What this supports

- Acceptance criteria for local DOC/data source routing and `file-<ext>-...` identity are covered by unit tests and the real CSV smoke plan.
- PDF backward compatibility is covered by existing and updated PDF tests.
- Artifact privacy is covered by unit tests and the smoke `rg` check.
- Local-only plan/crawl guardrails are supported by summary fields and existing plan/apply tests.
- Dependency lock coherence is supported by `uv lock --check`.

## Limits

- The smoke test used CSV because it is a deterministic local text/data format. DOCX/PPTX/XLS/XLSX/EPUB converters are covered by MarkItDown dependency extras and routing tests, but not by real office-file smoke fixtures in this evidence record.
- No live turbopuffer apply, delete, replacement, or retrieval mutation was run.
