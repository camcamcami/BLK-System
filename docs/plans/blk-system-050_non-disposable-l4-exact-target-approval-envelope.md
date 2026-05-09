# BLK-SYSTEM-050 — Non-Disposable L4 Exact-Target Approval Envelope Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as current roadmap authority, retains BLK-024 maturity vocabulary, and preserves BLK-001 through BLK-006 plus BLK-049 through BLK-052 boundaries.

**Goal:** Convert BLK-SYSTEM-049 request readiness into a deterministic exact-target approval-envelope fixture for human review, without executing a non-disposable runtime pilot.

**BLK-024/BLK-045 track:** Track F — BLK-test production-readiness ladder / Fork C completion prerequisite; maturity L0/L1 approval-envelope fixture only.

**Architecture:** BLK-SYSTEM-049 established evidence-trust request readiness but still lacked a mechanically validated non-disposable target approval envelope. BLK-SYSTEM-050 creates the next approval-envelope gate: it accepts only one exact target, binds operator/source/replay/expiry/target/workspace/tool/output/cleanup/stop fields, rejects adjacent authority laundering, and emits review-ready evidence only. Runtime execution remains blocked until a later sprint receives explicit human approval for the exact envelope and performs one bounded read-only `run_ast_validation` pilot.

**Tech Stack:** Markdown doctrine, Python deterministic fixture, unittest, Go verification.

**Authority boundary:** This sprint is non-runtime. It does not execute against a non-disposable repository. It does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary shell, caller-supplied commands, package-manager/network/model/browser/cyber tooling, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-10T08:47:47+10:00
Branch: main...origin/main
HEAD: ade6d2c docs: close blk-system sprint 049 evidence trust gate
Remote HEAD: ade6d2c2fb703a4a9d5dc715c89020d31319afb9 refs/heads/main
Existing highest system plan: docs/plans/blk-system-049_blk-test-l4-evidence-trust-and-non-disposable-request-gate.md
Existing highest BLK boundary doc: docs/BLK-052_blk-test-l4-evidence-trust-and-non-disposable-request-gate.md
```

Discovery found no existing `BLK-SYSTEM-050`, `blk-system-050`, or `BLK-053` owner in the repository.

---

## 1. Why This Is the Next Logical Sprint

BLK-SYSTEM-049 closeout names the next safe BLK-System step as a human decision between a non-disposable exact-target L4 runtime approval sprint and returning to Codex live-dispatch L3. The operator requested the next logical BLK-System sprint without naming a live Codex frontier or an exact non-disposable runtime target.

Because BLK-045 rejects additional generic rungs without a concrete blocker, BLK-SYSTEM-050 fixes the concrete blocker left by BLK-SYSTEM-049: the system can say a non-disposable L4 request is ready for human review, but it cannot yet mechanically prove that a proposed exact-target approval envelope is complete, single-frontier, bounded, replay-safe, non-mutating, non-publishing, and non-RTM.

The only positive state this sprint may produce is:

```text
NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

It must not produce runtime approval or execute the requested future pilot.

---

## 2. Governing Documents and Obligations

| Governing doc | BLK-SYSTEM-050 obligation |
| --- | --- |
| BLK-045 | Advance Fork C only by removing a concrete approval-envelope blocker; do not add broad scaffolding or adjacent runtime authority. |
| BLK-052 | Treat BLK-SYSTEM-049 readiness as request evidence only; do not inherit runtime approval. |
| BLK-051 | Preserve L4 runtime as evidence-only and disposable-scoped; do not generalize to non-disposable execution. |
| BLK-050 | Preserve exact repo/path/branch/workspace/replay/output/cleanup/operator-stop obligations for future L4 runtime. |
| BLK-049 | Preserve fixed-tool-only `run_ast_validation`; no production/generic BLK-test MCP. |
| BLK-048 | Ensure exactly one frontier and block BEO/RTM/publication/drift inheritance. |
| BLK-047 | Preserve authority-request package semantics and required proof markers. |
| BLK-001 | Keep BLK-test as verification evidence only; BEO publication and RTM/blk-link remain separate organs. |
| BLK-002 / BLK-005 / BLK-006 | Preserve active/protected BLK-req vault isolation and no protected body reads. |
| BLK-003 / BLK-004 | Preserve human gates, hostile audit, bounded context, and BLK-pipe ownership of mutation/Git authority. |

---

## 3. Implementation Surface

