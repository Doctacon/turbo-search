# turbo-search

Local Python prototype for testing turbopuffer-backed RAG over exported Jellyfish site docs.

## Scope

Implemented so far:

- Safe Markdown indexing CLI, dry-run by default.
- Safe generic website crawl and plan CLIs, dry-run/local-only by default, using Scrapling for fetch/extraction.
- Recursive `*.md` discovery under `jellyfish-site-docs/`.
- Frontmatter parsing for `url` and `title`.
- Conservative site-chrome normalization.
- Heading-aware Markdown chunking with ~300-token target chunks and sentence overlap.
- Deterministic chunk IDs and citation/debug metadata.
- Explicit `--write` mode that embeds locally with `BAAI/bge-small-en-v1.5` and upserts batches to turbopuffer.
- Hybrid retrieval CLI/library with query embedding, turbopuffer multi-query ANN + boosted BM25, server RRF, and client-side RRF fallback.

## Setup

Install dependencies with `uv`:

```bash
uv sync
```

Non-secret defaults used by the prototype:

```bash
export TURBOPUFFER_REGION=gcp-us-central1
export TURBOPUFFER_NAMESPACE=jellyfish-site-docs-v1
```

Do not store `TURBOPUFFER_API_KEY` in this repository. Write mode and live retrieval read it from the environment at runtime only.

## Safe commands

Show CLI help without credentials:

```bash
PYTHONPATH=src uv run --no-sync python -m turbo_search --help
```

Dry-run the full local corpus. This parses and chunks files only; it does not load embeddings, read secrets, or contact turbopuffer:

```bash
PYTHONPATH=src uv run --no-sync python -m turbo_search index --corpus-dir jellyfish-site-docs
```

Optional dry-run limits:

```bash
PYTHONPATH=src uv run --no-sync python -m turbo_search index \
  --corpus-dir jellyfish-site-docs \
  --max-files 25 \
  --limit-chunks 100
```

Dry-run crawl a public website with Scrapling. This writes a local generated Markdown corpus and chunks it, but does not read credentials, embed text, create namespaces, or contact turbopuffer:

```bash
uv run turbo-search crawl \
  --base-url "https://scrapling.readthedocs.io/en/latest/" \
  --max-pages 10 \
  --max-chunks 100 \
  --css-selector ".md-content__inner" \
  --json
```

The crawl command prefers robots/sitemap discovery first and falls back to capped same-domain link crawling if no sitemap pages are scraped. It reports a namespace candidate such as `site-scrapling-readthedocs-io-v1`; it never creates that namespace.

Create a Terraform-like local website RAG plan. This reuses the same Scrapling crawl/extract/chunk path, loads local applied state from `.turbo-search/` when present, writes review artifacts, and still does not read credentials, embed text, create namespaces, or contact turbopuffer:

```bash
uv run turbo-search plan \
  --base-url "https://scrapling.readthedocs.io/en/latest/" \
  --out-dir artifacts/site-crawls/scrapling-readthedocs-io-plan \
  --max-pages 1000 \
  --max-chunks 10000 \
  --css-selector ".md-content__inner" \
  --json
```

Plan artifacts include:

```text
plan.json
summary.json
manifest.json
chunks.jsonl
pages/*.md
```

Use `--namespace <stable-namespace>` to diff against a specific local state namespace. `plan` is preview-only.

Verify a saved plan before live work. Apply preflight re-reads `plan.json`, `manifest.json`, and `chunks.jsonl`, verifies the artifact hash and namespace, recomputes the local diff from state, and does not read credentials, load embeddings, or call turbopuffer:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json
```

Approved apply is explicitly live. Only run it after reviewing the plan and putting `TURBOPUFFER_API_KEY` in the environment. It embeds/upserts only chunks selected by the recomputed incremental diff. By default, stale rows are not deleted; they are retained in local state as `retained_stale` for a future cleanup pass.

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --approve \
  --json
```

Delete stale rows only with an additional explicit flag. Preflight with `--delete-stale` reports the exact stale row IDs that would be deleted but still makes no live calls. Live stale deletion requires both `--approve` and `--delete-stale`:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --approve \
  --delete-stale \
  --json
