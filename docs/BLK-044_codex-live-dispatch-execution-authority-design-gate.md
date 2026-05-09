# BLK-044 — Codex live-dispatch execution authority design gate

**Status:** Active design/fixture boundary — Codex live-dispatch execution-authority design gate only
**Sprint:** BLK-SYSTEM-042
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L0 doctrine boundary plus L1 fixture/local implementation; not L5 production authority

---

## 1. Purpose

BLK-044 records the BLK-SYSTEM-042 boundary for a review-only Codex live-dispatch execution authority design gate. It follows BLK-040, BLK-041, BLK-042, and BLK-043 by defining the evidence contracts that a later sprint would need before requesting live Codex execution through BLK-pipe. BLK-044 can represent design readiness for review only; design readiness does not mean execution approval.

BLK-044 does not authorize live Codex execution, runtime dispatch, BLK-pipe invocation, production BLK-test MCP, source mutation, Git mutation, package-manager execution, network/model/cyber tooling, protected BLK-req vault body reads, BEO publication, RTM generation, drift rejection, or production sandbox claims. The design-gate helper may construct, validate, and evaluate dictionaries only. It must not start subprocesses, call `codex`, call Git, create worktrees, call BLK-pipe, inspect user Codex configuration, create directories, read artifact bodies, mutate files, or treat design readiness as execution approval.

Active boundary vocabulary:

- `CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_GATE_FAILS_CLOSED`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_AUTHORITY_REQUEST_PACKAGE`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_APPROVAL_ENVELOPE_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_BLK_PIPE_INTEGRATION_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_CONTAINMENT_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_TELEMETRY_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_ROLLBACK_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_MONITORING_OPERATOR_CONTROL_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_FAILURE_CEILING_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_REPLAY_PROTECTION_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_HOSTILE_AUDIT_CONTRACT`
- `CODEX_EXECUTION_AUTHORITY_DESIGN_GRANTS_NO_EXECUTION_AUTHORITY`
- `EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION`
- `EXECUTION_AUTHORITY_DESIGN_BLOCKED`
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

Persistent doctrine gate marker: BLK-SYSTEM-042 pins Codex live-dispatch execution-authority design-gate non-execution scope.

---

## 2. Required Design-Gate Evidence

A valid `CODEX_LIVE_DISPATCH_EXECUTION_AUTHORITY_DESIGN_GATE_FIXTURE_ONLY` record must preserve all of the following before a later sprint may request any live execution authority:

1. a valid BLK-043 authority request package with `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION`;
2. an approval envelope contract describing source system, operator identity, expiry, exact approved scope, explicit exclusions, replay state, and separation from runtime approval;
3. a BLK-pipe integration contract describing how Go `blk-pipe` remains the final mutation and validation enforcement authority;
4. a containment contract describing expected isolation evidence without claiming production sandbox, network firewall, or host-secret isolation enforcement;
5. a telemetry contract describing bounded event, final-message, report, and blocked-reason persistence without granting canonical mutation evidence;
6. a rollback contract describing cleanup, revert, abort, and operator escalation expectations without executing rollback;
7. a monitoring/operator controls contract describing kill switch, status, escalation, and stop conditions;
8. a failure ceiling contract describing iteration limits, retry ceilings, and mandatory escalation;
9. a replay protection contract describing one-run IDs, approval IDs, and stale/replayed request rejection;
10. a hostile audit contract describing authority non-expansion, side-effect, protected-vault, telemetry, rollback, and containment review checks;
11. explicit false non-authority flags.

The design gate must be rejected or evaluated as `EXECUTION_AUTHORITY_DESIGN_BLOCKED` whenever any required section is missing, malformed, stale, expired, replayed, broad, side-effect-bearing, or authority-bearing.

---

## 3. Review-Only Design Contract Rules

BLK-044 makes `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_APPROVAL_ENVELOPE_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_BLK_PIPE_INTEGRATION_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_CONTAINMENT_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_TELEMETRY_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_ROLLBACK_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_MONITORING_OPERATOR_CONTROL_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_FAILURE_CEILING_CONTRACT`, `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_REPLAY_PROTECTION_CONTRACT`, and `CODEX_EXECUTION_AUTHORITY_DESIGN_REQUIRES_HOSTILE_AUDIT_CONTRACT` active fixture requirements.

These are review-only design contracts. They are not execution approval, not BLK-pipe dispatch approval, not BLK-test approval, not BEO publication approval, not RTM generation approval, and not drift rejection approval.

`EXECUTION_AUTHORITY_DESIGN_READY_FOR_REVIEW_NOT_EXECUTION` means only that a later operator may review a design-gate package. It must not be shortened or mapped to `READY_FOR_EXECUTION`, `APPROVED_FOR_LIVE_EXECUTION`, or `AUTHORIZED_FOR_LIVE_EXECUTION`.

---

## 4. Builder Restrictions

The execution-authority design-gate helper must not import or call subprocess helpers, shell helpers, Git helpers, network clients, browser tools, package managers, BLK-pipe, BLK-test, BEO tooling, RTM tooling, protected-vault readers, model APIs, or Codex itself.

The helper may validate BLK-043 authority-request records, review-only contract dictionaries, bounded request metadata, false side-effect flags, failure ceiling metadata, replay protection metadata, hostile audit checklist entries, and operator escalation cases. It may return human-readable blocked reasons and escalation hints.

---

## 5. Explicit Non-Authorities

BLK-044 does not authorize live tactical LLM execution, live Codex execution, reusable runtime dispatch, BLK-pipe execution, production BLK-test MCP, arbitrary shell, network/API/model/cyber tooling, browser automation, remote service access, dependency installation, package-manager execution, source mutation, Git mutation, protected BLK-req vault body reads/copying/parsing/hashing/summarizing, active-vault path scans, BLK-req staging or promotion, BEO publication, RTM generation, RTM drift rejection, signer key access, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, or final drift decisions.

BLK-044 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, host-secret isolation, kernel containment, or comprehensive host side-effect observation. Any containment contract remains review-only.

---

## 6. Stop Conditions

Stop and treat any proposed change as outside BLK-044 authority if it executes Codex, starts a subprocess, invokes BLK-pipe, calls Git, creates worktrees, fetches network resources, installs packages, mutates source, reads Codex configuration or user rules, reads protected vault bodies, copies active-vault content, publishes BEOs, generates RTMs, decides drift, grants production authority, converts design-gate evidence into execution approval, or turns the disabled adapter into a live adapter.

---

## 7. Future Handoff

Future work may request explicit live Codex dispatch authority only through a separate sprint that explicitly grants runtime execution through BLK-pipe under a bounded approval envelope and fresh hostile review. BLK-044 alone grants no execution authority.
