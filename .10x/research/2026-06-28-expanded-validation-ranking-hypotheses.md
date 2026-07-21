Status: done
Created: 2026-06-28
Updated: 2026-06-28

# Expanded Validation Ranking Hypotheses

## Question

What are 10 additional testable hypotheses for improving `turbo-search` repository and website retrieval after expanding validation to pytest, Typer repo, Ruff docs, and Typer docs?

## Sources and methods

This hypothesis set is based on current project evidence and records:

- `.10x/evidence/2026-06-28-cross-corpus-live-retrieval-evals.md`
- `.10x/evidence/2026-06-28-cross-corpus-live-apply.md`
- `.10x/evidence/2026-06-28-cross-corpus-seed-eval-datasets.md`
- `.10x/evidence/2026-06-28-repo-adaptive-aggregation-validation.md`
- `.10x/evidence/2026-06-28-repo-role-diversification-validation.md`
- `.10x/evidence/2026-06-28-website-ranking-evidence-hardening.md`
- `.10x/knowledge/repo-search-ranking-defaults.md`
- `.10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md`
- `.10x/tickets/done/2026-06-28-website-capped-aggregation-default-review.md`

Current default baselines:

```text
repo/general = file / repo_code / pool100 / adaptive_sum_3
site-* = page / none / pool20 / max
```

Key observed constraints:

- Repo `adaptive_sum_3` generalizes better than strict `max` on the expanded repo basket.
- Full repo `capped_sum_3` still regresses at least one repo and remains opt-in.
- Website capped aggregation improved Ruff and Typer docs but is blocked from default promotion by prior Pi-site regression evidence.
- Current GitHub repo planning skips files over 50 KiB, including important central files in pytest and Typer.
- Seed labels remain assistant-drafted and are useful for calibration, not human-approved ground truth.

## Ten additional hypotheses

### H1: Oversized text files should be chunked instead of skipped

**Hypothesis:** Repository search quality, especially on Typer and pytest, will improve if large text/code files above 50 KiB are line-window chunked instead of excluded.

**Rationale:** The expanded basket found skipped authority files such as `typer/main.py`, `typer/params.py`, `src/_pytest/fixtures.py`, and `src/_pytest/python.py`. Labels had to avoid those files, which weakens validation.

**Experiment:** Local-only plan comparison on current repo basket with a higher cap or oversize line-window chunking. Measure added files/chunks and then, after approval, live eval against a new namespace.

**Keep criterion:** Improved repo score on Typer/pytest without material regressions on existing repo validation and without admitting binary/vendor noise.

### H2: Oversized source files need stricter role/path controls than normal files

**Hypothesis:** Adding oversized source files will improve recall only if large docs/generated/examples are still excluded or downweighted.

**Rationale:** Raising the file-size cap globally could pull in changelogs, generated docs, vendored assets, or large example suites that hurt precision.

**Experiment:** Compare three local plans: global higher cap, source-extension-only higher cap, and explicit oversize allowlist for source directories. Validate row-count growth and selected file roles before any apply.

**Keep criterion:** Central source files are included while large generated/vendor/process artifacts remain excluded.

### H3: Repo queries need a stronger implementation-vs-docs-vs-tests classifier

**Hypothesis:** A query-intent classifier that chooses implementation, docs, tests, or mixed role priors will improve repo precision more than one universal `repo_code` prior.

**Rationale:** Current `repo_code` is conservative. Some eval queries ask for implementation files; others legitimately expect docs/tests companions. Typer and pytest contain many docs/tutorial/test files that can either help or distract.

**Experiment:** Add a scoring-only classifier over query terms such as “implement”, “where is”, “test”, “document”, “tutorial”, “usage”, “example”, “fixture”, “CLI”. Adjust role multipliers only, then compare across all repo datasets.

**Keep criterion:** No repo target regresses under the no-regression policy; docs/test-oriented cases improve or stay stable.

### H4: Exact path/title/identifier tokens should become searchable text, not only scoring signals

**Hypothesis:** Indexing normalized path, file stem, module path, and split identifier tokens into searchable text will improve BM25 candidate recall for code queries.

**Rationale:** Current path/symbol boosts only help if the right candidate is already retrieved. Exact terms like `caplog`, `pytester`, `TyperGroup`, `CompletionItem`, or `line-too-long` may need better first-stage lexical recall.

**Experiment:** Reindex one repo namespace with generated metadata text prepended or appended to chunks, without schema changes. Compare candidate recall and final metrics.

**Keep criterion:** Recall@10/NDCG improve without a precision drop from path-token spam.

