# BLK-034 — Track I advisory health-check runner boundary

**Status:** Active pilot boundary — local advisory fixed-profile execution only
**Sprint:** BLK-SYSTEM-032
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L4 pilot runtime for local fixed profiles only; not L5 production authority

---

## 1. Purpose

BLK-034 records the narrow advisory health-check runner authority created by BLK-SYSTEM-032. It follows BLK-032's non-executing fixture boundary and grants only enough local pilot runtime to execute two fixed profiles under bounded, advisory, no-adjacent-authority semantics.

Active boundary vocabulary:

- `HEALTH_CHECK_RUNNER_PILOT_ADVISORY_ONLY`
- `HEALTH_CHECK_EXECUTED_LOCAL_FIXED_PROFILE`
- `HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY`
- `NO_ARBITRARY_SHELL`
- `NO_NETWORK_MODEL_CYBER_TOOLING`
- `NO_PACKAGE_MANAGER`
- `NO_GIT_MUTATION`
- `NO_SOURCE_MUTATION`
- `NO_PROTECTED_BODY_READ`
- `NO_ACTIVE_VAULT_SCAN`
- `NO_BEO_PUBLICATION`
- `NO_RTM_GENERATION`
- `NO_DRIFT_REJECTION`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

Persistent doctrine gate marker: BLK-SYSTEM-032 pins advisory fixed-profile health-check runner only.

---

## 2. Authorized Fixed Profiles

BLK-034 authorizes only these profile IDs and exact argv arrays:

```text
git_status_short_branch -> ['git', 'status', '--short', '--branch']
active_doctrine_gate -> ['python3', '-m', 'unittest', 'python.test_active_doctrine_review_gates']
```

Profiles are selected by ID only. caller-supplied argv is not accepted. Caller-supplied command strings are not accepted. unknown profiles fail closed before subprocess startup.

---

## 3. Execution Rules

The runner must execute fixed profiles with `shell=False`; no shell, shell string, inline interpreter snippet, wrapper, alias, or dynamic command construction is authorized.

The runner may start a subprocess only for a known fixed profile. It must resolve executables through trusted absolute paths rather than inherited `PATH`, validate the canonical BLK-System repository root before startup, use bounded timeouts, enforce a process-output byte gate before evidence construction, emit bounded stdout/stderr excerpts, compute deterministic evidence hashes, and use a scrubbed environment. Output evidence must not embed raw flood output or secret-bearing environment values.

The runner is local advisory tooling only. `git_status_short_branch` is read-only advisory context. `active_doctrine_gate` runs the existing doctrine test module and returns advisory PASS/FAIL/BLOCKED evidence. Neither profile grants authority to mutate state.

---

## 4. Explicit Non-Authorities

BLK-034 does not authorize arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package-manager execution, browser automation, remote service access, or dependency installation.

BLK-034 does not authorize Git mutation or source mutation. The runner must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, restore, edit files, delete files, or repair state.

BLK-034 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault path scans, runtime active-vault comparison, backend promotion, or requirement/use-case body inspection.

BLK-034 does not authorize production BLK-test MCP, new BLK-test smoke, BLK-pipe dispatch, live tactical LLM execution, Codex execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation beyond existing BLK-033 fixture evidence, RTM drift rejection, or final drift decisions.

---

## 5. Result Semantics

Health-check results are advisory. Allowed status vocabulary is:

- `PASS_ADVISORY_ONLY`
- `FAIL_ADVISORY_ONLY`
- `BLOCKED_ADVISORY_ONLY`

`HEALTH_CHECK_PASS_GRANTS_NO_AUTHORITY` means a passing result is useful operator context only. PASS does not approve execution, verification, publication, RTM generation, drift rejection, Git cleanup, protected-vault access, or production health-check operation.

---

## 6. Stop Conditions

Stop and treat any proposed change as outside BLK-034 authority if it attempts to add raw command execution, caller-supplied argv, shell invocation, inline code execution, network/model/cyber/package tooling, new profile IDs, Git/source mutation, protected-vault body access, active-vault scans, BEO/RTM/drift/publication authority, or production monitoring claims.

---

## 7. Future Handoff

Future sprints may request additional fixed profiles or production health-check authority only through a fresh plan, explicit approval provenance, RED/GREEN tests, hostile review, and a new or amended boundary. BLK-034 does not authorize deferred profiles from BLK-032 such as full Python discovery, `go test ./...`, or `go vet ./...`.
