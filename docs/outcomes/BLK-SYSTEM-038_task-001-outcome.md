# BLK-SYSTEM-038 — Task 1 Outcome

**Status:** Complete
**Date:** 2026-05-09T10:42:47+10:00
**Sprint:** BLK-SYSTEM-038
**Task:** Task 1 — Doctrine boundary and active gate

---

## 1. Objective

Add BLK-040 as an active boundary document and add a persistent doctrine gate proving the Codex deterministic invocation profile remains fixture-only, advisory, and non-authorizing.

---

## 2. Files Changed

```text
docs/BLK-040_codex-deterministic-invocation-profile-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-038_task-001-outcome.md
```

---

## 3. RED Evidence

The doctrine gate was written before the BLK-040 document existed, then run as a focused test. It failed for the expected reason: the boundary document was missing.

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint038_codex_deterministic_invocation_profile_boundary_denies_live_authority -q

FAIL: test_sprint038_codex_deterministic_invocation_profile_boundary_denies_live_authority
AssertionError: False is not true : BLK-040 Codex deterministic invocation profile boundary missing
FAILED (failures=1)
```

---

## 4. GREEN Evidence

Created `docs/BLK-040_codex-deterministic-invocation-profile-boundary.md` with the required fixture-only markers, ambient-feature disable markers, advisory telemetry markers, native-sandbox non-trust statement, and explicit non-authority vocabulary.

Focused and full doctrine-gate verification then passed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint038_codex_deterministic_invocation_profile_boundary_denies_live_authority -q
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
----------------------------------------------------------------------
Ran 58 tests in 0.004s

OK
```

---

## 5. Verification Commands and Results

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint038_codex_deterministic_invocation_profile_boundary_denies_live_authority -q
PASS

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PASS

git diff --check -- docs/BLK-040_codex-deterministic-invocation-profile-boundary.md python/test_active_doctrine_review_gates.py
PASS
```

---

## 6. Authority Boundary Statement

Task 1 was doctrine/test work only. It did not authorize live Codex execution, live tactical LLM execution, BLK-pipe dispatch, production BLK-test MCP, protected BLK-req body reads, protected body copying, active-vault scans, source mutation outside the allowed files, Git mutation outside this task commit, BEO publication, RTM generation, drift rejection, package-manager/network/model/cyber/browser tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

BLK-040 explicitly states `CODEX_PROFILE_GRANTS_NO_EXECUTION_AUTHORITY`, `CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST`, `CODEX_JSONL_EVENTS_ADVISORY_ONLY`, and `CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY`.

No protected BLK-req body reads occurred.

---

## 7. Commit

Planned task commit message:

```text
docs: define blk040 codex invocation boundary
```

The exact pushed commit hash is recorded in the sprint closeout because a commit cannot contain its own final hash without changing that hash.

---

## 8. Next Task

Proceed to Task 2: implement the pure deterministic Codex invocation profile builder and validation tests.
