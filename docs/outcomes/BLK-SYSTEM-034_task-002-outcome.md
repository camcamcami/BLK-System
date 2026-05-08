# BLK-SYSTEM-034 — Task 002 Outcome

**Status:** Complete — pending commit/push at document creation
**Date:** 2026-05-08T19:21:29+10:00
**Sprint:** BLK-SYSTEM-034
**Task:** 002 — Implement runner boundary hardening with TDD
**Plan:** `docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md`

---

## 1. Summary

Hardened the advisory health-check runner with BLK-036 side-effect observation semantics:

- per-run runner-owned temp/cache directories outside the repository;
- `TMPDIR`, `TMP`, `TEMP`, and `PYTHONPYCACHEPREFIX` routed into the runner-owned temp tree;
- repo-local `__pycache__` / `.pyc` snapshot observation;
- repo-local cache artifact changes block advisory PASS;
- timeout cleanup attempts process-group kill via `start_new_session=True` and `os.killpg(..., SIGKILL)`;
- result evidence now reports explicit observation scope and non-claims for production sandbox, network firewall, and host-secret isolation.

The fixed profile set remains unchanged.

---

## 2. RED Evidence

Focused runner tests failed before implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
FAILED (failures=2, errors=1)

Failures/errors covered:
- expected side_effect_observation_scope GIT_STATUS_AND_REPO_CACHE_AND_RUNNER_TEMP_ONLY but received GIT_STATUS_BEFORE_AFTER_ONLY
- expected repo-local cache artifact change to return BLOCKED_ADVISORY_ONLY but received PASS_ADVISORY_ONLY
- expected subprocess Popen start_new_session and process-group kill evidence, but start_new_session was absent
```

---

## 3. GREEN Verification

```text
rm -rf python/__pycache__
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 15 tests in 0.211s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 54 tests in 0.005s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 451 tests in 6.826s
OK

go test ./...
PASS across all packages

go vet ./...
exit 0

git diff --check
exit 0
```

Live profile smoke after hardening:

```text
git_status_short_branch PASS_ADVISORY_ONLY 0 False False True NOT_ENFORCED_BY_PILOT
active_doctrine_gate PASS_ADVISORY_ONLY 0 False False True NOT_ENFORCED_BY_PILOT
python_unittest_discovery PASS_ADVISORY_ONLY 0 False False True NOT_ENFORCED_BY_PILOT
go_test_all PASS_ADVISORY_ONLY 0 False False True NOT_ENFORCED_BY_PILOT
go_vet_all PASS_ADVISORY_ONLY 0 False False True NOT_ENFORCED_BY_PILOT
```

---

## 4. Delivered Artifacts

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`

---

## 5. Authority Boundary

Task 002 preserves exactly the five BLK-035 fixed profile IDs and remains local advisory-only. It does not authorize arbitrary shell, caller-supplied commands, new health-check profiles, production sandbox/cgroup/VM/network/host-secret isolation claims, protected-vault body reads, active-vault scans, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, new BLK-test smoke, BEO publication, runtime RTM generation, RTM drift rejection, or final drift decisions.

---

## 6. Exact Paths Staged

```text
python/blk_operator_health_check_runner.py
python/test_blk_operator_health_check_runner.py
docs/outcomes/BLK-SYSTEM-034_task-002-outcome.md
```
