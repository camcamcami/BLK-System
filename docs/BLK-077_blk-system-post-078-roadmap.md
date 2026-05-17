# BLK-077 — BLK-System Acceleration Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-17T11:55:00+10:00
**Purpose:** Keep BLK-System moving through bounded production evidence while preserving exact authority cutlines.
**Scope:** Current production state, next frontier, authority boundaries, and stop/split rules. This is not a sprint plan, BEB, BEO, runtime approval, blanket `blk-link` authority, broad protected-body access, or global replay ledger.

---

## 1. Acceleration Contract

```text
LEAN_DOCUMENTATION_MODEL_ACTIVE
NO_BLK_DOC_PER_SPRINT
ONE_OUTCOME_PER_SPRINT_NO_TASK_OUTCOME_DOCS
BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE
ROADMAP_OCCAM_PRODUCTION_ONLY
ACCELERATION_MODE_BOUNDED_PRODUCTION_MOVEMENT
PRODUCTION_CAPABILITY_OVER_AUTHORITY_TREADMILL
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```

A sprint should deliver one bounded capability or directly unblock one bounded capability. Broad hardening is only the default when a concrete observed failure or hostile finding requires it.

---

## 2. Current Production State

```text
BLK_SYSTEM_200_KURONODE_BLK_REQ_VAULT_BOOTSTRAP_BLUEPRINT_READY
BLK_SYSTEM_199_BLK_REQ_PRODUCTION_GATEWAY_RECONCILED_CLEAN
BLK_SYSTEM_198_BLK_REQ_GATEWAY_HOSTILE_INPUTS_HARDENED
BLK_SYSTEM_197_BLK_REQ_EXACT_ID_LIFECYCLE_SMOKE_PASSED
BLK_SYSTEM_196_BLK_REQ_PRODUCTION_GATEWAY_CONTRACT_READY
BLK_SYSTEM_195_BLK_REQ_GATEWAY_READINESS_REVIEW_CLEAN
BLK_SYSTEM_194_REPEATABLE_TRUSTED_BLK_LINK_RECONCILED_CLEAN
BLK_SYSTEM_193_REPEATABLE_TRUSTED_BLK_LINK_REPEAT_RUNS_RECORDED_CLEAN
BLK_SYSTEM_192_REPEATABLE_TRUSTED_BLK_LINK_LEDGER_READY
BLK_SYSTEM_191_REPEATABLE_TRUSTED_BLK_LINK_CONTRACT_EMITTED
BLK_SYSTEM_190_REPEATABLE_TRUSTED_BLK_LINK_POST_RUN_REVIEW_CLEAN
BLK_SYSTEM_189_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_RECONCILED_CLEAN
BLK_SYSTEM_188_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_EXECUTION_RECORDED
BLK_SYSTEM_187_SINGLE_PRODUCTION_BLK_LINK_WRAPPER_RUN_REQUEST_READY
BLK_SYSTEM_186_REUSABLE_BLK_LINK_READINESS_KERNEL_RECONCILED_CLEAN
BLK_SYSTEM_185_REUSABLE_BLK_LINK_READINESS_KERNEL_DRY_RUN_RECORDED
BLK_SYSTEM_184_REUSABLE_BLK_LINK_READINESS_KERNEL_CONTRACT_EMITTED
BLK_SYSTEM_183_REUSABLE_BLK_LINK_READINESS_KERNEL_DECISION_READY
BLK_SYSTEM_182_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_EXPORT_RECONCILED_CLEAN
BLK_SYSTEM_181_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_METADATA_EXPORT_EMITTED
BLK_SYSTEM_180_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_RECONCILED_CLEAN
BLK_SYSTEM_179_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_EXECUTION_RECORDED
BLK_SYSTEM_178_RTM_BLK_LINK_PROTECTED_BODY_EVIDENCE_FOLLOWUP_AUTHORITY_REQUEST_READY
BLK_SYSTEM_177_AUTHORITY_LAUNDERING_BYPASS_HARDENED
BLK_SYSTEM_176_RTM_BLK_LINK_PROTECTED_BODY_VERIFICATION_EVIDENCE_INTEGRATED
BLK_SYSTEM_175_PROTECTED_BODY_VERIFICATION_DECISION_EXECUTION_RECORDED
BLK_SYSTEM_174_PROTECTED_BODY_VERIFICATION_DECISION_AUTHORITY_REQUEST_READY
BLK_SYSTEM_173_METADATA_BOUND_DRIFT_COVERAGE_DECISION_RECONCILED_CLEAN
BLK_SYSTEM_172_METADATA_BOUND_DRIFT_COVERAGE_DECISION_EXECUTION_RECORDED
BLK_SYSTEM_171_METADATA_BOUND_DRIFT_COVERAGE_DECISION_AUTHORITY_REQUEST_READY
BLK_SYSTEM_170_ACTIVE_VAULT_HASH_COMPARISON_RECONCILED_CLEAN
BLK_SYSTEM_169_ACTIVE_VAULT_HASH_COMPARISON_DECISION_EXECUTION_RECORDED
BLK_SYSTEM_168_ACTIVE_VAULT_HASH_COMPARISON_AUTHORITY_REQUEST_READY
BLK_SYSTEM_167_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_POST_RUN_RECONCILED_CLEAN
BLK_SYSTEM_166_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_DECISION_EXECUTION_RECORDED
BLK_SYSTEM_165_PRODUCTION_BLK_LINK_RTM_TRACE_CLOSURE_AUTHORITY_REQUEST_READY
BLK_SYSTEM_164_ACTIVE_DOC_DENIED_SURFACE_SYNC_HARDENED
BLK_SYSTEM_163_CURRENT_STATE_DENIED_SURFACE_HARDENED
POST-METADATA-TRACE-CLOSURE-REVIEW-162-001
sha256:5d16dd57fefc7028b70e38843b76469a80a9ea3786195000ad49330f27f93ff9
blk190_review_package_hash=sha256:14dd668a8848351ebfcc05ee0bfa58ea979a6c6a861bc9b9449d86f980dc665e
blk191_contract_package_hash=sha256:c6d056a59f6ef0b182223c6bcac6737466a40d049cbdc8e844219fab2c7150f5
blk192_ledger_package_hash=sha256:ddff687aa4b4a67f218bb317fab47c7380b542ac538d3daf8794567f00b23140
blk193_repeat_runs_package_hash=sha256:318eec761911be1767b915207d86449879132545d061bbf758d6662ac2f4297e
blk194_reconciliation_package_hash=sha256:30292f85d1222eb2108f0eadeec07337834e9b47d8e00fa9969aeeafb1bbf4f7
blk200_bootstrap_package_hash=sha256:8e0414e4564d7ae6567487e807374497fee337f20ec53eb47a6e7ca9a3958229
NEXT_FRONTIER_KURONODE_BLK_REQ_EXACT_ID_MAPPING_OR_OPERATOR_USE_NOT_GRANTED
```

