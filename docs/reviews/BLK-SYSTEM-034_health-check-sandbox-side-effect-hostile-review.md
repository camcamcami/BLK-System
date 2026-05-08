# BLK-SYSTEM-034 — Health-Check Sandbox and Side-Effect Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T19:43:45+10:00
**Sprint:** BLK-SYSTEM-034
**Plan:** `docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md`
**Boundary:** `docs/BLK-036_track-i-health-check-sandbox-side-effect-observation-boundary.md`

---

## 1. Review Scope

This hostile review covered the BLK-SYSTEM-034 side-effect observation hardening for the advisory health-check runner:

- `docs/plans/blk-system-034_health-check-sandbox-side-effect-observation-boundary.md`
- `docs/BLK-036_track-i-health-check-sandbox-side-effect-observation-boundary.md`
- `docs/reviews/BLK-SYSTEM-034_health-check-side-effect-inventory.md`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`
- task outcome documents for BLK-SYSTEM-034

Review lens: BLK-024 Track I / Track J, BLK-034, BLK-035, BLK-036, and the sprint plan's no-adjacent-authority exclusions.

---

## 2. Initial Hostile Findings

An adversarial review returned `BLOCKED` with four findings:

| ID | Severity | Finding | Remediation status |
| --- | --- | --- | --- |
| BLK-SYSTEM-034-HR-001 | High | Runner temp/cache containment outside the repo was asserted but not explicitly enforced because `TemporaryDirectory` had no safe `dir=` parent and result evidence unconditionally reported outside-repo containment. | CLOSED |
| BLK-SYSTEM-034-HR-002 | High | Repo-local cache artifact observation was path-only, so a preexisting `.pyc` rewritten at the same path could pass even though BLK-036 says appearance/change blocks PASS. | CLOSED |
| BLK-SYSTEM-034-HR-003 | High | Subprocess startup failure raised an exception instead of returning bounded `BLOCKED_ADVISORY_ONLY` evidence. | CLOSED |
| BLK-SYSTEM-034-HR-004 | Medium | Timeout cleanup evidence collapsed process-group kill success and direct-child fallback into one `PROCESS_GROUP_KILL_ATTEMPTED` vocabulary. | CLOSED |

---

## 3. Remediation Summary

### BLK-SYSTEM-034-HR-001 — CLOSED

- Added `_safe_temp_parent()` to select an existing temp parent outside `REPO_ROOT`.
- `TemporaryDirectory` now receives an explicit safe `dir=` parent.
- Added `_path_inside()` and result evidence derived from the actual resolved runner temp path instead of an unconditional false.
- Added a regression that sets repo-local temp environment variables and verifies runner temp/cache env paths stay outside the repository.

### BLK-SYSTEM-034-HR-002 — CLOSED

- Expanded `_repo_cache_snapshot()` to include relative path, file size, and `st_mtime_ns` for `.pyc` files; directory snapshots include mtime.
- Added a regression proving an existing repo-local `.pyc` content/signature change blocks advisory PASS.

### BLK-SYSTEM-034-HR-003 — CLOSED

- Extended `ProcessOutcome` with `startup_failed` and bounded startup-failure evidence.
- `_run_fixed_process()` now catches `OSError` from `subprocess.Popen` and returns a blocked outcome instead of escaping.
- Added a regression proving startup failure returns `BLOCKED_ADVISORY_ONLY`, `exit_code=None`, and bounded stderr evidence.

### BLK-SYSTEM-034-HR-004 — CLOSED

- Extended `ProcessOutcome` with explicit timeout cleanup vocabulary.
- Successful process-group kill reports `PROCESS_GROUP_KILL_ATTEMPTED`.
- Direct-child fallback reports `DIRECT_CHILD_KILL_FALLBACK`.
- Added a regression proving process-group kill failure reports direct-child fallback.

---

## 4. Review Checklist Result

| Check | Verdict | Evidence |
| --- | --- | --- |
| No new profile IDs | PASS | Runner tests pin exactly five profile IDs from BLK-035. |
| No caller-supplied commands or argv | PASS | Existing fail-closed tests preserved. |
| Runner-owned temp/cache outside repo | PASS | `_safe_temp_parent()` and regression for repo-local temp env. |
| Repo-local cache artifacts block PASS | PASS | Path appearance and path/signature change tests pass. |
| Process-group timeout cleanup | PASS | `start_new_session=True`, `os.killpg`, direct-child fallback test. |
| Startup failure bounded | PASS | `startup_failed` outcome test. |
| Output byte gate and redaction remain bounded | PASS | Existing output/redaction tests pass. |
| No production sandbox/network/host-secret claims | PASS | Result vocabulary uses `NOT_ENFORCED_BY_PILOT`; BLK-036 pins explicit non-claims. |
| No protected-vault, active-vault, BEO, RTM, drift, BLK-pipe, BLK-test authority | PASS | BLK-036 non-authorities and tests preserve advisory-only semantics. |
| Health-check PASS remains advisory | PASS | Result keeps `health_check_pass_grants_authority=False` and `production_authority_granted=False`. |

---

## 5. Verification After Remediation

```text
rm -rf python/__pycache__ python/__tmp_parent_probe
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 19 tests in 0.268s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates
Ran 54 tests in 0.006s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 455 tests in 6.854s
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
git_status_short_branch PASS_ADVISORY_ONLY 0 False False True PROCESS_GROUP_KILL_NOT_NEEDED NOT_ENFORCED_BY_PILOT
active_doctrine_gate PASS_ADVISORY_ONLY 0 False False True PROCESS_GROUP_KILL_NOT_NEEDED NOT_ENFORCED_BY_PILOT
python_unittest_discovery PASS_ADVISORY_ONLY 0 False False True PROCESS_GROUP_KILL_NOT_NEEDED NOT_ENFORCED_BY_PILOT
go_test_all PASS_ADVISORY_ONLY 0 False False True PROCESS_GROUP_KILL_NOT_NEEDED NOT_ENFORCED_BY_PILOT
go_vet_all PASS_ADVISORY_ONLY 0 False False True PROCESS_GROUP_KILL_NOT_NEEDED NOT_ENFORCED_BY_PILOT
```

---

## 6. Final Verdict

PASS after remediation. BLK-SYSTEM-034 preserves the BLK-035 fixed-profile advisory runner while improving local side-effect observation and process hygiene. It does not authorize production health-check authority, arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package-manager execution, protected-vault body reads, active-vault scans, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, BEO publication, runtime RTM generation, RTM drift rejection, final drift decisions, or production sandbox/network/host-secret isolation claims.
