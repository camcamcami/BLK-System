# BLK-042 — Codex live-dispatch readiness gate boundary

**Status:** Active fail-closed fixture boundary — Codex live-dispatch readiness gate only
**Sprint:** BLK-SYSTEM-040
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L1 fixture/local implementation plus L2 disabled/fail-closed transport semantics; not L5 production authority

---

## 1. Purpose

BLK-042 records the BLK-SYSTEM-040 boundary for a fail-closed Codex live-dispatch readiness gate. It follows BLK-040 and BLK-041 by defining the local readiness evidence that must exist before a later human-approved sprint can even review a live Codex dispatch authority request.

BLK-042 does not authorize live Codex execution, runtime dispatch, BLK-pipe invocation, production BLK-test MCP, source mutation, Git mutation, package-manager execution, network/model/cyber tooling, protected BLK-req vault body reads, BEO publication, RTM generation, drift rejection, or production sandbox claims. The readiness gate helper may construct, validate, and evaluate dictionaries only. It must not start subprocesses, call `codex`, call Git, create worktrees, call BLK-pipe, inspect user Codex configuration, create directories, read artifact bodies, mutate files, or treat readiness as execution approval.

Active boundary vocabulary:

- `CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY`
- `CODEX_LIVE_DISPATCH_GATE_FAILS_CLOSED`
- `CODEX_LIVE_DISPATCH_GATE_STARTS_NO_SUBPROCESS`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_RUNTIME_APPROVAL`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_BLK_PIPE_WIRING_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_CONTAINMENT_EVIDENCE`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_VALIDATION_EXECUTION_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_TELEMETRY_PERSISTENCE_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_ROLLBACK_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_MONITORING_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_OPERATOR_CONTROLS`
- `CODEX_LIVE_DISPATCH_GATE_GRANTS_NO_EXECUTION_AUTHORITY`
- `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION`
- `BLOCKED_NOT_AUTHORIZED`
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

Persistent doctrine gate marker: BLK-SYSTEM-040 pins Codex live-dispatch readiness gate fail-closed non-execution scope.

---

## 2. Required Readiness Evidence

A valid `CODEX_LIVE_DISPATCH_READINESS_GATE_FIXTURE_ONLY` record must preserve all of the following before a later sprint may request live execution authority review:

1. a valid BLK-040 deterministic invocation profile fixture;
2. a valid BLK-041 deterministic dispatch envelope fixture;
3. runtime approval provenance for review only;
4. BLK-pipe wiring plan;
5. containment evidence;
6. validation execution plan;
7. telemetry persistence plan;
8. rollback plan;
9. monitoring plan;
10. operator controls;
11. failure ceiling metadata;
12. hostile audit checklist;
13. replay state for runtime approval IDs and readiness run IDs;
14. explicit false non-authority flags.

The gate must return `BLOCKED_NOT_AUTHORIZED` whenever any required section is missing, malformed, stale, expired, replayed, broad, or authority-bearing.

---

## 3. Runtime Approval Rules

BLK-042 makes `CODEX_LIVE_DISPATCH_GATE_REQUIRES_RUNTIME_APPROVAL` an active fixture requirement. Runtime approval in this sprint is a local review prerequisite only. It is not execution approval, not BLK-pipe dispatch approval, not BLK-test approval, not BEO publication approval, not RTM generation approval, and not drift rejection approval.

Runtime approval evidence must record source system, operator identity, message/event ID, timestamp, expiry, exact approved review scope, runtime approval ID, and explicit excluded authorities. It must fail closed when missing, expired, replayed, scope-mismatched, or carrying execution-authority wording.

`READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION` means only that a later human-approved authority sprint has enough prerequisite evidence to review. It must not be shortened or mapped to `READY_FOR_EXECUTION`.

---

## 4. Required Prerequisite Plans

BLK-042 makes each of the following an active fail-closed prerequisite:

- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_BLK_PIPE_WIRING_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_CONTAINMENT_EVIDENCE`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_VALIDATION_EXECUTION_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_TELEMETRY_PERSISTENCE_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_ROLLBACK_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_MONITORING_PLAN`
- `CODEX_LIVE_DISPATCH_GATE_REQUIRES_OPERATOR_CONTROLS`

Each prerequisite is evidence for review only. None may contain live dispatch commands, subprocess startup claims, package-manager commands, network/model/cyber/browser tooling, protected-vault body access, BEO publication, RTM generation, drift rejection, or production sandbox claims.

---

## 5. Builder Restrictions

The readiness gate helper must preserve `CODEX_LIVE_DISPATCH_GATE_STARTS_NO_SUBPROCESS` and must not import or call subprocess helpers, shell helpers, Git helpers, network clients, browser tools, package managers, BLK-pipe, BLK-test, BEO tooling, RTM tooling, protected-vault readers, model APIs, or Codex itself.

The helper may validate BLK-040 profile fixtures, BLK-041 dispatch envelope fixtures, runtime approval dictionaries, prerequisite evidence dictionaries, failure ceiling metadata, hostile audit checklist entries, and operator controls. It may return human-readable blocked reasons and escalation hints.

---

## 6. Explicit Non-Authorities

BLK-042 does not authorize live tactical LLM execution, live Codex execution, reusable runtime dispatch, BLK-pipe execution, production BLK-test MCP, arbitrary shell, network/API/model/cyber tooling, browser automation, remote service access, dependency installation, package-manager execution, source mutation, Git mutation, protected BLK-req vault body reads/copying/parsing/hashing/summarizing, active-vault path scans, BLK-req staging or promotion, BEO publication, RTM generation, RTM drift rejection, signer key access, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, or final drift decisions.

BLK-042 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, host-secret isolation, kernel containment, or comprehensive host side-effect observation. Any readiness evidence about containment is review evidence only and cannot become a production sandbox claim.

---

## 7. Stop Conditions

Stop and treat any proposed change as outside BLK-042 authority if it executes Codex, starts a subprocess, invokes BLK-pipe, calls Git, creates worktrees, fetches network resources, installs packages, mutates source, reads Codex configuration or user rules, reads protected vault bodies, copies active-vault content, publishes BEOs, generates RTMs, decides drift, grants production authority, or converts readiness evidence into execution approval.

---

## 8. Future Handoff

Future work may use this readiness gate in an explicit live-dispatch authority request only after a separate sprint asks for and receives authority to run Codex through BLK-pipe under a bounded approval envelope. BLK-042 alone grants no execution authority.
