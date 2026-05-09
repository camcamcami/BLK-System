# BLK-040 — Codex deterministic invocation profile boundary

**Status:** Active fixture boundary — deterministic Codex invocation profile construction only
**Sprint:** BLK-SYSTEM-038
**BLK-024 track:** Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening; Track C — BLK-pipe blast shield and forge
**Maturity:** BLK-024 L1 fixture/local implementation plus L0 doctrine boundary; not L5 production authority

---

## 1. Purpose

BLK-040 records the BLK-SYSTEM-038 boundary for repository-owned deterministic Codex invocation profile construction. It captures the include-now Codex CLI profile shape for future BLK/Hermes tactical-engine compatibility while preserving BLK-System separation of authority: Hermes plans and audits, Codex remains an untrusted tactical engine, BLK-pipe remains the mutation enforcement authority, BLK-test remains separately governed evidence, and BLK-link trace closure remains separate from profile construction.

BLK-040 does not authorize live Codex execution, live tactical LLM execution, BLK-pipe dispatch, production BLK-test MCP, source mutation, Git mutation, package-manager execution, network/model/cyber tooling, protected BLK-req vault body reads, BEO publication, RTM generation, drift rejection, or production sandbox claims. The profile builder may construct dictionaries and argv arrays only. It must not start subprocesses, run `codex`, inspect user Codex configuration, create directories, read artifact bodies, mutate files, or treat telemetry as canonical evidence.

Active boundary vocabulary:

- `CODEX_DETERMINISTIC_INVOCATION_PROFILE_FIXTURE_ONLY`
- `CODEX_AMBIENT_FEATURES_DISABLED`
- `CODEX_PROFILE_BUILDER_STARTS_NO_SUBPROCESS`
- `CODEX_JSONL_EVENTS_ADVISORY_ONLY`
- `CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY`
- `CODEX_NATIVE_SANDBOX_NOT_TRUSTED_ON_THIS_HOST`
- `CODEX_PROFILE_GRANTS_NO_EXECUTION_AUTHORITY`
- `NO_LIVE_CODEX_EXECUTION_AUTHORITY`
- `NO_BLK_PIPE_DISPATCH_AUTHORITY`
- `NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY`
- `NO_PROTECTED_BODY_READ`
- `NO_PROTECTED_BODY_COPY`
- `NO_ACTIVE_VAULT_SCAN`
- `NO_BEO_PUBLICATION`
- `NO_RTM_GENERATION`
- `NO_DRIFT_REJECTION`
- `NO_NETWORK_MODEL_CYBER_TOOLING`
- `NO_PACKAGE_MANAGER`
- `NO_GIT_MUTATION`
- `NO_SOURCE_MUTATION`
- `NO_PRODUCTION_SANDBOX_CGROUP_VM_CLAIM`
- `NO_NETWORK_FIREWALL_CLAIM`
- `NO_HOST_SECRET_ISOLATION_CLAIM`

Persistent doctrine gate marker: BLK-SYSTEM-038 pins Codex deterministic invocation profile fixture-only scope.

---

## 2. Deterministic Profile Shape

The deterministic local Codex profile fixture must include the following argv properties when it builds the profile for a future explicitly approved tactical packet:

```text
codex exec
--model <approved-model>
-C <worktree>
-s danger-full-access
-a never
--ephemeral
--ignore-user-config
--ignore-rules
--disable hooks
--disable plugins
--disable goals
--json
--output-last-message <relative-artifact-path>
```

`danger-full-access` is recorded only as a local host workaround because this host's Codex native Linux sandbox still fails with the known bubblewrap/RTM_NEWADDR class. It is not production sandbox authority, not a security claim, and not permission to execute Codex without separate dispatch approval and hostile audit.

The deterministic profile suppresses hidden user configuration and rules with `--ignore-user-config` and `--ignore-rules`, requests an ephemeral session with `--ephemeral`, disables ambient Codex feature surfaces with `--disable hooks`, `--disable plugins`, and `--disable goals`, emits JSONL telemetry with `--json`, and writes the final assistant message to a bounded relative artifact path with `--output-last-message`.

---

