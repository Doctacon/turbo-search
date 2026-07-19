Status: recorded
Created: 2026-07-19
Updated: 2026-07-19
Target: .10x/tickets/done/2026-07-18-review-stale-ticket-statuses.md
Verdict: pass

# Stale Ticket Status Closure Review

## Target and method

Adversarial closure review of the eight tickets named by `.10x/tickets/done/2026-07-18-review-stale-ticket-statuses.md`. The review used only existing tickets, active specs/decisions/knowledge, evidence, reviews, and narrowly inspected material current source/tests where the float16 and single-pass semantic authority needed a drift check. No test, benchmark, live operation, implementation repair, new verification evidence, or residual-risk acceptance was performed.

Node.js-action and retrieval-tag tickets were not read for disposition and were not changed.

## Disposition table

| Ticket | Disposition | Basis |
|---|---|---|
| `.10x/tickets/done/2026-07-13-float16-embedding-inference.md` | done | All criteria map to the active precision spec, existing validation/benchmark, current material tests/source, and this review; no spec drift found. |
| `.10x/tickets/done/2026-07-14-single-pass-plan-and-stage-timing.md` | done | Existing evidence plus current exact call-count/equivalence tests support every criterion; this review supplies the required closure review. |
| `.10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md` | done | Four existing evidence records prove datasets, local plans, separately approved new-namespace applies, zero deletes, retrieval-only comparisons, metrics, and no-regression disposition. |
| `.10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md` | cancelled/no action | Evidence rejects global promotion and preserves opt-in behavior, but full-basket characterization and explicit binary/vendor/generated-noise audit are absent; `done` is unsupported. |
| `.10x/tickets/done/2026-06-28-website-capped-aggregation-default-review.md` | done | Existing five-site metrics apply the active no-regression policy and support no promotion; conditional implementation criterion is not applicable. |
| `.10x/tickets/done/2026-06-28-repo-searchable-path-symbol-metadata.md` | done | Existing local evidence proves the opt-in repository-only implementation, safety, tests, and unchanged defaults; later separately approved evidence does not invalidate the bounded slice. |
| `.10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md` | remain active | Many experiments and promotions are supported, but named code-aware embedding, syntax-aware chunking, learning-to-rank, and routed-selector/profile outcomes lack terminal evidence or no-action authority. |
| `.10x/tickets/cancelled/2026-07-14-conditional-website-replanning.md` | cancelled/no action | The independently reviewed gate found material acquisition but 0/12 authoritative 304 responses; the ticket contract forbids heuristic implementation, so stopping is the supported outcome. |

## Acceptance mapping

### Float16 embedding inference

1. **Specification behavior/compatibility/integrity:** `.10x/evidence/2026-07-14-float16-embedding-inference.md` records plan/apply/retrieval/eval/autoresearch propagation, old-plan compatibility, stable row IDs, precision-driven re-upsert, accelerator guard, summaries, tests, and no live operations. Material current `config.py`, `plan_artifacts.py`, `apply.py`, `chunker.py`, `retriever.py`, and named tests still implement/assert those behaviors.
2. **Float32 default and old plans:** the active spec remains `float32`-default; current tests assert default precision and legacy hash verification without rewriting artifacts.
3. **Re-embedding/stable IDs:** existing evidence and `test_float16_plan_reupserts_float32_state_with_stable_row_id` support the criterion.
4. **Parity/throughput benchmark:** the stored 1,024-real-chunk MPS benchmark passes minimum cosine `0.999756` and exact top-10 identity; neutral throughput is reported without a speed claim.
5. **Focused/full suites and review:** existing evidence records focused/full/build/diff results. This aggregate adversarial review supplies the previously missing review without adding verification evidence.

**Spec-drift gate:** pass. Commit `aa6110d` is an ancestor of the reviewed head. The active spec's post-rebrand package/environment names match current source. Later routing/catalog additions preserve, rather than weaken, the precision compatibility contract. Benchmark limits remain explicit.

### Single-pass planning and stage timing

1. **One corpus pass:** existing evidence records exact one-call assertions for website, repository, and local-document paths; current material tests retain those assertions.
2. **One complete artifact build:** same evidence/tests assert one `build_plan_artifacts` call for all paths.
3. **Best-effort timing:** evidence and current clock-failure coverage show diagnostic failures return zero timing rather than fail planning.
4. **Compatibility:** old-pattern/full-rebuild equivalence compares the complete plan after excluding only volatile `created_at`, plus exact hash, plan ID, diff, manifest, and chunks JSONL.
5. **Validation/benchmark/review:** focused 145, full 248, build/lock/diff, and retained-corpus benchmark are already recorded; this is the required review.

**Drift gate:** pass. Current `_run_plan` consumes the retained `CrawlExecution.indexing_plan`, builds artifacts once, replaces only the diff, and retains stage timing. No active spec conflicts.

### Cross-corpus validation basket

