Status: active
Created: 2026-07-14
Updated: 2026-07-18

# Apply-to-Retrieval Handoff

## Purpose and scope

Make apply preflight sufficient for an operator to review the selected plan and make successful apply hand directly to correctly configured retrieval without reconstructing settings.

## Decision-complete apply output

- Apply preflight and approved-apply summaries MUST identify the selected `plan_path`, source `base_url`, `plan_id`, `artifact_hash`, namespace, region, embedding model, embedding precision, and whether local state considers this a first apply.
- Human text MUST show rows to upsert, unchanged rows, embeddings to generate, stale rows, already-retained stale rows, and the exact delete-versus-retain intent.
- When `--delete-stale` is absent, text MUST say how many stale rows will be retained. When present, it MUST say how many stale rows will be deleted. It MUST not require the operator to infer intent from multiple counters.
- Explicit `apply --dry-run` and the pre-prompt phase of interactive plain apply remain local-only: loading non-secret region configuration is allowed, but credentials, embeddings, and Turbopuffer calls remain prohibited.

## Retrieval commands

- Apply preflight and successful approved apply MUST add a `retrieval_commands` object to JSON with `preview` and `live` strings.
- Both commands MUST use the actual region, namespace, embedding model, and embedding precision selected for apply.
- Commands MUST use the primary `buoy` executable and a shell-quoted `<query>` placeholder.
- `live` MUST use plain live-by-default retrieval without `--live`; `preview` MUST be otherwise identical and append `--dry-run`.
- Every dynamic value MUST be shell-quoted using standard POSIX shell joining rather than interpolated unsafely.
- Human preflight MUST label the commands as usable after a successful apply. Successful approved apply MUST label them as the next retrieval step.
- Failed apply MUST emit no success handoff command.

Example shape:

```text
buoy retrieve '<query>' --namespace site-example-com-v1 --region gcp-us-central1 --embedding-model BAAI/bge-small-en-v1.5 --embedding-precision float32
```

## Compatibility

- Existing JSON field names and object schema MUST remain compatible. The `retrieval_commands.preview` and `.live` string values intentionally change to the ratified preview/live defaults; `region` and `retrieval_commands` remain additive relative to older consumers.
- Existing plan verification, automatic latest-plan selection, namespace resolution, apply safety, deletion behavior, timing, state commit, and cleanup remain unchanged.
- The command MUST preserve pre-rebrand remote namespace identities exactly.

## Acceptance scenarios

### Automatic plan preflight

Given multiple local plans and `apply --dry-run` or interactive plain apply with no `--plan`, when apply selects the latest valid plan, then text identifies its exact path/source/artifact and all decision counters plus explicit stale intent.

### Approved apply

Given a successful approved apply, when output is rendered, then its preview/live commands parse as shell tokens and contain the exact applied namespace, runtime region, verified plan model, and verified precision.

### Unsafe values

Given configuration values containing shell metacharacters or spaces, when commands are produced, then shell parsing recovers each original value as one argument and does not execute interpolation.

### JSON compatibility

Given existing automation fields, when preflight or approved apply emits JSON, then they remain present with the same values and the new region/command fields are additive.

## Explicit exclusions

Automatic query text, automatic command execution by apply, namespace discovery, multi-namespace command generation, per-namespace metadata persistence, and plan-command retrieval output before apply review.
