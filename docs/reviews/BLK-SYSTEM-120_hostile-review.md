# BLK-SYSTEM-120 Hostile Review — HITL Baseline Promotion

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `python/lint_artifacts.py`, `python/test_blk_req_legislative_gateway.py`, `python/blk_current_state_authority_index.py`, `docs/BLK-077_blk-system-post-078-roadmap.md`, `docs/BLK-079_post-078-current-state-authority-index.md`, `docs/BLK-120_hitl-baseline-promotion.md`

## Required Markers

```text
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION_COMPLETE
DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES
NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY
BASELINE_VERSION_HASH_ASSIGNED_ON_PROMOTION
ACTIVE_VAULT_PUBLISH_IS_NO_OVERWRITE_EXCLUSIVE_CREATE
APPROVAL_REPLAY_LEDGER_CONSUMES_BASELINE_APPROVAL_IDS
APPROVAL_REPLAY_LEDGER_NOT_CONSUMED_ON_PUBLISH_FAILURE
DISCORD_IDENTITY_VALUES_MUST_BE_SNOWFLAKE_STRINGS
NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120
NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY
```

## Hostile Checks

| Probe | Result |
| --- | --- |
| Approval payload omits or supplies malformed Discord identity fields | BLOCKED by exact approval schema, non-empty checks, and numeric Discord snowflake checks. This is structural capture, not live Discord API authentication. |
| Approval uses a timezone-naive or malformed timestamp | BLOCKED by ISO-8601 timezone-aware timestamp parsing. |
| Approval path points at a different staging artifact | BLOCKED by `APPROVAL_PATH_MISMATCH`. |
| Approval hash does not match the current staging draft | BLOCKED by `APPROVAL_HASH_MISMATCH`. |
| Caller reuses an approval ID | BLOCKED by caller-provided replay state and workspace-local approval replay ledger; `APPROVAL_REPLAY` fires before promotion. |
| Invalid or unapproved payload creates an active-vault file | BLOCKED by rejection-before-active-dir/write regressions. |
| Active-vault write path traverses symlinks or collides with existing artifact | BLOCKED by `ACTIVE_PATH_SYMLINK` / `ACTIVE_TARGET_EXISTS` guards and no-overwrite exclusive-create publish. |
| Active-vault target appears after the guard but before publish | BLOCKED by no-overwrite exclusive create; raced targets return `ACTIVE_TARGET_EXISTS` and preserve the existing file. |
| Active publish fails after validation | BLOCKED before replay consumption; `ACTIVE_PUBLISH_FAILED` returns with staging retained and no replay ledger written. |
| Promotion assigns hash before permanent ID/status | BLOCKED by test comparing final active text to `compute_version_hash(active_text)`. |
| Promotion deletes staging before active write | BLOCKED by implementation ordering and regression coverage for rejected cases keeping staging. |
| Backend launders revision overwrite, exact-ID retrieval, BEO, RTM, BLK-test, or BLK-pipe authority | NOT PRESENT; explicit result flags and doctrine markers keep adjacent authorities false/denied. |
| Roadmap/index remain stuck at post-119 HITL planning wording | BLOCKED by BLK-SYSTEM-120 doctrine gate and current-state updates. |
| Current-state scanner accepts denied next-frontier overclaims | BLOCKED by exact-ID retrieval, staged revision overwrite, and public-authority ledger rollback authorization probes. |

## Delegated Hostile Re-Review Remediation

A delegated final hostile review found multiple blocking issues before commit across repeated re-review passes:

1. Approval replay protection was optional and non-consuming. Fixed by adding a workspace-local approval replay ledger and a regression proving the same approval ID cannot promote a recreated identical draft.
2. Discord identity values accepted arbitrary non-empty strings. Fixed by requiring numeric Discord snowflake user/message IDs and a regression for malformed values. This still captures supplied HITL metadata; it does not claim live Discord API authentication.
3. Active-vault publish used overwrite-prone or race-prone publish mechanics. Fixed with direct no-overwrite exclusive-create publishing and regressions for raced active targets.
4. Replay ledger consumption could occur before active publish success or remain falsely consumed after persistence failure. Fixed by consuming replay only after successful publish, writing the replay ledger via atomic temp/replace, rolling back active publish if replay persistence fails, and adding failure regressions.
5. Current-state scanner allowed denied BLK-120-adjacent overclaims such as exact-ID retrieval, staged revision overwrite, and public-authority ledger rollback authorization. Fixed by extending scanner tokens and regression phrase probes.

## Final Hostile Audit Evidence

The final delegated hostile re-review timed out and is not counted as PASS evidence. A local hostile audit then executed concrete probes and passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python /tmp/blk120_local_hostile_audit.py
LOCAL_HOSTILE_AUDIT_PASS: race/no-overwrite, ledger rollback/no-false-consumption, and BLK-120 scanner probes passed
```

## Review Result

PASS for BLK-SYSTEM-120 scope after re-review remediation. The sprint creates deterministic local backend support for explicit Discord approval capture and new-baseline promotion only. It does not implement staged revisions, exact-ID retrieval, BEB dispatch, BLK-pipe runtime, BLK-test runtime, BEO publication, RTM generation, drift rejection, signer/storage/public-authority-ledger behavior, package/network/model/browser/cyber tooling, or production isolation.
