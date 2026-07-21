Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Relates-To: .10x/tickets/done/2026-07-21-bridge-v0-4-squash-topology-once.md

# v0.4 Squash Topology Bridge

## Observation

The sole authorized content-neutral bridge completed through protected PR #97.

- pre-bridge develop `D`: `7ecd34172b4f7729c27ef3de12d36c6e3ef792ee`
- exact v0.4 main: `c49dc0582bf3f06a16eafdcca0707d1e64e1c58d`
- bridge commit: `691d28e543659a2ef11acc47e66f5f8993e8c64b`, ordered parents `[D, main]`
- protected integration merge: `5ce5c11553ac69a997b25567023b4765f5e780c8`, ordered parents `[D, bridge]`
- all four commits' relevant develop/bridge/integration tree: `8229b5647f43854760c3a339e756ddd96f5916df`

PR #97 had zero changed files/additions/deletions. Strict CI run `29875124848` passed Python 3.11, Python 3.13, and Build distributions. Integration used merge commit, not squash/rebase.

## Verification

After integration:

- exact main and bridge are ancestors of develop;
- develop tree equals pre-bridge `D` with zero diff;
- main remained exact v0.4 commit;
- no v0.4.1 tag/Release existed;
- branch protections matched pre-bridge readback;
- PR #93 refreshed to exact develop, became mergeable, constructed a prospective merge result, and started release readiness.

The first readiness run exposed a separate job-name/protection-context mismatch; it did not challenge bridge correctness and no release occurred.

## Limits

No source/version/changelog/workflow/product/protection/provider/release content changed in the bridge. The exception is consumed and MUST NOT recur.
