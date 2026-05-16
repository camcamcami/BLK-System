# BLK-077 — BLK-System Acceleration Roadmap

**Status:** Active lean roadmap guidance — not sprint authority and not runtime authority
**Date:** 2026-05-17T09:30:00+10:00
**Purpose:** Keep BLK-System moving through bounded production evidence while preserving exact authority cutlines.
**Scope:** Current production state, next frontier, authority boundaries, and stop/split rules. This is not a sprint plan, BEB, BEO, runtime approval, reusable approval capture, blanket production `blk-link` authority, or global replay ledger.

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
NEXT_FRONTIER_REPEATABLE_TRUSTED_BLK_LINK_OPERATOR_USE_READY_PER_RUN_EXACT_APPROVAL_NOT_BLANKET_AUTHORITY
```

BLK-SYSTEM-190..194 consumed the clean BLK-189 single-run reconciliation and established a repeatable trusted per-run exact-approval mechanism: post-run review, repeatable contract, caller-supplied hash-chain ledger, three exact repeat-run evidence samples, and clean reconciliation. This is operator-use ready under the contract, not blanket `blk-link` authority.

---

## 3. Active Next Frontier

**Next production-driving frontier:** use the repeatable trusted `blk-link` mechanism for operator-selected per-run exact approvals, or request a narrower automation promotion only after more clean ledger samples.

Preferred next sprint shape:

- consume the exact BLK-194 reconciliation package;
- require exact approval ID, run ID, nonce, canonical upstream hash, and ledger previous hash per run;
- keep the caller-supplied ledger explicit and avoid claiming global replay prevention;
- harden only if a concrete observed failure or hostile finding exists;
- keep protected bodies isolated and continue using metadata/hashes only;
- publish exactly one sprint closeout for the sprint.

---

## 4. Authority Boundaries

This roadmap does not authorize:

- blanket production `blk-link`, no production `blk-link` without per-run exact approval, no reusable run-ID reservation/consumption, no approval reuse, and no global replay-ledger claim;
- RTM generation, reusable RTM generation, no drift rejection, no coverage truth, or no active-vault comparison authority;
- no protected-body text return, no protected-body access beyond previously captured caller-supplied hash metadata, and no protected BLK-req body reads/copying/parsing/hashing/scanning/mutation;
- reusable BEO publication/signing/storage/ledger authority, no signer reuse, no storage reuse, no ledger reuse, and no future publication run;
- rollback, revocation, or supersession execution;
- no BEB dispatch or no BEO closeout execution;
- no live Codex or reusable tactical LLM dispatch;
- no BLK-pipe runtime outside separately approved exact payloads and no runtime tooling;
- production/generic BLK-test MCP and no production BLK-test MCP;
- no target/source/Git mutation or package-manager, network, model-service, browser, cyber tooling, or production-isolation claims.

---

## 5. Minimal Roadmap Queue

1. **Per-run operator use** — execute future `blk-link` runs only through the BLK-194 repeatable trusted contract.
2. **Observed-failure hardening if required** — only if an exact run, ledger chain, or hostile review finds a concrete bypass/failure.
3. **Narrow promotion request** — after additional clean samples, request a scoped automation promotion; no blanket authority by default.

---

## 6. Stop / Split Rules

Stop or split a proposed sprint when it:

- produces authority-denial paperwork without unblocking or executing a bounded capability;
- creates a new BLK-### without a durable future contract;
- creates per-task outcome docs instead of one sprint closeout;
- updates BLK-001 through BLK-006 with sprint-current-state text;
- bundles unrelated authority surfaces into one opaque package;
- turns PASS evidence, a dry-run, a reusable contract, repeat-run samples, or clean reconciliation into blanket production `blk-link`, RTM truth, drift truth, coverage truth, production-isolation proof, or reusable runtime authority;
- reads, copies, parses, hashes, scans, summarizes, or mutates protected requirement body text beyond explicit caller-supplied hash metadata for the approved feature.
