Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/2026-07-19-capture-current-repo-candidates-and-baselines.md, .10x/tickets/done/2026-07-19-freeze-repo-ranking-experiment-contract.md, .10x/tickets/done/2026-07-20-remove-buoy-internal-ranking-judgment.md

# C3 / Buoy Baseline Approval Checkpoint

## Checkpoint result

The two live operations needed before C3 can complete are separate approval decisions:

1. populate and register the missing same-source Buoy baseline; then
2. only after that baseline is verified compatible, capture one retrieval-only raw-candidate pass over the frozen 90 composite identities.

Neither operation is approved by this record. C3 remains `blocked` and non-executable. This checkpoint read no credential, queried no Turbopuffer resource, loaded or downloaded no model, wrote no namespace/catalog/applied state, and issued no retrieval call.

The requested worktree-root `context.md` and `plan.md` were absent. The active C3 ticket, completed C1 contract/evidence, completed Buoy judgment-removal ticket/evidence, current source, retained C1 temporary plan artifacts, and local immutable model-cache metadata governed this checkpoint.

## Exact current content-embedding contract

Current plan/apply/retrieval source establishes this content-vector contract:

| Field | Exact value | Local authority |
|---|---|---|
| model | `BAAI/bge-small-en-v1.5` | `src/buoy_search/config.py`, `src/buoy_search/plan_artifacts.py` |
| immutable revision proposed for this baseline | `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a` | local Hugging Face `refs/main`; same immutable revision already fixed for routing in `src/buoy_search/catalog.py` |
| precision | `float32` | plan plus `src/buoy_search/config.py` |
| dimensions | 384 | model `config.json`, pool config, and `src/buoy_search/chunker.py` |
| maximum sequence length | 512 | cached `sentence_bert_config.json` |
| pooling | CLS token | cached `1_Pooling/config.json` (`pooling_mode_cls_token=true`, mean/max false) |
| normalization | L2 normalized | `SentenceTransformerEmbedder.encode(... normalize_embeddings=True)` and cached `2_Normalize` module |
| document transform | `Title: <title>\n\nSection: <section_path>\n\n<content>`, omitting empty title/section components | `src/buoy_search/apply.py::embedding_text_for_chunk` |
| document prefix | none beyond the labeled title/section transform above | current apply source |
| query transform/prefix | trim surrounding whitespace, then encode raw query; no BGE instruction prefix | `src/buoy_search/retriever.py::HybridRetriever.retrieve` |
| distance | `cosine_distance` | `src/buoy_search/chunker.py::TurbopufferWriter` |

The content-query no-prefix behavior is distinct from catalog routing. Catalog routing uses the exact query prefix `Represent this sentence for searching relevant passages: `, but that prefix MUST NOT be attributed to namespace content retrieval.

### Immutable cache and byte envelope

Read-only cache inspection found one `BAAI/bge-small-en-v1.5` snapshot and `refs/main` points to the revision above. The snapshot contains 12 resolved files totaling **267,599,430 bytes**. A canonical sorted JSON manifest of each file's relative path, byte count, and SHA-256 hashes to `5f783ebce23b6ac957d2741399b46e19502b1751acfd3c744b8c41103b138f35`.

- `model.safetensors`: 133,466,304 bytes; SHA-256 `3c9f31665447c8911517620762200d2245a2518d6e7208acc78cd9db317e21ad`.
- Torch/SentenceTransformer runtime files excluding the optional ONNX export and README: 134,411,157 bytes.
- Snapshot excluding only optional `onnx/model.onnx`: 134,505,940 bytes.
- Optional `onnx/model.onnx`: 133,093,490 bytes; SHA-256 `828e1496d7fabb79cfa4dcd84fa38625c0d3d21da474a00f08db0f559940cf35`.

No cache file was downloaded, modified, or loaded as a model. A prior same-model Apple M2 Pro / 16 GB, float32 Torch/MPS, batch-32 observation in `.10x/evidence/.storage/2026-07-14-open-embedding-backend-bakeoff.json` recorded 14.974 seconds to load, 498,368,512 bytes RSS after load, and 641,138,688 bytes observed peak process RSS over 1,024 rows. Those are an observed local resource envelope, not a guaranteed cap; unified accelerator allocations are a stated limit. The proposed Buoy apply uses batch 32 over 903 rows.

