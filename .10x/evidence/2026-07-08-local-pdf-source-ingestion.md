Status: recorded
Created: 2026-07-08
Updated: 2026-07-08
Relates-To: .10x/tickets/done/2026-07-08-local-pdf-source-ingestion.md, .10x/specs/local-pdf-source-ingestion.md

# Local PDF Source Ingestion Evidence

## What was observed

The implementation supports local text PDF planning through MarkItDown, preserves filename/hash metadata, avoids persisting the absolute PDF source filepath in plan artifacts, and keeps plan/crawl local-only with respect to turbopuffer.

## Procedure

### Compile check

```bash
uv run python -m compileall -q src tests
```

Result: passed.

### Targeted tests

```bash
uv run --with pytest python -m pytest tests/test_crawler.py tests/test_cli.py tests/test_plan_artifacts.py tests/test_retriever.py
```

Result:

```text
collected 94 items

...

============================== 94 passed in 1.66s ==============================
```

### Full test suite

```bash
uv run --with pytest python -m pytest
```

Result:

```text
collected 170 items

...

============================= 170 passed in 4.10s ==============================
```

### Lockfile consistency

```bash
uv lock --check
```

Result: resolved successfully in 8ms, exit code 0.

### Whitespace check

```bash
git diff --check
```

Result: no output, exit code 0.

### Local-only MarkItDown PDF smoke plan

Generated a minimal text PDF at `/tmp/turbo-search-pdf-smoke/Smoke Document.pdf`, then ran:

```bash
uv run turbo-search plan \
  /tmp/turbo-search-pdf-smoke/Smoke\ Document.pdf \
  --out-dir /tmp/turbo-search-pdf-smoke/plan \
  --state-root /tmp/turbo-search-pdf-smoke/state \
  --json \
  --no-progress
```

Observed summary excerpt:

```json
{
  "chunks_generated": 1,
  "namespace_candidate": "pdf-smoke-document-774b310573ae1751-v1",
  "pages_scraped": 1,
  "plan_path": "/tmp/turbo-search-pdf-smoke/plan/plan.json",
  "result_source_kind": "pdf",
  "turbopuffer_api_calls": false
}
```

Checked concatenated `plan.json`, `manifest.json`, `chunks.jsonl`, and `summary.json` for the absolute source filepath.

Result:

```text
source_path_present= False
```

### Local-only apply preflight against PDF plan

Ran preflight on the generated PDF plan:

```bash
uv run turbo-search apply \
  --plan /tmp/turbo-search-pdf-smoke/plan/plan.json \
  --state-root /tmp/turbo-search-pdf-smoke/state \
  --json
```

Observed summary excerpt:

```json
{
  "api_calls_occurred": false,
  "approved": false,
  "credentials_required": false,
  "namespace": "pdf-smoke-document-774b310573ae1751-v1",
  "rows_to_upsert": 1
}
```

No `apply --approve`, live retrieval, namespace creation, row write, or stale deletion command was run.

## What this supports

- `turbo-search plan <local.pdf> --json` works for a text PDF and reports `source_kind: pdf`, one generated page, generated chunks, deterministic `pdf-<filename-stem>-<sha16>-v1` namespace, and no turbopuffer calls.
- PDF plan artifacts preserve filename/hash/source metadata without storing the absolute source PDF filepath.
- Apply preflight accepts PDF plans locally and remains no-credential/no-API-call.
- `crawl --base-url <local.pdf>` and `plan <local.pdf>` are covered by unit tests with MarkItDown mocked at the converter boundary.
- Empty MarkItDown extraction fails before writing a successful summary.
- Existing website/GitHub source-routing, plan/apply, retrieval, and artifact tests continue to pass.

## Limits

- The smoke PDF is a simple generated text PDF; it does not prove support for every PDF producer/layout.
- v1 intentionally does not support OCR, page-number citations, directories, multi-PDF batches, or remote PDF URLs.
- No live turbopuffer write/delete/replacement path was exercised.
