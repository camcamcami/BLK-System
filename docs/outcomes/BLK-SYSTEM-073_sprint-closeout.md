# BLK-SYSTEM-073 Sprint Closeout — Kuronode Workspace Read-Only BLK-test Pilot Runtime

**Status:** Complete — one approved read-only pilot executed; evidence FAIL recorded; hostile-review blockers remediated
**Date:** 2026-05-11
**Final runtime evidence:** `BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY`

---

## Summary

BLK-SYSTEM-073 completed the next logical BLK-System sprint after the BLK-SYSTEM-071 request package, BLK-SYSTEM-072 exact-target review envelope, and authorized Kuronode push.

The sprint executed exactly one read-only BLK-test functional-module pilot over the real Kuronode workspace target at:

```text
/home/dad/code/Kuronode-v1
38e332b188e45edcb484765694112c9041ad1a3b
```

The pilot result was `FAIL` evidence-only:

```text
smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
```

This is a BLK-test module evidence finding. It is not a BLK-System test-suite result, not a BEO, not RTM, not coverage/drift truth, not source mutation authority, and not approval for production BLK-test MCP.

---

## Delivered Artifacts

```text
docs/plans/blk-system-073_kuronode-workspace-read-only-blk-test-pilot-runtime.md
docs/BLK-074_blk-test-kuronode-workspace-read-only-pilot-runtime-boundary.md
docs/outcomes/BLK-SYSTEM-073_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-073_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-073_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-073_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-073_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-073_task-005-outcome.md
docs/outcomes/BLK-SYSTEM-073_runtime-evidence.json
docs/reviews/BLK-SYSTEM-073_kuronode-workspace-read-only-pilot-hostile-review.md
python/blk_test_kuronode_workspace_read_only_pilot_runtime.py
python/test_blk_test_kuronode_workspace_read_only_pilot_runtime.py
python/test_active_doctrine_review_gates.py
```

---

## Commit Chain

```text
7c97173 docs: plan blk-system 073 kuronode read-only pilot
51d0f50 feat: add blk-system 073 kuronode read-only pilot
bcee16d docs: record blk-system 073 pilot evidence
1ee1115 test: harden blk-system 073 pilot runtime
```

The closeout document and Task 005 outcome are committed separately after this file is written.

---

## Runtime Evidence

Runtime identity:

```text
approval_id: APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
target_repo_path: /home/dad/code/Kuronode-v1
source_subtree_path: /home/dad/code/Kuronode-v1/scripts
workspace_clone_path: /tmp/blk-system-073-kuronode-workspace-read-only-pilot-workspace
replay_ledger_path: /tmp/blk-system-073-kuronode-workspace-read-only-pilot-replay-ledger.json
target_head_sha: 38e332b188e45edcb484765694112c9041ad1a3b
fixed_tool: run_ast_validation
```

Result:

```json
{
  "status": "FAIL",
  "pilot_status": "BLK_TEST_KURONODE_WORKSPACE_READ_ONLY_PILOT_FAIL_EVIDENCE_ONLY",
  "findings_count": 1,
  "evidence_json_bytes": 2210
}
```

Finding:

```text
smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
```

Safety evidence:

```text
source_mutation_detected: false
git_mutation_detected: false
workspace_cleanup_verified: true
beo_publication: DRAFT_ONLY
rtm_status: NOT_GENERATED
coverage_claim_promoted: false
protected_body_read: false
production_mcp_authority: false
generic_mcp_authority: false
```

---

## Replay Closeout

The production runtime IDs were consumed by the one real pilot and are now retired:

```text
APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
```

Post-hostile-review remediation added production-entrypoint retirement against the committed evidence artifact, so deleting the `/tmp` replay ledger cannot reopen the already-consumed BLK-SYSTEM-073 production IDs.

---

## Hostile Review Summary

Hostile review found and remediated blockers involving:

1. public custom-envelope target laundering;
2. replay bypass after `/tmp` ledger deletion/process restart;
3. caller-provided remote-head evidence laundering;
4. PASS-as-approval and publish-BEO wording gaps;
5. post-replay exceptions without bounded BLOCKED evidence;
6. findings-count/truncation truthfulness;
7. compact-evidence size enforcement;
8. secret-like descendant coverage.

The real Kuronode pilot was not rerun during remediation. Synthetic tests were used to prove hardening.

---

## Verification

Focused BLK-SYSTEM-073 runtime tests:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_workspace_read_only_pilot_runtime -q
----------------------------------------------------------------------
Ran 8 tests in 0.011s

OK
```

Focused active doctrine gate:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint073_blk_test_kuronode_workspace_read_only_pilot_runtime_is_evidence_only -q
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

Full Python suite:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover python 'test_*.py'
----------------------------------------------------------------------
Ran 759 tests in 9.558s

OK
```

Go suite:

```text
go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
```

Diff hygiene:

```text
git diff --check
# OK
```

---

## Final Repository State Before Closeout Commit

```text
BLK-System status: ## main...origin/main
BLK-System HEAD: 1ee1115 test: harden blk-system 073 pilot runtime
BLK-System remote main: 1ee11158f822d95a353bb5012c3a2564aedbfe47 refs/heads/main
Kuronode status: ## main...origin/main
Kuronode HEAD: 38e332b188e45edcb484765694112c9041ad1a3b
Kuronode remote main: 38e332b188e45edcb484765694112c9041ad1a3b refs/heads/main
```

---

## Remaining Work

- Address the BLK-test finding `smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED` in a future sprint only if fresh scope/authority is granted.
- Do not rerun BLK-SYSTEM-073 production IDs; they are consumed and retired.

---

## Non-Authority Statement

BLK-SYSTEM-073 did not authorize or start production/generic BLK-test MCP, did not run Electron/smoke/TypeScript/package-manager tooling against Kuronode, did not invoke Codex, did not invoke BLK-pipe, did not mutate Kuronode source or Git state, did not push Kuronode after the already-authorized earlier Kuronode push, did not read protected BLK-req bodies, did not publish authoritative BEOs, did not generate RTM, did not promote coverage/drift decisions, did not mutate public ledgers, and did not prove production sandbox or host-secret isolation.