Current content embedding construction accepts only the model ID and does not pass an immutable revision or `local_files_only=True`. Therefore an approved baseline run MUST set `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`, revalidate the cache ref and manifest hash immediately before execution, and stop on any mismatch. The routing-card loader already passes this exact revision with `local_files_only=True`. This checkpoint does not change either loader.

## Reproduced retained Buoy plan

The retained C1 temporary artifacts at `/tmp/buoy-c1-current-plan` still verify locally against an absent `/tmp/buoy-c1-state` first-apply ledger. `load_verified_apply_plan` reproduced the exact preflight without reading credentials, loading a model, or contacting Turbopuffer:

| Field | Exact value |
|---|---|
| repository | `Doctacon/buoy-search` |
| source ref / commit | `develop` / `fcb7abbe1652d2eab4ee23816b6d992d893603ac` |
| selected public paths | 64 total pages: 57 selected files plus 7 oversize file cards |
| rows | 903 |
| namespace | `github-doctacon-buoy-search-v1` |
| plan ID/name | `plan_b6c5d128295f442f` |
| selected-corpus artifact hash | `b6c5d128295f442fcae21472c9bcb037ecb44101ca648115e8f666ba59a6f0ce` |
| `plan.json` | 1,192,285 bytes; SHA-256 `f1316f233857c59f6467071b95750638276ac364a6994f3b25a0a3a2c42d3b46` |
| `manifest.json` | 2,747,684 bytes; SHA-256 `a8e82bd81e5303157691494dfb2f8de50955d072c21cef2e150ec31ae261079c` |
| `chunks.jsonl` | 2,351,065 bytes; SHA-256 `5fc9a5c14a47552fbfc8cf02d251150db3fbfe521c7c8036a4dee417af269185` |
| preflight diff | first apply; 903 embeddings; 903 upserts; 0 unchanged; 0 stale; 0 deletes |
| default batching | embedding batch 32; write batch 64; 29 embedding batches and 15 content upsert calls |
| local state path | `/tmp/buoy-c1-state/state/github-doctacon-buoy-search/github-doctacon-buoy-search-v1/state.duckdb` |

All 903 manifest pages/chunks carry the one source commit. The plan uses target 300 tokens, overlap 2, 50 KiB normal-file cap, and oversize file cards. The retained artifact is the exact C1 plan; this checkpoint did not re-crawl or rewrite it.

## Baseline apply effects that cannot be represented as “namespace rows only”

Current approved-apply source makes these effects part of one operation:

1. Acquire/create the local namespace apply lock under `/tmp/buoy-c1-state`.
2. Construct a pinned local routing-card embedding before reading a credential.
3. Read `TURBOPUFFER_API_KEY`, then strongly inspect the remote namespace list and `buoy-routing-catalog-v1` twice around one metadata read; card pagination count depends on unqueried remote state.
4. Create a mode-0600 pending registration at `/tmp/buoy-c1-state/catalog-pending/plan_b6c5d128295f442f.json`.
5. Generate 903 local content embeddings and issue 15 target-namespace upsert calls of at most 64 rows each. The first successful write can create `github-doctacon-buoy-search-v1` implicitly. No delete call is requested.
6. Persist a local DuckDB ledger containing 903 active rows plus one apply-run summary.
7. Create or revision-conditionally update one generated card for `github-doctacon-buoy-search-v1` in `buoy-routing-catalog-v1`, including a local routing vector; verify that card twice.
8. Strongly reread the remote catalog and namespace list, then remove the pending file on complete success.
9. Remove the successful temporary plan directory through CLI cleanup. On partial failure, content rows and DuckDB state can already be committed while the catalog is uncommitted/unverified and the pending file remains for reconciliation.

