# BLK-SYSTEM-075 Hostile Review — Kuronode Lifecycle Cleanup Patch Approval Envelope

**Status:** Complete — blockers found and remediated
**Date:** 2026-05-11
**Scope:** `python/kuronode_lifecycle_cleanup_patch_approval_envelope.py`, `python/test_kuronode_lifecycle_cleanup_patch_approval_envelope.py`, `docs/BLK-076_kuronode-lifecycle-cleanup-patch-approval-envelope-boundary.md`, and the BLK-076 active doctrine gate.

---

## Review Summary

Hostile review found authority-boundary blockers in the initial BLK-SYSTEM-075 implementation. The blockers were remediated with additional regression tests and stricter validation.

BLK-SYSTEM-075 remains a review-only exact-target approval envelope. It does not grant patch approval and does not execute any patch.

---

## Blockers Found

### BLOCKER 1 — Recomputed forged upstream remediation packets accepted

Initial validation recomputed `packet_hash` from the submitted upstream packet body but did not enforce the complete BLK-SYSTEM-074 packet schema or nested identity fields. A forged packet could add `codexApproval`, remove/alter `finding`, alter retired IDs, alter future runtime policy, alter obligations, or alter denied authorities and pass after recomputing its own hash.

**Remediation:** Added strict upstream packet schema validation, exact scalar checks, exact nested `finding`, `retired_runtime_ids`, `future_runtime_id_policy`, `remediation_obligations`, `remediation_guidance`, `required_future_patch_boundary`, and exact upstream denied-authority checks.

### BLOCKER 2 — Upstream false side-effect validation incomplete

Initial validation checked only a subset of BLK-SYSTEM-074 packet false flags. Several prohibited upstream side effects such as `public_ledger_mutated`, `runtime_published_beo_output_emitted`, `active_vault_hash_comparison_performed`, `coverage_claim_promoted`, and `fresh_runtime_id_allocated` could pass if truthy after recomputing `packet_hash`.

**Remediation:** Imported and enforced the complete BLK-SYSTEM-074 `PACKET_FALSE_SIDE_EFFECT_FLAGS` set. Every upstream false flag must exist and be exactly `False`.

### BLOCKER 3 — Compact/camel/acronym authority laundering variants accepted

Initial request laundering checks missed compact/camel/acronym variants such as `SignatureGenerated`, `CryptographicSigning`, `KEYMATERIAL`, `SIGNERKEYMATERIAL`, `beoPubApproved`, `ABPApproved`, `RTPBEO`, `publishBEO`, `blkPipeSuccess`, and `blkTestPassApproval`.

**Remediation:** Added compact-token normalization and denylist checks, with regression tests for whole-field and embedded variants.

### BLOCKER 4 — Active doctrine gate under-scoped exact authority/false-flag contract

Initial active doctrine gate checked only a small subset of BLK-SYSTEM-075 denied authorities and false side-effect flags.

**Remediation:** Replaced subset checks with exact expected sets for `EXACT_EXCLUDED_AUTHORITIES` and `PATCH_FALSE_SIDE_EFFECT_FLAGS`.

### BLOCKER 5 — Upstream and envelope identity fields forgeable

Follow-up hostile review found that upstream `request_id` / `operator_identity` and envelope `request_id` / `operator_identity` were not exact-bound.

**Remediation:** Added exact constants and validation for upstream request identity and BLK-SYSTEM-075 envelope request identity.

### BLOCKER 6 — Compact denylist rejected only whole-field compact matches

Follow-up hostile review found that compact laundering tokens embedded inside otherwise normal text could pass.

**Remediation:** Changed compact laundering validation to reject any denied compact token appearing inside the normalized string.

---

## Regression Tests Added

```text
test_rejects_recomputed_upstream_packet_schema_forgery
test_rejects_every_upstream_packet_false_side_effect_flag
test_rejects_compact_camel_and_acronym_laundering_variants
test_rejects_forged_upstream_and_envelope_identity_fields
test_rejects_embedded_compact_laundering_variants
```

---

## Focused Verification After Remediation

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_kuronode_lifecycle_cleanup_patch_approval_envelope -q
----------------------------------------------------------------------
Ran 11 tests in 0.084s

OK
```

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint075_kuronode_lifecycle_cleanup_patch_approval_envelope_is_review_only -q
----------------------------------------------------------------------
Ran 1 test in 0.009s

OK
```

---

## Remaining Issues

No known blockers remain after the listed remediations and focused verification.

---

## Non-Authority Statement

The review did not grant patch approval, did not apply a Kuronode patch, did not invoke BLK-pipe or Codex, did not rerun BLK-test, did not run Electron/smoke/TypeScript/package-manager tooling, did not mutate Kuronode source or Git state, did not read protected BLK-req bodies, did not publish BEOs, did not generate RTM, and did not promote coverage or drift authority.
