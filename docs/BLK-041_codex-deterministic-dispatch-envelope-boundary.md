# BLK-041 — Codex deterministic dispatch envelope boundary

**Status:** Active fixture boundary — deterministic Codex dispatch envelope construction only
**Sprint:** BLK-SYSTEM-039
**BLK-024 track:** Track C — BLK-pipe blast shield and forge; Track I — Operator UX, observability, and escalation; Track J — Security, sandbox, and capability hardening
**Maturity:** BLK-024 L1 fixture/local implementation plus L0 doctrine boundary; not L5 production authority

---

## 1. Purpose

BLK-041 records the BLK-SYSTEM-039 boundary for repository-owned deterministic Codex dispatch envelope construction. It follows BLK-040 by defining the non-executing fixture shape that must surround a future Codex tactical invocation profile before a later sprint asks for live execution authority.

BLK-041 does not authorize live Codex execution, live tactical LLM execution, BLK-pipe dispatch, production BLK-test MCP, source mutation, Git mutation, package-manager execution, network/model/cyber tooling, protected BLK-req vault body reads, BEO publication, RTM generation, drift rejection, or production sandbox claims. The dispatch envelope helper may construct and validate dictionaries only. It must not start subprocesses, call `codex`, call Git, create worktrees, call BLK-pipe, inspect user Codex configuration, create directories, read artifact bodies, mutate files, or treat telemetry as canonical evidence.

Active boundary vocabulary:

- `CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY`
- `CODEX_DISPATCH_ENVELOPE_STARTS_NO_SUBPROCESS`
- `CODEX_DISPATCH_REQUIRES_APPROVAL_PROVENANCE`
- `CODEX_DISPATCH_REQUIRES_EXACT_FILE_BOUNDARIES`
- `CODEX_DISPATCH_REQUIRES_VALIDATION_GATES`
- `CODEX_DISPATCH_REQUIRES_FAILURE_CEILING`
- `CODEX_DISPATCH_REQUIRES_HOSTILE_AUDIT`
- `CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY`
- `CODEX_DISPATCH_GRANTS_NO_EXECUTION_AUTHORITY`
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

Persistent doctrine gate marker: BLK-SYSTEM-039 pins Codex deterministic dispatch envelope fixture-only scope.

---

## 2. Required Envelope Contract

A valid `CODEX_DETERMINISTIC_DISPATCH_ENVELOPE_FIXTURE_ONLY` record must preserve all of the following before a later sprint may request live execution authority:

1. a valid BLK-040 deterministic invocation profile identity;
2. approval provenance with source system, operator identity, message/event ID when available, timestamp, exact approved scope, and explicit excluded authorities;
3. exact file boundaries for modified and new files;
4. validation gates tied to repository-owned validation profiles or explicit non-shell gate descriptors;
5. bounded relative telemetry artifact paths;
6. failure ceiling metadata;
7. hostile audit checklist requirements;
8. operator escalation cases;
9. replay state for approval IDs and run IDs;
10. explicit false non-authority flags.

The envelope must be rejected if any of these required sections are absent, malformed, expired, replayed, broad, or authority-bearing.

---

## 3. Approval Provenance Rules

BLK-041 makes `CODEX_DISPATCH_REQUIRES_APPROVAL_PROVENANCE` an active fixture requirement. Approval provenance must record:

```text
source_system
operator_identity
message_event_id
timestamp
exact_approved_scope
explicit_excluded_authorities
approval_id
expires_at
```

Approval provenance in this sprint is fixture validation only. It does not substitute for future runtime approval, BLK-test approval, BEO publication approval, RTM generation approval, or drift rejection approval. A dispatch envelope must fail closed when approval provenance is missing, expired, malformed, replayed, stale, scope-mismatched, or missing explicit excluded authorities.

---

## 4. File Boundary and Validation Gate Rules

BLK-041 makes `CODEX_DISPATCH_REQUIRES_EXACT_FILE_BOUNDARIES` and `CODEX_DISPATCH_REQUIRES_VALIDATION_GATES` active fixture requirements.

The envelope must reject broad pathspecs, globs, parent traversal, `.git` paths, protected BLK-req paths, active-vault paths, empty path elements, shell metacharacter-like file entries, and path classes that are not explicitly separated into allowed modified files and allowed new files.

Validation gates must be repository-owned validation profiles or explicit non-shell gate descriptors. The envelope must reject free-form shell, package-manager commands, network/model/cyber/browser wording, secret-reading wording, protected-vault wording, broad host-inspection wording, or any gate that claims BLK-test production authority.

---

## 5. Telemetry, Failure Ceiling, Hostile Audit, and Escalation

Codex JSONL telemetry, final messages, and dispatch-envelope telemetry are `CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY`. They may support operator UX but are not canonical proof of mutation safety, validation success, approval, trace closure, BEO publication, RTM generation, or drift status.

A valid dispatch envelope must include a failure ceiling, hostile audit checklist, and operator escalation metadata. Operator escalation must cover at least missing approval, policy block, validation failure, failure ceiling, malformed telemetry, and denied authority. Failure ceiling and escalation metadata make failure modes visible; they do not grant retry, dispatch, mutation, publication, RTM, or drift authority.

---

## 6. Builder Restrictions

The dispatch envelope helper must preserve `CODEX_DISPATCH_ENVELOPE_STARTS_NO_SUBPROCESS` and must not import or call subprocess helpers, shell helpers, Git helpers, network clients, browser tools, package managers, BLK-pipe, BLK-test, BEO tooling, RTM tooling, protected-vault readers, model APIs, or Codex itself.

The helper may validate a BLK-040 profile fixture, approval provenance dictionaries, exact file boundary lists, validation gate descriptors, telemetry path strings, failure ceiling metadata, hostile audit checklist entries, and operator escalation cases.

---

## 7. Explicit Non-Authorities

BLK-041 does not authorize live tactical LLM execution, live Codex execution, reusable runtime dispatch, production BLK-test MCP, arbitrary shell, network/API/model/cyber tooling, browser automation, remote service access, dependency installation, package-manager execution, source mutation, Git mutation, protected BLK-req vault body reads/copying/parsing/hashing/summarizing, active-vault path scans, BLK-req staging or promotion, BLK-pipe execution, BEO publication, RTM generation, RTM drift rejection, signer key access, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, or final drift decisions.

BLK-041 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux enforcement, network firewall enforcement, host-secret isolation, kernel containment, or comprehensive host side-effect observation. Any BLK-040 `danger-full-access` field remains a host workaround inside an external audit envelope, not a trusted sandbox.

---

## 8. Stop Conditions

Stop and treat any proposed change as outside BLK-041 authority if it executes Codex, starts a subprocess, invokes BLK-pipe, calls Git, creates worktrees, fetches network resources, installs packages, mutates source, reads Codex configuration or user rules, reads protected vault bodies, copies active-vault content, publishes BEOs, generates RTMs, decides drift, captures runtime approval, grants production authority, or converts telemetry into canonical evidence.

---

## 9. Future Handoff

Future work may use this dispatch-envelope fixture in an explicit live-dispatch authority request only after a separate sprint defines and approves runtime execution, BLK-pipe wiring, external containment, validation execution, telemetry persistence, rollback, monitoring, and operator controls. This BLK-041 fixture boundary alone grants no execution authority.