With one namespace-list page and one card page per pass, source implies a minimum of 13 remote catalog read/write calls in addition to the 15 content upsert calls. Actual catalog reads can be higher because current remote pagination was deliberately not queried. The catalog action is `create` if the card is absent or a revision-bound `update` if present; current preflight correctly reports it as unknown until the approved remote read. Thus a claim of “903 writes with zero catalog/local-state effects” would be false for the current apply path.

## Approval A — Buoy baseline write only

Exact proposed approval text:

> Approve one first apply of retained plan `plan_b6c5d128295f442f` (artifact `b6c5d128295f442fcae21472c9bcb037ecb44101ca648115e8f666ba59a6f0ce`) from `Doctacon/buoy-search@fcb7abbe1652d2eab4ee23816b6d992d893603ac` into `github-doctacon-buoy-search-v1`: 903 local float32 embeddings with `BAAI/bge-small-en-v1.5@5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`, 903 row upserts in 15 batches of at most 64, zero row/namespace/card deletes, plus the current apply path's required local DuckDB/pending/lock state and one generated remote catalog-card create or revision-bound update with verification. Run model access offline only after the cache ref and manifest hash `5f783ebce23b6ac957d2741399b46e19502b1751acfd3c744b8c41103b138f35` revalidate; stop on source/artifact/model/state mismatch or any stale/delete intent. This approval does not authorize C3 retrieval, a recrawl/replan, another namespace, a default change, or promotion.

This approval has not been granted. After any approved apply, independent evidence MUST record actual content/catalog request and provider-billing counters, resulting applied-state/card revisions, exact remote row count/source commit/model attestation, zero deletes, and any partial-success state before Buoy can be marked compatible.

## Frozen retrieval map after compatible baseline evidence

| `repo_key` | Namespace | Source commit |
|---|---|---|
| `black` | `github-psf-black-v1` | `c4c9a93111309459a3f0e1e268160f7ef2159077` |
| `buoy` | `github-doctacon-buoy-search-v1` | `fcb7abbe1652d2eab4ee23816b6d992d893603ac` |
| `click` | `github-pallets-click-v4-oversize-cards` | `6ec99f89261b32f8a50848786eca055e1967659f` |
| `django` | `github-django-django-v1` | `54495840a6a8b09ec40c793495e6541a3c0d3d5b` |
| `flask` | `github-pallets-flask-v1` | `36e4a824f340fdee7ed50937ba8e7f6bc7d17f81` |
| `httpx` | `github-encode-httpx-v1` | `b5addb64f0161ff6bfe94c124ef76f6a1fba5254` |
| `mkdocs` | `github-mkdocs-mkdocs-v1` | `2862536793b3c67d9d83c33e0dd6d50a791928f8` |
| `pydantic` | `github-pydantic-pydantic-v1` | `080c741ecf4e113b9c7487de16ffbba5182f03bf` |
| `pytest` | `github-pytest-dev-pytest-v1` | `1aa747de62dd9e9f395513c25298ba604f1724d0` |
| `requests` | `github-psf-requests-v1` | `4ed3d1b3204caa6806a36125a39589044a02e807` |
| `rich` | `github-textualize-rich-v1` | `9d8f9a372cc5916fd4781fec207ced7ddac2f08f` |
| `ruff` | `github-astral-sh-ruff-v1` | `e6856de97d72225196444b7d969b8fe084140503` |
| `typer` | `github-fastapi-typer-v1` | `b210c0e2376d99344f79f11fab3ad34cf890cc20` |

The inventory remains exactly 13 datasets, 90 composite `repo_key:case_id` identities, and 369 judgments; every remaining judgment path resolves. Dataset-local IDs remain unchanged.

## Exact C3 request and cost exposure derivable from source

One raw pass is:

- 90 logical cases and 90 local query embeddings;
- 90 ANN subqueries plus 90 BM25 subqueries = **180 retrieval subqueries**;
- one two-subquery `multi_query` per case = **90 physical retrieval requests** when retries and schema-fallback repeats are disabled;
- `candidates=200` for each list = at most **36,000 returned candidate-list positions** before de-duplication (90 × 2 × 200);
- one offline client RRF/default-ranking replay from those lists; no second direct provider pass;
- zero writes, deletes, catalog operations, namespace discovery, or local applied-state changes.

