# BLK-SYSTEM-049 — BLK-test L4 Evidence Trust and Non-Disposable Request Gate Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-045/BLK-047/BLK-048/BLK-049/BLK-050/BLK-051 and BLK-001 through BLK-006 as applicable.

**Goal:** Review whether BLK-SYSTEM-048 disposable L4 verification evidence is trustworthy enough to request a later non-disposable exact-target L4 pilot, while keeping that later pilot non-runtime and human-review-only in this sprint.

**BLK-024 track:** Track F — BLK-test production-readiness ladder / Track G prerequisite guard; maturity L0/L1 gate fixture only.

**Architecture:** BLK-SYSTEM-048 proved one harness-owned disposable real-repo L4 runtime slice. BLK-SYSTEM-049 must not jump to arbitrary repositories or BEO/RTM. It creates a trust gate that inspects evidence, hostile-review outcomes, final verification, and non-authority flags before producing a request-ready package for a later exact-target non-disposable L4 pilot.

**Tech Stack:** Markdown doctrine, Python deterministic fixture, unittest, Go verification.

**Authority boundary:** This sprint is non-runtime. It does not execute against non-disposable repositories. It does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary shell, package-manager/network/model/browser/cyber tooling, source/Git mutation by BLK-test, protected BLK-req body reads, authoritative BEO publication, RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-10T08:09:46+10:00
Branch: main...origin/main
HEAD: 9ccb17c docs: close blk-system sprint 048 disposable l4 runtime
Remote HEAD: 9ccb17cf95efaf7c4ac1acfefa08f7e436c6816a refs/heads/main
Existing highest system plan: docs/plans/blk-system-048_blk-test-fixed-tool-l4-disposable-real-repo-runtime.md
Existing highest BLK boundary doc: docs/BLK-051_blk-test-fixed-tool-l4-disposable-real-repo-runtime-boundary.md
```

Discovery found no existing `BLK-SYSTEM-049`, `blk-system-049`, or `BLK-052` owner in the repository.

---

## 1. Why This Is the Next Logical Sprint

BLK-SYSTEM-048 closeout says the safe next step is to pause and review whether L4 disposable real-repo verification evidence is trustworthy enough to request a narrowly scoped non-disposable exact-target L4 pilot, or whether to return to Codex live-dispatch L3. Because the operator requested the next logical BLK-System sprint without naming a non-disposable target repository, BLK-SYSTEM-049 cannot safely execute a non-disposable L4 pilot. The safe completion step is therefore an evidence-trust and request gate.

The sprint may produce:

```text
NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
```

It must not produce runtime approval or execute the requested future pilot.

---

## 2. Governing Documents and Obligations

| Governing doc | BLK-SYSTEM-049 obligation |
| --- | --- |
| BLK-045 | Continue Fork C and do not pursue BEO publication before verification evidence is trustworthy. |
| BLK-051 | Treat disposable L4 evidence as evidence only; do not authorize arbitrary repositories. |
| BLK-050 | Preserve exact-target repo/path/branch/workspace/replay/output/cleanup/operator-stop requirements for any future L4 runtime. |
| BLK-049 | Preserve fixed-tool-only `run_ast_validation` and no production/generic BLK-test MCP. |
| BLK-048 | Do not select BEO/RTM until verification evidence is trustworthy and separately authorized. |
| BLK-047 | Preserve approval-request boundary and no adjacent authority inheritance. |
| BLK-001 | BLK-test remains verification evidence only; publication and trace closure remain separate. |
| BLK-002 / BLK-005 / BLK-006 | Preserve protected-vault isolation and no protected body reads. |
| BLK-003 / BLK-004 | Preserve human gates, hostile review, bounded context, and BLK-pipe ownership of mutation/Git authority. |

---

## 3. Implementation Surface

### New boundary document

```text
docs/BLK-052_blk-test-l4-evidence-trust-and-non-disposable-request-gate.md
```

Required markers:

```text
BLK_TEST_L4_EVIDENCE_TRUST_AND_NON_DISPOSABLE_REQUEST_GATE
NON_DISPOSABLE_L4_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME
DISPOSABLE_L4_EVIDENCE_TRUST_REVIEW_ONLY
NO_NON_DISPOSABLE_RUNTIME_THIS_SPRINT
EXACT_TARGET_NON_DISPOSABLE_REPO_REQUIRED_FOR_FUTURE_RUNTIME
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_049
```

### New trust-gate fixture

```text
python/blk_test_l4_evidence_trust_request_gate.py
python/test_blk_test_l4_evidence_trust_request_gate.py
```

The fixture must:

1. consume only local evidence summaries and docs from BLK-SYSTEM-048;
2. require BLK-SYSTEM-048 PASS evidence, hostile review PASS-after-remediation, and final verification markers;
3. require all non-authority flags to remain false/disabled;
4. reject PASS-as-approval, BEO/RTM/coverage/drift/publication, production MCP, protected-body, target-repo, and source-mutation laundering;
5. reject any proposed non-disposable target that is missing exact repo/path/branch/workspace/replay/output/cleanup/operator-stop fields;
6. return request-ready-for-human-review only, never runtime approval.

---

## 4. Tasks

### Task 0 — Plan publication

1. Write this plan and Task 000 outcome.
2. Verify Markdown fences and `git diff --check`.
3. Commit and push exact plan/outcome paths.

### Task 1 — BLK-052 boundary and active-doctrine gate

1. Add a failing active-doctrine gate for BLK-052.
2. Verify RED because BLK-052 is missing.
3. Write BLK-052.
4. Verify GREEN focused doctrine gate.
5. Write Task 001 outcome.
6. Commit and push exact paths.

### Task 2 — Evidence-trust request-gate fixture

1. Add failing tests for request-ready, missing evidence, hostile-review not-pass, BEO/RTM/production authority laundering, missing future exact-target fields, and attempted runtime approval.
2. Verify RED because the module/API is missing.
3. Implement the deterministic fixture.
4. Verify GREEN focused and related suites.
5. Write Task 002 outcome.
6. Commit and push exact paths.

### Task 3 — Hostile review, remediation, and closeout

1. Run hostile review focused on authority laundering, target inheritance, BEO/RTM drift, protected-body leakage, and runtime approval confusion.
2. Remediate blockers with tests first.
3. Run focused tests, full Python discovery, `go test ./...`, `go vet ./...`, and `git diff --check`.
4. Write hostile review, Task 003 outcome, and sprint closeout.
5. Commit and push exact paths.

---

## 5. Stop Conditions

Pause and require new human approval if any task attempts to:

1. execute against a non-disposable repository;
2. treat BLK-SYSTEM-049 request-readiness as runtime approval;
3. authorize production/generic BLK-test MCP;
4. mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test;
5. read protected BLK-req bodies;
6. publish authoritative BEOs;
7. generate RTM or reject drift;
8. claim production isolation.

---

## 6. Definition of Done

BLK-SYSTEM-049 is complete when:

- BLK-052 exists and is pinned by a persistent doctrine gate;
- the evidence trust fixture returns request-ready only for complete BLK-SYSTEM-048 evidence and future exact-target proposal fields;
- no runtime, BEO, RTM, production MCP, protected-body, or source-mutation authority is granted;
- hostile review passes after remediation;
- full verification passes;
- all outcome docs and closeout are committed and pushed to `origin/main`.
