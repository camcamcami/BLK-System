# BLK-SYSTEM-035 — Health-Check Isolated Workspace Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T21:24:23+10:00
**Sprint:** BLK-SYSTEM-035
**Plan:** `docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md`
**Boundary:** `docs/BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md`

---

## 1. Review Scope

This hostile review covered the BLK-SYSTEM-035 isolated-workspace execution hardening for the advisory health-check runner:

- `docs/plans/blk-system-035_health-check-isolated-workspace-execution-boundary.md`
- `docs/BLK-037_track-i-health-check-isolated-workspace-execution-boundary.md`
- `docs/reviews/BLK-SYSTEM-035_health-check-isolated-workspace-inventory.md`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`
- BLK-SYSTEM-035 task outcome documents

Review lens: BLK-024 Track I / Track J, BLK-034, BLK-035, BLK-036, BLK-037, and the sprint plan's no-adjacent-authority exclusions.

---

## 2. Initial Hostile Findings

The first hostile review returned `BLOCKED` with two blockers and several non-blocking coverage gaps:

| ID | Severity | Finding | Remediation status |
| --- | --- | --- | --- |
| BLK-SYSTEM-035-HR-001 | High | Cleanup failure did not return bounded `BLOCKED_ADVISORY_ONLY` evidence because `TemporaryDirectory.__exit__` could raise before result mutation. | CLOSED |
| BLK-SYSTEM-035-HR-002 | High | Inherited `BLK_HEALTH_CHECK_ISOLATED_WORKSPACE=1` allowed `.git`-less copied runners to bypass `_validated_repo_root()`, weakening the Git/source-root boundary. | CLOSED |
| BLK-SYSTEM-035-HR-003 | Medium | Symlink exclusion existed but lacked direct regression coverage. | CLOSED |
| BLK-SYSTEM-035-HR-004 | Medium | Isolated-mode source-cache mutation blocking was implemented generically but lacked isolated-specific regression coverage. | ACCEPTED AS COVERED BY SOURCE STATUS/CACHE PATH AND GENERIC CACHE TESTS; no new authority added. |

The remediation pass was re-reviewed and returned two additional cleanup-evidence blockers:

| ID | Severity | Finding | Remediation status |
| --- | --- | --- | --- |
| BLK-SYSTEM-035-HR-005 | High | Cleanup failure over a process-level `FAIL_ADVISORY_ONLY` result still left final status as `FAIL_ADVISORY_ONLY` instead of cleanup-blocked evidence. | CLOSED |
| BLK-SYSTEM-035-HR-006 | High | Cleanup-failure mutation changed final status/stderr after `evidence_hash` was computed, leaving a stale hash. | CLOSED |

---

## 3. Remediation Summary

### BLK-SYSTEM-035-HR-001 — CLOSED

- Replaced `TemporaryDirectory(...)` context management in `run_health_check()` with explicit `tempfile.mkdtemp(...)` plus `try/finally` cleanup.
- Cleanup errors are caught and converted into bounded advisory evidence instead of escaping.
- Added regressions for runner temp cleanup failure and isolated cleanup failure.

### BLK-SYSTEM-035-HR-002 — CLOSED

- Removed the `.git`-less `_validated_repo_root()` bypass.
- `_validated_repo_root()` again requires the canonical source root to contain `.git`.
- Isolated subprocess environments now use `BLK_HEALTH_CHECK_SKIP_GIT_ROOT_SELFTESTS=1` only to skip source-root-assumption selftests during copied full discovery; they do not grant repo-root validation authority.
- Added regressions proving a `.git`-less root is rejected even if the old inherited marker is present and that isolated env does not include `BLK_HEALTH_CHECK_ISOLATED_WORKSPACE`.

### BLK-SYSTEM-035-HR-003 — CLOSED

- `_copy_isolated_workspace()` ignores symlinks in the isolated copy.
- Manual hostile-review probing confirmed symlink copy escape was prevented.

### BLK-SYSTEM-035-HR-005 — CLOSED

- Cleanup failure now forces final `status` to `BLOCKED_ADVISORY_ONLY` and `exit_code` to `None` regardless of whether the process result would otherwise have been PASS or FAIL.
- Added a regression where the subprocess returns nonzero and cleanup fails; final result is cleanup-blocked.

### BLK-SYSTEM-035-HR-006 — CLOSED

- Cleanup-failure handling now recomputes `evidence_hash` after final `status`, `exit_code`, and `stderr_excerpt` mutation.
- Added a regression that recomputes the expected final hash and compares it to the result hash.

---

## 4. Review Checklist Result

| Check | Verdict | Evidence |
| --- | --- | --- |
| No new profile IDs | PASS | Runner tests pin the existing BLK-035 five-profile set. |
| No caller-supplied commands or argv | PASS | Existing fail-closed tests preserved. |
| Isolated workspace outside source repository | PASS | `workspace_mode="isolated_copy"` uses runner-owned temp outside `REPO_ROOT`; tests assert `cwd` is not source repo. |
| `.git` excluded from isolated copy | PASS | Copy helper excludes `.git`; `git_status_short_branch` rejects isolated mode before subprocess startup. |
| Protected BLK-req paths excluded from isolated copy | PASS | Copy helper/test exclude `docs/active`, `docs/requirements`, and `docs/use_cases`. |
| Source status/cache observation preserved | PASS | Source status/cache snapshots are taken before/after isolated execution; status-change regression blocks PASS. |
| Isolated workspace cleanup evidence bounded | PASS | Cleanup failure returns `BLOCKED_ADVISORY_ONLY`, bounded stderr, and final hash recomputation. |
| Copied runner `.git` bypass absent | PASS | `_validated_repo_root()` requires `.git`; old inherited marker does not bypass. |
| Output byte gate and redaction remain bounded | PASS | Existing output/redaction tests pass. |
| No production sandbox/network/host-secret claims | PASS | Result vocabulary uses explicit `NOT_ENFORCED_BY_PILOT` / `NOT_MEASURED_BY_PILOT` non-claims; BLK-037 pins explicit non-authorities. |
| No protected-vault, active-vault, BEO, RTM, drift, BLK-pipe, BLK-test authority | PASS | BLK-037 non-authorities and tests preserve advisory-only semantics. |
| Health-check PASS remains advisory | PASS | Result keeps `health_check_pass_grants_authority=False` and `production_authority_granted=False`. |

---

## 5. Verification After Remediation

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 28 tests in 0.385s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 55 tests in 0.005s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 465 tests in 6.858s
OK

go test ./...
PASS across all packages

go vet ./...
exit 0

git diff --check
exit 0
```

Live profile smoke after remediation:

```text
SOURCE MODE
git_status_short_branch PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
active_doctrine_gate PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
python_unittest_discovery PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
go_test_all PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED
go_vet_all PASS_ADVISORY_ONLY 0 source_repo False False True PROCESS_GROUP_KILL_NOT_NEEDED

ISOLATED MODE
active_doctrine_gate PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
python_unittest_discovery PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
go_test_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
go_vet_all PASS_ADVISORY_ONLY 0 isolated_copy ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO False False True
```

---

## 6. Final Verdict

PASS after remediation. BLK-SYSTEM-035 preserves the BLK-035 fixed-profile advisory runner while adding optional isolated-workspace execution for eligible non-Git profiles. It does not authorize production health-check authority, arbitrary shell, caller-supplied commands, new profile IDs, network/API/model/cyber tooling, package-manager execution, `.git` copying, protected-vault body reads/copying/parsing/hashing/summarizing, active-vault scans, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, BEO publication, runtime RTM generation, RTM drift rejection, final drift decisions, or production sandbox/network/host-secret isolation claims.
