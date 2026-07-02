Status: active
Created: 2026-07-02
Updated: 2026-07-02

# Turbo Search Site Planning Workflow

For a new public website, the shortest local-only planning command is:

```bash
uv run turbo-search plan "https://example.com/"
```

From 2026-07-02 onward, interactive text-mode `plan` and `crawl` runs show a default one-line progress indicator on stderr. It updates in place with crawl/plan phases so long crawls do not feel stalled and do not spam terminal output. The renderer truncates messages to terminal width so long URLs do not soft-wrap into apparent new lines.

Default website planning caps are `3000` pages and `120000` chunks. Use lower caps for smoke tests or when you only need a subset.

Progress behavior:

- enabled by default only for interactive terminals;
- suppressed automatically for `--json`;
- suppressed automatically when stderr is not a TTY, such as redirected logs or CI;
- disabled explicitly with `--no-progress`.

Useful bounded planning variants:

```bash
uv run turbo-search plan "https://example.com/" --max-pages 10 --max-chunks 200
uv run turbo-search plan "https://example.com/" --include-path "/docs/**" --max-pages 100
uv run turbo-search plan "https://example.com/" --crawl-strategy sitemap
```

After inspecting the plan, preflight with:

```bash
uv run turbo-search apply
```

Only use `uv run turbo-search apply --approve` after explicit approval for live turbopuffer writes.
