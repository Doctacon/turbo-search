Status: done
Created: 2026-06-28
Updated: 2026-07-19
Depends-On: .10x/research/2026-06-28-expanded-validation-ranking-hypotheses.md, .10x/tickets/done/2026-06-28-cross-corpus-validation-basket.md

# Repo Searchable Path and Symbol Metadata

## Scope

Test whether repository indexing improves when generated code pages include searchable path, file-stem, and symbol metadata/breadcrumbs.

This owns the local implementation and validation slice for expanded-validation hypotheses H4 and H5:

- H4: exact path/title/identifier tokens should become searchable text;
- H5: symbol breadcrumbs should be added to code chunks.

## Acceptance criteria

- Add an explicit opt-in plan/crawl option so existing repo planning defaults remain unchanged.
- Include searchable metadata only in generated repository Markdown, not website crawls.
- Keep local-only plan behavior: no credentials, embeddings, turbopuffer calls, writes, deletes, or namespace mutation during local validation.
- Validate with unit tests and local plan/preflight artifacts.
- Do not promote as a default or live-apply new namespaces without separate approval.

## Explicit exclusions

- No Tree-sitter dependency.
- No proprietary model APIs.
- No live apply/reindex in this slice unless separately approved.
- No stale deletion or namespace deletion.

## Blockers

None. Local validation completed first, and the later live evaluation was separately approved.

## References

- `.10x/research/2026-06-28-expanded-validation-ranking-hypotheses.md`
- `.10x/tickets/cancelled/2026-06-28-repo-oversize-source-indexing.md`

## Progress and notes

- 2026-06-28: Activated after user requested execution of the next three recommended hypotheses.
- 2026-06-28: Added opt-in `--repo-search-metadata`, which includes path tokens, file stem, Python symbol names/tokens, and per-line-window symbol breadcrumbs in generated repository code pages. Local pytest/Typer plans and preflights passed without live writes. Evidence: `.10x/evidence/2026-06-28-repo-oversize-metadata-local-validation.md`.
- 2026-06-28: After explicit user approval for writes/evals to new namespaces, live-applied metadata-only ablations for pytest/Typer. Metadata-only improved both existing seed datasets (`pytest 84.742 -> 85.971`, `Typer 59.423 -> 62.062`) without changing the file-size cap. Metadata-only is now the strongest promotion candidate from this slice, pending validation on the older repo basket. Evidence: `.10x/evidence/2026-06-28-repo-oversize-metadata-live-eval.md`.
- 2026-07-19: Closure review mapped every criterion to the local implementation/plan evidence and confirmed the later live work had separate approval. The dependent older-basket validation subsequently rejected default promotion, without invalidating this ticket's completed opt-in slice. Review: `.10x/reviews/2026-07-19-stale-ticket-status-closure-review.md`.

## Closure mapping

- Explicit opt-in and unchanged defaults: `--repo-search-metadata`, `repo_search_metadata=false`, recorded in `.10x/evidence/2026-06-28-repo-oversize-metadata-local-validation.md`.
- Repository-only generated metadata: local evidence records repository Markdown path/stem/Python symbol text; the option is on the GitHub repo planning path.
- Local-only safety and plan/preflight validation: local evidence records no credentials, embeddings, remote calls, writes, deletes, or state mutation.
- Unit/full tests: 34 focused and 142 full tests recorded in the local evidence.
- No same-slice default promotion: defaults stayed unchanged; later separately approved live evidence remained experimental, and `.10x/evidence/2026-06-28-repo-search-metadata-cross-repo-validation.md` rejected universal promotion.

## Retrospective

Searchable metadata improved pytest and Typer but later regressed turbo-search and Requests. The durable lesson already recorded by the workstream is to keep metadata opt-in and test placement/scoring across the full basket rather than infer universal safety from two corpora.
