Status: draft
Created: 2026-07-20
Updated: 2026-07-20

# Crow-Plus Resource-Verification Checkpoint

## Draft status

This is one exact conservative **proposal**, not an approved budget or operation. It resolves the sequencing ambiguity: every cache, hardware, precision, input, load-time, host/device, batch, observation, and abort value MUST be ratified before bounded measurement begins; the resulting measured values then gate implementation and indexing. The user has not yet approved these exact values.

No executable implementation/evaluation ticket, bootstrap, load, inference, source change, test, or remote operation is authorized while this specification is draft.

## Observed host and immutable candidate inputs

Read-only host inspection on 2026-07-20 observed:

- Apple MacBook Pro `Mac14,9`, Apple M2 Pro, 10 CPU cores and 16 GPU cores;
- 17,179,869,184 bytes (16 GiB) unified memory;
- macOS 26.5.1 (`25F80`);
- 34,890,539,008 bytes (32.494 GiB) available on the data volume at observation time.

C2's immutable snapshot records Crow-Plus revision `96ff525a7aa3bf8bfa90d77337c2b24bd45229af`, 606,681,112 listed weight bytes and 611,525,163 total listed repository bytes. These are source facts, not measured cache or runtime values.

This checkpoint is host-specific. A different model identifier, chip, memory size, OS build, accelerator, dependency lock, or candidate revision requires a new proposed checkpoint and approval.

## Proposed bootstrap checkpoint (separate approval)

- Repository/revision: exactly `Shuu12121/CodeSearch-ModernBERT-Crow-Plus@96ff525a7aa3bf8bfa90d77337c2b24bd45229af`.
- Cache root: exactly `/Users/crlough/Library/Caches/buoy/models/crow-plus-96ff525a7aa3bf8bfa90d77337c2b24bd45229af`; it MUST be absent before bootstrap. No default/global cache fallback or pre-existing blob reuse is allowed.
- Allowlist: the complete regular-file tree of that immutable revision and no other repository/revision. The pre-transfer manifest MUST bind every immutable path and advertised size and MUST total exactly 611,525,163 bytes. Any inability to reproduce that exact manifest stops before transfer.
- Transfer ceiling: 611,525,163 bytes. Cache-root allocated-size ceiling after bootstrap: 805,306,368 bytes (768 MiB), including Hub metadata, lock, and filesystem allocation overhead.
- Free-disk start floor: 5,368,709,120 bytes (5 GiB) on the cache volume; free disk after bootstrap MUST remain at least 4,294,967,296 bytes (4 GiB).
- Dependencies: existing lock only; no install, update, resolver, remote code, credential, or token.
- Observation: record pre/post free bytes, per-file path/size/hash, transferred bytes, and final allocated cache bytes. Abort before the next file if the next advertised size would exceed transfer or free-disk bounds; delete only the dedicated incomplete cache root after recording failure.
- Bootstrap success authorizes no model import, construction, load, or inference.

## Proposed bounded-measurement checkpoint (separate approval after bootstrap)

### Hardware and runtime

