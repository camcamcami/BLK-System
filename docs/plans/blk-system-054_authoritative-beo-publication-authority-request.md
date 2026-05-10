# BLK-SYSTEM-054 — Authoritative BEO Publication Authority Request Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-045_blk-system-post-042-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Create a deterministic authority-request package for future authoritative BEO publication, without performing publication or granting signer/storage/ledger authority.
**BLK-024 / BLK-045 track:** Track G — BEO publication path; Fork C step 2 after trustworthy BLK-test evidence; maturity L0/L1 request/doctrine/fixture only.
**Architecture:** BLK-SYSTEM-052 proved one trusted BLK-test L4 fixed-tool evidence path. BLK-SYSTEM-053 cleaned the wrapper for future repeatable approvals. BLK-SYSTEM-054 now prepares the next right-side V-model authority boundary: publication-specific approval request readiness for authoritative BEOs. It must keep BLK-test evidence, BEO publication, RTM generation, and drift rejection separate.
**Tech Stack:** Python deterministic fixture module/tests; Markdown boundary, review, and outcome docs.
**Authority boundary:** Request-readiness fixture only. No authoritative BEO publication, no runtime `PUBLISHED` BEO output, no live approval capture, no signer key material, no cryptographic signing, no immutable storage write, no public ledger mutation, no rollback/revocation/supersession execution, no RTM generation, and no protected BLK-req body reads.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T13:00:14+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: fc3a3d3 docs: close blk-system sprint 053 wrapper cleanup
git rev-parse HEAD: fc3a3d3f1d9fb69ab9227c080c3e97a63724b692
```

ID discovery found no existing BLK-SYSTEM-054 plan and no existing BLK-057 document.

Recent prerequisite closeout:

```text
docs/outcomes/BLK-SYSTEM-053_sprint-closeout.md
```

BLK-SYSTEM-053 authorizes only wrapper maintainability hardening and approval-envelope support for future separately authorized runs.

---

## 2. Governing Doctrine Alignment

- **BLK-045:** Controls current sequencing. Fork C recommends BLK-test evidence first, then authoritative BEO publication authority request, then runtime RTM / blk-link request.
- **BLK-024:** Classifies this as Track G / L0-L1 readiness work, not L4/L5 publication runtime.
- **BLK-001:** Preserves component separation: BLK-test returns evidence, BEO publication is a separate authority, and blk-link/RTM remains later trace closure.
- **BLK-002 / BLK-005 / BLK-006:** Preserve protected BLK-req vault immutability and no protected body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison.
- **BLK-003 / BLK-004:** Preserve execution/validation separation and do not convert BLK-pipe or BLK-test success into publication permission.
- **BLK-022:** Design-only authoritative BEO publication boundary; publication-specific approval must bind exact BEO identity, content hash, BLK-test evidence identity, signer/storage/ledger/rollback policy, and operator identity.
- **BLK-026 / BLK-028:** Candidate and published-input fixtures are not authoritative publication. BLK-SYSTEM-054 may consume their vocabulary but must not turn fixtures into runtime publication.

---

## 3. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, any new non-disposable runtime run, live Codex execution, arbitrary shell, caller-supplied commands, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, package-manager/network/model/browser/cyber tooling, or production isolation claims.

---

## 4. Implementation Intent

Create a deterministic local fixture module that builds and validates an authority-request package with a status such as:

```text
AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION
```

The request must require:

1. source BLK-test evidence identity and hash;
2. BEO identity and canonical BEO hash;
3. publication-specific operator approval request identity;
4. explicit signer identity policy without key material;
5. immutable storage target policy without writes;
6. public ledger target policy without mutation;
7. rollback, revocation, and supersession policy without execution;
8. exact excluded-authority set equality;
9. no-side-effect flags for every adjacent authority;
10. strict rejection for nested authority laundering, protected-body/RTM fields, secret material, stale/replayed/expired approvals, mismatched hashes, malformed IDs, and side-effect claims.

---

## 5. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-054_authoritative-beo-publication-authority-request.md
docs/outcomes/BLK-SYSTEM-054_task-000-outcome.md
```

Actions:

1. Record preflight state and governing docs.
2. Publish plan and Task 000 outcome via exact-path commit/push.
3. Do not modify runtime code in Task 000.

### Task 001 — Authority-request fixture via TDD

Deliverables:

```text
python/authoritative_beo_publication_authority_request.py
python/test_authoritative_beo_publication_authority_request.py
docs/outcomes/BLK-SYSTEM-054_task-001-outcome.md
```

Actions:

1. Write RED tests for a valid request package and disabled/no-side-effect adapter summary.
2. Write RED tests for authority laundering in nested strings/keys, runtime publication wording, RTM/coverage/drift fields, signer key material, storage/ledger/rollback side effects, protected-body references, stale/replayed/expired approvals, mismatched hashes, and exact excluded-authority set mismatch.
3. Implement the smallest deterministic fixture/validator that passes.
4. Verify focused tests.

### Task 002 — BLK-057 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-057_authoritative-beo-publication-authority-request-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-054_authoritative-beo-publication-authority-request-hostile-review.md
docs/outcomes/BLK-SYSTEM-054_task-002-outcome.md
```

Actions:

1. Add BLK-057 markers proving request-readiness only.
2. Add persistent active doctrine gate coverage for BLK-057.
3. Hostile-review code/docs for PASS-as-publication laundering, nested signer/storage/ledger authority, RTM/drift inheritance, protected-body access, and side-effect claims.
4. Remediate blockers with tests and docs.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-054_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-054_sprint-closeout.md
```

Actions:

1. Run focused authority-request tests, active doctrine gates, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 6. Stop Conditions

Stop and report before closeout if any implementation:

1. emits runtime `PUBLISHED` BEO output;
2. performs publication, signing, storage writes, public ledger mutation, rollback, revocation, or supersession;
3. captures or claims live publication approval;
4. reads, copies, parses, hashes, summarizes, scans, mutates, or compares protected BLK-req bodies;
5. generates RTM, coverage matrices, drift decisions, or active-vault hash comparisons;
6. treats BLK-test PASS, BLK-pipe success, Codex approval, existing candidate fixtures, or published-input fixtures as publication authority;
7. weakens existing BLK-test/BEO/RTM denial flags;
8. fails hostile review or verification.
