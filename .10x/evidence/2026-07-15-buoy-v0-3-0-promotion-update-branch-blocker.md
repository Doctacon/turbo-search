Status: recorded
Created: 2026-07-15
Updated: 2026-07-15
Relates-To: .10x/tickets/done/2026-07-15-promote-develop-to-main-for-v0-3-0.md

# Buoy v0.3.0 Promotion Update-Branch Blocker

## What was observed

Release preparation was present on exact remote `develop` commit `1441c142dae2f501fd8d7306ab3bf1a9db1532d2`; exact remote `main` was `1fa99431de85b9de435250f273919bf2d247d1fc`. Divergence was one main-only commit and eighteen develop-only commits, with merge base `934aee92e9b6fd6e8e6c103acaf3d2f0f833c254`.

Both protected branches reported strict required checks `Python 3.11`, `Python 3.13`, and `Build distributions`, zero required approvals, administrator enforcement, and force-push/deletion denial. No release PR was open; no `v0.3.0` tag or GitHub Release existed. Project, module, and lock metadata were exactly 0.3.0, and `git diff --check origin/main..origin/develop` passed.

Release PR #22 was opened from `develop` to `main`:

- URL: `https://github.com/Doctacon/buoy-search/pull/22`
- exact pre-update head: `1441c142dae2f501fd8d7306ab3bf1a9db1532d2`
- exact base: `1fa99431de85b9de435250f273919bf2d247d1fc`
- initial state: `OPEN`, `MERGEABLE`, `BEHIND`

Immediately before mutation, remote refs were re-read and matched those exact values. The prescribed request was bound to the observed head:

```text
PUT /repos/Doctacon/buoy-search/pulls/22/update-branch
expected_head_sha=1441c142dae2f501fd8d7306ab3bf1a9db1532d2
```

GitHub rejected it with HTTP 422:

```text
protected branch 'develop' check failed:
  Changes must be made through a pull request. 3 of 3 required status checks are expected.
```

After the rejection, remote `main` and `develop` remained byte-for-byte at their preflight SHAs and divergence remained `1 18`. PR #22 remained open, mergeable, and behind. No update merge commit was created.

## Procedure

1. Read active promotion ticket, branch-protection specification, and release-governance decision.
2. Fetched exact remote refs and inspected divergence, merge base, versions, tag/release conflicts, open PRs, protection API output, diff check, and diff summary.
3. Opened PR #22 with the reviewed v0.3.0 release scope and merge-commit/no-PyPI/no-Turbopuffer boundaries.
4. Re-read exact remote head/base and asserted equality before invoking GitHub's update-branch endpoint with `expected_head_sha`.
5. Stopped on the endpoint rejection as the ticket explicitly requires; did not attempt a direct push, rebase, squash, alternate ancestry mechanism, or main merge.
6. Re-fetched refs and verified no branch mutation occurred.

## What this supports or challenges

This supports all read-only preflight claims and demonstrates that the exact ratified ancestry mechanism is mechanically unavailable under current `develop` protection. It challenges the shaping assumption that GitHub's update-branch endpoint could merge `main` into protected `develop` while that branch requires every change through a PR.

## External-side-effect boundary

The only successful GitHub mutation was opening release PR #22. The update-branch mutation failed before changing `develop`. No main merge, direct push, branch-protection change, tag, environment approval, GitHub Release, PyPI operation, source mutation, credential output, or Turbopuffer operation occurred.

## Limits

This evidence does not authorize or choose an alternate ancestry path. A new ratified mechanism is required before promotion can continue. CI triggered for the open release PR, but passing checks on a behind head cannot satisfy strict freshness or replace the missing ancestry merge.
