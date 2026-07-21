Status: done
Created: 2026-07-13
Updated: 2026-07-19
Parent: None
Depends-On: .10x/tickets/done/2026-07-12-approved-apply-throughput-measurement.md, .10x/tickets/done/2026-07-14-buoy-release-integration-validation.md

# Add Opt-In Float16 Embedding Inference

## Scope

Implement `.10x/specs/embedding-inference-precision.md` across plan, apply, retrieval, eval/autoresearch runtime configuration, documentation, and operational skills.

## Acceptance criteria

- Satisfy every behavior, compatibility, integrity, and verification requirement in the governing specification.
- Keep float32 as the default and preserve old plan verification without rewriting old artifacts.
- Prove precision changes drive re-embedding without changing row IDs.
- Run the specified real-chunk local parity/throughput benchmark without credentials or remote calls and record raw/summarized evidence.
- Run focused and complete test suites; record independent review.

## Explicit exclusions

- Live Turbopuffer apply/retrieval/evals, changing defaults, backend/model/chunk changes, concurrency, retries, and automatic remote precision discovery.

## References

- `.10x/specs/embedding-inference-precision.md`
- `.10x/research/2026-07-12-approved-apply-throughput-options.md`
- `.10x/evidence/2026-07-13-live-dagster-throughput-benchmark.md`

## Evidence expectations

Focused tests, full-suite output, real-chunk no-write vector/ranking parity, host-specific throughput measurements, docs/skill consistency, and independent review.

## Progress and notes

- 2026-07-13: User authorized implementation and selected explicit precision configuration: plans govern apply; retrieval/evals use a CLI flag or environment setting.
- 2026-07-14: Blocked behind the Buoy package rebrand to avoid implementing and then mechanically renaming the same cross-cutting plan/apply/retrieval surface. The governing spec now targets `buoy_search`, `buoy`, and `BUOY_EMBEDDING_PRECISION` with the 0.2 legacy environment contract.
- 2026-07-14: Buoy release integration closed with pass review; this ticket is unblocked and remains separately executable after the rebrand plan.
- 2026-07-14: User prioritized implementation; assigned to a single worker.
- 2026-07-14: Initial review found missing live/eval text precision, true re-upsert/query propagation tests, and autoresearch supported-set validation. Repaired all four with focused 86 and full 246 tests passing; build and diff checks pass. Evidence updated; awaiting re-review.
- 2026-07-14: Implemented opt-in precision across plan/apply/retrieve/evals/autoresearch/config/docs/skill, old-plan compatibility, stable-row precision re-upsert, accelerator guard, and precision summaries. Focused 146 and full 242 tests plus build pass. Real 1,024-chunk MPS parity passed (minimum cosine 0.999756; exact top-10), but repeated median throughput was neutral (64.66 float32 vs 64.58 float16 rows/s), so no speedup claim is made. Evidence: `.10x/evidence/2026-07-14-float16-embedding-inference.md`.
- 2026-07-19: Closure review mapped every criterion to the existing validation record, active precision specification, and material current tests/source. Commit `aa6110d` remains an ancestor of the reviewed head. The aggregate adversarial review found no spec drift or unsupported behavior claim. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Blockers

None.

## Closure mapping

- Governing behavior and compatibility: `.10x/specs/embedding-inference-precision.md` and the observed-behavior section of `.10x/evidence/2026-07-14-float16-embedding-inference.md`.
- Float32 default, legacy-plan verification, plan-governed apply, stable row IDs, precision-driven re-upsert, query precision, and accelerator failure: existing focused tests named in the evidence and materially inspected current tests/source.
- Required no-write parity/throughput benchmark: the stored 1,024-real-chunk MPS benchmark met minimum cosine and exact top-10 criteria; it did not support a speedup claim.
- Focused/full validation and review: existing command output in the evidence plus `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Retrospective

The existing benchmark evidence corrected an earlier throughput expectation: numerical parity passed, but repeated median float16 throughput was neutral on the observed M2 Pro. Keep float16 opt-in and separate parity support from host-specific performance claims.
