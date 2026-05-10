# BLK-056 — Repeatable Non-Disposable L4 Wrapper Approval Boundary

**Status:** Active wrapper-hardening boundary — repeatable approval-envelope support only; no new runtime run
**Date:** 2026-05-10T12:20:00+10:00
**Sprint:** BLK-SYSTEM-053
**Marker:** BLK_TEST_REPEATABLE_NON_DISPOSABLE_L4_WRAPPER_APPROVAL_BOUNDARY
**Readiness marker:** REPEATABLE_APPROVAL_ENVELOPE_SUPPORT_READY_NOT_RUNTIME_AUTHORITY

---

## 1. Purpose

BLK-056 defines the authority boundary for cleaning up the BLK-test non-disposable L4 runtime wrapper after the BLK-SYSTEM-052 PASS evidence.

BLK-SYSTEM-052 proved that one exact approved fixed-tool `run_ast_validation` non-disposable L4 runtime pilot can return trustworthy evidence. It also left a historical compatibility wart: future fresh approvals should not need to reuse BLK-SYSTEM-051-specific nonce and marker strings.

BLK-056 therefore authorizes only wrapper cleanup that supports repeatable future approval envelopes. It does not authorize another runtime execution.

---

## 2. Required Wrapper Contract

Typed L4RuntimeApprovalEnvelope required for future fresh approvals.

Future envelopes must bind sprint, approval_id, run_id, expected_head, approved paths, replay ledger path, marker nonce binding, and workspace marker name.

marker_nonce_binding must equal the approval envelope sprint, not a weak substring.

approval_id and run_id must bind to the approval envelope sprint and public fresh-envelope construction must not reuse consumed BLK-SYSTEM-051 or BLK-SYSTEM-052 IDs.

The internal legacy BLK-SYSTEM-051 default envelope is retained only to preserve historical tests/callers and must not be used as a fresh approval path.

replay_ledger_path must not overlap target_repo_path, source_subtree_path, `.git`, protected BLK-req descendants, or workspace_clone_path.

Envelope fixed_tool must remain run_ast_validation.

workspace_marker_name must be a single hidden filename inside the wrapper-owned workspace.

Legacy BLK-SYSTEM-051 wrapper path remains historical compatibility only.

No reuse of BLK-SYSTEM-051 or BLK-SYSTEM-052 consumed approval/run IDs.

PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_053_WRAPPER_APPROVAL_CLEANUP

---

## 3. Safety Invariants Preserved

The wrapper cleanup must preserve all existing safety properties from BLK-SYSTEM-051 and BLK-SYSTEM-052:

1. exact path spelling checks before path resolution;
2. exact approved target repository path;
3. exact approved source subtree path;
4. exact approved workspace clone path;
5. exact approved expected Git HEAD;
6. fixed `run_ast_validation` tool only;
7. required caller-owned replay sets;
8. process-local approval/run replay sets;
9. durable disk replay ledger;
10. replay consumption before workspace creation or tool execution;
11. pre-owned workspace rejection;
12. wrapper-owned workspace marker nonce check;
13. source scope rejection for nested Git metadata, protected BLK-req descendants, secret-like descendants, and symlink escapes;
14. source content/metadata/symlink/root snapshot before and after runtime;
15. `.git` content/metadata/root snapshot before and after runtime;
16. workspace cleanup on PASS, FAIL, BLOCKED, output overflow, and runtime exceptions after ownership;
17. bounded evidence output with accurate serialized byte accounting;
18. evidence-only denial flags for BEO, RTM, MCP, source mutation, shell, network, model-service, browser, cyber, and production-isolation authority.

---

## 4. Explicit Non-Authority Boundary

BLK-056 does not authorize:

- No production BLK-test MCP authority
- No generic BLK-test MCP authority
- No reusable BLK-test service startup
- No new non-disposable runtime run
- No live Codex execution authority
- No arbitrary shell or caller-supplied commands
- No dynamic tool expansion
- No source mutation, staging, commit, push, reset, stash, checkout, revert, or autofix by BLK-test
- No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison
- No authoritative BEO publication
- No runtime RTM generation or RTM drift rejection
- No public ledger mutation
- No package-manager, network, model-service, browser, or cyber tooling authority
- No production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claim

---

## 5. Relationship to Prior Boundaries

BLK-054 and BLK-055 remain historical one-run L4 runtime/passed-evidence boundaries. Their approval/run IDs are consumed and cannot be replayed.

BLK-056 is not a successor runtime approval. It is a maintainability and safety-cleanup boundary so a later separately approved sprint can create a fresh exact target envelope without mixed historical nonce text.

A future fresh runtime sprint must still provide its own human approval, exact target repository, exact source subtree, exact expected Git HEAD, exact workspace, exact replay ledger, expiration, approval/run IDs, fixed tool, and hostile review.
