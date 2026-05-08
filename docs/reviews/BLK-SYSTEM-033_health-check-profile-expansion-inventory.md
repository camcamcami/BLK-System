# BLK-SYSTEM-033 — Health-Check Profile Expansion Inventory

**Status:** Complete inventory — not production health-check authority
**Date:** 2026-05-08T18:08:00+10:00
**Sprint:** BLK-SYSTEM-033
**Plan:** `docs/plans/blk-system-033_health-check-fixed-profile-expansion.md`

---

## 1. Purpose

This inventory defines the exact additional command surface for the BLK-SYSTEM-033 Track I advisory health-check profile expansion. It is an allowlist input to `docs/BLK-035_track-i-health-check-profile-expansion-boundary.md` and to the Python runner implementation.

The inventory does not authorize arbitrary command execution, production health-check authority, BLK-pipe dispatch, BLK-test startup, BEO publication, RTM generation, drift rejection, protected-vault body reads, active-vault scans, Git/source mutation, network/API/model/cyber tooling, or package-manager execution.

---

## 2. Existing Profiles Preserved

| Profile ID | Exact argv tail | Classification | Status |
| --- | --- | --- | --- |
| `git_status_short_branch` | `['status', '--short', '--branch']` behind trusted absolute `git` | `ADVISORY_ONLY` | Preserved from BLK-034 |
| `active_doctrine_gate` | `['-m', 'unittest', 'python.test_active_doctrine_review_gates']` behind trusted absolute Python | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Preserved from BLK-034 |

---

## 3. New Fixed Profiles Authorized by BLK-SYSTEM-033

| Profile ID | Exact argv tail | Executable source | Classification | Purpose |
| --- | --- | --- | --- | --- |
| `python_unittest_discovery` | `['-m', 'unittest', 'discover', '-s', 'python', '-p', 'test_*.py']` | trusted absolute Python executable | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Advisory full Python suite health-check evidence. |
| `go_test_all` | `['test', './...']` | trusted absolute `go` executable | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Advisory Go test health-check evidence. |
| `go_vet_all` | `['vet', './...']` | trusted absolute `go` executable | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Advisory Go vet health-check evidence. |

No other new profile is authorized by BLK-SYSTEM-033.

---

## 4. Execution Constraints

The runner must enforce all of the following mechanically:

1. Profiles are selected only by profile ID; caller-supplied argv and raw command strings are not accepted.
2. Commands run with `shell=False`.
3. Unknown profiles fail closed before subprocess start.
4. Trusted absolute executables are resolved through controlled paths; inherited `PATH` must not select the executable.
5. The subprocess environment may include trusted tool directories needed for Go/Python operation, but must reject inherited token, SSH agent, askpass, key, password, passphrase, authorization, and secret variables.
6. The canonical BLK-System repository root is validated before subprocess startup.
7. Shells, inline interpreter snippets outside approved `python -m unittest`, wrappers, aliases, network commands, package-manager commands, cyber tools, model-service clients, and Git mutation commands are rejected by source-level allowlist design.
8. Stdout/stderr are subject to a process-output byte gate before evidence construction, then bounded again as excerpts; raw flood output is not embedded in returned evidence.
9. Evidence hashes are computed from captured stdout/stderr/exit metadata to preserve deterministic auditability without embedding unbounded logs.
10. Health-check PASS remains advisory and must not approve BLK-pipe dispatch, BLK-test startup, BEO publication, RTM generation, drift rejection, Git cleanup, protected-vault access, or production health-check operation.

---

## 5. Explicitly Still Deferred

The following remain outside BLK-SYSTEM-033:

- production health-check service/daemon authority;
- arbitrary operator-defined health-check commands;
- network/API/model/cyber health checks;
- package-manager installation or dependency-update checks;
- BLK-test live/smoke profile execution;
- protected-vault or active-vault scans;
- automatic Git cleanup or source repair.

---

## 6. Inventory Verdict

The three-profile expansion is acceptable for a narrow Track I / Track J L4 pilot runtime because it uses project verification commands that are already part of sprint closeout, converts them into fixed advisory runner profiles, and preserves the BLK-034 no-adjacent-authority model.