BLK-SYSTEM-200 selected a Kuronode-facing BLK-req sibling-vault blueprint at `/home/dad/BLK-req-Kuronode`, preserving Kuronode source/Git non-mutation and deferring exact ID mapping/operator use to a fresh decision. BLK-SYSTEM-195..199 remains the production BLK-req exact-operation gateway; BLK-SYSTEM-190..194 remains repeatable trusted `blk-link` per-run exact approval.

---

## 3. Active Next Frontier

**Next production-driving frontier:** Kuronode BLK-req exact-ID mapping or exact operator use under the sibling-vault blueprint.

Preferred next sprint shape:

- consume the BLK-SYSTEM-200 blueprint hash exactly;
- map Kuronode `R-*` / `UC-*` IDs to `REQ-###` / `UC-###` metadata only, or run one exact gateway operation with explicit HITL approval;
- keep Kuronode source/Git mutation, broad doc scans, protected-body migration, RTM generation, BEO publication, runtime/tooling, and blanket `blk-link` denied;
- harden only if a concrete observed failure or hostile finding exists;
- publish exactly one sprint closeout for the sprint.

---

## 4. Authority Boundaries

This roadmap does not authorize:

- blanket production `blk-link`, no production `blk-link` without per-run exact approval, no reusable run-ID reservation/consumption, no approval reuse, and no global replay-ledger claim;
- RTM generation, reusable RTM generation, no drift rejection, no coverage truth, or no active-vault comparison authority;
- no protected-body text return outside exact BLK-req gateway operations, no protected-body access beyond exact-ID gateway operations or previously captured caller-supplied hash metadata, and no protected BLK-req body reads/copying/parsing/hashing/scanning/mutation outside exact BLK-req gateway operations;
- reusable BEO publication/signing/storage/ledger authority, no signer reuse, no storage reuse, no ledger reuse, and no future publication run;
- rollback, revocation, or supersession execution;
- no BEB dispatch or no BEO closeout execution;
- no live Codex or reusable tactical LLM dispatch;
- no BLK-pipe runtime outside separately approved exact payloads and no runtime tooling;
- production/generic BLK-test MCP and no production BLK-test MCP;
- no target/source/Git mutation or package-manager, network, model-service, browser, cyber tooling, or production-isolation claims.

---

## 5. Minimal Roadmap Queue

1. **Kuronode BLK-req exact ID map or operator use** — consume the BLK-200 sibling-vault blueprint, then either build the caller-supplied ID map or run one exact BLK-req operation with HITL approval.
2. **Observed-failure hardening if required** — only if exact mapping/use or hostile review finds a concrete bypass/failure.
3. **Next component closeout** — move to the next BLK-System surface rather than reopening `blk-link` without a real use case.

---

## 6. Stop / Split Rules

Stop or split a proposed sprint when it:

- produces authority-denial paperwork without unblocking or executing a bounded capability;
- creates a new BLK-### without a durable future contract;
- creates per-task outcome docs instead of one sprint closeout;
- updates BLK-001 through BLK-006 with sprint-current-state text;
- bundles unrelated authority surfaces into one opaque package;
- turns PASS evidence, a dry-run, a reusable contract, repeat-run samples, gateway smoke, or clean reconciliation into blanket production `blk-link`, RTM truth, drift truth, coverage truth, production-isolation proof, or reusable runtime authority;
- reads, copies, parses, hashes, scans, summarizes, or mutates protected requirement body text outside exact BLK-req gateway operations.
