Status: recorded
Created: 2026-07-16
Updated: 2026-07-16
Target: tag object `21a8d122151711a863dfb63d356baebbddca8d45`, release run `29538957482`, GitHub Release `355388511`, records commits `a8715f5` and `44685a4`
Verdict: pass

# Buoy v0.3.0 GitHub Release Review

## Findings

Two independent reviewers verified the hosted release and corrected one record-only chronology blocker.

- Remote `v0.3.0` is an annotated tag object peeling to exact reviewed main `595d157177bd032c20cf6e6c0112ee6b43212a88`.
- Exact-main CI and the single tag-triggered release run succeeded.
- Hosted timestamps prove validation/build completed before the protected environment waited and was approved; attestation and Release/assets mutation followed approval.
- Release `355388511` is non-draft/non-prerelease, targets the expected tag/main, has generated notes, and contains exactly the wheel and sdist.
- Fresh downloads match recorded sizes and SHA-256 digests. Package metadata/content, entry points, RECORD, archive safety, and selected source equality to the tag passed.
- Public attestations bind both asset digests to SLSA provenance v1, the expected repository/workflow/tag/run, GitHub-hosted execution, and exact release commit. Stored strict verification passed; later retries encountered transient GitHub 503 responses without contradictory evidence.
- v0.2.0/v0.2.1 history remains immutable; v0.2.0 still has no Release; PyPI remains absent; main/source/workflow surfaces show no unauthorized branch, source, registry, or Turbopuffer mutation.
- Commit `44685a4` corrected evidence chronology to July 16 and repaired all references without changing substantive release data.

## Verdict

Pass. The hosted publication child is closure-ready. The parent remains open for the separately owned post-release changelog finalization.

## Residual risk

Historical approval-count and no-Turbopuffer observations rely on contemporaneous evidence plus inspected workflow boundaries rather than a replayable external audit log. GitHub attestation APIs can be transiently unavailable, though stored strict verification and direct signed bundles support the release.
