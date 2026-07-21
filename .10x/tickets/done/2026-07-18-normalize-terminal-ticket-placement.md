Status: done
Created: 2026-07-18
Updated: 2026-07-19
Parent: .10x/tickets/done/2026-07-18-repository-cleanup-plan.md
Depends-On: .10x/tickets/done/2026-07-18-remove-unreachable-local-catalog-persistence.md

# Normalize Terminal Ticket Placement

## Scope

Mechanically move the 19 `done` and one `cancelled` ticket currently stored directly under `.10x/tickets/` into `.10x/tickets/done/` and `.10x/tickets/cancelled/`, then repair every affected `.10x/` reference.

## Acceptance criteria

- Enumerate exact source/destination paths and refuse collisions.
- Move only tickets whose existing status is already terminal; do not alter status, semantics, progress history, or closure claims.
- Repair all Markdown path references across `.10x/` while preserving historical meaning.
- No top-level ticket has `done` or `cancelled` status afterward.
- No `.10x/` Markdown reference points to a missing path; `git diff --check` passes.
- Independent record review confirms no active authority was changed.

## Evidence expectations

Before/after terminal inventory, move map, reference validation count, diff check, and no source/runtime changes.

## Blockers

None. The source-cleanup dependency integrated at `326d070` before execution began.

## Explicit exclusions

Closing, cancelling, rewriting, or deleting any ticket; changing source/tests/docs outside reference repair; moving evidence/reviews/research.

## References

- `.10x/tickets/done/2026-07-18-repository-cleanup-plan.md`
- `.10x/research/2026-07-18-repository-dead-end-inventory.md`

## Progress and notes

- 2026-07-19: Moved the 19 already-`done` and one already-`cancelled` top-level tickets to their collision-free terminal directories and repaired 57 exact `.10x` Markdown path references. Validation found zero remaining top-level terminal statuses, preserved each moved record's status and all content other than affected path references, introduced no new broken `.10x` references, and left the 27 pre-existing unrelated broken references unchanged. Evidence: `.10x/evidence/2026-07-19-normalize-terminal-ticket-placement.md`. Independent review remains required before closure.
- 2026-07-19: Completed the literal no-missing-reference criterion by auditing all 27 pre-existing candidates against active and terminal records plus Git history: repaired 20 live pointers to actual `done/` owners, preserved four fenced historical path strings as evidence, and verified three commit-qualified historical paths in their cited tree. Semantic validation now reports zero missing current or commit-qualified `.10x` Markdown references, with no top-level terminal statuses and no source/runtime/test changes. Evidence: `.10x/evidence/2026-07-19-normalize-terminal-ticket-placement.md`.
- 2026-07-19: Independent review passed at head `a5b89f9735435e7c9b4adc1209ef810709a11215`; no blocker or residual risk remained. Review: `.10x/reviews/2026-07-19-normalize-terminal-ticket-placement-review.md`.

## Closure mapping

- Exact collision-free move map and terminal status preservation: evidence inventory and independent reconstruction.
- Reference repair and historical meaning: 57 moved-path substitutions plus complete 27-candidate audit.
- Graph validity: zero missing non-fenced current/commit-qualified references and zero top-level terminal statuses.
- Scope: all changed paths are `.10x` Markdown; no source/runtime/tests changed.
- Validation: diff/reference/status checks, hosted CI, evidence, and independent pass review.

## Retrospective

Path validation must distinguish live graph edges from fenced historical output and commit-qualified historical citations. A raw regex both over-reports quoted evidence and under-explains whether old paths ever existed. Future record moves should validate semantic references by context and cited tree, not path existence alone.
