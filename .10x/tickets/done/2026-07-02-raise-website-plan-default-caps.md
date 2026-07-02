Status: done
Created: 2026-07-02
Updated: 2026-07-02
Depends-On: None

# Raise Website Plan Default Caps

## Scope

Raise default website crawl planning caps so ordinary `turbo-search plan "https://site"` can cover larger docs websites without requiring manual flags.

In scope:

- Set website default `max_pages` to `3000`.
- Raise website default `max_chunks` proportionally from the prior `250 pages / 10000 chunks` ratio, yielding `120000` chunks.
- Preserve GitHub repository defaults (`5000` files, `100000` chunks) unless separately requested.
- Update tests and docs/knowledge that describe default website caps.

Out of scope:

- Changing live apply behavior.
- Changing GitHub repository source caps.
- Adding a full/smoke profile system.

## Acceptance criteria

- CLI help and runtime default assignment report website defaults as `3000` pages and `120000` chunks.
- GitHub repository defaults remain unchanged.
- Existing tests pass.
- Documentation and site-planning skill records reflect the new defaults.

## Progress and notes

- 2026-07-02: User requested raising default caps to `3000` pages and selected raising chunks as well.
- 2026-07-02: Set website defaults to `3000` pages and `120000` chunks; preserved GitHub repository defaults. Updated tests, README, docs, site-planning knowledge, and site RAG skill reference.

## Blockers

- None.

## Evidence

- `.10x/evidence/2026-07-02-website-default-cap-increase-validation.md`
