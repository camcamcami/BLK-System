# BLK-SYSTEM-053 — Hostile Review: Repeatable Non-Disposable L4 Wrapper Approvals

**Status:** PASS after remediation
**Date:** 2026-05-10T12:40:00+10:00
**Sprint:** BLK-SYSTEM-053
**Scope:** `L4RuntimeApprovalEnvelope`, non-disposable L4 wrapper parameterization, BLK-056 active boundary, focused tests

---

## 1. Review Scope

Reviewed files:

```text
python/blk_test_non_disposable_l4_runtime_pilot.py
python/test_blk_test_non_disposable_l4_runtime_pilot.py
python/test_active_doctrine_review_gates.py
docs/BLK-056_repeatable-non-disposable-l4-wrapper-approval-boundary.md
docs/plans/blk-system-053_repeatable-non-disposable-l4-wrapper-approvals.md
docs/outcomes/BLK-SYSTEM-053_task-001-outcome.md
```

Review target: prove BLK-SYSTEM-053 cleaned the wrapper for repeatable future approvals without adding new runtime authority or weakening BLK-SYSTEM-051/052 safety controls.

---

## 2. Initial Hostile Findings

The first hostile review returned BLOCKERS:

1. `replay_ledger_path` could be placed inside the target repo/source/`.git` before mutation snapshots, laundering source/Git mutation as PASS.
2. `marker_nonce_binding` accepted weak substrings such as `BLK`, allowing stale nonce laundering.
3. Fresh parameterized envelopes could reuse consumed BLK-SYSTEM-051/052 approval/run IDs if caller sets a fresh ledger and empty replay sets.
4. Planned Task 002 review/outcome docs were not yet present.

The second hostile review confirmed items 1 and 2 were remediated but found one remaining BLOCKER:

1. A custom `L4RuntimeApprovalEnvelope` using `sprint="BLK-SYSTEM-051"` could still reuse `APPROVAL-BLK-SYSTEM-051-001` and `RUN-BLK-SYSTEM-051-001` with a fresh ledger/workspace.

---

## 3. Remediations

Remediations added after hostile review:

1. Public `L4RuntimeApprovalEnvelope` construction rejects any consumed BLK-SYSTEM-051 or BLK-SYSTEM-052 approval/run IDs.
2. The internal BLK-SYSTEM-051 default envelope is retained only through `_default_approval_envelope()` for historical compatibility, not for fresh public approval-envelope construction.
3. `marker_nonce_binding` must exactly equal `sprint`, not merely be a substring.
4. `approval_id` and `run_id` must bind to the approval envelope sprint.
5. `replay_ledger_path` must not overlap `target_repo_path` or `workspace_clone_path`; this blocks source, `.git`, protected-doc descendant, and repo-root ledger mutation laundering.
6. `workspace_marker_name` remains constrained to a single hidden filename inside the wrapper-owned workspace.
7. BLK-056 and active doctrine gate coverage were expanded to pin the above requirements.

Regression tests added/updated:

```text
test_parameterized_envelope_rejects_tool_expansion_and_marker_path_escape
test_parameterized_envelope_rejects_weak_nonce_binding_consumed_ids_and_repo_ledger
test_sprint053_repeatable_non_disposable_l4_wrapper_approval_cleanup_is_not_runtime_authority
```

---

## 4. Final Review Verdict

Final verdict: PASS.

No remaining blocker was found in the reviewed scope after remediation.

The wrapper remains evidence-only and fixed-tool only. It does not start production/generic BLK-test MCP, does not start a reusable service, does not run another real non-disposable pilot, does not accept arbitrary shell/caller commands, does not dynamically expand tools, does not mutate source/Git as BLK-test behavior, does not read protected BLK-req bodies, does not publish BEOs, and does not generate RTMs or drift decisions.

---

## 5. Verification Evidence

Focused verification after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_non_disposable_l4_runtime_pilot -q
Ran 20 tests in 0.182s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 73 tests in 0.006s — OK
```

---

## 6. Remaining Non-Authority Boundary

BLK-SYSTEM-053 does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, any new non-disposable runtime run, arbitrary repositories, arbitrary shell, caller-supplied commands, dynamic tool expansion, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, package-manager/network/model/browser/cyber tooling, live Codex execution, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.
