# BLK-036 — Track I health-check sandbox and side-effect observation boundary

**Status:** Active pilot boundary — local advisory side-effect observation only
**Sprint:** BLK-SYSTEM-034
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L4 pilot runtime for local fixed profiles only; not L5 production authority

---

## 1. Purpose

BLK-036 records the BLK-SYSTEM-034 hardening boundary for the BLK-034/BLK-035 advisory health-check runner. It authorizes only stronger local execution hygiene and side-effect observation around the existing fixed profiles. It does not authorize new profile IDs, production health-check authority, or production sandbox claims.

Active boundary vocabulary:

- `HEALTH_CHECK_SANDBOX_SIDE_EFFECT_OBSERVATION_BOUNDARY`
- `RUNNER_TEMP_CONTAINMENT_OUTSIDE_REPO`
- `PYTHON_BYTECODE_CACHE_PER_RUN_OUTSIDE_REPO`
- `PROCESS_GROUP_TIMEOUT_CLEANUP_REQUIRED`
- `REPO_CACHE_ARTIFACT_OBSERVATION_REQUIRED`
- `GIT_STATUS_BEFORE_AFTER_OBSERVATION_REQUIRED`
- `OBSERVED_SIDE_EFFECTS_BLOCK_ADVISORY_PASS`
- `NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM`
- `NO_NETWORK_FIREWALL_CLAIM`
- `NO_HOST_SECRET_ISOLATION_CLAIM`
- `NO_NEW_PROFILE_IDS`
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

Persistent doctrine gate marker: BLK-SYSTEM-034 pins sandbox and side-effect observation only.

---

## 2. Preserved Fixed Profiles

BLK-036 preserves exactly the BLK-035 fixed profile set:

```text
git_status_short_branch
active_doctrine_gate
python_unittest_discovery
go_test_all
go_vet_all
```

No new profile IDs are authorized. Profiles remain selected by ID only. Caller-supplied argv and caller-supplied command strings remain forbidden and must fail closed before subprocess startup.

---

## 3. Authorized Observation Boundary

BLK-036 authorizes runner-owned temporary directories outside the repository for each profile run. These directories may carry `TMPDIR`, `TMP`, `TEMP`, and per-run Python bytecode cache state. The runner must report whether its runner-owned temporary directory was removed after completion.

BLK-036 authorizes repo-local cache artifact observation for `__pycache__` directories and `.pyc` files under the repository. Repo-local cache artifacts block advisory PASS when they appear or change during a profile run. The same rule is stated for gate clarity as: repo-local cache artifacts block advisory PASS. This observation supplements Git status before/after checks; it is not a proof of all possible source-byte side effects.

BLK-036 requires process-group timeout cleanup for the fixed profile subprocess when a timeout occurs. This is bounded local process hygiene only. It is not production process isolation, not a container boundary, and not a guarantee against every same-user host escape.

Observed side effects block advisory PASS. health-check PASS remains advisory operator context only.

---

## 4. Honest Sandbox Vocabulary

The BLK-SYSTEM-034 runner hardening is local advisory containment and observation. It does not claim production sandbox/cgroup/VM enforcement, Linux namespace enforcement, seccomp, AppArmor, SELinux, network firewall enforcement, or host-secret isolation. It does not claim to observe every filesystem, process, network, IPC, credential, kernel, or host side-effect surface.

Allowed result vocabulary may report observed surfaces such as:

- Git status changed or not changed;
- repo-local cache artifacts changed or not changed;
- runner-owned temp directory removed or not removed;
- process-group timeout cleanup attempted or not needed;
- explicit non-claims for network firewall, production sandbox, host-secret isolation, protected-vault body access, active-vault scanning, BEO publication, RTM generation, and drift decisions.

---

## 5. Explicit Non-Authorities

BLK-036 does not authorize arbitrary shell, caller-supplied commands, new profile IDs, network/API/model/cyber tooling, package-manager execution, browser automation, remote service access, dependency installation, or production health-check service/daemon behavior.

BLK-036 does not authorize Git mutation or source mutation. The runner must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, restore, edit files, delete files, or repair state.

BLK-036 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault path scans, runtime active-vault comparison, backend promotion, or requirement/use-case body inspection by the runner.

BLK-036 does not authorize production BLK-test MCP, new BLK-test smoke, BLK-pipe dispatch, live tactical LLM execution, Codex execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, or final drift decisions.

---

## 6. Stop Conditions

Stop and treat any proposed change as outside BLK-036 authority if it attempts to add a new profile ID, raw command execution, caller-supplied argv, shell invocation, inline code execution outside approved unittest module invocation, network/model/cyber/package tooling, Git/source mutation or repair, protected-vault body access, active-vault scans, BEO/RTM/drift/publication authority, BLK-pipe validation authority, production monitoring claims, or production sandbox/cgroup/VM/network/host-secret isolation claims.

---

## 7. Future Handoff

Future sprints may request isolated-workspace health-check execution or production health-check authority only through a fresh plan, explicit approval provenance, RED/GREEN tests, hostile review, and a new or amended boundary. BLK-036 does not authorize those future rungs.