```

See [`docs/generic-site-rag-plan-apply.md`](docs/generic-site-rag-plan-apply.md) for the full generic site plan/apply safety model.

Plan retrieval without credentials. This is the default for `retrieve`; it does not load the embedding model or contact turbopuffer:

```bash
PYTHONPATH=src uv run --no-sync python -m turbo_search retrieve \
  "What are DORA metrics?" \
  --dry-run \
  --top-k 5 \
  --candidates 100 \
  --json
```

Generic site namespaces can be targeted without code changes by passing non-secret runtime overrides, or by setting the corresponding environment variables:

```bash
uv run turbo-search retrieve \
  "How does Scrapling LinkExtractor filter links?" \
  --dry-run \
  --namespace site-scrapling-readthedocs-io-v1 \
  --region gcp-us-central1 \
  --embedding-model BAAI/bge-small-en-v1.5 \
  --json
```

List the built-in retrieval smoke eval questions and expected URL/topic hints without credentials:

```bash
PYTHONPATH=src uv run --no-sync python -m turbo_search evals \
  --dry-run \
  --top-k 5 \
  --candidates 100 \
  --json
```

List the Scrapling docs eval hints for a future approved generic-site namespace, still without credentials or turbopuffer calls:

```bash
uv run turbo-search evals \
  --dry-run \
  --dataset src/turbo_search/data/scrapling_retrieval_smoke_evals.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --top-k 5 \
  --candidates 100 \
  --json
```

## Explicit write mode

Only run this after credentials are approved and `TURBOPUFFER_API_KEY` is already present in the environment:

```bash
uv run turbo-search index --corpus-dir jellyfish-site-docs --write --batch-size 64
```

Write mode uses local open-source BGE embeddings by default:

- Model: `BAAI/bge-small-en-v1.5`
- Override: `TURBO_SEARCH_EMBEDDING_MODEL`

Rows contain:

- `id`
- `vector`
- `content`
- `title`
- `url`
- `path`
- `section_path`
- `chunk_index`
- `doc_kind`
- `tags`
- `source_hash`

The turbopuffer schema enables ANN on `vector` and BM25 full-text search on `content`, `title`, and `section_path`.

## Agent answering workflow

Before answering user questions from Jellyfish docs, retrieve context and follow the citation/insufficient-context guardrails in [`docs/agent-answering-workflow.md`](docs/agent-answering-workflow.md).

## Explicit live retrieval and smoke evals

Only run these after indexing has completed and credentials are approved in the shell environment:

```bash
uv run turbo-search retrieve "What does Jellyfish say about developer productivity?" --live --top-k 5 --candidates 100 --json
```

Run the lightweight smoke/eval harness against the indexed namespace:

```bash
uv run turbo-search evals --live --top-k 5 --candidates 30 --json
```

For a generic applied site namespace, pass the namespace and dataset explicitly after live retrieval has been approved and `TURBOPUFFER_API_KEY` is already in the environment:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/scrapling_retrieval_smoke_evals.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --top-k 5 \
  --candidates 30 \
  --json
```

The built-in Jellyfish eval dataset lives at `src/turbo_search/data/retrieval_smoke_evals.json` and covers five representative Jellyfish questions with expected URL/topic hints for developer productivity, DORA metrics, DevFinOps, Claude Code/Cursor integrations, and AI coding tool adoption. The Scrapling example dataset lives at `src/turbo_search/data/scrapling_retrieval_smoke_evals.json`.

Live retrieval:

- Reads `TURBOPUFFER_API_KEY` from the environment only when `--live` is passed.
- Embeds the query with the same local `BAAI/bge-small-en-v1.5` model used by the indexer.
- Sends one turbopuffer `multi_query` containing an ANN vector subquery and a boosted BM25 subquery over `title`, `section_path`, and `content`.
- Prefers server-side `rerank_by=("RRF",)` and falls back to local reciprocal-rank fusion when needed.
- Returns citation fields (`title`, `url`, `section_path`, `content`, `path`) and score info. Vectors are not requested or returned by default.
- Supports `--doc-kind` filters such as `blog`, `library`, `platform`, or `integrations`.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m compileall src tests
```
