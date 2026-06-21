# Generic site RAG plan/apply workflow

This workflow is the Terraform-like path for turning a public website crawl into a reviewed, incremental turbopuffer index.

## Safety model

There are three distinct modes:

1. **Plan**: local-only preview. Crawls, extracts, chunks, compares with local applied state, and writes review artifacts. It does not read credentials, load embeddings, create namespaces, or call turbopuffer.
2. **Apply preflight**: local-only verification of a saved plan. It recomputes artifact hashes and local diff state. It does not read credentials, load embeddings, or call turbopuffer.
3. **Approved apply**: explicit live mutation. It requires `--approve` and `TURBOPUFFER_API_KEY` in the environment. It embeds/upserts only new or changed chunks from the recomputed diff.

Stale deletes have an additional guardrail: stale rows are retained by default. Live stale deletion requires both `--approve` and `--delete-stale`.

## Plan

```bash
uv run turbo-search plan \
  --base-url "https://scrapling.readthedocs.io/en/latest/" \
  --out-dir artifacts/site-crawls/scrapling-readthedocs-io-plan \
  --max-pages 1000 \
  --max-chunks 10000 \
  --css-selector ".md-content__inner" \
  --json
```

Plan artifacts:

```text
plan.json
summary.json
manifest.json
chunks.jsonl
pages/*.md
```

The plan compares generated chunks to local applied state under `.turbo-search/state/...` unless `--state-root` is supplied. `.turbo-search/` is local state and is gitignored.

## Apply preflight

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json
```

Preflight verifies:

- plan schema and namespace;
- `manifest.json` and `chunks.jsonl` match;
- embedding-text hashes are still valid;
- artifact hash matches reviewed content/options;
- local applied state is compatible.

Preflight makes no live calls and does not read `TURBOPUFFER_API_KEY`.

## Approved apply

Only after reviewing plan artifacts and explicitly choosing the namespace:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --approve \
  --json
```

Approved apply:

- requires `TURBOPUFFER_API_KEY` from the environment;
- embeds only rows selected by the freshly recomputed diff;
- upserts only those rows;
- updates local applied state only after successful live work;
- retains stale rows by default as `retained_stale` in local state.

Do not store API keys, private vault names, item titles, share IDs, or token values in files.

## Stale delete guardrail

Preview exact stale deletes without live calls:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --delete-stale \
  --json
```

Actually delete stale rows only with both flags:

```bash
uv run turbo-search apply \
  --plan artifacts/site-crawls/scrapling-readthedocs-io-plan/plan.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --approve \
  --delete-stale \
  --json
```

`--delete-stale` deletes exact stale row IDs from the recomputed diff. It does not delete namespaces.

## Retrieval and eval validation

After a site has been applied with explicit approval, retrieval and eval commands can target that generic namespace with CLI overrides. Dry-run retrieval planning remains local-only:

```bash
uv run turbo-search retrieve \
  "How does Scrapling LinkExtractor filter links?" \
  --dry-run \
  --namespace site-scrapling-readthedocs-io-v1 \
  --region gcp-us-central1 \
  --json
```

List the Scrapling docs eval cases without credentials or live calls:

```bash
uv run turbo-search evals \
  --dry-run \
  --dataset src/turbo_search/data/scrapling_retrieval_smoke_evals.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json
```

Live generic retrieval/evals remain explicitly gated by `--live` and `TURBOPUFFER_API_KEY` in the environment:

```bash
uv run turbo-search evals \
  --live \
  --dataset src/turbo_search/data/scrapling_retrieval_smoke_evals.json \
  --namespace site-scrapling-readthedocs-io-v1 \
  --json
```

Do not run live retrieval/evals unless the namespace has been applied and the user explicitly approves live validation.

## What is still not automatic

- Remote/shared state is not implemented; state is local-first.
- Live generic applies/deletes/retrievals/evals should only be run when explicitly approved for the current site/namespace.
- Live SDK compatibility should be validated on a disposable namespace before relying on generic apply for production use.
