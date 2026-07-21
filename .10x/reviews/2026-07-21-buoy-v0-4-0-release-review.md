Status: recorded
Created: 2026-07-21
Updated: 2026-07-21
Target: local post-release record head `07b3afe` and hosted v0.4.0 release state
Verdict: pass

# Buoy v0.4.0 Release Review

## Findings

Independent review confirmed:

- PR #85 squash commit `c49dc0582bf3f06a16eafdcca0707d1e64e1c58d` has exact reviewed develop tree `7de04d70c442de5fb5051cd6ceafda5b4c39c285`, and the user explicitly accepted that release topology;
- exact-main CI run `29851219914` passed;
- post-release sync commit `644867f9ef8a26b137e0aabf69cb0cf4f66601a3` has exact parents develop `e702aee115a57b5057b8d5d5917b260e6417c74d` and released main `c49dc0582bf3f06a16eafdcca0707d1e64e1c58d`, with the same exact tree;
- annotated tag object `1a527da870a1b6d8acedee8b93dbf85d24dac8b9` peels to exact released main;
- unique release run `29851435791`, validation job `88705013738`, protected deployment `5542522847`, and publication job `88705440328` have coherent success chronology;
- Release `357504706`, wheel/sdist identities, sizes, API/downloaded SHA-256 digests, and SLSA provenance claims match recorded evidence;
- PyPI returns HTTP 404 for `buoy-search` 0.4.0;
- promotion/release tickets are done, dependencies resolve, changelog finalization is open/unblocked, and post-release records change no product source.

## Verdict

Pass. The existing branch may integrate to `develop` with a merge commit only. Squash or rebase would discard released-main ancestry and invalidate the repair.

## Residual risk

The tag and Release are immutable external state. The open changelog finalization must use the authoritative publication date and links without modifying released main/tag contents. Upstream pinned Actions emitted Node.js forced-runtime warnings but all release jobs and provenance succeeded.
