Status: open
Created: 2026-07-18
Updated: 2026-07-18
Parent: .10x/tickets/2026-07-18-direct-command-defaults-plan.md
Depends-On: None

# Make Retrieval Live by Default

## Scope

Implement `.10x/specs/default-remote-namespace-routing.md` and the retrieval portion of `.10x/decisions/direct-commands-execute-by-default.md`:

- plain automatic and explicit retrieval execute live;
- `--dry-run` and `--plan` request preview;
- `--live` remains accepted as a compatibility no-op and conflicts with preview flags;
- preserve automatic routing, explicit namespace bypass, credential boundaries, all-or-nothing results, and output truthfulness;
- reverse generated apply handoff commands so live is plain and preview appends `--dry-run`;
- update retrieval/help/README/changelog/migration documentation affected by the default.

## Acceptance criteria

- Parser and validation matrices cover plain/`--live`/`--dry-run`/`--plan`, automatic/explicit namespaces, contradictory flags, whitespace, missing credentials, and existing `--auto-route` compatibility.
- Plain automatic route performs the established catalog read/route/content query; plain explicit route skips catalog/router and queries content.
- Preview behavior remains exact: automatic preview uses read-only list/catalog calls; explicit preview is credential/API/model-free.
- Plain and compatibility `--live` outputs are byte-equivalent after normalizing invocation-only fields; preview remains truthful.
- Any selected namespace failure emits no partial content result; no fallback or changed route ranking occurs.
- Generated `retrieval_commands.live` omits `--live`; `.preview` appends `--dry-run`, with shell quoting preserved.
- No catalog/apply write behavior changes.
- Focused/full Python 3.11/3.13 tests, distributions, evidence, independent review, and hosted checks pass.

## Evidence expectations

Exact fake call traces for automatic/explicit live and preview modes; parser/help snapshots; generated command tokenization; all-or-nothing failures; full/hosted check identities; no-write attestation.

## Blockers

None.

## Explicit exclusions

Apply prompt/mode implementation; catalog command defaults; routing algorithm/card changes; concurrent namespace queries; confidence thresholds; telemetry; release.

## References

- `.10x/tickets/2026-07-18-direct-command-defaults-plan.md`
- `.10x/decisions/direct-commands-execute-by-default.md`
- `.10x/specs/default-remote-namespace-routing.md`
- `.10x/specs/apply-to-retrieval-handoff.md`

## Progress and notes
