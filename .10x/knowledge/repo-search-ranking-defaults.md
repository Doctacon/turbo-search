Status: active
Created: 2026-06-28
Updated: 2026-06-28

# Repo Search Ranking Defaults

`turbo-search` retrieval defaults to hybrid ANN + BM25 + RRF followed by repository-aware final ranking:

```text
candidates = 200
ranking_mode = file
ranking_profile = repo_code
ranking_pool = 100
```

`ranking_mode=file` groups GitHub repository hits by `repo_path` so duplicate chunks from the same file do not consume the top-k result slots. The representative chunk is the earliest fused hit for that file.

`ranking_profile=repo_code` is a gentle post-fusion path prior for repository rows only:

- process/project-agent paths such as `.pi/`, `.10x/`, `.loom/`, `.claude/`, and `.cursor/` are demoted strongly;
- `docs/`, README/CHANGELOG, and other Markdown files are demoted gently;
- source/test/config files are left at neutral weight.

Generic website rows without `repo_path` remain chunk-keyed and are not collapsed by file ranking.

Use URL/page-level grouping for website experiments with:

```bash
turbo-search retrieve "..." --ranking-mode page --ranking-profile none
```

`ranking_mode=page` groups website chunks by canonical URL while repository rows still group by `repo_path`. Page mode is experimental and not the default as of 2026-06-28. Use raw chunk order for debugging with:

```bash
turbo-search retrieve "..." --ranking-mode chunk --ranking-profile none
```

The repo default was promoted after live retrieval-only experiments improved the `turbo-search` seed repo eval from `Precision@5 = 0.300` and `repo_search_score = 59.967` to `Precision@5 = 0.500` and `repo_search_score = 87.251` on namespace `github-doctacon-turbo-search-v1`.

Evidence: `.10x/evidence/2026-06-28-repo-search-file-ranking-promotion-validation.md`.
