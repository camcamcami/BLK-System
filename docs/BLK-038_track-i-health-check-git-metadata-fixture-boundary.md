# BLK-038 — Track I health-check Git metadata fixture boundary

**Status:** Active pilot boundary — isolated Git metadata fixture advisory evidence only
**Sprint:** BLK-SYSTEM-036
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L4 pilot runtime for local fixed profiles only; not L5 production authority

---

## 1. Purpose

BLK-038 records the BLK-SYSTEM-036 boundary for safe isolated-mode `git_status_short_branch` evidence after BLK-SYSTEM-035 deliberately left that profile source-repository mode only. It authorizes only a source-bound, read-only Git metadata fixture command shape that runs from the runner-owned isolated workspace while pointing Git at the source repository through explicit `--git-dir` and `--work-tree` arguments.

Active boundary vocabulary:

- `HEALTH_CHECK_GIT_METADATA_FIXTURE_BOUNDARY`
- `GIT_STATUS_ISOLATED_METADATA_FIXTURE`
- `SOURCE_GIT_METADATA_READ_ONLY`
- `GIT_OPTIONAL_LOCKS_DISABLED`
- `GIT_STATUS_CWD_IS_ISOLATED_WORKSPACE`
- `GIT_DIR_AND_WORK_TREE_EXPLICIT`
- `DOT_GIT_NOT_COPIED`
- `SYNTHETIC_GIT_HISTORY_FORBIDDEN`
- `NO_CLONE_OR_WORKTREE_SETUP`
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

Persistent doctrine gate marker: BLK-SYSTEM-036 pins Git metadata fixture only.

---

## 2. Preserved Fixed Profiles

BLK-038 preserves exactly the BLK-035 fixed profile set:

```text
git_status_short_branch
active_doctrine_gate
python_unittest_discovery
go_test_all
go_vet_all
```

No new profile IDs are authorized. Profiles remain selected by ID only. Caller-supplied argv, caller-supplied commands, shell strings, network tools, package-manager tools, tactical model tools, and cyber tools remain forbidden and must fail closed before subprocess startup.

---

## 3. Authorized Git Metadata Fixture Shape

BLK-038 authorizes only this isolated-mode Git status shape for the existing `git_status_short_branch` profile:

1. create a runner-owned temporary directory outside the source repository;
2. create or reuse the filtered isolated workspace directory from BLK-037;
3. keep `.git`, protected BLK-req path families, repo-local cache artifacts, and symlinks excluded from the isolated copy;
4. execute the trusted absolute Git binary with a fixed argv equivalent to `git --git-dir <source>/.git --work-tree <source> status --short --branch`;
5. set `cwd` for that Git process to the isolated workspace, not to the source repository;
6. set `GIT_OPTIONAL_LOCKS=0` so status observation avoids optional lock writes;
7. set `shell=False` and preserve the existing bounded output, timeout, redaction, startup-failure, and process-group cleanup behavior;
8. continue source repository status/cache before/after observations and block advisory PASS if they change.

The fixture is a metadata-read path only. It may observe source Git status output and branch information. It must not copy `.git`, synthesize Git history, create a clone, create a worktree, initialize a repository, stage files, commit, push, reset, checkout, clean, revert, merge, rebase, switch, restore, repair source state, or delete source files.

---

## 4. Protected BLK-Req and Active-Vault Boundary

The isolated workspace copy must continue excluding:

```text
.git
docs/active
docs/requirements
docs/use_cases
```

BLK-038 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault comparisons, backend promotion, requirement/use-case body inspection, or runtime RTM drift decisions. The Git metadata fixture may report Git status metadata for the source repository; it must not open protected bodies to build that evidence.

---

## 5. Honest Isolation Vocabulary

BLK-SYSTEM-036 is a local pilot health-check boundary. It is not production health-check authority and not an OS-level production sandbox. Evidence may state that the Git status process `cwd` was the runner-owned isolated workspace and that `.git` was not copied. Evidence must not claim production sandbox/cgroup/VM enforcement, Linux namespace enforcement, seccomp, AppArmor, SELinux, network firewall enforcement, host-secret isolation, kernel-level containment, comprehensive host side-effect observation, or broad source non-mutation proof.

Allowed result vocabulary may include:

- `GIT_STATUS_ISOLATED_METADATA_FIXTURE`;
- `SOURCE_GIT_METADATA_READ_ONLY`;
- `GIT_STATUS_CWD_IS_ISOLATED_WORKSPACE`;
- `GIT_OPTIONAL_LOCKS_DISABLED`;
- `GIT_DIR_AND_WORK_TREE_EXPLICIT`;
- `DOT_GIT_NOT_COPIED`;
- source repository status/cache observation before and after execution;
- explicit non-claims for network firewall, production sandbox, host-secret isolation, protected-vault body access, active-vault scanning, BEO publication, RTM generation, and drift decisions.

health-check PASS remains advisory operator context only. It does not authorize BLK-pipe dispatch, BLK-test startup, BEO publication, RTM generation, drift rejection, protected-vault access, production monitoring, or production health-check service/daemon operation.

---

## 6. Explicit Non-Authorities

BLK-038 does not authorize arbitrary shell, caller-supplied commands, caller-supplied argv, new profile IDs, network/API/model/cyber tooling, package-manager execution, browser automation, remote service access, dependency installation, or production health-check service/daemon behavior.

BLK-038 does not authorize Git mutation or source mutation. The runner must not stage, commit, push, reset, checkout, stash, clean, revert, merge, rebase, switch, restore, edit source files, delete source files, synthesize Git history, clone, create worktrees, initialize repositories, or repair source state. Any temporary-file cleanup authority is limited to runner-owned temporary directories outside the source repository.

BLK-038 does not authorize protected BLK-req vault body reads, copying, parsing, hashing, summarizing, active-vault path scans, runtime active-vault comparison, backend promotion, or requirement/use-case body inspection by the runner.

BLK-038 does not authorize production BLK-test MCP, new BLK-test smoke, BLK-pipe dispatch, live tactical LLM execution, Codex execution, authoritative BEO publication, runtime `PUBLISHED` BEO output, publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, or final drift decisions.

---

## 7. Stop Conditions

Stop and treat any proposed change as outside BLK-038 authority if it attempts to add a new profile ID, raw command execution, caller-supplied argv, shell invocation, inline code execution, network/model/cyber/package tooling, `.git` copying, protected BLK-req path copying, clone/worktree/synthetic Git setup, Git/source mutation or repair, protected-vault body access, active-vault scans, BEO/RTM/drift/publication authority, BLK-pipe validation authority, production monitoring claims, or production sandbox/cgroup/VM/network/host-secret isolation claims.

---

## 8. Future Handoff

Future sprints may request production health-check authority, deeper OS-level sandbox/cgroup/namespace/network policy, or broader Git evidence only through a fresh plan, explicit approval provenance, RED/GREEN tests, hostile review, and a new or amended boundary. BLK-038 does not authorize those future rungs.
