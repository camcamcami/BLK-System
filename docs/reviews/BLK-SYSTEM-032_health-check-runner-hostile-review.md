# BLK-SYSTEM-032 — Health-Check Runner Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T17:49:00+10:00
**Sprint:** BLK-SYSTEM-032
**Plan:** `docs/plans/blk-system-032_track-i-minimal-advisory-health-check-runner.md`
**Reviewed commit before remediation:** `a7d73b5 feat: add advisory health-check runner pilot`

---

## 1. Review Scope

Reviewed files:

- `docs/plans/blk-system-032_track-i-minimal-advisory-health-check-runner.md`
- `docs/BLK-034_track-i-advisory-health-check-runner-boundary.md`
- `docs/reviews/BLK-SYSTEM-032_health-check-runner-inventory.md`
- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/outcomes/BLK-SYSTEM-032_task-000-outcome.md`
- `docs/outcomes/BLK-SYSTEM-032_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-032_task-002-outcome.md`

Review checklist:

- fixed argv only;
- no raw command string or caller-supplied argv execution;
- no shell or inline interpreter escape;
- no network/API/model/cyber/package-manager tooling;
- no Git/source mutation by the runner;
- no protected-vault body reads or active-vault scans;
- no BEO publication, signer/storage/public-ledger, runtime RTM generation, or drift rejection;
- output bounds and redaction are mechanical;
- health-check PASS cannot become approval or production authority;
- sprint-dispatch approval provenance remains separate from runtime/profile evidence.

---

## 2. Initial Findings

### HIGH-1 — Fixed argv could be bypassed through inherited `PATH`

**Initial risk:** The runner used bare `git` and `python3` profile argv while preserving inherited `PATH`, so a poisoned `PATH` could execute an attacker-controlled binary despite `shell=False`.

**Remediation:** The runner now resolves executables through trusted absolute paths before subprocess startup and sets subprocess `PATH` to `/usr/bin:/bin`. Tests prove malicious `/tmp/evil` PATH entries are not used and secret env keys are removed.

**Status:** PASS after remediation.

### HIGH-2 — Caller-controlled `repo_root` could shadow the doctrine module

**Initial risk:** `repo_root` was resolved and used as subprocess `cwd` without proving it was the canonical BLK-System repository root. Because `active_doctrine_gate` uses Python module resolution, a caller could point the runner at another directory containing a fake `python.test_active_doctrine_review_gates` module.

**Remediation:** The runner now validates `repo_root` against the canonical repository root derived from `python/blk_operator_health_check_runner.py` and requires `.git` to exist before subprocess startup. Tests prove non-repository temporary roots fail closed before `Popen` is called.

**Status:** PASS after remediation.

### MEDIUM-1 — Output bounds were post-capture only

**Initial risk:** The first implementation used `subprocess.run(..., capture_output=True)`, which captured full stdout/stderr in memory before excerpt truncation.

**Remediation:** The runner now uses `subprocess.Popen` with temporary stdout/stderr files, a configurable output byte gate, and blocked advisory status when captured output exceeds the gate. Tests prove output flood returns `BLOCKED_ADVISORY_ONLY`, includes an output-limit marker, and does not embed raw output.

**Status:** PASS after remediation.

### MEDIUM-2 — No-authority side-effect flags were vulnerable to subprocess subversion

**Initial risk:** Adjacent authority flags were returned as false even if subprocess identity or cwd had been subverted by HIGH-1/HIGH-2.

**Remediation:** HIGH-1 and HIGH-2 were closed by trusted absolute executable resolution, scrubbed trusted PATH, and canonical repo-root validation. The remaining flags are still advisory assertions, not sandbox proof; BLK-034 now explicitly states this is not production health-check authority and cannot support new profiles or production claims without a future sprint.

**Status:** PASS for BLK-SYSTEM-032 pilot scope; future production authority would require stronger sandbox/observation.

---

## 3. Post-Remediation Verification

Focused tests:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 8 tests in 0.003s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint032_advisory_health_check_runner_boundary_preserves_no_adjacent_authority
Ran 1 test in 0.000s
OK
```

Full verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 441 tests in 6.463s
OK

go test ./...
ok across all packages

go vet ./...
exit 0

git diff --check
exit 0
```

Local runner smoke after remediation:

```text
git_status_short_branch PASS_ADVISORY_ONLY 0 sha256:dc7702d6f59bdf1934f54b3c861e4aeb6dafdb060558edf573d08638281d5523
active_doctrine_gate PASS_ADVISORY_ONLY 0 sha256:7388d0e6e1ab2379e5c9523af039537a64733f62ff84b29a2346e162ee88ea21
```

---

## 4. Final Authority Verdict

BLK-SYSTEM-032 is acceptable after remediation for its narrow Track I L4 local advisory pilot scope.

The sprint does not authorize arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package managers, protected-vault body reads, active-vault scans, Git/source mutation by the runner, production BLK-test MCP, new BLK-test smoke, BEO publication, signer/storage/public-ledger writes, runtime RTM generation outside BLK-033 fixture evidence, RTM drift rejection/final drift decisions, or L5 production health-check authority.

Residual caution: the runner is still not a production sandbox or host-secret isolation mechanism. Future profiles or production health-check authority require a separate sprint with stronger sandbox, filesystem, process, network, and side-effect observation claims.
