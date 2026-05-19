# BLK-079 — BLK-System Current-State Authority Index
**Status:** Active lean current-state authority index — not sprint authority and not runtime authority
**Date:** 2026-05-20
**Purpose:** Authority map after BLK-SYSTEM-269..271 exact BEO publication finality evidence on top of the BLK-SYSTEM-266..268 run-package preparation.
**Scope:** Current surfaces/cutlines. This document is not a sprint plan, BEB, BEO, runtime approval, blanket `blk-link` authority, protected-body access, or replay ledger.
---
## 1. Lean Index Contract
```text
LEAN_DOCUMENTATION_MODEL_ACTIVE
NO_BLK_DOC_PER_SPRINT
ONE_OUTCOME_PER_SPRINT_NO_TASK_OUTCOME_DOCS
BLK_001_TO_006_FIXED_OVERVIEW_NOT_SPRINT_STATE
LEAN_CURRENT_STATE_INDEX_ACTIVE
CURRENT_STATE_INDEX_GRANTS_NO_LIVE_AUTHORITY
ACCELERATION_MODE_BOUNDED_PRODUCTION_MOVEMENT
NO_KURONODE_MUTATION_AUTHORITY
BLK_TEST_FUNCTIONAL_MODULE_NOT_BLK_SYSTEM_TEST_SUITE_PINNED
```
BLK-079 is a compact current-state map; historical detail lives in `docs/outcomes/`.
---
## 2. Current State
```text
BLK_SYSTEM_271_EXACT_BEO_PUBLICATION_FINALITY_RECONCILED / BLK_SYSTEM_270_EXACT_BEO_PUBLICATION_FINALITY_RECORD_EXECUTED / BLK_SYSTEM_269_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_CAPTURED / BLK_SYSTEM_268_EXACT_BEO_PUBLICATION_RUN_PACKAGE_RECONCILED / BLK_SYSTEM_267_EXACT_BEO_PUBLICATION_RUN_PREFLIGHT_BLOCKED / BLK_SYSTEM_266_EXACT_BEO_PUBLICATION_RUN_PACKAGE_READY / BLK_SYSTEM_265_EXACT_BEO_PUBLICATION_APPROVAL_CAPTURE_RECONCILED / BLK_SYSTEM_264_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CAPTURED / BLK_SYSTEM_263_SPRINT_PACKAGE_SELECTION_GATE_READY / BLK_SYSTEM_262_SPRINT_PACKAGE_GRANULARITY_CONTRACT_READY / BLK_SYSTEM_261_SPRINT_PACKAGE_FRONTIER_REVIEW_READY
BLK_SYSTEM_260_EXACT_BEO_PUBLICATION_APPROVAL_RECONCILED_NOT_GRANTED / BLK_SYSTEM_259_EXACT_BEO_PUBLICATION_APPROVAL_PREFLIGHT_RECORDED / BLK_SYSTEM_258_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_CONTRACT_READY / BLK_SYSTEM_257_EXACT_BEO_PUBLICATION_RUN_REQUEST_READY
BLK_SYSTEM_256_RTM_BLK_LINK_DRIFT_COVERAGE_RECONCILED / BLK_SYSTEM_255_EXACT_METADATA_ONLY_DRIFT_COVERAGE_DRY_RUN_RECORDED / BLK_SYSTEM_254_DRIFT_COVERAGE_VERIFIER_CONTRACT_READY / BLK_SYSTEM_253_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_SCOPED / BLK_SYSTEM_252_RTM_BLK_LINK_DRIFT_COVERAGE_SURFACE_REVIEW_READY
BLK_SYSTEM_251_REUSABLE_BEO_PUBLICATION_RECONCILED_PER_RUN_EXACT_APPROVAL_READY / BLK_SYSTEM_250_BLK003_LOOP_BEO_PUBLICATION_REVIEW_INTEGRATION_READY / BLK_SYSTEM_249_EXACT_BEO_PUBLICATION_DRY_RUN_REVIEW_READY / BLK_SYSTEM_248_REUSABLE_BEO_PUBLICATION_CONTRACT_READY / BLK_SYSTEM_247_REUSABLE_BEO_PUBLICATION_REQUEST_SCOPED
BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY / BLK_SYSTEM_245_BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY / BLK_SYSTEM_244_METADATA_ONLY_BLK_TEST_ORACLE_FIXTURE_READY
BLK_SYSTEM_243_PRODUCTION_BLK_TEST_MCP_ORACLE_CONTRACT_READY / BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED / BLK_SYSTEM_241_REUSABLE_BLK003_LOOP_KERNEL_READY
BLK_SYSTEM_240_HITL_GATEWAY_COMPLETION_SLICE_READY / BLK_SYSTEM_239_BLK_ID_RELAY_SCOPE_DECIDED / BLK_SYSTEM_238_ROOT_DOCTRINE_DEVIATION_OVERLAY_READY / BLK_SYSTEM_237_KURONODE_ROUTE_SELECTION_READY
BLK_SYSTEM_235_AGENT_A_CONTEXT_PACKET_PR_MERGED / BLK_SYSTEM_234_REPEAT_KURONODE_FEATURE_DROP_EXECUTED / BLK_SYSTEM_233_CODEX_PROGRESS_EVENTS_READY / BLK_SYSTEM_232_BEB_L2_PACKET_HELPER_READY / BLK_SYSTEM_231_AGENT_A_HEADER_PR_MERGED / BLK_SYSTEM_230_AGENT_A_HEADER_DROP_EXECUTED / BLK_SYSTEM_229_PRIVATE_BWRAP_WORKSPACE_WRITE_SETUP_READY / BLK_SYSTEM_228_EXACT_KURONODE_CLEAN_WORKTREE_FEATURE_DROP_EXECUTED / BLK_SYSTEM_227_EXTERNAL_CODEX_ARTIFACT_READY / BLK_SYSTEM_226_KURONODE_WORKTREE_STATIC_PROFILE_READY / BLK_SYSTEM_225_CLEAN_WORKTREE_MANIFEST_READY / BLK_SYSTEM_224_IGNORED_RESIDUE_CLEANUP_PLAN_READY / BLK_SYSTEM_223_BEB_L2_PREFLIGHT_GUARD_READY / BLK_SYSTEM_222_BEB_L2_BLK_PIPE_CODEX_ROUTE_READY
BLK_SYSTEM_221_FOURTH_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED
BLK_SYSTEM_220_NATIVE_CODEX_SANDBOX_REPAIR_RECHECK_RECORDED
BLK_SYSTEM_219_NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED
BLK_SYSTEM_218_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED
BLK_SYSTEM_217_CODEX_EXACT_UNDO_EXERCISE_RECORDED
BLK_SYSTEM_216_CODEX_PERMISSION_PROFILE_CONTAINMENT_DRILL_RECORDED
BLK_SYSTEM_215_SUPERVISED_CODEX_KURONODE_FEATURE_LOOP_EXECUTED
BLK_SYSTEM_214_BOUNDED_KURONODE_FEATURE_LOOP_EXECUTED
BLK_SYSTEM_213_BLK_TEST_OPTIONAL_DIAGNOSTIC_UNBLOCK_READY
BLK_SYSTEM_212_VALIDATION_PROFILE_RECONCILED_CLEAN
BLK_SYSTEM_211_VALIDATION_PROFILE_CONTRACT_READY
BLK_SYSTEM_210_VALIDATION_PROFILE_SURFACE_REVIEW_READY
BLK_SYSTEM_209_PYTHON_ADAPTER_RECONCILED_CLEAN
BLK_SYSTEM_208_PYTHON_ADAPTER_CONTRACT_READY
BLK_SYSTEM_207_PYTHON_ADAPTER_SURFACE_REVIEW_READY
BLK_SYSTEM_206_BLK_PIPE_BOUNDED_ENFORCEMENT_RECONCILED_CLEAN
BLK_SYSTEM_205_BLK_PIPE_BOUNDED_ENFORCEMENT_CONTRACT_READY
BLK_SYSTEM_204_BLK_PIPE_SURFACE_REVIEW_READY
BLK_SYSTEM_203_KURONODE_BLK_REQ_BRIDGE_RECONCILED_CLEAN
BLK_SYSTEM_202_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MATERIALIZED
BLK_SYSTEM_201_KURONODE_BLK_REQ_EXACT_ID_MAPPING_MANIFEST_READY
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
blk200_bootstrap_package_hash=sha256:8e0414e4564d7ae6567487e807374497fee337f20ec53eb47a6e7ca9a3958229 / blk201_mapping_manifest_hash=sha256:97cbec0a33c9cbd01aaf0c7a0256694997c3cfdff731f09897215037ed924a51 / blk202_mapping_materialization_hash=sha256:3b01bba50b42f5ef2bf33257911cf6052109115dd1eddb9dbcf876febe32785a / blk203_bridge_reconciliation_hash=sha256:402c1620e40d3dfaa907af697670752fe7d8e3b394d0211d646b296d1fc99650
blk252_surface_review_hash=sha256:d3ff6c7b6229a903df02357cc0d97b47019712e7863bbd2a1166cf4f6cca198c / blk253_request_hash=sha256:70f8dd51dbdad839aa4fe0a32f1e1f3bf1c3a1b8bd066eca6c101dbcdb6b4861 / blk254_contract_hash=sha256:d5e4e81b0416a8ef95030753a4de97c37fdc8ac6fb736b1da9b453c113612f84 / blk255_dry_run_hash=sha256:86930819cc0b57f98d08148c8e9f78869232776cdc537aabe07469514b4b461a / blk256_reconciliation_hash=sha256:de39b2ece921871e31c6c7892d1fbbd971c15ec68f2db6dd67c3d7c7db1f4e5f
blk257_request_hash=sha256:a406ef82b236d5cabbd0aede735ee2d9149f6d1b80245ca335496dfb5d8ce218 / blk258_contract_hash=sha256:b8e47c5343bfd73e2db4d1b6eabcc474c2140080339cd98c857356024b2e9581 / blk259_preflight_hash=sha256:09df68a4bd7dae47deb4001a7c7dcb0870b6b084fc20c1eb822e6939e02d58f2 / blk260_reconciliation_hash=sha256:e66022d4906aeb4749407a6c0557c66813f099d2ebec37f87ef2c51a784317a9
blk261_frontier_review_hash=sha256:7c70581968eae55b6629498df2515dcb18eb7913431bd4aba9b9e5c5f42b14a6 / blk262_granularity_contract_hash=sha256:26b22fb7679f282bce29308d514d59d234110b9475a4a3223df929aedef44b99 / blk263_selection_gate_hash=sha256:b3fbfbc3ba4384a4b60143f9ff66aae41ddfe156eed4706575f48c645861cbc8
blk264_approval_capture_hash=sha256:cdf22534b46214ebf8b57a580c183536f289e15a1e482d7726638e0628237399 / blk265_approval_capture_reconciliation_hash=sha256:c20f5a0a39383fbfdd811d15aab4f56fae7973d2ddf4f22d9e6b3337c7ca9b21
blk266_run_package_hash=sha256:7815590afd45c9ab978e6bcfffa09446b870e9c17d66688c31c5ca36905e4a23 / blk267_run_preflight_hash=sha256:9ed5a7ee1139be7d48df8d2a6baaee10a8a24a7bdbd7abc469b062e5b95b2e5c / blk268_run_package_reconciliation_hash=sha256:e1602b1abd0c96badb12efca01e794f48da06e6d69ab1b3d8e86b27f0e882172
blk269_execution_approval_hash=sha256:856ae211896f2fe55cfac21ec955583399182a479ccbaf955ccb6c6612a8d9e9 / blk270_finality_execution_hash=sha256:2cd4b38b78452fadd96456acfc2cbc6a218e46c4d0a9342220fbca6d9d8a389e / blk271_reconciliation_hash=sha256:19195c218d30eb18b5343d40b3177e3c1cce3260c8519810b3e424cdccc1d49c
NEXT_FRONTIER_RTM_BLK_LINK_DRIFT_COVERAGE_REQUEST_READY_AFTER_EXACT_BEO_PUBLICATION / previous_frontier=NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_REQUIRED_FOR_RTM_DRIFT_COVERAGE_NOT_GRANTED / NEXT_FRONTIER_EXACT_BEO_PUBLICATION_OPERATOR_APPROVAL_TEXT_REQUIRED_NOT_GRANTED / NEXT_FRONTIER_EXACT_BEO_PUBLICATION_RUN_PACKAGE_REQUIRED_NOT_EXECUTED / NEXT_FRONTIER_EXACT_BEO_PUBLICATION_EXECUTION_APPROVAL_REQUIRED_NOT_GRANTED
```
Active state: BLK-SYSTEM-269..271 bind the exact execution approval text, one run ID, signature/storage/ledger receipt hashes, finality record hash, and next-frontier reconciliation. BLK-SYSTEM-263 still keeps generic package directives non-approval. BLK-SYSTEM-222 remains the closed-schema dispatch route; Kuronode mutation still requires a separate exact BEB-L2 payload.
---
## 3. Current Authority Surfaces
| Surface | Current state | Authority cutline |
| --- | --- | --- |
| BLK-req legislative gateway | BLK-240 HITL gateway slice ready | BLK-SYSTEM-240 binds exact-ID lifecycle operations, metadata-only exact ID mapping, and per-operation approval capture after BLK-SYSTEM-239 boxed blk-id/blk-relay as target names. No Kuronode source/Git mutation, broad doc scan, protected-body migration, body access without exact ID, BEO closeout/publication, drift rejection, RTM generation, runtime/tooling, or blanket `blk-link`. |
| BLK-pipe blast shield | BLK-206 bounded non-authorizing enforcement surface closed | Structured validation-profile argv, failure/denial/cleanup evidence, and exact allowlists are boxed evidence only: no broad dispatch, no target/source/Git mutation, no runtime tooling, and no production-isolation claim. |
| Python adapter layer | BLK-241 loop kernel ready | BLK-SYSTEM-241 layers iteration state, per-iteration approval, failure ceiling, stop conditions, and BEO draft rules over the proven BEB-L2 route. BLK-SYSTEM-237/238 keep Kuronode mutation separate from root-doctrine cleanup. No broad BLK-pipe runtime, Hermes-direct Kuronode mutation, reusable live Codex authority, protected-body, RTM/BEO closeout, runtime/tooling, package-manager, host containment claim, or production-isolation authority. |
| Validation profiles | BLK-226 Kuronode worktree static profile ready | `kuronode-worktree-static` is a repository-owned `git diff --check -- .` argv profile for exact clean-worktree BEB-L2 drops. It is local whitespace/static evidence only; no package manager, network, runtime, mutation, publication, RTM, tooling, production-isolation, BLK-pipe dispatch, or BLK-test MCP authority. |
| BLK-test | BLK-246 verifier-only oracle reconciled | BLK_SYSTEM_246_PRODUCTION_BLK_TEST_MCP_ORACLE_RECONCILED_VERIFIER_ONLY after BLK_SYSTEM_242_PRODUCTION_BLK_TEST_MCP_ORACLE_REQUEST_SCOPED through BLK_SYSTEM_245_BLK003_LOOP_ORACLE_EVIDENCE_INTEGRATION_READY. BLK-test is verifier-only after governed loop evidence; transport remains disabled and PASS is not approval. No planner/dispatcher, source of truth, source/Git mutation, BEO/RTM, drift/coverage truth, tooling, or protected-body authority. |
| Operator health / observability | Advisory local pilot | Health output is advisory only; PASS is not execution approval, sandbox evidence, BEO/RTM truth, or protected-body authority. |
| Codex live-dispatch ladder | BLK-229 private-bwrap setup descriptor verified for BLK-230 | BLK-SYSTEM-229 documents the private bwrap AppArmor route for Codex `workspace-write` while keeping `kernel.apparmor_restrict_unprivileged_userns=1`; BLK-SYSTEM-230 verified `/opt/blk-system/codex-bwrap/bwrap`, loaded `blk-codex-bwrap`, and descriptor `READY` before dispatch. BLK-SYSTEM-220 remains the workspace-write smoke passed only under runtime host-admin AppArmor userns relaxation anchor. Future runs must recheck the descriptor. No reusable Codex dispatch, persistent host-wide relaxation, broad source mutation, package/network/model/browser/cyber tooling, or production-isolation claim is granted. |
| BEO publication path | BLK-271 finality evidence reconciled | BLK-SYSTEM-271 reconciles BLK-SYSTEM-270 one-run finality record after BLK-SYSTEM-269 exact approval capture. One run ID was consumed into deterministic signature/storage/ledger receipt evidence only. No future publication run, reusable signer/storage/ledger authority, BEO closeout execution, RTM generation, drift/coverage truth, protected-body access, runtime/tooling, or target/source/Git mutation. |
| RTM / blk-link | Request-ready after exact BEO finality evidence | BLK-SYSTEM-256 metadata-only drift/coverage verifier can now move to a request-only RTM / `blk-link` drift-coverage package, but no RTM generation, production `blk-link`, drift rejection, coverage truth, protected-body text return, or target/source/Git mutation is granted. |
---
## 4. Governing Pointers
- Active roadmap/index gate: `docs/BLK-077_blk-system-post-078-roadmap.md`, `python/blk_current_state_authority_index.py`
- BLK-SYSTEM-241/240/239/238/237 and BLK-SYSTEM-230/229/228/227/226/225/224/223/222 loop/route/profile/tests: `python/beb_l2_blk_pipe_route.py`, `python/test_beb_l2_blk_pipe_route.py`, `python/codex_private_bwrap_setup.py`, `docs/runbooks/codex-private-bwrap-apparmor.md`
- Codex anchors: `docs/BLK-121_codex-configuration-and-containment-contract.md`, `python/product_codex_native_sandbox_repair_recheck_220.py`
---
## 5. Authority Boundary
This index grants no blanket production `blk-link`, no production `blk-link` without per-run exact approval, no approval reuse, no reusable run-ID reservation/consumption, and no global replay-ledger claim.
It grants no reusable RTM generation, no drift rejection, no coverage truth, no active-vault comparison authority, no protected-body text return, no broad Kuronode doc scan, no protected-body migration, and no protected BLK-req body reads/copying/parsing/hashing/scanning/mutation outside exact BLK-req gateway operations.
It grants no reusable BEO publication/signing/storage/ledger authority, no future publication run, no rollback/revocation/supersession execution, no BEB dispatch outside separately approved exact BEB-L2 payloads, no BEO closeout execution, no live Codex outside separately approved exact BEB-L2 / BLK-pipe payloads, no reusable Codex dispatch, no BLK-pipe runtime beyond an exact approved payload, no broad dispatch, no production BLK-test MCP transport, no generic BLK-test MCP transport, no broad target/source/Git mutation, no package/network/model/browser/cyber tooling, no runtime tooling, no host-side containment claim for Codex sandbox mode (`workspace-write` or prior `danger-full-access` fallback), and no production-isolation claim.
---
## 6. Documentation Burden Guard
BLK-079 should remain short enough to read in one pass. Do not append sprint-by-sprint status chains here. Add current-state deltas only when they affect operator selection; otherwise record evidence in the single sprint closeouts under `docs/outcomes/`.
