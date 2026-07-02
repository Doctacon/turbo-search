Status: recorded
Created: 2026-07-02
Updated: 2026-07-02
Relates-To: .10x/tickets/done/2026-07-02-raise-website-plan-default-caps.md

# Website Default Cap Increase Validation

## What was observed

Website planning defaults were raised from:

```text
max_pages: 250
max_chunks: 10000
```

to:

```text
max_pages: 3000
max_chunks: 120000
```

GitHub repository defaults remain unchanged:

```text
max_files: 5000
max_chunks: 100000
max_file_bytes: 51200
```

## Procedure

Commands run:

```bash
uv run python -m unittest tests.test_crawler tests.test_cli
uv run python -m unittest discover -s tests
uv run turbo-search plan --help | rg -n "websites=|max-pages|max-chunks"
```

Observed output:

```text
Ran 43 tests in 0.040s
OK

Ran 150 tests in 2.504s
OK

3:                         [--max-pages MAX_PAGES] [--max-chunks MAX_CHUNKS]
39:  --max-pages MAX_PAGES
41:                        websites=3000, GitHub repos=5000.
42:  --max-chunks MAX_CHUNKS
43:                        Maximum chunks to generate. Defaults: websites=120000,
```

## What this supports or challenges

Supports:

- CLI help reflects the new website defaults.
- Unit tests confirm website defaults changed and GitHub repo defaults remain unchanged.
- Full test suite still passes.

Limits:

- No live crawl was run as part of this validation.
- Larger defaults increase local crawl duration and requests to public websites; robots.txt, host restriction, concurrency, and delay defaults still apply.
