# BLK-011 — BLK-pipe Cyber Readiness and Usability Guardrails

**Status:** Active Sprint 002.2 operator guidance
**Scope:** `blk-pipe` security guardrails, diagnostics, and cyber-use boundaries
**Date:** 2026-05-04

---

## 1. Boundary Statement

BLK-pipe is a deterministic local transport, repository mutation gate, and commit/revert controller. It is not a tactical LLM runner, not a malware-analysis environment, not a network isolation layer, and not an operating-system containment boundary.

Sprint 002.2 does not run Codex. It does not call live LLM APIs, live tactical engines, or offensive cyber tooling. Sprint 002.2 only hardens local fake-engine and deterministic-tool workflows around the repository blast shield.

**BLK-pipe is not a complete sandbox.** Treat it as a repository safety guard, not as a substitute for a container, VM, cgroup policy, seccomp/AppArmor/SELinux profile, network namespace, secret manager, or host-level process isolation.

---

## 2. Operational Profiles

These profiles describe intended operating modes. They are guidance only; Sprint 002.2 does not implement profile selection.

| Profile | Intended use | Required operator posture |
|---|---|---|
| `dev-smoke` | Local fake-engine work only. | Verbose diagnostics are acceptable. Use no live secrets. Use disposable local fixtures when testing strict failures. |
| `strict-ci` | Ephemeral clean clone with fake or deterministic local tools. | Start from no pre-existing residue, pass a minimal non-secret environment, and fail closed on any dirty preflight or unauthorized mutation. |
| `codex-dry-run` | Fake/dry-run parity fixtures for Codex command shape. | No live model call, no Codex API invocation, and deterministic fixture output only. |
| `codex-live` | Future live Codex tactical execution profile. | Not implemented or authorized in Sprint 003. codex-live requires explicit user approval plus sandbox/capability decisions before any live use. |
| `cyber-execution` | Future live cyber-capable execution profile. | Not implemented in Sprint 002.2 or Sprint 003. cyber-execution requires a future sandbox boundary with container/VM/cgroup/process/network/filesystem/secret controls before live use. |

Sprint 003 does not run Codex, does not authorize live LLM execution, and does not authorize cyber execution. See [`BLK-012 — BLK-pipe Integration Readiness and Capability Profiles`](BLK-012_blk-pipe-integration-readiness-and-capability-profiles.md) for the Sprint 003 profile boundary document. BLK-pipe is not a full sandbox and does not provide general host-secret isolation.

Do not treat `dev-smoke`, `strict-ci`, or `codex-dry-run` as permission to run real cyber-program repositories, offensive tooling, live targets, live model calls, or live secrets through BLK-pipe.

---

## 3. Clean Preflight Is Mandatory

BLK-pipe expects the target repository to be clean before destructive execute or revert behavior. Clean preflight rejects tracked dirt, untracked files, ignored files, nested `.git` residue, and empty directory residue that Git would otherwise fail to report as normal tracked changes.

Operator guidance:

1. Inspect the failure report, especially `status`, `error`, `untracked_files`, and `destroyed_files`.
2. Decide whether each path is legitimate local residue or a real safety signal.
3. Remove legitimate local residue outside BLK-pipe with ordinary Git/worktree hygiene, for example by deleting a temp directory or using a fresh clone.
4. Re-run from a clean repository.

**do not bypass clean preflight** by broadening allowlists, hiding files under `.gitignore`, changing production code to ignore residue, or running BLK-pipe in a dirty worktree. For `strict-ci`, prefer an ephemeral clone so pre-existing untracked/ignored/empty directory residue is impossible by construction.

BLK-req active vault candidates are protected repository-law paths, not tactical execution targets. Do not allowlist `docs/active/`, `docs/requirements/`, or `docs/use_cases/` for BLK-pipe engine writes. If a BLK-req artifact needs revision, use the HITL/staged revision path that preserves canonical hashes instead of direct tactical mutation of the active vault.

---

## 4. Validation Commands Are Read-Only Gates

In Sprint 002.2, **validation commands are read-only gates** relative to the candidate production diff produced by the engine. They may inspect, compile, test, lint, and write to external caches or temporary directories, but they must not author or modify production worktree files and must not mutate `.git`.

If validation attempts to mutate production files, BLK-pipe reports `UNAUTHORIZED_FILE_MUTATION`, records actionable paths in `destroyed_files` when available, restores the run where possible, and does not create a success commit. Fix the validation command so it reads the worktree without rewriting it. Examples include redirecting formatter output to a temp path, using a check/diff mode instead of a write mode, or pre-configuring tool caches outside the repository.

If validation attempts to mutate `.git`, BLK-pipe also treats that as `UNAUTHORIZED_FILE_MUTATION`. `.git` changes are repository-control changes, not candidate product changes. Fix the command by disabling hook installation, commit/config writes, index edits, or tool behavior that initializes nested repository state during validation.

Do not convert validation commands into hidden second engines. If a file must be produced, list it as an engine output in the payload allowlist and have the engine produce it before validation begins.

Validation work is also payload-bounded. BLK-pipe accepts at most 16 validation commands, rejects command strings over 4096 bytes without echoing the long command body, and gives the entire validation phase one overall `timeout_seconds` window after engine success. This preserves validation as a deterministic read-only gate instead of allowing many payload commands to multiply local work.

