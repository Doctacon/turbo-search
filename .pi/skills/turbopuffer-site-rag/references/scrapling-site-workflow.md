# Scrapling site workflow for turbopuffer RAG

## Goal

Turn an arbitrary public website into a cost-conscious searchable RAG namespace:

```text
base URL
  -> namespace candidate
  -> Scrapling crawl
  -> clean Markdown/text + metadata
  -> chunks
  -> local embeddings
  -> turbopuffer namespace
  -> hybrid retrieval with citations
```

## Default crawl policy

- Prefer sitemap discovery first.
- Fall back to same-domain link crawling if sitemaps are absent or incomplete.
- Obey robots.txt by default.
- Restrict to the base URL host/domain unless the user approves otherwise.
- Use conservative caps until the site shape is known:
  - `--max-pages 10` or `25` for smoke tests
  - `--max-chunks 100` or `200` for smoke tests
  - low concurrency, e.g. `2`
  - crawl delay, e.g. `0.25` to `1.0` seconds
- Use static HTTP fetching first. Escalate to browser rendering only when pages are empty or clearly JavaScript-dependent.

## Preview and plan CLI

Use `crawl` for a simple local crawl/chunk preview:

```bash
uv run turbo-search crawl \
  --base-url "https://scrapling.readthedocs.io/en/latest/" \
  --max-pages 10 \
  --max-chunks 100 \
  --css-selector ".md-content__inner" \
  --json
```

Use `plan` for Terraform-like review/apply artifacts and incremental diffing against local state:

```bash
uv run turbo-search plan \
  --base-url "https://scrapling.readthedocs.io/en/latest/" \
  --out-dir artifacts/site-crawls/scrapling-readthedocs-io-plan \
  --max-pages 1000 \
  --max-chunks 10000 \
  --css-selector ".md-content__inner" \
  --json
```

Expected safety fields for crawl/plan:

```json
{
  "dry_run": true,
  "turbopuffer_api_calls": false,
  "credentials_required": false
}
```

The CLI writes local generated Markdown pages under the requested `artifacts/...` output directory and chunks them with the existing `turbo_search.indexer` Markdown pipeline. `artifacts/` is gitignored. Plan also writes `plan.json`, `summary.json`, `manifest.json`, and `chunks.jsonl`, and reads local applied state from `.turbo-search/` when present. `.turbo-search/` is gitignored local state. Use `--css-selector` when a docs site has clear main-content wrappers; this reduces nav/sponsor/sidebar noise before chunking.

## Metadata to preserve per page

At minimum:

- `url`
- `title`
- `status`
- `content_type`
- `source_hash`
- `crawl_timestamp`
- `fetcher` / crawl mode

Future production indexing should also consider:

- canonical URL
- final redirected URL
- HTTP headers relevant to cache validation, e.g. `etag` and `last-modified`
- sitemap source URL if discovered from sitemap
- crawl depth
- language

## Namespace naming

Use a deterministic, URL-derived candidate with a version suffix:

```text
site-<host-slug>-v1
```

Examples:

- `https://jellyfish.co/` -> `site-jellyfish-co-v1`
- `https://scrapling.readthedocs.io/en/latest/` -> `site-scrapling-readthedocs-io-v1`

Ask before creating/writing a namespace. Never delete or overwrite an existing namespace unless the user explicitly approves deletion/replacement.

## Apply sequence

Apply has a preflight mode and an explicit live mode.

Preflight, no credentials or live calls:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json
```

Approved live upsert, only after explicit user approval and after `TURBOPUFFER_API_KEY` is already in the environment:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --approve \
  --json
```

Stale row deletion is off by default. Preflight with `--delete-stale` reports exact stale row IDs without live calls. Live stale deletion requires both `--approve` and `--delete-stale`:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --approve \
  --delete-stale \
  --json
```

Only after explicit user approval:

1. Run `plan` and inspect page/chunk counts, samples, and diff.
2. Run apply preflight and confirm namespace, rows to upsert, embeddings to generate, stale rows, and local state path.
3. Retrieve `TURBOPUFFER_API_KEY` into shell memory only.
4. Set `TURBOPUFFER_REGION` and `TURBOPUFFER_NAMESPACE` in shell only.
5. Run approved apply; it embeds/upserts only new or changed chunks.
6. Delete stale rows only with `--delete-stale`; this deletes row IDs only, not namespaces.
7. Record evidence without secret values or private credential identifiers.

## Retrieval validation

After an explicitly approved apply, generic retrieval/eval commands can target the site namespace without code changes:

```bash
uv run turbo-search retrieve \
  "How does Scrapling LinkExtractor filter links?" \
  --dry-run \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json

uv run turbo-search evals \
  --dry-run \
  --dataset src/turbo_search/data/scrapling_retrieval_smoke_evals.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json
```

Dry-run/list mode is credential-free and turbopuffer-free. Live retrieval/evals require `--live` and `TURBOPUFFER_API_KEY` in the environment; do not run them without explicit user approval.

## Known gaps before productionizing

The current implementation has a local-first plan/apply workflow but still needs:

- live SDK smoke validation against a disposable namespace before production reliance
- remote/shared state backend for multi-machine workflows
- resumable crawl manifests
- HTTP cache metadata such as `etag`/`last-modified` for crawl efficiency
- local content store for cost-optimized turbopuffer rows
- namespace lifecycle commands with explicit safety prompts
