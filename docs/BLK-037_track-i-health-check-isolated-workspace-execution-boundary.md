# BLK-037 — Track I health-check isolated workspace execution boundary

**Status:** Active pilot boundary — optional local isolated-workspace advisory execution only
**Sprint:** BLK-SYSTEM-035
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L4 pilot runtime for local fixed profiles only; not L5 production authority

---

## 1. Purpose

BLK-037 records the BLK-SYSTEM-035 boundary for optional isolated-workspace execution by the BLK-034/BLK-035 advisory health-check runner after BLK-036 side-effect observation hardening. It authorizes only a runner-owned local workspace copy outside the source repository for eligible non-Git fixed profiles. It does not authorize new profile IDs, production health-check authority, BLK-test authority, or production sandbox claims.

Active boundary vocabulary:

- `HEALTH_CHECK_ISOLATED_WORKSPACE_EXECUTION_BOUNDARY`
- `ISOLATED_WORKSPACE_COPY_OUTSIDE_REPO`
- `SOURCE_REPO_NOT_EXECUTION_CWD`
- `PROTECTED_BLK_REQ_PATHS_EXCLUDED_FROM_COPY`
- `DOT_GIT_EXCLUDED_FROM_COPY`
- `SOURCE_REPO_STATUS_BEFORE_AFTER_OBSERVATION_REQUIRED`
- `SOURCE_REPO_CACHE_OBSERVATION_REQUIRED`
- `ISOLATED_WORKSPACE_REMOVAL_REQUIRED`
- `GIT_STATUS_PROFILE_SOURCE_REPO_ONLY`
- `NO_NEW_PROFILE_IDS`
- `NO_ARBITRARY_SHELL`
- `NO_NETWORK_MODEL_CYBER_TOOLING`
- `NO_PACKAGE_MANAGER`
- `NO_GIT_MUTATION`
- `NO_SOURCE_MUTATION`
- `NO_PROTECTED_BODY_READ`
- `NO_PROTECTED_BODY_COPY`
- `NO_ACTIVE_VAULT_SCAN`
- `NO_BEO_PUBLICATION`
- `NO_RTM_GENERATION`
- `NO_DRIFT_REJECTION`
- `NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM`
- `NO_NETWORK_FIREWALL_CLAIM`
- `NO_HOST_SECRET_ISOLATION_CLAIM`
- `NOT_PRODUCTION_HEALTH_CHECK_AUTHORITY`

Persistent doctrine gate marker: BLK-SYSTEM-035 pins isolated-workspace execution only.

---

## 2. Preserved Fixed Profiles

BLK-037 preserves exactly the BLK-035 fixed profile set:

```text
git_status_short_branch
active_doctrine_gate
python_unittest_discovery
go_test_all
go_vet_all
```

No new profile IDs are authorized. Profiles remain selected by ID only. Caller-supplied argv and caller-supplied command strings remain forbidden and must fail closed before subprocess startup.

Because the isolated workspace copy deliberately excludes `.git`, the `git_status_short_branch` profile is source-repository mode only. BLK-037 does not authorize copying `.git`, creating synthetic Git history, staging, committing, worktree creation, clone-based metadata setup, or Git repair as part of isolated health-check execution. A future sprint may define a separate safe Git-metadata fixture boundary if needed.

---

## 3. Authorized Isolated Workspace Boundary

BLK-037 authorizes an optional isolated-workspace mode for non-Git fixed profiles. In that mode, the runner may create a temporary workspace under its runner-owned temp directory outside the source repository and execute the profile with that isolated workspace as `cwd`. This satisfies `SOURCE_REPO_NOT_EXECUTION_CWD` for eligible profiles.

The isolated workspace copy must exclude `.git`, repo-local Python cache artifacts, and protected BLK-req path families including `docs/active/`, `docs/requirements/`, and `docs/use_cases/`. This exclusion is path-level copy avoidance only. It does not authorize reading, copying, parsing, hashing, summarizing, or comparing protected BLK-req bodies.

The runner must preserve source-repository observations before and after the isolated profile run:

- source repository Git status before/after observation;
- source repository repo-local cache observation;
- runner-owned isolated workspace removal observation.

If the source repository status or source repository cache artifact snapshot changes during isolated execution, advisory PASS is blocked. If the isolated workspace cannot be removed, advisory PASS is blocked. isolated workspace PASS remains advisory operator context only.

---

## 4. Honest Isolation Vocabulary

BLK-SYSTEM-035 isolated-workspace execution is a local copy/cwd separation, not an OS-level production sandbox. It does not claim production sandbox/cgroup/VM enforcement, Linux namespace enforcement, seccomp, AppArmor, SELinux, network firewall enforcement, host-secret isolation, kernel-level containment, or comprehensive host side-effect observation.

Allowed result vocabulary may report observed surfaces such as:

- source repository status changed or unchanged;
- source repository repo-local cache artifacts changed or unchanged;
- profile execution workspace mode;
- whether the execution `cwd` was the source repository or an isolated workspace;
- whether the isolated workspace path was inside the source repository;
- whether the isolated workspace was removed;
- explicit non-claims for network firewall, production sandbox, host-secret isolation, protected-vault body access, active-vault scanning, BEO publication, RTM generation, and drift decisions.

---

## 5. Explicit Non-Authorities

BLK-037 does not authorize arbitrary shell, caller-supplied commands, caller-supplied argv, new profile IDs, network/API/model/cyber tooling, package-manager execution, browser automation, remote service access, dependency installation, or production health-check service/daemon behavior.

BLK-037 does not authorize Git mutation or source mutation. The runner must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, restore, edit source files, delete source files, or repair source state. Any temporary-file cleanup authority is limited to runner-owned temporary directories outside the source repository.

BLK-037 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault path scans, runtime active-vault comparison, backend promotion, or requirement/use-case body inspection by the runner.

BLK-037 does not authorize production BLK-test MCP, new BLK-test smoke, BLK-pipe dispatch, live tactical LLM execution, Codex execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, or final drift decisions.

---

## 6. Stop Conditions

Stop and treat any proposed change as outside BLK-037 authority if it attempts to add a new profile ID, raw command execution, caller-supplied argv, shell invocation, inline code execution outside approved unittest module invocation, network/model/cyber/package tooling, `.git` copying, protected BLK-req path copying, Git/source mutation or repair, protected-vault body access, active-vault scans, BEO/RTM/drift/publication authority, BLK-pipe validation authority, production monitoring claims, or production sandbox/cgroup/VM/network/host-secret isolation claims.

---

## 7. Future Handoff

Future sprints may request a safe Git-metadata fixture for isolated `git_status_short_branch`, production health-check authority, or deeper OS-level sandbox/cgroup/namespace/network policy only through a fresh plan, explicit approval provenance, RED/GREEN tests, hostile review, and a new or amended boundary. BLK-037 does not authorize those future rungs.
