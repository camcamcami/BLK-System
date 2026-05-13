# BLK-SYSTEM-097 Task 001 Outcome — RED Exact-Target Evidence-Refresh Gates

**Sprint:** BLK-SYSTEM-097 — Bounded BLK-test Evidence Refresh Request / Exact-Target Frontier
**Task:** 001 — Add RED gates for exact-target evidence refresh, fresh IDs, denied authority, and outcome docs
**Status:** Complete

## Delivered Gate Changes

- Added `python/test_blk_test_kuronode_workspace_bounded_evidence_refresh.py` covering the BLK-SYSTEM-097 wrapper contract:
  - fresh BLK-SYSTEM-097 approval/run IDs;
  - exact Kuronode target path, source-subtree path, workspace path, replay-ledger path, branch, and HEAD;
  - fixed `run_ast_validation` tool only;
  - caller-owned, process-local, durable, and committed-evidence replay checks;
  - raw path spelling aliases, pre-owned workspace, secret-like descendants, target/remote HEAD drift, output byte limits, and PASS-as-approval text rejection;
  - source/Git mutation detection and workspace cleanup evidence.
- Extended `python/test_active_doctrine_review_gates.py` with a persistent BLK-SYSTEM-097 active-doctrine gate.
- Extended `python/test_blk_current_state_authority_index.py` to require a BLK-097 current-state surface.

## RED Verification Observed

Focused RED command:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_test_kuronode_workspace_bounded_evidence_refresh python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint097_bounded_blk_test_evidence_refresh_is_one_run_evidence_only python.test_blk_current_state_authority_index.CurrentStateAuthorityIndexTest.test_post_078_governing_docs_and_profile_surfaces_are_current -q
```

Expected RED failures were observed before the implementation was complete:

```text
ModuleNotFoundError: No module named 'blk_test_kuronode_workspace_bounded_evidence_refresh'
KeyError: 'BLK-097 bounded BLK-test evidence refresh'
AssertionError: BLK-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md missing
```

After the wrapper/doc skeleton existed but before runtime/current-state completion, the same focused command failed on the expected missing runtime evidence and missing post-097 roadmap/current-state markers.

## Non-Authority Boundary

Task 001 created tests only. It did not run BLK-test runtime, did not mutate Kuronode, did not execute BLK-pipe/Codex/MCP transport, did not publish BEOs, did not generate RTM, did not read protected BLK-req bodies, and did not promote coverage or drift truth.
