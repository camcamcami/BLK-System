# BLK-SYSTEM-120 Sprint Closeout — HITL Baseline Promotion

**Status:** COMPLETE
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-120
**Plan:** `docs/plans/blk-system-120_hitl-baseline-promotion.md`
**Record:** `docs/BLK-120_hitl-baseline-promotion.md`
**Hostile review:** `docs/reviews/BLK-SYSTEM-120_hostile-review.md`

## Summary

BLK-SYSTEM-120 implements deterministic BLK-req HITL approval capture and backend-only new-baseline promotion in `python/lint_artifacts.py`. It also reconciles BLK-077, BLK-079, and `python/blk_current_state_authority_index.py` to mark BLK-SYSTEM-120 complete and select the next frontier: staged revision/concurrency plus exact-ID retrieval planning.

## Required Markers

```text
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION
BLK_SYSTEM_120_HITL_BASELINE_PROMOTION_COMPLETE
DISCORD_HITL_APPROVAL_CAPTURED_FOR_NEW_BASELINES
NEW_BASELINE_PROMOTION_WRITES_ACTIVE_VAULT_BY_BACKEND_ONLY
BASELINE_VERSION_HASH_ASSIGNED_ON_PROMOTION
APPROVAL_BINDS_DISCORD_USER_MESSAGE_TIMESTAMP_PATH_AND_HASH
ACTIVE_VAULT_WRITE_PATH_REJECTS_SYMLINKS_AND_COLLISIONS
ACTIVE_VAULT_PUBLISH_IS_NO_OVERWRITE_EXCLUSIVE_CREATE
APPROVAL_REPLAY_LEDGER_CONSUMES_BASELINE_APPROVAL_IDS
APPROVAL_REPLAY_LEDGER_NOT_CONSUMED_ON_PUBLISH_FAILURE
DISCORD_IDENTITY_VALUES_MUST_BE_SNOWFLAKE_STRINGS
NO_REVISION_OVERWRITE_OR_EXACT_ID_RETRIEVAL_BY_120
NEXT_FRONTIER_BLK_REQ_STAGED_REVISION_AND_EXACT_ID_RETRIEVAL_PLANNING_NOT_EXECUTION_AUTHORITY
```

## RED Evidence

Focused BLK-req test initially failed because the implementation did not exist:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway.BlkReqHitlBaselinePromotionTest -v
ImportError: cannot import name 'capture_baseline_approval' from 'lint_artifacts'
```

The doctrine gate initially failed because BLK-120 did not exist:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint120_hitl_baseline_promotion_markers_and_next_frontier_are_pinned -v
AssertionError: False is not true : BLK-120 missing
```

## Focused GREEN Evidence

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_req_legislative_gateway.BlkReqHitlBaselinePromotionTest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint120_hitl_baseline_promotion_markers_and_next_frontier_are_pinned python.test_blk_current_state_authority_index -v
Ran 26 tests
OK
```

## Aggregate Verification

```text
rm -rf /tmp/blk-system-pycache && PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
Ran 1033 tests in 41.526s
OK

go test ./...
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/execguard
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/runtimeguard
ok github.com/camcamcami/BLK-System/internal/testutil
ok github.com/camcamcami/BLK-System/internal/validation
ok github.com/camcamcami/BLK-System/internal/validationprofiles
```

## Hostile Re-Review Remediation

A delegated hostile re-review found multiple pre-commit blockers across repeated passes:

1. Approval replay protection was optional and non-consuming. Remediation: added a workspace-local replay ledger/registry and regression coverage for same-approval replay against a recreated identical draft.
2. Discord identity capture accepted arbitrary non-empty strings. Remediation: added numeric Discord snowflake validation for user/message IDs and regression coverage for malformed values. This remains structural metadata capture, not live Discord API authentication.
3. Active-vault publish used overwrite-prone or race-prone mechanics. Remediation: changed promotion to direct no-overwrite exclusive-create publish and added race regressions preserving a sentinel active baseline.
4. Replay ledger consumption could happen before active publish success or remain falsely consumed after persistence failure. Remediation: consume replay only after successful publish, write the replay ledger via atomic temp/replace, roll back active publish if replay persistence fails, and add failure regressions.
5. Current-state scanner accepted denied BLK-120-adjacent overclaims. Remediation: added exact-ID retrieval, staged revision overwrite, and public-authority ledger rollback authorization probes to the scanner and tests.

## Final Hostile Audit Evidence

The final delegated hostile re-review timed out and was not counted as PASS evidence. A local hostile audit then executed concrete probes and passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python /tmp/blk120_local_hostile_audit.py
LOCAL_HOSTILE_AUDIT_PASS: race/no-overwrite, ledger rollback/no-false-consumption, and BLK-120 scanner probes passed
```

## Authority Boundary

BLK-SYSTEM-120 authorizes deterministic local backend code for new-baseline promotion under explicit HITL approval input. It does not promote any real BLK-req artifact in this sprint; tests use temporary workspaces.

BLK-SYSTEM-120 grants no staged revision checkout, no active-vault overwrite of an existing baseline, no concurrency-lock revision overwrite, no exact-ID retrieval for BEB planning, no BEB dispatch, no BLK-pipe runtime dispatch, no BLK-test runtime, no BEO publication, no RTM generation, no RTM drift rejection, no protected active body reads for trace closure, no non-BLK-req/Kuronode mutation, no package/network/model/browser/cyber tooling, no signer/storage/public-authority-ledger/rollback behavior, and no production isolation claim.

## Next Slice

The next sequence should start with staged revision checkout/concurrency and exact-ID retrieval, under a separate authority boundary.
