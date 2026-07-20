Status: recorded
Created: 2026-07-20
Updated: 2026-07-20
Relates-To: .10x/tickets/2026-07-20-shape-dynamic-content-vector-dimensions.md, .10x/research/2026-07-20-dynamic-content-vector-dimensions.md

# Dynamic Content-Vector Dimension Shaping Evidence

## What was observed

At current source commit `72d1344fe344b444dcb6977f18aa461aa8fdb0e0`:

- content namespace vector schema is fixed at `[384]f16` through `src/buoy_search/chunker.py`;
- content model construction is unpinned/network-capable by default and applies `.half()` only after construction;
- plans bind content model/precision but omit revision, dimension, role prefixes, pooling, normalization, and complete model-contract identity;
- card `vector` is a distinct pinned normalized 384-dimensional BGE routing projection, while card `vector_dimensions` is currently forced from the same routing constant and therefore cannot represent dynamic content dimensions;
- remote catalog routing schema is fixed at `[384]f32`, while the separate `vector_dimensions` compatibility attribute is a `uint`; current parsing/default compatibility still requires 384;
- automatic routing filters to one runtime content model/precision/dimension contract, embeds one 384-dimensional routing query for card selection, then reuses one content query vector across selected namespaces;
- active specifications/decision fix card content dimensions and automatic catalog authority to the current v1/384 behavior.

The lockfile resolves `sentence-transformers==5.6.0`, `transformers==5.12.1`, `torch==2.12.1`, and `huggingface-hub==1.20.1`. Read-only inspection of the cached locked Hub source confirmed `snapshot_download` exposes exact `revision`, explicit `cache_dir`, `token`, and `local_files_only`; Hub constants read `HF_HUB_OFFLINE`/`TRANSFORMERS_OFFLINE`, `HF_HUB_DISABLE_TELEMETRY`/`DO_NOT_TRACK`, and `HF_HUB_DISABLE_UPDATE_CHECK`.

C2's immutable source snapshot records:

- Crow-Plus: exact revision `96ff525a7aa3bf8bfa90d77337c2b24bd45229af`, 768 dimensions, 1,024-token maximum, no prefixes, CLS pooling, no model Normalize module, 606,681,112 weight bytes, and 611,525,163 total listed bytes;
- Nomic: exact revision `11114029805cee545ef111d5144b623787462a52`, 3,584 dimensions, 32,768-token maximum, exact query-only prefix, last-token pooling, Normalize module, 28,282,512,976 weight bytes, and 28,298,426,837 total listed bytes.

`.10x/research/2026-07-20-dynamic-content-vector-dimensions.md` initially recorded a side-by-side resource/compatibility matrix, strict content/routing separation, card/catalog options, namespace/plan/apply/retrieval/automatic-routing failure behavior, no-migration isolation, pinned offline bootstrap/load controls, role semantics, dependency implications, stop conditions, and a four-part user checkpoint.

The user subsequently ratified Crow-Plus 768 first, explicit namespace only with no cards/catalog/automatic routing, complete vector/resource/output staging before remote content write 1, and separate bootstrap/bounded-measurement/implementation/indexing-write approvals. Read-only host inspection observed `Mac14,9`, Apple M2 Pro (10 CPU/16 GPU cores), 17,179,869,184 bytes unified memory, macOS 26.5.1 (`25F80`), and 34,890,539,008 bytes available disk. No device/model runtime was invoked.

The repaired research and draft focused specifications now define a separate experimental stage-then-write path rather than weakening the active depth-one default. `.10x/specs/crow-plus-resource-verification-checkpoint.md` proposes exact unratified cache/disk/hardware/precision/batch/input/load/RSS/MPS/observation/abort/output bounds. `.10x/specs/crow-plus-explicit-namespace-pilot.md` binds the ratified explicit-only lifecycle and complete-stage gate.

## Procedure

1. Ran required branch/worktree and clean-status checks.
2. Read the shaping ticket, parent/C2/C4 tickets, C2 immutable research/source snapshot/evidence/review, current source paths named by the ticket, automatic routing/retrieval paths, active routing/card/apply specifications and decision, `pyproject.toml`, and `uv.lock` package entries.
3. Used arithmetic only to render exact C2 byte values as GB/GiB and raw f16/f32 vector element bytes.
4. Inspected cached source for the already-locked Hub package only; no package was imported, installed, resolved, or executed.
5. Wrote record-only research/evidence and updated the shaping ticket. No source/test/configuration/dependency/lockfile file was changed.
6. After the user's ratification, inspected current host hardware/disk read-only, read the active depth-one apply contract, incorporated `origin/develop` commit `4325a08` from PR #60, and drafted two inactive focused specifications. No source or test command ran.

## What this supports or challenges

This supports the conclusion that dynamic content dimensions need a complete immutable content contract and must not change the independent 384-dimensional routing projection. For the ratified first pilot, the smaller safe boundary is stronger: explicit namespace only and no card/catalog/automatic-routing surface at all.

It challenges any assumption that changing the content schema constant alone is sufficient or that the active depth-one apply can satisfy complete pre-write staging. The pilot needs a separate governed experimental path that stages and validates every vector before a later approved serial write; the current active default remains unchanged.

## Validation boundary

This is shaping evidence, not implementation or runtime evidence. Markdown/path/diff checks can establish record completeness and scope hygiene. They cannot prove model compatibility, quality, cache transfer size, host/device RAM, inference output, Turbopuffer behavior for a new schema, or production migration safety.

## Safety observation

No model/dependency download or install, model load, inference, credential access, Buoy runtime/Hugging Face model/Turbopuffer service call, namespace/card/catalog/default read or write, source/test/configuration/dependency/lockfile change, or C4 execution occurred. The only external mutation was the task-required Git push and record-only pull request.

## Residual risk

- Independent review of the record-only PR is required before the shaping ticket can close.
- Candidate and pilot containment are ratified; exact proposed resource/output thresholds remain unratified, so both focused specs remain draft.
- Construction peak, steady host RSS, and peak/steady MPS allocation are unknown and unmeasured by design; measured values must pass the approved future checkpoint before implementation/indexing.
- Exact pilot namespaces, rows, writes, storage, staged-artifact identity, and public experimental selection surface remain unavailable until later local planning and separate approvals.
