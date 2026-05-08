# BLK-SYSTEM-033 — Health-Check Profile Expansion Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-08T18:47:53+10:00
**Sprint:** BLK-SYSTEM-033
**Plan:** `docs/plans/blk-system-033_health-check-fixed-profile-expansion.md`
**Boundary:** `docs/BLK-035_track-i-health-check-profile-expansion-boundary.md`

---

## 1. Review Scope

This hostile review covered the BLK-SYSTEM-033 fixed-profile expansion of the advisory health-check runner:

- `python/blk_operator_health_check_runner.py`
- `python/test_blk_operator_health_check_runner.py`
- `python/blk_test_mcp_fixed_tool_live_smoke.py`
- `python/test_blk_test_mcp_fixed_tool_live_smoke.py`
- `python/test_active_doctrine_review_gates.py`
- `docs/BLK-035_track-i-health-check-profile-expansion-boundary.md`
- `docs/reviews/BLK-SYSTEM-033_health-check-profile-expansion-inventory.md`
- BLK-SYSTEM-033 plan/outcome artifacts

The review checked the sprint against BLK-024 Track I / Track J, BLK-034, BLK-035, and the sprint plan's authority exclusions.

---

## 2. Hostile Findings and Remediation

### Finding 1 — Python executable trust could be inherited from mutable interpreter state

**Risk:** A profile using `sys.executable` directly could trust a caller-influenced or untrusted interpreter path.

**Remediation:** `_trusted_executable("python3")` now resolves through trusted path roots rather than trusting `sys.executable`. Regression coverage verifies that patching `sys.executable` to `/bin/sh` does not change the trusted Python path.

### Finding 2 — Trusted-path symlink escape could launder an unsafe executable

**Risk:** A trusted directory entry could be a symlink to an executable outside approved roots.

**Remediation:** trusted executable resolution canonicalizes the candidate and rejects paths that escape the trusted roots. Regression coverage creates a temporary trusted-bin symlink to `/bin/sh` and expects rejection.

### Finding 3 — Python discovery dirtied the repository through repo-local bytecode cache

**Risk:** The `python_unittest_discovery` profile initially returned `BLOCKED_ADVISORY_ONLY` because full discovery created `python/__pycache__/blk_test_mcp_approval_authorization.cpython-312.pyc`. The generator was isolated to the existing Sprint 014 fixed-tool live-smoke harness, whose child environment scrubbed Python bytecode controls.

**Remediation:** runner environments now set `PYTHONPYCACHEPREFIX` to an out-of-repository cache prefix in addition to `PYTHONDONTWRITEBYTECODE=1`. The Sprint 014 fixed-tool child scrubbed environment now preserves `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX`, without allowing secrets. Live runner verification confirmed `python_unittest_discovery` returns `PASS_ADVISORY_ONLY` and does not create repo-local `__pycache__`.

### Finding 4 — Side-effect flags over-claimed unobserved surfaces

**Risk:** Returning Boolean `False` for network/package/protected-vault/BEO/RTM/drift side effects implied those surfaces were observed, when the pilot does not measure them.

**Remediation:** unobserved surfaces now return explicit non-claims such as `NOT_MEASURED_BY_PILOT`. PASS remains advisory and grants no authority.

### Finding 5 — Workspace mutation observation was over-claimed

**Risk:** Before/after `git status --porcelain` can detect status changes but cannot prove no source bytes changed if a profile rewrites an already-dirty file without changing Git status shape. Reporting `source_mutated=False` would over-claim.

**Remediation:** the runner now reports `workspace_status_changed` as the actually observed Boolean. `git_mutated` is reported as `WORKSPACE_STATUS_CHANGED` or `NO_WORKSPACE_STATUS_CHANGE_OBSERVED`; `source_mutated` is `WORKSPACE_STATUS_CHANGED` or `NOT_MEASURED_BY_PILOT`. A status change blocks the result, but absence of a status change is no longer presented as proof of no source mutation.

### Finding 6 — Git status snapshot could take optional locks / refresh state

**Risk:** plain `git status` may take optional locks or refresh index metadata, creating mutation risk in the observation path.

**Remediation:** `_git_status_snapshot()` injects `GIT_OPTIONAL_LOCKS=0` into the subprocess environment. Regression coverage asserts the optional-lock guard is present.

---

## 3. Authority Review Verdict

PASS after remediation.

- Fixed profile IDs only: PASS.
- Caller-supplied argv / raw command strings rejected: PASS.
- Trusted absolute executable resolution: PASS.
- Symlink escape rejection: PASS.
- Canonical BLK-System repo-root validation: PASS.
- `shell=False` subprocess execution: PASS.
- No network/model/cyber/package-manager profile surface: PASS.
- No Git/source mutation authority: PASS as an authority boundary; observed workspace status changes block, while unobserved mutation surfaces are not over-claimed.
- Protected-vault/body and active-vault scans excluded: PASS.
- No BEO publication, signer/storage/ledger writes, RTM generation, or drift rejection: PASS.
- Bounded output/redaction: PASS.
- PASS remains advisory and not production health-check authority: PASS.

---

## 4. Verification Evidence

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_operator_health_check_runner
Ran 13 tests in 0.007s
OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 448 tests in 6.511s
OK

go test ./...
ok across all packages

go vet ./...
exit 0

git diff --check
exit 0
```

Live profile verification after remediation:

```text
git_status_short_branch PASS_ADVISORY_ONLY 0 False NO_WORKSPACE_STATUS_CHANGE_OBSERVED NOT_MEASURED_BY_PILOT
active_doctrine_gate PASS_ADVISORY_ONLY 0 False NO_WORKSPACE_STATUS_CHANGE_OBSERVED NOT_MEASURED_BY_PILOT
python_unittest_discovery PASS_ADVISORY_ONLY 0 False NO_WORKSPACE_STATUS_CHANGE_OBSERVED NOT_MEASURED_BY_PILOT
go_test_all PASS_ADVISORY_ONLY 0 False NO_WORKSPACE_STATUS_CHANGE_OBSERVED NOT_MEASURED_BY_PILOT
go_vet_all PASS_ADVISORY_ONLY 0 False NO_WORKSPACE_STATUS_CHANGE_OBSERVED NOT_MEASURED_BY_PILOT
```

---

## 5. Residual Non-Authorities

BLK-SYSTEM-033 does not authorize production health-check authority, arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package-manager execution, protected-vault body reads, active-vault scanning, Git/source repair, BLK-pipe dispatch, production BLK-test MCP, new BLK-test smoke authority, BEO publication, signer/storage/public-ledger mutation, runtime RTM generation, RTM drift rejection, or final drift decisions.