### New boundary document

```text
docs/BLK-053_non-disposable-l4-exact-target-approval-envelope-boundary.md
```

Required markers:

```text
BLK_TEST_NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE
NON_DISPOSABLE_L4_EXACT_TARGET_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
EXACTLY_ONE_NON_DISPOSABLE_TARGET_REQUIRED
APPROVAL_ENVELOPE_DOES_NOT_AUTHORIZE_RUNTIME
READ_ONLY_RUN_AST_VALIDATION_ONLY_FUTURE_RUNTIME
NO_NON_DISPOSABLE_RUNTIME_THIS_SPRINT
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_050
```

### New approval-envelope fixture

```text
python/blk_test_non_disposable_l4_exact_target_approval_envelope.py
python/test_blk_test_non_disposable_l4_exact_target_approval_envelope.py
```

The fixture must:

1. require BLK-SYSTEM-049 request-ready evidence and artifact hashes;
2. require exactly one selected frontier: `blk_test_non_disposable_l4_run_ast_validation`;
3. require exact target repo path, source subtree path, branch/worktree identity, workspace clone path, workspace marker nonce, fixed tool, timeout/output caps, approval ID, run ID, issue/expiry timestamps, operator identity, source system, cleanup/rollback obligations, operator stop control, hostile-review criteria, and excluded authorities;
4. require read-only and no-side-effect flags for source/Git mutation, package/network/model/browser/cyber tooling, BEO, RTM, drift, publication, and protected-body reads;
5. reject nested or free-form runtime approval wording, selected-frontier multiplication, target/workspace path inheritance, traversal, secret/protected paths, BLK-System repo targeting, malformed timestamps, replay/expiry placeholders, and missing artifact SHA256 binding;
6. return human-review readiness only, never runtime approval.

---

## 4. Tasks

### Task 0 — Plan publication

1. Write this plan and Task 000 outcome.
2. Verify Markdown fences and `git diff --check`.
3. Commit and push exact plan/outcome paths.

### Task 1 — BLK-053 boundary and active-doctrine gate

1. Add a failing active-doctrine gate for BLK-053.
2. Verify RED because BLK-053 is missing.
3. Write BLK-053.
4. Verify GREEN focused doctrine gate.
5. Write Task 001 outcome.
6. Commit and push exact paths.

### Task 2 — Exact-target approval-envelope fixture

1. Add failing tests for review-ready, missing BLK-SYSTEM-049 evidence, multiple frontiers, malformed target/workspace, runtime-approval laundering, BEO/RTM/publication/drift laundering, protected-body/secret path leakage, replay/expiry gaps, and artifact hash mismatch.
2. Verify RED because the module/API is missing.
3. Implement the deterministic fixture.
4. Verify GREEN focused and related suites.
5. Write Task 002 outcome.
6. Commit and push exact paths.

### Task 3 — Hostile review, remediation, and closeout

1. Run hostile review focused on approval inheritance, target inheritance, replay/expiry bypass, single-frontier enforcement, BEO/RTM/publication/drift laundering, protected-body leakage, and runtime approval confusion.
2. Remediate blockers with tests first.
3. Run focused tests, related doctrine tests, full Python discovery, `go test ./...`, `go vet ./...`, and `git diff --check`.
4. Write hostile review, Task 003 outcome, and sprint closeout.
5. Commit and push exact paths.

---

## 5. Stop Conditions

Pause and require a new explicit human decision if any task attempts to:

1. execute against a non-disposable repository;
2. treat BLK-SYSTEM-049 request readiness or BLK-SYSTEM-050 envelope readiness as runtime approval;
3. select more than one frontier;
4. authorize production/generic BLK-test MCP;
5. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test;
6. read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies;
7. publish authoritative BEOs;
8. generate RTM or reject drift;
9. claim production isolation;
10. start live Codex execution.

---

## 6. Definition of Done

BLK-SYSTEM-050 is complete when:

- BLK-053 exists and is pinned by a persistent doctrine gate;
- the approval-envelope fixture returns human-review-ready only for a complete single-frontier non-disposable L4 exact-target envelope with bound BLK-SYSTEM-049 evidence;
- runtime, BEO, RTM, production MCP, protected-body, source-mutation, and live Codex authorities remain denied;
- hostile review passes after remediation;
- full verification passes;
- all outcome docs and closeout are committed and pushed to `origin/main`.
