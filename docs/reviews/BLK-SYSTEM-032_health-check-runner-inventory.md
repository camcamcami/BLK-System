# BLK-SYSTEM-032 — Advisory Health-Check Runner Inventory

**Status:** Complete inventory — not production health-check authority
**Date:** 2026-05-08T17:29:00+10:00
**Sprint:** BLK-SYSTEM-032
**Plan:** `docs/plans/blk-system-032_track-i-minimal-advisory-health-check-runner.md`

---

## 1. Purpose

This inventory defines the exact initial command surface for the BLK-SYSTEM-032 Track I advisory health-check runner pilot. It is an allowlist input to `docs/BLK-034_track-i-advisory-health-check-runner-boundary.md` and to the Python runner implementation.

The inventory does not authorize arbitrary command execution, production health-check authority, BLK-pipe dispatch, BLK-test startup, BEO publication, RTM generation, drift rejection, protected-vault body reads, active-vault scans, Git/source mutation, network/API/model/cyber tooling, or package-manager execution.

---

## 2. Initial Fixed Profiles

| Profile ID | Exact argv | Working directory | Classification | Purpose |
| --- | --- | --- | --- | --- |
| `git_status_short_branch` | `['git', 'status', '--short', '--branch']` | Repository root | `ADVISORY_ONLY` | Show local branch/dirty-state context without changing Git state. |
| `active_doctrine_gate` | `['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']` | Repository root | `BLOCKING_IF_LATER_EXECUTION_AUTHORIZED` | Run active doctrine gates so the operator can see whether authority-bearing docs are currently consistent. |

No other profile is authorized by BLK-SYSTEM-032.

---

## 3. Execution Constraints

The runner must enforce all of the following mechanically:

1. Profiles are selected only by profile ID; caller-supplied argv and raw command strings are not accepted.
2. Commands run with `shell=False`.
3. Unknown profiles fail closed before subprocess start.
4. Shells, inline interpreter snippets, wrappers, aliases, network commands, package-manager commands, cyber tools, model-service clients, and Git mutation commands are rejected by source-level allowlist design.
5. The working directory is validated as the canonical BLK-System repository root before subprocess startup; profile definitions do not accept caller-controlled repository aliases or paths from untrusted result fields.
6. Executables are resolved through trusted absolute paths rather than inherited `PATH` so a poisoned operator environment cannot hijack `git` or `python3`.
7. The environment is scrubbed to a small allowlist and removes token/SSH/askpass/key/password/passphrase-style variables.
8. Stdout/stderr are subject to a process-output byte gate before evidence construction, then bounded again as excerpts; raw flood output is not embedded in returned evidence.
9. Evidence hashes are computed from captured stdout/stderr/exit metadata to preserve deterministic auditability without embedding unbounded logs.
10. `git_status_short_branch` is advisory only and must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, or restore.
11. `active_doctrine_gate` may read doctrine docs as part of existing test behavior, but the runner itself does not scan protected-vault bodies, active-vault paths, or source trees for new data.

---

## 4. Result Semantics

Allowed result statuses:

- `PASS_ADVISORY_ONLY`
- `FAIL_ADVISORY_ONLY`
- `BLOCKED_ADVISORY_ONLY`

A PASS never grants approval to dispatch BLK-pipe, start BLK-test, publish BEOs, generate RTM, reject drift, mutate source, clean Git state, capture approvals, access protected vaults, or treat the pilot as production authority.

---

## 5. Explicitly Deferred Profiles

The following BLK-032 fixture candidates remain deferred and are not authorized by BLK-SYSTEM-032:

- `['go', 'test', './...']`
- `['go', 'vet', './...']`
- `['python3', '-m', 'unittest', 'discover', 'python', 'test_*.py']`

They may be considered by a future sprint after the initial runner surface has passed hostile review.

---

## 6. Inventory Verdict

The initial two-profile surface is acceptable for a narrow Track I L4 pilot runtime because it is local, fixed, bounded, read-only/advisory in authority semantics, and surrounded by explicit denial of adjacent BLK-System authorities.
