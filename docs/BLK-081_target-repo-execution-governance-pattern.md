# BLK-081 — Target-Repo Execution Governance Pattern

**Status:** Active L0/L1 target-repository execution governance boundary — deterministic fixture and doctrine gate only; not runtime authority
**Date:** 2026-05-11
**Purpose:** Define the BLK-System governance pattern that future exact-target repository work must satisfy before any separately approved target scan, target mutation, BEB dispatch, BEO closeout execution, publication, or RTM frontier can be requested.
**Scope:** BLK-System documentation, deterministic fixture validation, and active doctrine gates. This document is not a BEB, not a BEO, not target-work approval, not runtime approval, not BLK-pipe authority, not BLK-test authority, not BEO publication authority, and not RTM authority.

---

## 0. Boundary Markers

```text
BLK_SYSTEM_TARGET_REPO_EXECUTION_GOVERNANCE_PATTERN
TARGET_REPO_EXECUTION_GOVERNANCE_L0_L1_FIXTURE_ONLY
TARGET_REPO_GOVERNANCE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
REQUEST_PACKAGE_NOT_APPROVAL
PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
APPROVAL_ENVELOPE_REQUIRED_NOT_GRANTED
PREFLIGHT_REFUSAL_REQUIRED_FOR_ABSENT_STALE_EXPIRED_REPLAYED_OR_MISMATCHED_AUTHORITY
APPROVAL_CAPTURE_NOT_RETARGETING_AUTHORITY
BLK_PIPE_INVOCATION_BOUNDARY_NOT_EXECUTED
VALIDATION_EVIDENCE_PROFILE_NAMES_ONLY_NOT_SHELL
HOSTILE_AUDIT_REQUIRED_BEFORE_TARGET_CLOSEOUT
TARGET_REPO_CLOSEOUT_REQUIRES_SEPARATE_AUTHORITY
NO_GOVERNANCE_RECORD_RUNTIME_AUTHORITY
NO_TARGET_REPO_SCAN_AUTHORITY
NO_TARGET_REPO_MUTATION_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY
NO_APPROVAL_ENVELOPE_RETARGETING_AUTHORITY
NO_LIVE_CODEX_EXECUTION_AUTHORITY
NO_BLK_PIPE_EXECUTION_AUTHORITY
NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY
NO_BEO_PUBLICATION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

Persistent doctrine gate marker: BLK-SYSTEM-081 pins target-repo execution governance as L0/L1 non-runtime scope.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-081 is a governance-pattern boundary. It records the order and evidence obligations a future target-repository execution chain must satisfy. It does not start or approve that chain.

Denied authority statements:

- No governance-record runtime authority.
- No live target-repository scans.
- No target-repository source or Git mutation.
- No BEB dispatch or BEO closeout execution authority.
- No approval-envelope retargeting authority.
- No live Codex execution authority.
- No BLK-pipe execution authority.
- No production BLK-test MCP authority.
- No authoritative BEO publication authority.
- No runtime RTM generation or RTM drift rejection authority.
- No protected BLK-req body reads.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

A future sprint may consume this pattern to prepare or evaluate a separately approved target frontier. That future sprint must still name the exact repository, path, branch, local target HEAD, observed remote HEAD, source allowlist, protected denylist, validation profiles, profile-selection record, request ID, approval ID, run ID, expiry, replay policy, stop conditions, hostile-review criteria, and closeout obligations.

---

## 2. Relationship to BLK-080 and the Profile Architecture

BLK-080 created the first BLK-System-owned profile registry and Layer B extraction:

```text
docs/BLK-080_tactical-standard-profile-registry-and-layer-b-extraction.md
python/blk_tactical_profile_registry.py
```

BLK-081 consumes that work but does not weaken it:

| BLK-078/080 element | BLK-081 use | Boundary |
| --- | --- | --- |
| Layer A — BLK-System universal core | Governs every target-repo chain stage: HITL, trace, protected-body isolation, BLK-pipe blast shield, BLK-test evidence separation, BEO/RTM separation, hostile review, replay/expiry, and escalation. | Layer A cannot be bypassed by target profiles or governance records. |
| Layer B — universal tactical-output safety | Becomes required review metadata for future target work where tactical output is produced. | Layer B constrains approved output shape; it does not choose or approve target work. |
| Layer C — target tactical profiles | Provides profile-specific constraints, currently `kuronode-typescript` from BLK-058. | Layer C applies only when a future sprint separately selects and approves that target frontier. |
| Profile-selection record | Attached to the target-governance record as evidence of selected constraints. | The record remains review-only until a separate exact authority envelope approves a specific frontier. |

The deterministic fixture path for this doctrine is:

```text
python/blk_target_repo_execution_governance.py
```

---

## 3. Required Governance Stages

A future target-repository execution chain must preserve this order:

1. **Request package — `REQUEST_PACKAGE_NOT_APPROVAL`**
   - Captures the future operator intent, target candidate, requested frontier, scope, and non-goals.
   - The request package is not approval and cannot start target work.

2. **Profile selection — `PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY`**
   - Attaches the BLK-080 profile-selection record when a tactical standard is relevant.
   - For current Kuronode TypeScript work, this means the `kuronode-typescript` profile sourced from BLK-058 and BLK-078/080.
   - Profile selection constrains future work; it does not scan, mutate, dispatch, test, publish, or generate trace closure.

3. **Approval envelope — `APPROVAL_ENVELOPE_REQUIRED_NOT_GRANTED`**
   - Names exact target repository ID, absolute path string, branch, local target HEAD, observed remote HEAD, source allowlist, protected denylist, validation profiles, selected profile, request ID, approval ID, run ID, expiry, replay policy, and stop conditions.
   - A stale or mismatched target identity blocks rather than retargeting itself.

4. **Preflight refusal — `PREFLIGHT_REFUSAL_REQUIRED_FOR_ABSENT_STALE_EXPIRED_REPLAYED_OR_MISMATCHED_AUTHORITY`**
   - Fails closed when exact authority is absent, stale, expired, replayed, or mismatched.
   - Failure evidence is not permission to modify the target.

5. **Approval capture — `APPROVAL_CAPTURE_NOT_RETARGETING_AUTHORITY`**
   - Captures the human decision in a future approved sprint.
   - Captured approval names exactly one target envelope and cannot silently follow a newer branch head.

6. **BLK-pipe invocation boundary — `BLK_PIPE_INVOCATION_BOUNDARY_NOT_EXECUTED`**
   - Defines the future exact BLK-pipe payload boundary for mutation work.
   - BLK-081 does not run BLK-pipe, build a payload for execution, or mutate a target.

7. **Validation evidence — `VALIDATION_EVIDENCE_PROFILE_NAMES_ONLY_NOT_SHELL`**
   - Names repository-owned validation profile identifiers only.
   - Validation profile names are not arbitrary shell, package-manager commands, network calls, model-service calls, browser operations, or cyber tooling.

8. **Hostile audit — `HOSTILE_AUDIT_REQUIRED_BEFORE_TARGET_CLOSEOUT`**
   - Reviews exact target identity, profile-selection status, approval freshness, replay/expiry, allowlists, protected denylists, validation evidence, side effects, authority wording, and failure classification.

9. **Target-repo closeout — `TARGET_REPO_CLOSEOUT_REQUIRES_SEPARATE_AUTHORITY`**
   - Future target-repo outcome/BEO closeout occurs only under a separately approved frontier.
   - BLK-081 records the obligation but does not write, publish, or close a BEO.

---

## 4. Deterministic Fixture Contract

`python/blk_target_repo_execution_governance.py` must keep these properties true:

- `GOVERNANCE_STAGES` exactly matches the nine-stage chain above.
- The default record status is `TARGET_REPO_GOVERNANCE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME`.
- Target identity fields require exact repository ID, absolute path string, branch, local target HEAD SHA, and observed remote HEAD SHA.
- Local target HEAD and observed remote HEAD must match unless a future approval names a new exact target.
- The profile-selection record must validate through `python/blk_tactical_profile_registry.py` and remain `PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY`.
- Approval envelope metadata must include request ID, approval ID, run ID, UTC expiry, one-use replay policy, approval scope, and operator identity.
- Validation profile names must be repository-owned kebab-case metadata, not command-shaped strings.
- Denied authorities must match the exact BLK-081 denied-authority set.
- Side-effect flags must remain false for target scan, target mutation, BEB dispatch, BEO closeout execution, approval retargeting, live Codex, BLK-pipe, production BLK-test MCP, BEO publication, RTM generation, protected-body reads, package/network/model/browser/cyber tooling, and production isolation.
- Recursive hostile scanning must reject authority-laundering strings, unsupported fields, command-shaped validation profiles, promoted profile-selection records, and stale target identity.

---

## 5. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-081 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve V-model separation between BLK-req, Hermes planning, tactical implementation, BLK-pipe mutation enforcement, BLK-test evidence, BEO publication, and blk-link trace closure. Target-governance records are constraints, not execution. |
| BLK-002 — Artifact Lifecycle | Preserve staging/HITL/active-vault isolation and protect BLK-req bodies from reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates, Layer 2 bounded context, failure ceilings, hostile audit, BLK-test evidence boundaries, draft/authoritative BEO separation, and disabled RTM boundaries. |
| BLK-004 — BLK-pipe V47 Suite | Preserve Go BLK-pipe as final mutation enforcement for exact allowlists, validation profiles, output caps, cleanup, Git routing, target-hash checks, and reports. This doctrine does not run BLK-pipe. |
| BLK-005 — BLK-Req Specification | Preserve atomic requirements, bounded use cases, immutable IDs, canonical version hashes, trace binding, and disabled drift semantics unless separately approved. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny, staged revisions, no tactical write access, no protected body reads, and Discord/HITL authorization boundaries. |

---

## 6. What BLK-081 Makes Easier Later

BLK-081 creates the reusable checklist that future higher-authority sprints must satisfy before they can ask for one exact frontier:

- a BLK-058 / `kuronode-typescript` mechanical enforcement upgrade;
- a BEO publication decision package or pilot request;
- one bounded BLK-test evidence refresh;
- one Codex live-dispatch smoke;
- a later RTM authority request after publication prerequisites exist.

The key improvement is not runtime behavior. The improvement is that future target work must be expressed through one explicit, reviewable, fail-closed governance envelope rather than through ad hoc memory from earlier sprints.

---

## 7. Stop Conditions

Pause and require hostile review plus explicit human decision if a future sprint attempts to treat BLK-081, BLK-080, BLK-078, BLK-058, a profile-selection record, a request package, preflight evidence, validation evidence, or a prior target success as approval for runtime execution, target scanning, target mutation, BEB/BEO work, BEO publication, RTM generation, drift decisions, public ledger mutation, protected-body access, package/network/model/cyber/browser tooling, or production isolation claims.

BLK-081 is a pattern. It is not the future run, not the future target, not the future approval, and not a substitute for frontier-specific evidence.