1. Seed datasets: `.10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md` records four source-backed datasets and counts.
2. Local-only plan first: `.10x/evidence/2026-06-28-cross-corpus-validation-local-plans.md` records dry-run/no-credential/no-remote behavior.
3. New namespaces only after approval: `.10x/evidence/2026-06-28-cross-corpus-live-apply.md` records separate approval and the four new namespaces.
4. No deletes: apply evidence records zero rows deleted.
5. Retrieval only after apply/approval: `.10x/evidence/2026-06-28-cross-corpus-live-retrieval-evals.md` records separate approval and no mutation.
6. Baselines/alternates: repo default/max/capped/raw and site default/capped/raw are recorded per target.
7. Commands/counts/metrics/limits/conclusion: all are present in the four evidence records.
8. No-regression before defaults: active `.10x/decisions/namespace-ranking-defaults.md` remains unchanged by this basket; capped repo/site candidates were not promoted on regressing evidence.

**Dependency-coherence gate:** pass. The active namespace-ranking decision remains the basket's dependency. The active heavy-ranking umbrella receives context and evidence from this independently completed basket and is therefore a reference, not a prerequisite to closure.

### Repo oversize source indexing

1. Added files/chunks: supported for pytest and Typer, not the full then-current repo basket.
2. Local-only safety: supported.
3. Smallest safe direction: supported only as a 200 KiB opt-in/future query-routed direction.
4. Reviewable/no binary/vendor/generated noise: row growth and selected authority files are recorded, but an explicit noise audit is not.
5. No unapproved default/live mutation: later live work had separate approval, used new namespaces, and deleted zero rows.

**Finding:** significant — a `done` closure would overstate criteria 1 and 4. Cancellation with explicit no-action is supported because both live target datasets regress under oversize indexing and the records explicitly reject a global default. Future query-routed semantics are not silently inherited.

### Website capped aggregation default review

The existing five-site evidence compares max/adaptive/capped using retrieval-only calls; records P@5, score, recall, NDCG, MRR, and deltas; and applies the active no-regression policy. Capped regresses Pi and adaptive regresses turbopuffer, so no promotion is justified and the separate-implementation criterion is not applicable.

**Decision-drift gate:** pass. `.10x/decisions/namespace-ranking-defaults.md` and `.10x/knowledge/repo-search-ranking-defaults.md` still keep website `page/none/pool20/max` and capped opt-in.

### Repo searchable path/symbol metadata

Existing local evidence proves explicit `--repo-search-metadata`, unchanged defaults, repository-only generated Markdown metadata, local-only plan/preflight safety, 34 focused and 142 full tests, and no same-slice promotion. Later separately approved live evidence and the completed cross-repo validation reject universal promotion while preserving the bounded opt-in implementation.

**Authority check:** pass. Current ranking knowledge still documents the option as opt-in and its no-promotion evidence.

### Repo search heavy ranking experiments

Existing evidence supports experiment isolation, open-source/local rerankers, new namespaces with zero deletes for indexing ablations, comparison against evolving baselines, tests for source changes, retrieval-only metrics, no-regression promotions, rejected hypotheses, distribution-aware 13-repo validation, and an `80.316` routed evaluation result.

**Finding:** significant — terminal closure is unsupported. The umbrella scope expressly names code-aware embeddings, syntax-aware/symbol-breadcrumb chunking, and learning-to-rank; these have no completion evidence or durable no-action decision. The latest routed profile uses evaluation-time per-repo mapping/monkeypatching and explicitly says a production selector/profile is not implemented. Keeping the ticket active preserves those outcomes without misclassifying rejected hypotheses as implementation failures.

### Conditional website replanning

The existing baseline records the authorized local-only Oscilar plan and all requested stage timing. It shows acquisition at 96.3%, but 0/12 sampled pages returned authoritative 304 responses. The independent measurement-gate review passes the decision not to create cache/spec/implementation. Cache-key, equivalence, corruption, and fallback implementation criteria were correctly not executed because their prerequisite failed.

**Finding:** no blocker to cancellation. Cancellation is not acceptance of heuristic risk; it is the explicit no-action result required by the safety contract. A future different workload needs new authority.

## Scope and graph findings

- No Node.js-action or retrieval-tag record was changed.
- No source, tests, benchmarks, live operations, external state, defaults, or residual-risk decisions were changed.
- Completed experiments remain completed; rejected hypotheses remain negative evidence, not failed implementation.
- The heavy-ranking umbrella remains the durable owner for its unsupported terminal scope and receives the completed cross-corpus basket as context/evidence rather than blocking that basket's closure.
- Terminal paths and all affected `.10x` references were mechanically repaired and validated before the review ticket closed.

## Verdict

**Pass.** The dispositions are conservative and evidence-backed. The two cancellations include explicit no-action rationale, the five completed target tickets meet their bounded criteria using existing evidence plus this required aggregate review, and the heavy-ranking ticket remains active because terminal closure would overclaim.

## Residual risk

- Float16 numerical parity is one host and one query sample; no speedup claim is accepted.
- Ranking labels remain assistant-drafted; this limits promotion confidence but is already stated in governing records and does not invalidate the reviewed experiment dispositions.
- Heavy ranking remains broad and should be split before future execution; this review does not authorize or design that split.
- The outer cleanup plan remains open for its final compatibility-shaping child; this review does not close the parent.
