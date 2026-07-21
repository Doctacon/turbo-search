Status: active
Created: 2026-07-21
Updated: 2026-07-21

# Buoy Product and Repository Identity

## Context

The GitHub repository was intentionally renamed from `Doctacon/buoy-search` to `Doctacon/buoy` while Buoy v0.4.1 release preparation was in progress. GitHub redirects the old URL, but release readiness and provenance checks intentionally bind exact repository identity; silently relying on redirects would make future source/provenance authority ambiguous.

The package/distribution identity is separate from repository identity. Published v0.4.0 provenance and historical source/evidence records were created under `Doctacon/buoy-search` and are immutable.

## Decision

- Product remains **Buoy** with tagline **Search that stays anchored to the source.**, distribution `buoy-search`, Python package `buoy_search`, primary CLI `buoy`, Apache-2.0 license, and existing visual identity.
- Canonical current GitHub repository is `Doctacon/buoy`.
- Future readiness, API operations, release URLs, package project URLs, and provenance beginning with v0.4.1 MUST use `Doctacon/buoy`.
- The exact v0.4.0 legacy no-op exception MUST continue requiring its immutable historical provenance repository `Doctacon/buoy-search`; repository rename MUST NOT rewrite or generalize that exception.
- Historical evidence URLs, immutable experiment/source pins, archived fixtures, and records describing observations made under `Doctacon/buoy-search` remain historical unless an active runtime/documentation consumer requires the current canonical URL.
- Distribution/package/import/CLI names do not change because of the repository rename.
- Active code, tests, changelog comparison/release links, documentation, and release contracts MUST distinguish current repository identity from immutable legacy provenance explicitly rather than through a single overloaded constant.

This decision supersedes `.10x/decisions/superseded/buoy-product-identity-and-compatibility-v0-3.md` after its completed 0.3/0.4 compatibility schedule. Historical compatibility records remain authoritative for what those releases did, not for current repository identity.

## Alternatives considered

### Keep old identity through redirects

Rejected. GitHub runtime/provenance reports the canonical repository, and exact readiness checks must not depend on redirect behavior.

### Rename the distribution/package

Rejected. The user authorized a repository rename, not a package/API rebrand; changing published identities would create unnecessary compatibility cost.

### Rewrite all historical records

Rejected. Historical provenance and source observations must retain the identity under which they were produced.

## Consequences

Release automation needs a current-repository constant and a separately pinned v0.4 legacy provenance repository. Active links become canonical under `Doctacon/buoy`; old links may continue redirecting but are not future authority. v0.4.1 promotion remains blocked until this reconciliation is reviewed and integrated.
