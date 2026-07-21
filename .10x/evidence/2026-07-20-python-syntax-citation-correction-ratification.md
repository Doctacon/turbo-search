Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/specs/repo-python-syntax-chunking-experiment.md, .10x/specs/superseded/repo-python-syntax-chunking-experiment-originating-citation.md, .10x/tickets/done/2026-07-19-implement-opt-in-python-syntax-chunking.md, .10x/tickets/2026-07-19-evaluate-python-syntax-chunking.md

# Python Syntax Control Citation Correction Ratification

## What was ratified

The user explicitly ratified one narrow correction after the C6 pinned-corpus forecast disproved the original universal control-citation wording:

- `current-default` MUST preserve exact existing generic-renderer/parser/split/overlap citation output, including final source rows whose `section_path` has no parseable `Lines S-E` component because an embedded Markdown-like heading replaced it;
- `fixed-80-python-breadcrumbs` and `python-ast` still MUST emit payload-accurate exact `Lines S-E` ranges for every treatment source row; and
- corpus selection, normalized output, chunks, row identities, plan counts, storage, control/no-arm parity, default behavior, and all safety boundaries remain unchanged.

No missing control line range may be synthesized, and no default repair or token subdivision semantic was ratified.

## Supersession rationale

The prior active text said every control source final chunk retained an originating line-range component. The exact Ruff control/no-arm forecast instead found 2,722 rows across 170 paths with no parseable component while proving exact ordinary/current-default equivalence. Preserving both the old universal wording and actual parity was impossible. The original contract is therefore preserved at `.10x/specs/superseded/repo-python-syntax-chunking-experiment-originating-citation.md`; the active path contains the corrected contract so existing references continue to resolve to current authority.

This correction accepts observed existing control behavior; it does not approve that behavior as payload-accurate citation semantics and does not weaken treatment citation requirements.

## Safety and limits

The ratification authorizes record and deterministic preflight repair only. It grants no credential access, model inference, provider call, live retrieval, namespace write/delete, catalog/applied-state mutation, default change, truncation, token subdivision, C6 apply, or promotion. C6 remains blocked on exact model-tokenizer compatibility, independent review, and separate exact write approval.
