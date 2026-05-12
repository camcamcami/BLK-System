# BLK-SYSTEM-086 Hostile Review

**Date:** 2026-05-12T16:53:21+10:00
**Sprint:** BLK-SYSTEM-086 — BEO Publication Pilot Approval Decision
**Status:** PASS after remediation

## Scope

Hostile review covered:

```text
python/beo_publication_pilot_approval_decision.py
python/test_beo_publication_pilot_approval_decision.py
docs/BLK-086_beo-publication-pilot-approval-decision.md
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/test_active_doctrine_review_gates.py
```

The review target was exact approval-decision capture for the canonical BLK-085 request only. The review explicitly did not authorize or perform publication pilot execution, runtime `PUBLISHED` BEO output, signer/storage/ledger/rollback side effects, RTM generation, protected-body reads, target-repo scan or mutation, source/Git mutation, BEB dispatch, BEO closeout execution, BLK-test/Codex/BLK-pipe runtime, package/network/model/browser/cyber tooling, or production isolation claims.

## Round 1 Finding — Accepted Authority-Laundering Package IDs

A bounded adversarial probe mutated `approval_decision_package_id` with compact/camel/acronym authority strings. The pre-remediation validator accepted the following malicious or over-broad IDs:

```text
beoPubApproved
ABPApproved
approvedForRuntimeExecution
liveExecutionAuthorized
runtimeApproval
publicationGreenlit
publicationAllowed
publicationPermitted
allowedForPublication
permittedForPublication
claimsAreAuthorized
isAuthorized
publicationAuthorityAllowed
publicationAuthorityPermitted
blkTestPassApproval
codexApproval
approvalInherited
SignatureGenerated
CryptographicSigning
RTMID
RTPBEO
```

The same review also found that arbitrary fresh package IDs such as `BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-999` were accepted. That weakened the exact-decision boundary and left a token-smuggling surface in a caller-controlled identity field.

**Severity:** Blocker.

## Remediation

Remediation added RED/GREEN coverage and implementation hardening:

1. Added regression probes for compact/camel/acronym/allcaps/percent-encoded authority markers.
2. Added exact `approval_decision_package_id` enforcement:

```text
BEO-PUBLICATION-PILOT-APPROVAL-DECISION-086-001
```

3. Expanded forbidden normalized marker coverage for:

```text
beoPubApproved
ABPApproved
RTPBEO
RTMID
approvedForRuntimeExecution
liveExecutionAuthorized
runtimeApproval
publicationGreenlit
publicationAllowed
publicationPermitted
publicationAuthorityAllowed
publicationAuthorityPermitted
allowedForPublication
permittedForPublication
claimsAreAuthorized
isAuthorized
blkPipeSuccess
blkTestPassApproval
codexApproval
approvalInherited
SignatureGenerated
CryptographicSigning
```

4. Updated BLK-086 doctrine and BLK-077/079 current-state text to pin exact approval-decision package identity while preserving that the next movement is a separate exact execution sprint.
5. Restored historical BLK-084/085 roadmap marker compatibility required by the persistent active doctrine gates.

## RED Evidence

The new regression tests failed before implementation remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v \
  python.test_beo_publication_pilot_approval_decision.BeoPublicationPilotApprovalDecisionTest.test_rejects_secret_adjacent_authority_source_git_and_tooling_laundering \
  python.test_beo_publication_pilot_approval_decision.BeoPublicationPilotApprovalDecisionTest.test_requires_exact_approval_decision_package_id

FAILED (failures=22)
```

The failures showed accepted authority-laundering IDs and accepted arbitrary fresh package IDs.

## GREEN Evidence

After remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_beo_publication_pilot_approval_decision

Ran 8 tests

OK
```

Focused active-doctrine/current-state verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v \
  python.test_beo_publication_pilot_approval_decision \
  python.test_blk_current_state_authority_index \
  python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint086_beo_publication_pilot_approval_decision_captures_exact_request_without_execution \
  python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint086_completion_preserves_approval_decision_not_execution_boundary

Ran 22 tests

OK
```

Full active doctrine gate verification after doc marker remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest -v python.test_active_doctrine_review_gates

Ran 108 tests

OK
```

## Final Independent Hostile Review

A final bounded independent hostile review after remediation reported:

```text
Verdict: PASS
Focused BLK-086 tests: 8/8 OK
Active doctrine gates: 108/108 OK
Hostile probe: 27/27 mutated approval_decision_package_id values rejected
Files created/modified by reviewer: none
Blockers/issues: none
```

The final probe rejected arbitrary package IDs plus authority/secret variants including `beoPubApproved`, `ABPApproved`, `RTPBEO`, `RTMID`, `approvedForRuntimeExecution`, `liveExecutionAuthorized`, `runtimeApproval`, `publicationGreenlit`, `publicationAllowed`, `publicationPermitted`, `publicationAuthorityAllowed`, `publicationAuthorityPermitted`, `allowedForPublication`, `permittedForPublication`, `claimsAreAuthorized`, `isAuthorized`, `blkTestPassApproval`, `codexApproval`, `approvalInherited`, `SignatureGenerated`, `CryptographicSigning`, percent variants, `docs%252Factive`, `APIKEY`, and `PRIVATEKEY`.

## Final Verdict

PASS after remediation.

BLK-SYSTEM-086 captures only the exact approval decision for the canonical BLK-085 request. It does not execute publication pilot work and does not grant adjacent authorities.