---

## 5. Generated File Modes and Parent Directory Modes

Git stores only a narrow subset of mode information for regular files, but the physical worktree can contain unsafe mode bits that matter to local operators. Sprint 002.2 rejects unsafe generated file modes and unsafe parent directory modes for newly allowed files.

Rejected examples include:

- regular generated files with private or unexpected modes such as `0600` when the safe generated-file modes are `0644` or `0755`,
- setuid or setgid bits on generated files,
- sticky or world-writable generated parent directories such as `1777`,
- generated parent paths that are not safe directories,
- unsupported physical residue such as FIFOs or special files.

The failure is reported as `UNAUTHORIZED_FILE_MUTATION`; paths appear in `destroyed_files` when available. To fix a legitimate workflow, make the engine create ordinary files with `0644`, executable scripts with `0755`, and newly created parent directories with `0755`. Do not loosen the mode guard. Do not hide unsafe modes by committing from outside BLK-pipe.

---

## 6. Post-Return Process Safety Expectations

Sprint 002.2 makes a best-effort cleanup pass on timeout, output flood, and context cancellation paths before BLK-pipe returns. On Linux this includes the original process group, visible descendants, inherited stdout/stderr pipe holders, and visible descendants of those pipe holders. Darwin has a reduced process-tree/process-group capability.

This is a process-lifetime safety expectation for BLK-pipe-owned local subprocesses; it is not proof that arbitrary fully detached daemons are impossible on the host. Operators should use short-lived fake engines, deterministic local tools, and disposable repositories. Live cyber execution still requires an external sandbox boundary before use.

---

## 7. `l2_packet` Transport and Logging

`l2_packet is delivered to engine stdin` when present in the payload. BLK-pipe transports it as input to the bounded local engine; BLK-pipe does not parse it as an autonomous decision and does not pass it through command-line arguments or environment variables.

`l2_packet is bounded and not logged by default`. Sprint 002.2 rejects oversized packet input before engine execution and avoids echoing the packet body into report fields by default. Operators must still avoid placing live secrets in `l2_packet` during Sprint 002.2 because engine behavior, shell scripts, and downstream tools can choose to print stdin themselves.

For `dev-smoke`, use fake packets with no secrets. For `strict-ci`, use deterministic non-secret packets. For future `cyber-execution`, packet handling must be part of the future sandbox and secret-control design.

---

## 8. Host-Secret Limitation

BLK-pipe scrubs Git and SSH control variables from subprocess environments, including Git configuration controls and common SSH agent/askpass variables. This reduces accidental Git/SSH credential inheritance for BLK-pipe subprocesses.

**BLK-pipe does not provide general host-secret isolation.** It does not automatically remove every environment variable that might contain a token, prevent reads of files in the operator account, isolate OS keychains, restrict network egress, or stop an arbitrary local command from reading host-accessible secrets. Use a minimal non-secret environment for `strict-ci`, and reserve live secrets for a future profile with an actual sandbox/secret boundary.

---

## 9. Why BLK-pipe Is Not a Full Cyber Sandbox

BLK-pipe controls repository mutation and bounded local command execution. A full cyber sandbox would also need explicit controls for at least:

- filesystem mount scope and writable paths,
- process namespaces, cgroups, and descendant containment beyond best-effort cleanup,
- network egress/ingress policy,
- secret injection and revocation,
- syscall or capability filtering,
- artifact export policy,
- audit logging designed for hostile payloads,
- separate handling for malware, exploit tooling, and live target interaction.

Sprint 002.2 intentionally does not implement those controls. Therefore BLK-pipe can support local defensive development guardrails, but **cyber-execution requires a future sandbox boundary** before live use.

---

## 10. Safe Operator Response Matrix

| Failure class | What happened | Safe fix | Unsafe response |
|---|---|---|---|
| Pre-existing untracked/ignored/empty directory residue | The repo was dirty before BLK-pipe could trust rollback semantics. | Remove residue, use a fresh clone, or move local scratch files outside the repo. | Bypass preflight, hide files in `.gitignore`, or expand allowlists. |
| Validation mutated production files | A validation command authored or rewrote candidate worktree content. | Change the command to check-only mode or move generated output into the engine phase with explicit allowlists. | Treat validation as a second writer. |
| Validation mutated `.git` | A command changed repository control state. | Disable hook/config/index/repository writes during validation. | Allow `.git` paths or run with host Git state exposed. |
| Unsafe generated modes | A generated file or new parent directory has unsafe chmod/type state. | Create `0644` files, `0755` executable files/directories, and no setuid/setgid/sticky bits. | Commit unsafe physical modes outside BLK-pipe. |
| Timeout/flood/cancel | BLK-pipe stopped an engine path and performed best-effort process cleanup. | Inspect report, fix runaway local fake-engine behavior, rerun cleanly. | Assume this is a host sandbox for arbitrary detached daemons. |
| Packet rejected | `l2_packet` exceeded the configured bound. | Send a smaller deterministic non-secret packet or pass large artifacts by an explicit safe file workflow. | Put secrets in packets or rely on logs to hide engine-printed stdin. |

These guardrails are deliberately strict so legitimate local failures are repairable without weakening the repository blast shield.