### H5: Symbol breadcrumbs should be added to every code chunk

**Hypothesis:** Adding function/class/module breadcrumbs to chunk text and section paths will improve code-search NDCG and MRR.

**Rationale:** Current chunking can split implementation bodies away from their class/function names. Symbol breadcrumbs give both dense and lexical retrieval the identifier context users ask for.

**Experiment:** Add a lightweight Python symbol scanner for `def`, `class`, and module path breadcrumbs; no Tree-sitter required. Reindex a new namespace and compare against current repo default.

**Keep criterion:** Improves implementation cases without hurting docs/test companion cases.

### H6: Site `adaptive_sum_3` may resolve the capped-vs-max tradeoff better than full capped aggregation

**Hypothesis:** A website-specific adaptive aggregation, analogous to repo `adaptive_sum_3`, will capture Ruff/Typer capped gains while avoiding the Pi-site capped regression.

**Rationale:** Full `capped_sum_3` improves new sites but previously regressed Pi-site score slightly. A smaller close-evidence bonus may be safer than full capped summation.

**Experiment:** Add or simulate `page/adaptive_sum_3/pool20` across turbopuffer, SQLMesh, Pi, Ruff docs, and Typer docs.

**Keep criterion:** Beats or matches page/max on every site under the no-regression policy.

### H7: Website page representatives should choose the best answer section, not just the best grouped chunk

**Hypothesis:** Page-level ranking is right, but representative hit selection can improve user-visible citations and section-level relevance by selecting a section that best matches the query after page scoring.

**Rationale:** Page-level judgments hide section quality. The returned page may be correct while the shown chunk is less helpful, especially on long docs pages.

**Experiment:** Keep page scoring fixed but compare representative selection strategies: best RRF chunk, best lexical overlap chunk, best heading/title match chunk, and best combined local score.

**Keep criterion:** URL-level metrics do not regress; manual/top-hit inspection shows better snippets and section paths.

### H8: Site docs need heading/title/slug token expansion

**Hypothesis:** Adding page title, slug segments, headings, and normalized rule/code identifiers to every website chunk will improve docs retrieval, especially for rule/reference pages.

**Rationale:** Ruff rule pages and Typer tutorial pages are title/slug-heavy. Queries often mention concepts that appear in headings or URLs but not repeatedly in body text.

**Experiment:** Rebuild one site namespace with title/slug/heading metadata text in chunks. Compare current defaults and raw chunk retrieval.

**Keep criterion:** Improves Ruff/Typer docs without hurting existing turbopuffer/SQLMesh/Pi site evals.

### H9: Candidate depth and ranking pool should be namespace-class tuned after expansion

**Hypothesis:** Current `candidates=200`, repo `pool100`, and site `pool20` are safe but not necessarily optimal across larger repos/sites.

**Rationale:** Typer repo low score may reflect first-stage recall or pool depth, while site capped gains might vary with pool size. Earlier experiments were smaller and may not generalize.

**Experiment:** Config-only grid across candidates `{100, 200, 400}` and pools `{20, 50, 100, 150}` for repos/sites, using current and candidate aggregations.

**Keep criterion:** Any default change must satisfy no-regression across old and new targets and should prefer smaller pools when metrics are tied.

### H10: A tiny feature-based ranker may beat hand-tuned multipliers after labels expand

**Hypothesis:** A transparent logistic/linear ranker over existing retrieval features can improve ranking more safely than more hand-coded multipliers once the basket has enough labels.

**Rationale:** Current `repo_code` logic is hand-tuned. The expanded basket now has more cases, and future human review could support learning weights for features like RRF rank, BM25/vector ranks, path role, filename match, symbol match, duplicate count, and page/file aggregation counts.

**Experiment:** Offline only at first: export candidate features and judgments from live eval artifacts, fit a simple linear/logistic model with leave-one-repo/site-out validation, then compare simulated rankings before implementing.

**Keep criterion:** Improves leave-one-corpus-out metrics with interpretable weights and no target-specific overfit.

## Recommended next three

1. **H1/H2 oversize source indexing** because it fixes a real validation blind spot before optimizing around missing authority files.
2. **H6 website adaptive aggregation** because capped aggregation is promising but blocked by no-regression policy.
3. **H4/H5 searchable path/symbol metadata** because current boosts only help after retrieval, while metadata text can improve first-stage recall.

## Limits

These are hypotheses, not acceptance criteria or default decisions. Each requires isolated evidence before implementation or promotion. Live apply/reindex/retrieval still requires explicit approval, and no namespace deletion or stale deletion is implied.