The locked dependency is `turbopuffer==2.4.0`. Current production retrieval first asks for server-side RRF and can return fused-only rows; its unsupported-signature fallback can also call twice. That path does not satisfy C3's separate-list and one-pass contract. After approval, C3 implementation must instead make exactly one no-`rerank_by` multi-query per case, preserve the two provider-ordered result lists, and perform RRF/default ranking offline. It must stop rather than retry or use optional-attribute schema fallback; otherwise the approved 90-request bound would be exceeded.

No checked-in source or public immutable metadata establishes the account's dollar price or maps one multi-query/subquery/candidate row to a fixed billable amount. This checkpoint did not query the provider or account. Monetary exposure is therefore not honestly calculable in dollars before the pass. The exact source-backed cost bound is 90 physical requests, 180 subqueries, and at most 36,000 returned list positions, with provider-reported billing units recorded after each response and zero retries. Any implementation that cannot enforce or attest this bound must stop before calls and return for renewed approval.

## Approval B — C3 retrieval capture only

Exact proposed approval text, valid only after Approval A has separate completion/compatibility evidence:

> Approve one retrieval-only raw-candidate pass for the 90 frozen composite `repo_key:case_id` identities across the exact 13 namespace/source-commit map in `.10x/evidence/2026-07-20-c3-buoy-baseline-approval-checkpoint.md`, using the pinned current-default content contract `BAAI/bge-small-en-v1.5@5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`, raw trimmed queries with no prefix, normalized 384-dimensional float32 vectors, cosine ANN, boosted title/section/content BM25, 200 candidates per list, and separate provider-ordered ANN/BM25 lists. Authorize exactly 90 physical two-subquery multi-query requests (90 ANN + 90 BM25 = 180 subqueries; at most 36,000 returned list positions), zero retries or fallback requests, provider billing-unit recording at the existing account rate whose dollar total is not source-derivable, zero writes/deletes/catalog/namespace-discovery/applied-state changes, and one immutable cache shared by C7/C8. Fuse and run the current `file` / `repo_code` / pool 100 / `adaptive_sum_3` default offline from that same response; issue no second direct pass. Stop before calls on any namespace/source/model/corpus mismatch or if separate lists and the exact request bound cannot be enforced.

This approval has not been granted. Preparing or granting it does not ratify C7/C8 thresholds, authorize a duplicate capture, or authorize promotion.

## Procedure and validation

Read-only inspection covered current embedding, apply, plan, retrieval, catalog, pending-state, and applied-state source; completed C1 and label-removal records; the frozen inventory/source bundle; retained C1 plan artifacts; local Hugging Face symlink targets and text configuration; and prior same-model resource evidence. File sizes and hashes were computed by direct byte reads only. No model library was imported for cache inspection.

The retained plan was verified once through `load_verified_apply_plan` and `apply_preflight_summary`. That command created a disposable project `.venv` while resolving the locked environment; it was removed immediately and made no tracked diff, model load/download, credential read, or domain-side effect. Future verification should use an already-provisioned locked environment to avoid that local setup churn.

Validation expected after this record:

```text
scripts/validate_ranking_contract.py => 13 datasets; 90 identities; 369 judgments; all paths resolved; buoy pending approval
focused ranking-contract tests => pass
git diff --check => pass
tracked diff => record-only checkpoint plus narrow C3 ticket progress/reference update
```

## Limits

- Local cache state proves what is present now, not what an unpinned content loader would choose if offline controls or cache refs change.
- The prior RSS observation is not a hard device-memory cap and did not measure this exact approved apply lifecycle with repeated routing/content model constructions.
- No remote namespace/card existence, row contents/count, billing, retry behavior, source/model compatibility, or account price was observed.
- The retained `/tmp` plan is not durable project storage. Approval must bind its recorded hashes, and execution must stop if those exact bytes are absent or changed.
- Current source does not yet provide C3's exact raw separate-list artifact capture. This checkpoint authorizes no implementation and makes C3 non-executable until both approvals and required implementation/review gates are satisfied.
