# turbo-search

Tiny CLI for turning public websites into turbopuffer-backed hybrid RAG indexes.

The main workflow is intentionally Terraform-like:

1. **plan**: crawl and chunk locally; no credentials or turbopuffer calls.
2. **apply**: preflight the latest plan; still local-only.
3. **apply --approve**: embed and upsert only the approved diff.

It uses Scrapling for crawling/extraction, local `BAAI/bge-small-en-v1.5` embeddings, and turbopuffer hybrid retrieval with ANN + BM25 + RRF.

## Setup

```bash
uv sync
```

Optional but recommended for fewer Hugging Face download warnings:

```bash
uv run hf auth login
```

Do **not** commit API keys. Live apply/retrieval read `TURBOPUFFER_API_KEY` from the environment only.

## Optional global command

Install the CLI so `turbo-search` works from any directory:

```bash
# from the repo root
uv tool install --editable . --force

# or from anywhere
uv tool install --editable /path/to/turbo-search --force
```

Verify:

```bash
turbo-search --help
```

When run outside this repo, generated `artifacts/` and `.turbo-search/` state are created in the current directory.

## Index a new website

```bash
# 1. Create a local plan. No credentials, embeddings, or live writes.
uv run turbo-search plan https://example.com/

# 2. Review what would be applied. Still no credentials or live calls.
uv run turbo-search apply

# 3. If the plan looks good, explicitly upsert to turbopuffer.
export TURBOPUFFER_API_KEY="..."
uv run turbo-search apply --approve
```

The namespace is derived from the site, for example:

```text
https://example.com/ -> site-example-com-v1
```

Plan artifacts are written under `artifacts/site-crawls/...` and local applied state is written under `.turbo-search/state/...`. Both are local/generated paths and are gitignored.

## Shape the crawl

Defaults are meant for normal sites:

```text
crawl_strategy: hybrid
max_pages: 250
max_chunks: 10000
strip_trailing_slash: true
```

Useful filters:

```bash
# Only crawl docs pages
uv run turbo-search plan https://example.com/ --include-path /docs/**

# Exclude noisy paths
uv run turbo-search plan https://example.com/ --exclude-path /blog/**

# Bigger site
uv run turbo-search plan https://example.com/ --max-pages 1000 --max-chunks 50000
```

Other crawl strategies:

```bash
uv run turbo-search plan https://example.com/ --crawl-strategy sitemap
uv run turbo-search plan https://example.com/ --crawl-strategy link
```

## Incremental updates

Run the same sequence later:

```bash
uv run turbo-search plan https://example.com/
uv run turbo-search apply
uv run turbo-search apply --approve
```

`plan` compares the new crawl against local applied state and reports:

```text
upsert=<new or changed chunks>
unchanged=<already indexed chunks>
stale=<previously indexed chunks missing from the new crawl>
```

Approved apply embeds/upserts only new or changed chunks. Stale rows are retained by default. Delete them only with an extra explicit flag:

```bash
uv run turbo-search apply --approve --delete-stale
```

## Search an indexed site

```bash
uv run turbo-search retrieve \
  "How does this feature work?" \
  --live \
  --namespace site-example-com-v1 \
  --top-k 5 \
  --candidates 50
```

Dry-run retrieval is the default and does not contact turbopuffer:

```bash
uv run turbo-search retrieve "How does this feature work?" --namespace site-example-com-v1
```

## Evals

Use a small JSON dataset of questions, expected URLs, and expected topics:

```bash
uv run turbo-search evals \
  --live \
  --dataset path/to/evals.json \
  --namespace site-example-com-v1 \
  --top-k 5 \
  --candidates 50
```

## Legacy Jellyfish corpus

The repo still includes the original Jellyfish docs prototype:

```bash
uv run turbo-search index --corpus-dir jellyfish-site-docs
uv run turbo-search index --corpus-dir jellyfish-site-docs --write
```

Prefer the generic `plan`/`apply` workflow for new websites.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m compileall -q src tests
```
