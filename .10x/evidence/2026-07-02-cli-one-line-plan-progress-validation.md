Status: recorded
Created: 2026-07-02
Updated: 2026-07-02
Relates-To: .10x/tickets/done/2026-07-02-cli-one-line-plan-progress.md

# CLI One-Line Plan Progress Validation

## What was observed

Implemented default one-line progress support for interactive text-mode `turbo-search crawl` and `turbo-search plan` runs.

Behavior added:

- `OneLineProgress` writes carriage-return updates to stderr and clears the line before final output.
- Progress messages are truncated to terminal width minus one column to avoid soft-wrap creating apparent new lines.
- Progress is enabled by default only when stderr is a TTY and `--json` is not used.
- `--no-progress` disables the indicator explicitly.
- Website crawls emit high-level and per-page/scheduled-URL progress events.
- `plan` emits later local phases for chunking, state diffing, and artifact writing.

## Procedure

Commands run:

```bash
uv run python -m unittest tests.test_crawler tests.test_cli
uv run python -m unittest tests.test_cli
uv run python -m unittest discover -s tests
uv run turbo-search plan --help | rg -n "progress|json"
```

Observed results:

```text
Ran 42 tests in 0.042s
OK

Ran 23 tests in 0.036s
OK

Ran 150 tests in 2.568s
OK

15:                         [--overlap-sentences OVERLAP_SENTENCES] [--json]
16:                         [--no-progress]
84:  --json                Print JSON output. Text summary is used by default.
85:  --no-progress         Disable the default one-line interactive progress
```

## What this supports or challenges

Supports:

- The progress implementation is covered by unit tests for line reuse, JSON suppression, and crawl progress events.
- Existing test coverage still passes.
- The new `--no-progress` flag is visible in `plan --help`.

Limits:

- The validation did not run a live long crawl in an interactive terminal, so terminal rendering was verified via a TTY-like test stream rather than a real terminal session.
- The progress indicator is intentionally simple and does not estimate ETA.