- Host MUST exactly match the observed `Mac14,9` / Apple M2 Pro / 17,179,869,184-byte unified-memory / macOS 26.5.1 (`25F80`) contract.
- Accelerator: Apple MPS only; CPU fallback and CUDA are prohibited for this measurement.
- Dependency versions MUST remain `sentence-transformers==5.6.0`, `transformers==5.12.1`, `torch==2.12.1`, and `huggingface-hub==1.20.1`; no install or lock change.
- Construction: create from the exact dedicated cache in float32, then cast once to float16 before inference, matching the currently observed construct-then-`.half()` strategy. Stored/output validation uses float16-compatible values; no quantization or direct-dtype alternate path.
- Environment MUST be set before imports: `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, `HF_HUB_DISABLE_TELEMETRY=1`, `DO_NOT_TRACK=1`, and `HF_HUB_DISABLE_UPDATE_CHECK=1`; `local_files_only=True`, exact revision/cache root, and remote code disabled are mandatory.

### Exact workload and output checks

- One fresh child process, one model construction/load, and exactly two sequential encode calls.
- Embedding batch size: exactly 1. No concurrent encode and no remote/client thread.
- Inputs: one deterministic one-token query and one deterministic document tokenized to exactly 1,024 model tokens under the candidate tokenizer/truncation contract. The exact UTF-8 inputs and token IDs MUST be recorded before approval; token-count mismatch stops before inference.
- Each output MUST be shape `[1,768]`, contain only finite values, and have L2 norm in `[0.999, 1.001]`. The recorded model/module config MUST confirm empty query/document prefixes and CLS pooling.
- No credential lookup, Turbopuffer import/client/read/write, namespace operation, card/catalog/default operation, source/test mutation, or indexing is permitted.

### Exact resource and time bounds

- Start only when system available memory, computed from one recorded `vm_stat` snapshot as `(free + inactive + speculative) * page_size`, is at least 8,589,934,592 bytes (8 GiB).
- Child-process resident-set hard ceiling: 4,294,967,296 bytes (4 GiB).
- MPS current-allocated hard ceiling: 2,147,483,648 bytes (2 GiB).
- MPS driver-allocated hard ceiling: 3,221,225,472 bytes (3 GiB).
- Model construction/load deadline: 120.000 seconds from child start to ready-for-first-encode.
- End-to-end child deadline: 300.000 seconds.
- Sampling interval: at most 100 milliseconds from child start through synchronization after the second encode.
- Qualification headroom: measured peak RSS MUST be at most 3,221,225,472 bytes (3 GiB), measured peak MPS current allocation at most 1,610,612,736 bytes (1.5 GiB), measured peak MPS driver allocation at most 2,415,919,104 bytes (2.25 GiB), load time at most 90.000 seconds, and total time at most 225.000 seconds. Contacting a hard ceiling aborts; exceeding only a qualification threshold completes evidence collection but fails qualification.

### Observation and immediate abort

- An external watchdog MUST sample child RSS and elapsed time at least every 100 ms.
- An in-process monitor MUST sample `torch.mps.current_allocated_memory()` and `torch.mps.driver_allocated_memory()` at least every 100 ms and emit monotonic timestamped observations to the watchdog.
- The watchdog MUST send `SIGKILL` immediately when a sample is greater than or equal to any hard memory ceiling or when either deadline is reached. The child MUST also self-terminate on an in-process hard-bound observation. Any missing sample interval over 200 ms, monitor failure, MPS counter unavailability, process escape, network attempt, cache/revision drift, or output mismatch is a failed measurement.
- Evidence MUST preserve raw samples, exact commands/environment with secrets absent, cache manifest hash, input/token IDs, output hashes/statistics, exit/signal, load and total elapsed values, peaks, and pass/fail against every hard and qualification bound.

## Gate after measurement

A bounded measurement passes only when all identity, offline, workload, output, hard-bound, sampling, and qualification conditions pass. Passing proves compatibility only for this exact host/runtime/workload. It does not approve implementation, larger batch/input/corpus work, staging, indexing, or remote writes.

Measured values MUST be copied into the later implementation checkpoint. Any implementation plan must stay within the measured batch/device/precision path and retain at least the qualification headroom above. Exact local staging evidence must then precede a separate indexing/write approval under `.10x/specs/crow-plus-explicit-namespace-pilot.md`.

A failure requires a revised draft checkpoint and new approval; it MUST NOT be worked around by raising a bound, changing device/precision/batch, falling back to CPU, installing dependencies, or proceeding to implementation/indexing.

## Approval checkpoint

Confirm or correct this exact proposal before any bootstrap or measurement ticket is made executable: dedicated empty cache root; 611,525,163-byte transfer and 768-MiB cache ceilings; 5-GiB/4-GiB disk floors; exact observed Mac/MPS host; float32 construction then float16 inference; batch 1; two exact inputs; 120-second load and 300-second total hard deadlines; 4-GiB RSS, 2-GiB MPS-current, and 3-GiB MPS-driver hard ceilings; 100-ms dual monitoring; stated qualification headroom; immediate abort; and exact 768/finite/norm output checks.

Approval of this checkpoint would authorize record activation only. Bootstrap and bounded measurement would still require their own separate approvals and bounded executable tickets.
