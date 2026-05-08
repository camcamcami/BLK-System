# BLK-035 — Track I health-check profile expansion boundary

**Status:** Active pilot boundary — expanded local advisory fixed-profile execution only
**Sprint:** BLK-SYSTEM-033
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L4 pilot runtime for local fixed profiles only; not L5 production authority

---

## 1. Purpose

BLK-035 records the BLK-SYSTEM-033 expansion of the BLK-034 advisory health-check runner. It authorizes exactly three additional fixed local profiles and preserves all BLK-034 advisory-only, bounded-output, trusted-executable, canonical-root, no-adjacent-authority semantics.

Active boundary vocabulary:

- `HEALTH_CHECK_PROFILE_EXPANSION_ADVISORY_ONLY`
- `PYTHON_UNITTEST_DISCOVERY_PROFILE_ADVISORY_ONLY`
- `GO_TEST_ALL_PROFILE_ADVISORY_ONLY`
- `GO_VET_ALL_PROFILE_ADVISORY_ONLY`
- `TRUSTED_ABSOLUTE_EXECUTABLES_ONLY`
- `CANONICAL_REPO_ROOT_REQUIRED`
- `PROCESS_OUTPUT_BYTE_GATE_REQUIRED`
- `PYTHON_BYTECODE_CACHE_OUTSIDE_REPO_REQUIRED`
- `WORKSPACE_STATUS_CHANGE_OBSERVED_NOT_SOURCE_MUTATION_PROOF`
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

Persistent doctrine gate marker: BLK-SYSTEM-033 pins fixed-profile health-check expansion only.

---

## 2. Authorized Fixed Profiles

BLK-035 preserves the BLK-034 profiles:

```text
git_status_short_branch -> trusted absolute git + ['status', '--short', '--branch']
active_doctrine_gate -> trusted absolute Python + ['-m', 'unittest', 'python.test_active_doctrine_review_gates']
```

BLK-035 authorizes only these new profile IDs and exact argv tails:

```text
python_unittest_discovery -> trusted absolute Python + ['-m', 'unittest', 'discover', '-s', 'python', '-p', 'test_*.py']
go_test_all -> trusted absolute go + ['test', './...']
go_vet_all -> trusted absolute go + ['vet', './...']
```

The `python_unittest_discovery` profile provides full Python discovery evidence. The `go_test_all` profile provides `go test ./...` evidence. The `go_vet_all` profile provides `go vet ./...` evidence. Profiles are selected by ID only. Caller-supplied argv is not accepted. Caller-supplied command strings are not accepted. Unknown profiles fail closed before subprocess startup.

---

## 3. Execution Rules

The runner must execute fixed profiles with `shell=False`; no shell, shell string, inline interpreter snippet beyond approved `python -m unittest` module invocation, wrapper, alias, or dynamic command construction is authorized.

The runner may start a subprocess only for a known fixed profile. It must use trusted absolute executables rather than inherited `PATH`, validate the canonical BLK-System repository root before startup, use bounded timeouts, enforce a process-output byte gate before evidence construction, emit bounded stdout/stderr excerpts, compute deterministic evidence hashes, and use a scrubbed environment. Python profile environments must route bytecode caches outside the repository and preserve that control for fixed-profile child interpreters.

The runner may observe before/after workspace status changes using Git status snapshots with optional Git locks disabled. A workspace status change must block the health-check result. Absence of a status change is not proof that no source bytes changed; source-mutation surfaces not mechanically observed by the pilot must be reported as non-claims rather than Boolean falsehoods.

The runner is local advisory tooling only. It may report PASS/FAIL/BLOCKED evidence for full Python discovery, go test, and go vet, but health-check PASS remains advisory and does not grant approval or production authority.

---

## 4. Explicit Non-Authorities

BLK-035 does not authorize arbitrary shell, caller-supplied commands, network/API/model/cyber tooling, package-manager execution, browser automation, remote service access, or dependency installation.

BLK-035 does not authorize Git mutation or source mutation. The runner must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, restore, edit files, delete files, or repair state.

BLK-035 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault path scans, runtime active-vault comparison, backend promotion, or requirement/use-case body inspection by the runner.

BLK-035 does not authorize production BLK-test MCP, new BLK-test smoke, BLK-pipe dispatch, live tactical LLM execution, Codex execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation beyond existing BLK-033 fixture evidence, RTM drift rejection, or final drift decisions.

---

## 5. Result Semantics

Health-check results are advisory. Allowed status vocabulary remains:

- `PASS_ADVISORY_ONLY`
- `FAIL_ADVISORY_ONLY`
- `BLOCKED_ADVISORY_ONLY`

A passing result is useful operator context only. PASS does not approve execution, verification, publication, RTM generation, drift rejection, Git cleanup, protected-vault access, BLK-pipe validation success, or production health-check operation.

---

## 6. Stop Conditions

Stop and treat any proposed change as outside BLK-035 authority if it attempts to add raw command execution, caller-supplied argv, shell invocation, inline code execution outside approved unittest module invocation, network/model/cyber/package tooling, new profile IDs beyond the three above, Git/source mutation, protected-vault body access, active-vault scans, BEO/RTM/drift/publication authority, BLK-pipe validation authority, or production monitoring claims.

---

## 7. Future Handoff

Future sprints may request more fixed profiles, stronger side-effect observation, or production health-check authority only through a fresh plan, explicit approval provenance, RED/GREEN tests, hostile review, and a new or amended boundary. BLK-035 does not authorize production health-check service behavior.
