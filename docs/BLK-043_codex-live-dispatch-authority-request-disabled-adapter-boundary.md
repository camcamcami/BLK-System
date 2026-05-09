# BLK-043 — Codex live-dispatch authority request disabled adapter boundary

**Status:** Active disabled/fail-closed boundary — Codex live-dispatch authority request package and disabled adapter only
**Sprint:** BLK-SYSTEM-041
**BLK-024 track:** Track A — Doctrine, alignment, and review gates; Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L2 disabled/fail-closed transport with L1 fixture evidence and L0 doctrine boundary; not L5 production authority

---

## 1. Purpose

BLK-043 records the BLK-SYSTEM-041 boundary for a review-only Codex live-dispatch authority request package and a disabled/fail-closed adapter fixture. It follows BLK-040, BLK-041, and BLK-042 by packaging invocation-profile, dispatch-envelope, and readiness-gate evidence for later human review while refusing any actual live dispatch. The request can represent ready review evidence only; ready review does not mean execution approval.

BLK-043 does not authorize live Codex execution, runtime dispatch, BLK-pipe invocation, production BLK-test MCP, source mutation, Git mutation, package-manager execution, network/model/cyber tooling, protected BLK-req vault body reads, BEO publication, RTM generation, drift rejection, or production sandbox claims. The authority-request helper may construct, validate, and evaluate dictionaries only. The disabled adapter may return blocked metadata only. It must not start subprocesses, call `codex`, call Git, create worktrees, call BLK-pipe, inspect user Codex configuration, create directories, read artifact bodies, mutate files, or treat review readiness as execution approval.

Active boundary vocabulary:

- `CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY`
- `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FIXTURE_ONLY`
- `CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_READY_REVIEW`
- `CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_SEPARATE_HUMAN_GRANT`
- `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FAILS_CLOSED`
- `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_STARTS_NO_SUBPROCESS`
- `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_CODEX`
- `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_BLK_PIPE`
- `CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_GRANTS_NO_EXECUTION_AUTHORITY`
- `AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION`
- `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED`
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

Persistent doctrine gate marker: BLK-SYSTEM-041 pins Codex live-dispatch authority request disabled-adapter non-execution scope.

---

## 2. Required Authority Request Evidence

A valid `CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_FIXTURE_ONLY` record must preserve all of the following before a later sprint may request live execution authority:

1. a valid BLK-042 readiness gate record with `READY_FOR_AUTHORITY_REVIEW_NOT_EXECUTION`;
2. embedded BLK-041 dispatch envelope and BLK-040 invocation profile evidence through that readiness record;
3. separate human grant metadata for review only;
4. exact authority request scope;
5. explicit excluded authorities;
6. failure ceiling metadata;
7. hostile audit checklist;
8. operator escalation cases;
9. replay state for authority request IDs and human grant IDs;
10. explicit false non-authority flags;
11. disabled adapter blocked status.

The request must be rejected or evaluated as `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED` whenever any required section is missing, malformed, stale, expired, replayed, broad, or authority-bearing.

---

## 3. Separate Human Grant Rules

BLK-043 makes `CODEX_LIVE_DISPATCH_AUTHORITY_REQUEST_REQUIRES_SEPARATE_HUMAN_GRANT` an active fixture requirement. Separate human grant metadata in this sprint is still review-only. It is not execution approval, not BLK-pipe dispatch approval, not BLK-test approval, not BEO publication approval, not RTM generation approval, and not drift rejection approval.

A valid review grant must record source system, operator identity, message/event ID, timestamp, expiry, exact approved review scope, grant ID, and explicit excluded authorities. It must fail closed when missing, expired, replayed, scope-mismatched, or carrying execution-authority wording.

`AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_EXECUTION` means only that a later operator may review a package. It must not be shortened or mapped to `READY_FOR_EXECUTION` or `APPROVED_FOR_LIVE_EXECUTION`.

---

## 4. Disabled Adapter Contract

The disabled adapter fixture is mandatory. It proves `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_FAILS_CLOSED`, `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_STARTS_NO_SUBPROCESS`, `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_CODEX`, and `CODEX_LIVE_DISPATCH_DISABLED_ADAPTER_CALLS_NO_BLK_PIPE`.

The only acceptable adapter result is `DISABLED_ADAPTER_BLOCKED_NOT_AUTHORIZED`. It may include operator-facing blocked reasons and escalation hints. It must never return live dispatch success, Codex invocation success, BLK-pipe success, mutation success, validation PASS, BEO publication, RTM generation, drift rejection, production sandbox, network firewall, or host-secret isolation claims.

---

## 5. Builder Restrictions

The authority-request and disabled-adapter helper must not import or call subprocess helpers, shell helpers, Git helpers, network clients, browser tools, package managers, BLK-pipe, BLK-test, BEO tooling, RTM tooling, protected-vault readers, model APIs, or Codex itself.

The helper may validate BLK-042 readiness records, separate human grant dictionaries, bounded request metadata, failure ceiling metadata, hostile audit checklist entries, and operator escalation cases. It may return human-readable blocked reasons and escalation hints.

---

## 6. Explicit Non-Authorities

BLK-043 does not authorize live tactical LLM execution, live Codex execution, reusable runtime dispatch, BLK-pipe execution, production BLK-test MCP, arbitrary shell, network/API/model/cyber tooling, browser automation, remote service access, dependency installation, package-manager execution, source mutation, Git mutation, protected BLK-req vault body reads/copying/parsing/hashing/summarizing, active-vault path scans, BLK-req staging or promotion, BEO publication, RTM generation, RTM drift rejection, signer key access, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, or final drift decisions.

BLK-043 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, host-secret isolation, kernel containment, or comprehensive host side-effect observation. Any containment evidence remains review-only.

---

## 7. Stop Conditions

Stop and treat any proposed change as outside BLK-043 authority if it executes Codex, starts a subprocess, invokes BLK-pipe, calls Git, creates worktrees, fetches network resources, installs packages, mutates source, reads Codex configuration or user rules, reads protected vault bodies, copies active-vault content, publishes BEOs, generates RTMs, decides drift, grants production authority, converts authority-request evidence into execution approval, or turns the disabled adapter into a live adapter.

---

## 8. Future Handoff

Future work may request explicit live Codex dispatch authority only through a separate sprint that explicitly grants runtime execution through BLK-pipe under a bounded approval envelope and fresh hostile review. BLK-043 alone grants no execution authority.
