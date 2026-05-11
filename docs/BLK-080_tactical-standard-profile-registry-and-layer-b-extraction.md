# BLK-080 — Tactical Standard Profile Registry and Layer B Extraction

**Status:** Active L0/L1 profile-registry boundary — deterministic fixture and doctrine gate only; not runtime authority
**Date:** 2026-05-11
**Purpose:** Convert BLK-078's tactical-standard profile architecture into a BLK-System-owned Layer B safety standard extraction and a deterministic Layer C profile-registry fixture.
**Scope:** BLK-System documentation, deterministic fixture, and doctrine-gate work only. This document is not a BEB, not a BEO, not target-work approval, not runtime approval, not BLK-pipe authority, not BLK-test authority, not BEO publication authority, and not RTM authority.

---

## 0. Boundary Markers

```text
BLK_SYSTEM_TACTICAL_PROFILE_REGISTRY_AND_LAYER_B_EXTRACTION
TACTICAL_PROFILE_REGISTRY_L0_L1_FIXTURE_ONLY
LAYER_A_UNIVERSAL_CORE_NOT_WEAKENED
LAYER_B_UNIVERSAL_TACTICAL_OUTPUT_SAFETY_STANDARD
LAYER_C_TARGET_PROFILE_REGISTRY
BLK_058_REGISTERED_AS_KURONODE_TYPESCRIPT_LAYER_C_SOURCE
PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
EXACT_DENIED_AUTHORITIES_REQUIRED
NO_PROFILE_SELECTION_RUNTIME_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY
NO_TARGET_REPO_SCAN_AUTHORITY
NO_TARGET_REPO_MUTATION_AUTHORITY
NO_KURONODE_MUTATION_AUTHORITY
NO_LIVE_CODEX_EXECUTION_AUTHORITY
NO_BLK_PIPE_EXECUTION_AUTHORITY
NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY
NO_BEO_PUBLICATION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

Persistent doctrine gate marker: BLK-SYSTEM-080 pins tactical profile registry and Layer B extraction as L0/L1 non-runtime scope.

---

## 1. Non-Execution and Non-Authority Boundary

BLK-080 is a profile-registry and Layer B extraction boundary only. It records constraints for future reviewed work; it does not grant work.

Denied authority statements:

- No profile-selection runtime authority.
- No BEB dispatch or BEO closeout execution authority.
- No live target-repository scans.
- No target-repository source or Git mutation.
- No Kuronode source or Git mutation.
- No live Codex execution authority.
- No BLK-pipe execution authority.
- No production BLK-test MCP authority.
- No authoritative BEO publication authority.
- No runtime RTM generation or RTM drift rejection authority.
- No protected BLK-req body reads.
- No package-manager, network, model-service, browser, or cyber tooling authority.
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim.

Profile selection is planning/review metadata only. A selected profile can constrain a future authorized boundary, but it cannot start the boundary, choose a target, scan a target, mutate a target, run a tactical engine, publish, generate trace matrices, read protected bodies, install tools, call services, or prove production isolation.

---

## 2. Relationship to BLK-078

BLK-078 defines the three-layer profile architecture. BLK-080 implements the first L0/L1 representation of that model:

| BLK-078 layer | BLK-080 treatment |
| --- | --- |
| Layer A — BLK-System Universal Core | LAYER_A_UNIVERSAL_CORE_NOT_WEAKENED. Layer A remains governed by BLK-001 through BLK-006 and active boundary documents. No profile registry record can weaken HITL, traceability, protected-vault isolation, BLK-pipe enforcement, BLK-test evidence boundaries, BEO/RTM separation, hostile review, replay controls, or human escalation. |
| Layer B — Universal Tactical Output Safety Standard | LAYER_B_UNIVERSAL_TACTICAL_OUTPUT_SAFETY_STANDARD. BLK-080 extracts the universal safety principles into stable identifiers and deterministic fixture data. |
| Layer C — Target Tactical Profiles | LAYER_C_TARGET_PROFILE_REGISTRY. BLK-080 registers target-specific profile sources without granting target work. |

The architecture anchor remains:

```text
docs/BLK-078_tactical-standard-profile-architecture.md
```

The deterministic fixture path is:

```text
python/blk_tactical_profile_registry.py
```

---

## 3. Extracted Layer B Standard

BLK-080 defines the Layer B standard ID:

```text
blk-system-universal-tactical-output-safety
```

The extracted Layer B principle identifiers are:

1. `simple_reviewable_control_flow` — tactical output should avoid hidden state transitions, callback mazes, and control-flow-by-exception.
2. `bounded_iteration` — retries, traversals, polling, queue drains, and convergence loops require explicit limits.
3. `bounded_runtime_state` — caches, maps, arrays, queues, listener registries, logs, and pending-operation stores require bounded shapes.
4. `explicit_lifecycle_management` — created resources require visible teardown paths where cleanup semantics exist.
5. `small_hostile_reviewable_units` — authority-sensitive code should be small enough for focused hostile review.
6. `boundary_validation` — external, process-boundary, persistence, IPC, parser, and worker data require structural validation before use.
7. `checked_results_and_postconditions` — meaningful return values, nullable/error-shaped outputs, promises, validation results, and critical postconditions must not be ignored.
8. `minimal_mutable_scope` — prefer local immutable values and narrow mutation windows; avoid ambient mutable singletons used to bridge architecture gaps.
9. `no_dynamic_execution_laundering` — tactical output must not introduce generated executable strings, reflection-like dispatch, or unvalidated dynamic imports without separate exception authority.
10. `flat_validated_data_access` — nested or external structures must be normalized or validated before authority-sensitive use.
11. `zero_warning_intent_under_repository_owned_profiles` — repository-owned validation profiles may define warning-free evidence as blocking; autonomous boundaries must not replace those profiles with arbitrary shell.
12. `no_authority_laundering` — tactical quality evidence remains constraint evidence only and never permits adjacent runtime frontiers.

Layer B constrains approved tactical output. It does not authorize the output to exist.

---

## 4. Layer C Registry Entry: `kuronode-typescript`

BLK-080 registers BLK-058 as the first concrete Layer C source:

```text
profile_id: kuronode-typescript
profile_source_doc: docs/BLK-058_kuronode-typescript-power-of-ten-tactical-standard.md
profile_architecture_doc: docs/BLK-078_tactical-standard-profile-architecture.md
profile_maturity: L0_LAYER_C_SOURCE_ONLY
```

Marker:

```text
BLK_058_REGISTERED_AS_KURONODE_TYPESCRIPT_LAYER_C_SOURCE
```

Interpretation:

- BLK-058 remains the Kuronode TypeScript tactical standard source.
- Universal BLK-058 principles are represented in Layer B where target-agnostic.
- Kuronode-specific TypeScript, Electron, React, Zustand, ELK.js, JointJS, tree-sitter SysML, parser/Wasm lifecycle, renderer ownership, GraphAdapter quarantine, smoke-harness, and projected-node constraints remain Layer C overlays.
- `kuronode-typescript` constrains future approved Kuronode TypeScript work only.
- Selecting or registering `kuronode-typescript` does not grant Kuronode work.

---

## 5. Profile Selection Record Boundary

A profile selection record is an input to planning and review. It is not an execution envelope.

Required review-only marker:

```text
PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
```

A valid review-only profile selection record must bind at minimum:

| Field | Meaning |
| --- | --- |
| `selection_id` | Stable review fixture identity. |
| `selection_status` | Must remain `PROFILE_SELECTION_RECORD_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY`. |
| `selected_profile_id` | Stable profile ID such as `kuronode-typescript`. |
| `selected_profile_source_doc` | Source doctrine, currently BLK-058 for Kuronode TypeScript. |
| `selected_profile_architecture_doc` | Architecture anchor, currently BLK-078. |
| `selection_maturity` | L0/L1 planning fixture only unless a later explicit boundary advances it. |
| `layer_b_standard_id` | `blk-system-universal-tactical-output-safety`. |
| `layer_b_principles` | Exact list of Layer B identifiers extracted in this document. |
| `layer_c_overlays` | Target-specific overlay names. |
| `validation_profiles` | Repository-owned profile names as metadata only, never arbitrary shell. |
| `denied_authorities` | Exact denied-authority list. |

Selection records may become future Layer 2 packet context only after a separate authority boundary grants a specific run. Until then, they are review evidence only.

---

## 6. Exact Denied Authorities

BLK-080 requires exact denied-authority equality for registry and selection records:

```text
EXACT_DENIED_AUTHORITIES_REQUIRED
NO_PROFILE_SELECTION_RUNTIME_AUTHORITY
NO_BEB_DISPATCH_OR_BEO_CLOSEOUT_AUTHORITY
NO_TARGET_REPO_SCAN_AUTHORITY
NO_TARGET_REPO_MUTATION_AUTHORITY
NO_KURONODE_MUTATION_AUTHORITY
NO_LIVE_CODEX_EXECUTION_AUTHORITY
NO_BLK_PIPE_EXECUTION_AUTHORITY
NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY
NO_BEO_PUBLICATION_AUTHORITY
NO_RTM_GENERATION_OR_DRIFT_REJECTION_AUTHORITY
NO_PROTECTED_BLK_REQ_BODY_READS
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING_AUTHORITY
NO_PRODUCTION_SANDBOX_OR_HOST_ISOLATION_CLAIM
```

The deterministic fixture must reject missing entries, extra entries, duplicate entries, non-string entries, and nested authority-laundering attempts. On blocked evaluation, runtime/target/publication/trace/tooling/isolation flags must be forced to `False`.

---

## 7. Validation Profile Boundary

Repository-owned validation profile names can be carried as metadata and constraints. They are not executable commands in this sprint.

Valid metadata examples for the `kuronode-typescript` Layer C source include:

```text
kuronode-power-of-ten-static
kuronode-typecheck-strict
kuronode-eslint-zero-warning
```

Forbidden in BLK-080 registry and selection records:

- command-shaped validation profile strings;
- package-manager command strings;
- network URLs;
- arbitrary shell snippets;
- target scan commands;
- tool installation commands;
- dynamic execution strings.

BLK-080's fixture rejects command-shaped profile names to preserve BLK-004's repository-owned validation-profile boundary.

---

## 8. Deterministic Fixture Contract

The fixture module is:

```text
python/blk_tactical_profile_registry.py
```

The focused test module is:

```text
python/test_blk_tactical_profile_registry.py
```

The fixture must expose builders, validators, and evaluators for:

1. tactical profile registry records;
2. profile selection records;
3. exact denied-authority sets;
4. Layer B principle identity;
5. the first Layer C `kuronode-typescript` source;
6. blocked-record evaluation that forces denied flags false.

The fixture must not perform live imports/calls for subprocess execution, sockets, HTTP clients, dynamic imports, dynamic evaluation, shell invocation, target-repo scanning, target mutation, package-manager execution, BLK-pipe execution, BLK-test execution, BEO publication, or RTM generation.

---

## 9. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-080 alignment |
| --- | --- |
| BLK-001 — Master Architecture | Preserves separation between planning, tactical execution, deterministic enforcement, physical verification, BEO publication, and trace closure. Profile registry data is constraint metadata only. |
| BLK-002 — Artifact Lifecycle | Does not alter staging, linting, HITL promotion, baseline immutability, or protected-vault rules. |
| BLK-003 — Orchestration Protocol | Provides future Layer 2 context shape for constraints only. It does not create BEB/BEO artifacts, dispatch engines, or run audits. |
| BLK-004 — BLK-pipe V47 Suite | Preserves BLK-pipe as final mutation enforcement and preserves repository-owned validation profiles. Profile registry data does not replace BLK-pipe. |
| BLK-005 — BLK-Req Specification | Preserves canonical hash and trace binding boundaries without trace-matrix creation, drift decisions, or protected-body comparisons. |
| BLK-006 — BLK-Req Implementation Brief | Preserves protected-vault hard-deny behavior and no protected-body reads. |

---

## 10. Future Work Boundary

After BLK-SYSTEM-080, the next logical sprint is BLK-SYSTEM-081 — Target-Repo Execution Governance Pattern. BLK-SYSTEM-081 should define how a future target-repo execution boundary may consume a profile-selection record, while still requiring exact target, exact path, exact head, exact approval, replay controls, allowlists, validation profile ownership, stop conditions, and hostile review.

BLK-SYSTEM-081 must not inherit runtime permission from this document.

---

## 11. Final Doctrine Statement

BLK-080 turns BLK-078's architecture into L0/L1 doctrine and deterministic fixture evidence:

```text
Layer A remains BLK-System universal core and cannot be weakened by profiles.
Layer B is extracted as a universal tactical-output safety standard.
Layer C registers target tactical profile sources, beginning with BLK-058 as kuronode-typescript.
Profile selection records are review-only unless a later explicit authority boundary grants a specific run.
No layer, registry entry, selection record, validation profile name, fixture PASS, or profile-compliance evidence grants runtime authority by itself.
```
