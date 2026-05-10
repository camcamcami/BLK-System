# BLK-SYSTEM-055 — Authoritative BEO Publication Approval Envelope / Pilot Boundary Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Create a deterministic exact-target approval-envelope / pilot-boundary package for future authoritative BEO publication without performing publication or granting signer/storage/ledger authority.
**BLK-024 / BLK-059 track:** Track G — BEO publication path; BLK-059 Workstream C; maturity L0/L1 approval-envelope/preflight only.
**Architecture:** BLK-SYSTEM-054 produced request-readiness under BLK-057, but that request is not publication authority. BLK-SYSTEM-055 defines the next boundary: an exact-target approval envelope and future pilot contract that binds one BEO candidate/evidence bundle to signer, storage, ledger, rollback, audit, replay, expiry, and operator-stop controls while keeping publication side effects disabled. RTM / blk-link remains a later separate authority.
**Tech Stack:** Python deterministic fixture module/tests; Markdown boundary, review, and outcome docs.
**Authority boundary:** Approval-envelope / pilot-boundary readiness only. No authoritative BEO publication, no runtime `PUBLISHED` BEO output, no live publication approval capture, no signer key material, no cryptographic signing, no immutable storage write, no public ledger append/mutation, no rollback/revocation/supersession execution, no RTM generation, no RTM drift rejection, and no protected BLK-req body reads.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T15:19:59+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: 39153b1 docs: update blk-system post-058 roadmap
git rev-parse HEAD: 39153b1893ff46137e8c78d4a59cf4801c9d4271
```

ID discovery:

```text
BLK-SYSTEM-055 plan: not present before this sprint
BLK-060 document: not present before this sprint
Existing BLK-055 is docs/BLK-055_blk-test-fresh-non-disposable-l4-runtime-pass-boundary.md and is unrelated to sprint number BLK-SYSTEM-055.
```

Relevant prerequisite closeout:

```text
docs/outcomes/BLK-SYSTEM-054_sprint-closeout.md
```

BLK-SYSTEM-054 authorizes only request-readiness:

```text
AUTHORITATIVE_BEO_PUBLICATION_AUTHORITY_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION
```

---

## 2. Governing Doctrine Alignment

- **BLK-059:** Controls current sequencing. Workstream C recommends a BEO publication approval envelope before any publication pilot. Workstream D requires explicit later authority before one bounded publication pilot.
- **BLK-024:** Supplies maturity vocabulary. This sprint is L0/L1 approval-envelope/preflight only, not L4/L5 publication runtime.
- **BLK-001:** Preserves V-model separation: BLK-test evidence is not BEO publication, and BEO publication is not RTM / blk-link trace closure.
- **BLK-002 / BLK-005 / BLK-006:** Preserve protected BLK-req vault immutability and no protected body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison.
- **BLK-003 / BLK-004:** Preserve bounded execution, BLK-pipe mutation enforcement, validation/profile boundaries, and no implicit inheritance from BLK-pipe or BLK-test success.
- **BLK-022:** Requires publication-specific approval, signer identity, storage target, public ledger target, rollback/revocation/supersession planning, and audit/replay handling before publication authority.
- **BLK-057:** Provides request-readiness only. BLK-SYSTEM-055 may consume its request package but must not turn it into publication authority.

---

## 3. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, package-manager/network/model/browser/cyber tooling, or production isolation claims.

---

## 4. Implementation Intent

Create a deterministic local fixture module that builds and validates an approval-envelope / pilot-boundary package with status:

```text
AUTHORITATIVE_BEO_PUBLICATION_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_PUBLICATION
```

The envelope must bind:

1. upstream BLK-057 request package identity and hash;
2. exact BEO ID/hash, candidate ID, source evidence hash, and trace artifacts;
3. exact publication target identity and target URI/reference without writing;
4. publication approval envelope ID, operator identity, expiry, replay ID, pilot ID, and approval scope;
5. signer identity/policy without key material or signature generation;
6. immutable storage target/policy without writes;
7. public ledger target/policy without append/mutation;
8. rollback, revocation, and supersession policies without execution;
9. audit bundle identity/hash without durable publication side effects;
10. operator stop and timeout/output bounds;
11. exact denied-authority coverage and no-side-effect flags.

It must reject stale/replayed/expired/mismatched envelopes, inherited approval wording, side-effect flags, signer secrets, storage/ledger/rollback execution claims, RTM/coverage/drift fields, protected BLK-req path/body references, malformed hashes/IDs, duplicate or malformed denied-authority lists, arbitrary extra fields, and compact/camelCase/allcaps/acronym authority-laundering variants.

---

## 5. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-055_authoritative-beo-publication-approval-envelope.md
docs/outcomes/BLK-SYSTEM-055_task-000-outcome.md
```

Actions:

1. Record preflight state and governing docs.
2. Publish the plan and Task 000 outcome.
3. Do not modify runtime publication behavior in Task 000.

### Task 001 — Approval-envelope fixture via TDD

Deliverables:

```text
python/authoritative_beo_publication_approval_envelope.py
python/test_authoritative_beo_publication_approval_envelope.py
docs/outcomes/BLK-SYSTEM-055_task-001-outcome.md
```

Actions:

1. Write RED tests for a valid approval envelope and no-side-effect pilot-boundary summary.
2. Write RED tests for authority laundering in nested keys/strings, inherited BLK-test/BLK-pipe/Codex/request approval, signer/storage/ledger/rollback side effects, RTM/coverage/drift fields, protected-body references, stale/replayed/expired approvals, mismatched hashes, and exact excluded-authority set mismatch.
3. Implement the smallest deterministic fixture/validator that passes.
4. Verify focused tests.

### Task 002 — BLK-060 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-060_authoritative-beo-publication-approval-envelope-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-055_authoritative-beo-publication-approval-envelope-hostile-review.md
docs/outcomes/BLK-SYSTEM-055_task-002-outcome.md
```

Actions:

1. Add BLK-060 markers proving approval-envelope readiness only.
2. Add persistent active doctrine gate coverage for BLK-060.
3. Hostile-review code/docs for request-as-publication laundering, approval-as-publication laundering, signer/storage/ledger side effects, RTM/drift inheritance, protected-body access, and pilot-boundary scope creep.
4. Remediate blockers with tests and docs.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-055_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-055_sprint-closeout.md
```

Actions:

1. Run focused approval-envelope tests, active doctrine gates, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 6. Stop Conditions

Stop and report before closeout if any implementation:

1. emits runtime `PUBLISHED` BEO output;
2. performs publication, signing, storage writes, public ledger append/mutation, rollback, revocation, or supersession;
3. captures or claims live publication approval;
4. reads, copies, parses, hashes, summarizes, scans, mutates, or compares protected BLK-req bodies;
5. generates RTM, coverage matrices, drift decisions, or active-vault hash comparisons;
6. treats BLK-057 request-readiness, BLK-test PASS, BLK-pipe success, Codex approval, candidate fixtures, or published-input fixtures as publication authority;
7. weakens existing BLK-test/BEO/RTM denial flags;
8. fails hostile review or verification.
