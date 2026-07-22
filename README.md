# Buoy

[![CI](https://github.com/Doctacon/buoy/actions/workflows/ci.yml/badge.svg)](https://github.com/Doctacon/buoy/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/github/license/Doctacon/buoy)](LICENSE)

<img src="images/buoy.svg" height="120" alt="Buoy navigation marker logo" />

Turn a public website, GitHub repository, local document, or already-shaped DuckDB relation into a reviewed, incremental [turbopuffer](https://turbopuffer.com/) search index.

**Search that stays anchored to the source.**

## Quick start

Requires [uv](https://docs.astral.sh/uv/): `uv sync`

Build and search a website index:

```bash
# 1. Fetch, chunk, and plan locally. No Turbopuffer credentials, embeddings, or calls.
uv run buoy plan https://example.com/
# 2. Verify the plan and preview its diff. Still local-only and prompt-free.
uv run buoy apply --dry-run
# 3. Run the normal interactive flow: preflight, then exact [y/N] confirmation.
export TURBOPUFFER_API_KEY="..."
uv run buoy apply
# 4. Search through authenticated automatic remote routing.
uv run buoy retrieve "How does this feature work?"
```

`plan` may fetch a public source, but it does not read Turbopuffer credentials, load embeddings, or contact Turbopuffer. Plain interactive `apply` displays that local preflight and writes only after exact `y`/`yes`; use `apply --dry-run` for prompt-free preflight or `apply --approve` for non-interactive automation. Retrieval is live by default and requires `TURBOPUFFER_API_KEY`; use `retrieve --dry-run` (or `--plan`) for preview. Explicit `--namespace` retrieval previews remain local-only, while automatic previews perform read-only remote discovery and catalog reads. Compatibility flag `retrieve --live` remains accepted as a no-op.

## Choose a source

The same workflow accepts four source types:

```bash
# Website
uv run buoy plan https://example.com/
# Public GitHub repository
uv run buoy plan https://github.com/owner/repository
# Local document
uv run buoy plan ./research-notes.pdf
# DuckDB table or view
uv run buoy plan ./knowledge.duckdb --relation main.documents --source-id product-docs
```

Source type and namespace are detected automatically except for DuckDB mode, which is activated by `--relation` (or its `--table` alias) and requires an explicit stable `--source-id`. Use `uv run buoy plan --help` to shape a crawl, filter repository paths, map DuckDB columns, or inspect supported options.

For DuckDB, dlt, dbt, SQLMesh, or your own SQL owns extraction and transformation; Buoy reads one already-shaped table or view. One row is one logical document with `document_id` and nonblank `content`, plus optional `title` (or map ordinary identifier columns with `--id-column`, `--content-column`, and `--title-column`). A typical upstream model is:

```sql
CREATE VIEW documents AS SELECT CAST(id AS VARCHAR) AS document_id, markdown AS content, title FROM transformed_documents;
```

The table or view must be self-contained in that DuckDB database. Ordinary views over in-database relations are supported; persisted views that read external files or databases, or that require extension loading, are not. Buoy keeps external access and extension loading disabled. Materialize the final relation as an in-database table upstream before planning when a view has those dependencies.

`plan` and `crawl` open the database read-only, materialize reviewable Markdown, and use the shared chunker; one document can therefore produce multiple chunks with one stable logical document URI. `apply`, including `apply --dry-run`, reads only the integrity-verified saved plan and does not reopen the database. For source ID `product-docs`, identities are `duckdb://product-docs`, `duckdb-product-docs`, and `duckdb-product-docs-v1`; the database path is not part of them or serialized into artifacts. Arbitrary SQL, joins or transformations inside Buoy, non-DuckDB databases, metadata mapping, CDC, and watermarks are v1 non-goals. See [Index sources safely](docs/indexing.md) for the complete contract.

## What happens

1. **Plan** — Scrapling, git, MarkItDown, or a read-only DuckDB relation scan produces local Markdown and deterministic chunks.
2. **Preflight** — `apply --dry-run` verifies artifacts and compares them with the local DuckDB ledger.
3. **Confirmed apply** — plain interactive `apply` prompts after preflight; the local BGE model then embeds only new or changed chunks and turbopuffer upserts them.
4. **Retrieve** — hybrid ANN + BM25 search returns ranked, citable source chunks.

Plans live under `artifacts/`; new applied state lives under `.buoy/`. Both are generated, local, and gitignored. Existing users should read [Migrating from turbo-search](docs/migrating-to-buoy.md).

## Details on demand

- [Index sources safely](docs/indexing.md) — source support, crawl controls, plan artifacts, incremental state, approved apply, and stale deletion.
- [Retrieve and rank results](docs/retrieval.md) — dry runs, live search, citations, and namespace-aware ranking.
- [Manage the remote namespace catalog](docs/catalog.md) — authenticated cards, lifecycle commands, permissions, migration, and recovery.
- [Evaluate search quality](docs/evaluation.md) — smoke datasets, repository metrics, and one-shot autoresearch.
- [Migrate to Buoy 0.2](docs/migrating-to-buoy.md) — command, import, environment, state, and plan compatibility.
- [Contribute](CONTRIBUTING.md) or [prepare a GitHub release](docs/releasing.md).

The CLI is the exhaustive option reference:

```bash
uv run buoy --help
uv run buoy plan --help
```

## Optional global command

```bash
uv tool install --editable . --force
buoy --help
```

Generated artifacts and state are created in the directory where the installed command runs.

## Development

```bash
uv run python -m unittest discover -s tests -p 'test_*.py'
```

Licensed under [Apache-2.0](LICENSE).