## 3. Advisory Telemetry Only

Codex JSONL events are `CODEX_JSONL_EVENTS_ADVISORY_ONLY`. Final-message artifacts are `CODEX_FINAL_MESSAGE_ARTIFACT_ADVISORY_ONLY`. They may help future operator observability, but they are not canonical proof of mutation safety, validation success, approval, trace closure, BEO publication, RTM generation, or drift status.

Canonical physical evidence remains external: Git diff, exact allowed-file checks, BLK-pipe enforcement, BLK-test evidence where separately authorized, and hostile review under the relevant dispatch envelope.

---

## 4. Builder Restrictions

A valid `CODEX_DETERMINISTIC_INVOCATION_PROFILE_FIXTURE_ONLY` helper may:

1. accept explicit scalar inputs such as approved model, worktree path, relative final-message artifact path, and bounded prompt text;
2. construct a deterministic argv list;
3. return a structured dictionary recording advisory capability flags and non-authority markers;
4. validate that required flags and ambient disables are present; and
5. validate that caller-supplied extras do not expand authority.

The helper must preserve `CODEX_PROFILE_BUILDER_STARTS_NO_SUBPROCESS` and must not import or call subprocess helpers, shell helpers, Git helpers, network clients, browser tools, package managers, BLK-pipe, BLK-test, BEO tooling, RTM tooling, protected-vault readers, model APIs, or Codex itself.

---

## 5. Rejection Surface

The profile builder and validation fixture must fail closed if a caller attempts to:

- remove `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, `--json`, or `--output-last-message`;
- omit or re-enable disabled ambient features for hooks, plugins, or goals;
- add unsupported Codex flags, shell wrappers, aliases, plugin/hook/goal flags, MCP/server flags, network/package-manager/browser/cyber tooling, or `--dangerously-bypass-approvals-and-sandbox`;
- use absolute final-message artifact paths, parent-directory traversal, protected vault paths, `.git` paths, active-vault paths, or artifact paths outside the approved relative artifact root;
- launder production sandbox, firewall, VM, cgroup, namespace, seccomp, AppArmor, SELinux, network-denial, or host-secret isolation claims;
- claim live Codex execution authority, BLK-pipe dispatch authority, production BLK-test MCP authority, BEO publication, RTM generation, drift rejection, signer/storage/ledger authority, approval capture, or protected BLK-req body access; or
- treat Codex PASS-like wording, JSONL events, or final messages as approval, canonical validation, trace closure, mutation proof, publication proof, or drift decision.

Forbidden authority fields must fail closed even when nested in metadata or evidence containers. Dropping dangerous fields silently is not allowed.

---

## 6. Explicit Non-Authorities

BLK-040 does not authorize live tactical LLM execution, live Codex execution, reusable runtime dispatch, production BLK-test MCP, arbitrary shell, network/API/model/cyber tooling, browser automation, remote service access, dependency installation, package-manager execution, source mutation, Git mutation, protected BLK-req vault body reads/copying/parsing/hashing/summarizing, active-vault path scans, BLK-req staging or promotion, BLK-pipe execution, BEO publication, RTM generation, RTM drift rejection, signer key access, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, or final drift decisions.

BLK-040 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, host-secret isolation, kernel containment, or comprehensive host side-effect observation. The `-s danger-full-access` flag is a host workaround inside an external audit envelope, not a trusted sandbox.

---

## 7. Stop Conditions

Stop and treat any proposed change as outside BLK-040 authority if it executes Codex, starts a subprocess, reads Codex configuration or user rules, fetches network resources, installs packages, invokes BLK-pipe or BLK-test, mutates source, calls Git, creates worktrees, reads protected vault bodies, copies active-vault content, publishes BEOs, generates RTMs, decides drift, captures approval, grants production authority, or converts Codex telemetry into canonical evidence.

---

## 8. Future Handoff

Future work may wire this deterministic profile into an explicit dispatch plan only after a separate sprint defines approval provenance, file-boundary enforcement, sandbox/containment evidence, validation gates, telemetry storage, hostile review, failure ceilings, rollback behavior, and operator escalation. This BLK-040 fixture boundary alone grants no execution authority.
