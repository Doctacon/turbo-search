Status: active
Created: 2026-07-20
Updated: 2026-07-20
Parent: .10x/tickets/2026-06-28-repo-search-heavy-ranking-experiments.md
Depends-On: None

# Shape Deterministic Token-Budget Subdivision

## Outcome

Shape, without implementing or activating, a deterministic token-budget subdivision contract that could resolve C6's exact pinned-tokenizer incompatibility. The user explicitly authorized this separate shaping work after PR #71 recorded 21,292 treatment rows above the 512-token maximum. This ticket grants no implementation, plan regeneration, model construction or inference, credential or provider access, namespace write, retrieval, catalog/applied-state/default change, delete, evaluation, or promotion authority.

## Scope

- Inspect the active Python syntax chunking contract, the preserved nine-plan forecast, and exact tokenizer checkpoint `c3a1560e611114760909c110a118a3ce1a60f0527de08c769a85a20b263f4e0f` without changing those artifacts.
- Shape a deterministic subdivision contract against the exact pinned `BAAI/bge-small-en-v1.5@5c38ec7c405ec4b44b94cc5a9bb96e735b38267a` tokenizer and 512-token maximum, including how complete rendered-row text and special tokens consume the budget.
- Present candidate behavior for subdivision at source-line boundaries, exact citations for every resulting chunk, and fail-closed treatment when an individual line cannot fit the exact budget.
- Identify how any candidate composes with the active treatment arms' existing line-based subdivision, common header, exact source coverage, ownership, fallback, deterministic ordering, and control isolation.
- State the artifact, forecast, test, specification, review, and separate write-approval work that would be required after ratification; do not perform it here.

## Candidate semantics, not active behavior

The user authorized shaping, not these values. Until a later user-legible checkpoint is independently reviewed and explicitly ratified, all of the following remain candidates only:

- subdivide over-limit treatment rows only at deterministic source-line boundaries;
- preserve exact `Lines S-E` citations for every emitted subdivision;
- fail closed when one individually over-limit source line cannot fit the exact tokenizer budget;
- any header-budget allocation, blank-line handling, grouping rule, interaction with existing 80-line subdivision, identity derivation, or fallback behavior needed to make those candidates complete.

No active specification is changed by this ticket's creation. The current fail-closed behavior remains authoritative: any treatment row above 512 exact tokens fails C6 readiness.

## Acceptance criteria

- The shaping output maps every proposed semantic to active-record-backed, source-observed, user-ratified, or still-blocked provenance; candidate examples are not promoted into active acceptance criteria.
- A user-legible confirm-or-correct checkpoint covers exact tokenizer accounting, deterministic boundary/grouping behavior, citations and coverage, an individually over-limit line, headers, blank/trivia lines, existing subdivision/fallback interaction, identities/order, and control-arm non-change.
- Options and tradeoffs include at least preserving source-line boundaries versus any alternative, while retaining exact reconstruction/coverage and fail-closed tokenizer compatibility.
- Required spec, source/test, forecast regeneration, artifact identity/count, independent review, and separate write-approval consequences are explicit and remain downstream-only.
- C6 remains `blocked`; the preserved forecast/token artifacts and `scripts/c6_syntax_forecast.py validate` behavior remain byte-for-byte unchanged during shaping.
- No implementation, test encoding of candidate semantics, live plan/apply, model construction/inference, credential/provider access, namespace/catalog/state/default operation, delete, retrieval, evaluation, or promotion occurs.

## Blockers

The draft behavioral contract at `.10x/specs/deterministic-treatment-token-budget-subdivision.md` remains inactive pending independent review and explicit user confirm-or-correct ratification. Its exhaustive farthest-feasible prefix algorithm, inherited-parent breadcrumbs, complete-plan failure scope, and all adjacent mechanics are candidates only. No implementation ticket may be opened from them.

Read-only decomposition of the exact checkpoint found that 20,926 of the 21,292 incompatible treatment plan rows are source rows eligible for the draft physical-line mechanism, while 366 are unchanged prose rows (183 unique repository/row identities across 57 paths, duplicated across the two treatment plans). Prose subdivision is outside this ticket and remains semantically unresolved. The 366 rows are an independent fail-closed C6 blocker owned by the existing blocked C6 checkpoint; source-only ratification or later implementation cannot make readiness pass or authorize ignoring them.

## Explicit exclusions

Implementation or tests of subdivision; edits to active specifications; regeneration or mutation of the preserved C6 forecast, authority, or tokenizer report; live plan/apply; tokenizer/model download; model construction or inference; credentials; provider, namespace, catalog, applied-state, dataset, label, default, retrieval, delete, evaluation, or promotion operations; C6 activation or write approval.

## Evidence expectations

A record-only shaping artifact with provenance classification, options/tradeoffs, complete edge-case questions, source/record citations, a user-legible confirm-or-correct checkpoint, independent review, and explicit attestation that the preserved C6 artifacts and fail-closed validator were unchanged.

## References

- `.10x/tickets/2026-07-19-evaluate-python-syntax-chunking.md`
- `.10x/specs/repo-python-syntax-chunking-experiment.md`
- `.10x/evidence/2026-07-20-c6-python-syntax-pilot-forecast.md`
- `.10x/evidence/.storage/2026-07-20-c6-python-syntax-pilot-forecast.json`
- `.10x/evidence/.storage/2026-07-20-c6-python-syntax-tokenizer-preflight.json.gz`
- `.10x/specs/deterministic-treatment-token-budget-subdivision.md`
- `.10x/evidence/2026-07-20-deterministic-token-budget-subdivision-shaping.md`
- `scripts/c6_syntax_forecast.py`

## Progress and notes

- 2026-07-20: Opened from the user's explicit decision to shape deterministic token-budget subdivision separately. Source-line boundaries, exact citations, and individually over-limit line fail-closed handling are candidate scope, not ratified semantics. No active specification, implementation/test, preserved forecast/token artifact, plan, model, credential, provider, namespace, retrieval, catalog/state/default, delete, evaluation, or promotion operation was authorized or changed. C6 remains blocked and non-executable.
- 2026-07-20: Produced record-only draft `.10x/specs/deterministic-treatment-token-budget-subdivision.md` and shaping evidence with exact final-payload tokenizer accounting, exhaustive farthest-feasible prefixes within existing treatment parents, inherited breadcrumb/ownership, exact coverage/citations, deterministic identity/order, complete-plan one-line failure, downstream validation/regeneration gates, and a user-legible checkpoint. Exact report decomposition found 20,926 incompatible source plan rows plus 366 incompatible unchanged prose plan rows; the prose rows remain a separate fail-closed C6 blocker and no prose semantics were invented. A read-only pinned Buoy probe found zero individually unsplittable physical lines in either arm across 46 selected code files; pytest/Ruff remain unquantified without local pinned sources/plans. Ticket remains active pending independent review and explicit ratification; no active spec/source/test/artifact/validator/live surface changed.
