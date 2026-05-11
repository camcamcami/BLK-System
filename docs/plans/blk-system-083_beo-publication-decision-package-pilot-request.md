# BLK-SYSTEM-083 — BEO Publication Decision Package / Pilot Request Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `blk-system-authority-gated-sprints`, and `requesting-code-review` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current roadmap selection in `docs/BLK-077_blk-system-post-078-roadmap.md`, current-state indexing in `docs/BLK-079_post-078-current-state-authority-index.md`, BEO publication boundaries in `docs/BLK-022_authoritative-beo-publication-design-boundary.md`, `docs/BLK-026_beo-publication-candidate-fixture-boundary.md`, `docs/BLK-057_authoritative-beo-publication-authority-request-boundary.md`, `docs/BLK-060_authoritative-beo-publication-approval-envelope-boundary.md`, BLK-081, BLK-082, and BLK-001 through BLK-006 as applicable.

**Goal:** Build a BLK-System-owned BEO Publication Decision Package / Pilot Request fixture and doctrine surface that packages the existing BEO publication authority-request and approval-envelope readiness into an explicit human-review decision package, without approving or performing publication.
**BLK-024 track:** Track G — BEO publication path; Track A — Doctrine, alignment, and review gates / maturity L0 doctrine plus L1 deterministic local fixture.
**Architecture:** BLK-SYSTEM-081 and BLK-SYSTEM-082 completed target-repo governance and BLK-058 submitted-snippet mechanical enforcement. BLK-SYSTEM-083 selects the post-082 BEO Publication Decision Package / Pilot Request frontier and keeps it as a review package only. It consumes existing BLK-057/060 readiness surfaces, binds exact package identities and pilot prerequisites, and records that an actual publication pilot still requires a later explicit approval.
**Tech Stack:** Markdown doctrine, Python unittest fixture validators/evaluators, active doctrine gates, Go/Python verification.
**Authority boundary:** BLK-System documentation and deterministic local fixture/gate work only. No authoritative BEO publication, no runtime `PUBLISHED` BEO output, no live publication approval capture, no signer key material access, no cryptographic signing, no immutable storage writes, no public ledger append/mutation, no rollback/revocation/supersession execution, no RTM generation or drift rejection, no protected BLK-req body reads, no BLK-test/Codex/BLK-pipe runtime, and no target-repo scan or mutation.

---

## 0. Current Known State

Captured: `2026-05-12T07:03:45+10:00`

```text
repo: /home/dad/BLK-System
branch: main
local HEAD: db35411dc6acf4355369141f39e36a255246c94e
remote main: db35411dc6acf4355369141f39e36a255246c94e
status: ## main...origin/main
last commit: db35411 docs: close blk-system 082 mechanical enforcement
```

Discovery:

```text
existing BLK-083 doc: none
existing BLK-SYSTEM-083 plan/outcomes: none
current roadmap selector: docs/BLK-077_blk-system-post-078-roadmap.md
current authority index: docs/BLK-079_post-078-current-state-authority-index.md
BEO publication design boundary: docs/BLK-022_authoritative-beo-publication-design-boundary.md
BEO publication candidate fixture boundary: docs/BLK-026_beo-publication-candidate-fixture-boundary.md
BEO publication authority request boundary: docs/BLK-057_authoritative-beo-publication-authority-request-boundary.md
BEO publication approval envelope boundary: docs/BLK-060_authoritative-beo-publication-approval-envelope-boundary.md
BEO authority-request fixture: python/authoritative_beo_publication_authority_request.py
BEO approval-envelope fixture: python/authoritative_beo_publication_approval_envelope.py
```

---

## 1. Selection Rationale

BLK-077, BLK-079, and the BLK-SYSTEM-082 closeout require a fresh explicit operator decision before any higher-authority frontier after BLK-SYSTEM-082. Candidate frontiers include a bounded BLK-test evidence refresh, a BEO Publication Decision Package or pilot request, a Codex L3 smoke, or an RTM authority request after publication prerequisites exist.

This plan selects **BEO Publication Decision Package / Pilot Request** because:

1. BLK-SYSTEM-081/082 finished the target-governance and mechanical-enforcement cage, so the next strategic unlock is the right side of the BLK-System V-model: BEO publication readiness.
2. RTM authority remains premature until actual authoritative publication prerequisites are explicit.
3. Existing BLK-057 and BLK-060 packages are request/envelope readiness only; BLK-SYSTEM-083 can consolidate them into a current post-082 decision package without granting publication.
4. A deterministic decision-package fixture improves future human approval quality while preserving non-execution and no-publication boundaries.

This sprint does **not** choose or execute the later publication pilot. It prepares the decision package a human can approve or reject in a separate future sprint.

---

## 2. Governing Alignment

| Document | Relevance | Preserved boundary |
| --- | --- | --- |
| BLK-001 | Defines separation among planning, mutation enforcement, BLK-test evidence, BEO publication, and trace closure. | Publication decision readiness is not publication, RTM, mutation, or execution authority. |
| BLK-002 | Defines staged artifact lifecycle and protected-vault isolation. | Decision packages may cite hashes/metadata only and must not read protected BLK-req bodies. |
| BLK-003 | Defines BEB/BEO orchestration, hostile audit, BLK-test evidence, and disabled publication/RTM boundaries. | This sprint creates no BEB dispatch, no BEO closeout execution, no publication run, and no RTM. |
| BLK-004 | Defines BLK-pipe mutation boundaries and validation profiles. | BLK-pipe is not invoked; publication readiness cannot imply source/Git mutation. |
| BLK-005 | Defines traceability and canonical hashes. | The decision package binds existing BEO/evidence/trace hashes without producing RTM or drift decisions. |
| BLK-006 | Defines protected-vault hard deny and HITL authorization. | Future publication authority remains HITL and separate; protected bodies remain unread. |
| BLK-022 | Authoritative BEO publication design-only boundary. | Provides checklist and separation rules; no publisher is authorized. |
| BLK-026 | BEO publication candidate fixture boundary. | Candidate fixtures remain draft-only and not publication. |
| BLK-057 | BEO publication authority request boundary. | Request-readiness is an input, not approval. |
| BLK-060 | BEO publication approval-envelope / pilot-boundary readiness. | Approval-envelope readiness is an input, not publication authority. |
| BLK-077 / BLK-079 | Current post-082 roadmap/current-state authority. | Exactly one frontier is selected; adjacent BLK-test/Codex/RTM/target authorities remain disabled. |

---

## 3. Exact Scope and File Allowlist

### Planning, outcomes, and review docs

```text
docs/plans/blk-system-083_beo-publication-decision-package-pilot-request.md
docs/outcomes/BLK-SYSTEM-083_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-083_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-083_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-083_task-003-outcome.md
docs/reviews/BLK-SYSTEM-083_hostile-review.md
docs/outcomes/BLK-SYSTEM-083_sprint-closeout.md
```

### Doctrine docs

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
docs/BLK-083_beo-publication-decision-package-pilot-request.md
```

### Deterministic local fixtures/gates

```text
python/beo_publication_decision_package.py
python/test_beo_publication_decision_package.py
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
```

No target repository path is in scope. No publication target is written. No signer, storage, ledger, rollback, RTM, BLK-test, Codex, BLK-pipe, package-manager, network, model, browser, cyber, or shell operation is authorized.

---

## 4. Explicitly Forbidden

This sprint does not authorize:

- authoritative BEO publication, runtime `PUBLISHED` BEO output, BEO closeout execution, or BEO-as-success claims;
- live publication approval capture, publication approval acceptance, or actual pilot execution;
- signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback, revocation, or supersession execution;
- runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrix production, coverage truth, or drift decision;
- protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation;
- target-repository scans, TypeScript tooling over real target files, source/Git mutation, staging, commit, push, reset, checkout, revert, stash, cleanup, or autofix;
- BLK-test execution, production BLK-test MCP startup, evidence refresh, live Codex execution, BLK-pipe execution, BEB dispatch, or tactical worker subprocesses;
- network, model-service, browser, cyber, package-manager, signer, immutable storage, release tooling, or arbitrary shell;
- production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

---

## 5. Required Decision-Package Contract

The deterministic fixture must define and validate:

1. a status such as `BEO_PUBLICATION_DECISION_PACKAGE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PUBLISHED`;
2. a selected frontier exactly equal to `beo_publication_pilot_request`, with all adjacent frontier authority denied;
3. exact binding to a BLK-060 approval-envelope package, including canonical recomputation of the submitted envelope hash;
4. exact BEO, candidate, source-evidence, trace-artifact, publication-target, signer-policy, storage-policy, ledger-policy, rollback-policy, audit-bundle, approval ID, run ID, pilot ID, expiry, replay, output-bound, and operator-stop identities;
5. exact proof-obligation set equality for future publication-pilot approval;
6. exact denied-authority set equality and exact false side-effect flags;
7. strict closed schemas for package, decision request, operator attestation, and policy/control objects;
8. rejection of `approval_granted=True`, `publication_approved=True`, publication performed flags, side-effect claims, stale/replayed/expired IDs, malformed timestamps, forged upstream hashes, missing proof obligations, duplicate obligations, and multiple selected frontiers;
9. recursive rejection of BEO publication authority wording, signer/key/secret material, immutable storage/public ledger side effects, rollback/revocation/supersession execution, RTM generation/drift/coverage/active-vault claims, protected-body paths, BLK-test/Codex/BLK-pipe authority, target-repo mutation, tooling, and production-sandbox claims.

The output may be ready for human review only. It must not be approved, published, executed, or treated as a pilot run.

---

## 6. Task Plan

### Task 000 — Plan publication

**Objective:** Publish this sprint plan and task-000 outcome with exact-path staging.

**Files:**

```text
docs/plans/blk-system-083_beo-publication-decision-package-pilot-request.md
docs/outcomes/BLK-SYSTEM-083_task-000-outcome.md
```

**Verification:**

```bash
git diff --check -- docs/plans/blk-system-083_beo-publication-decision-package-pilot-request.md docs/outcomes/BLK-SYSTEM-083_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for name in [
    'docs/plans/blk-system-083_beo-publication-decision-package-pilot-request.md',
    'docs/outcomes/BLK-SYSTEM-083_task-000-outcome.md',
]:
    text = Path(name).read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, name
PY
git status --short --branch
```

**Commit:** `docs: plan blk-system 083 beo publication decision package`

### Task 001 — RED/GREEN decision-package fixture

**Objective:** Add deterministic fixture code and tests for a BEO Publication Decision Package / Pilot Request.

**Files:**

```text
python/beo_publication_decision_package.py
python/test_beo_publication_decision_package.py
docs/outcomes/BLK-SYSTEM-083_task-001-outcome.md
```

**RED:** Add tests first proving the module is missing and must enforce exact selected frontier, upstream envelope hash recomputation, no approval/no publication side effects, exact denied authorities, exact proof obligations, closed schemas, fresh replay/expiry semantics, and hostile laundering rejection.

**GREEN:** Implement the smallest pure-Python, no-file-read, no-live-surface fixture/evaluator needed for the tests to pass.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_beo_publication_decision_package -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
go test ./...
git diff --check -- python/beo_publication_decision_package.py python/test_beo_publication_decision_package.py docs/outcomes/BLK-SYSTEM-083_task-001-outcome.md
```

**Commit:** `feat: add beo publication decision package fixture`

### Task 002 — BLK-083 doctrine and active doctrine gate

**Objective:** Publish BLK-083 as the BEO Publication Decision Package / Pilot Request doctrine and pin it with active doctrine gates.

**Files:**

```text
docs/BLK-083_beo-publication-decision-package-pilot-request.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-083_task-002-outcome.md
```

**RED:** Add an active doctrine gate that fails until BLK-083 contains exact markers for review-only decision package scope, selected frontier, upstream BLK-057/060 binding, future-human-approval requirement, denied publication/signer/storage/ledger/rollback/RTM/protected-body/BLK-test/Codex/BLK-pipe/target/tooling authorities, fixture path, and no production-isolation claim.

**GREEN:** Write the doctrine document with the minimum markers and alignment required by the gate.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk083_beo_publication_decision_package_boundary -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
go test ./...
git diff --check -- docs/BLK-083_beo-publication-decision-package-pilot-request.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-083_task-002-outcome.md
```

**Commit:** `docs: add blk 083 beo publication decision doctrine`

### Task 003 — Roadmap/current-state alignment after BLK-SYSTEM-083

**Objective:** Update BLK-077, BLK-079, and current-state fixtures so BLK-SYSTEM-083 is complete and future actual publication still requires explicit human approval.

**Files:**

```text
docs/BLK-077_blk-system-post-078-roadmap.md
docs/BLK-079_post-078-current-state-authority-index.md
python/blk_current_state_authority_index.py
python/test_blk_current_state_authority_index.py
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-083_task-003-outcome.md
```

**RED:** Add tests that fail until current docs/fixture surfaces include BLK-083 completion markers, remove active BEO Publication Decision Package as an unselected future alternative, and require separate explicit human approval before actual publication pilot execution.

**GREEN:** Update docs and fixtures minimally.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_blk_current_state_authority_index -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint083_completion_requires_explicit_publication_pilot_approval -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
go test ./...
git diff --check -- docs/BLK-077_blk-system-post-078-roadmap.md docs/BLK-079_post-078-current-state-authority-index.md python/blk_current_state_authority_index.py python/test_blk_current_state_authority_index.py python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-083_task-003-outcome.md
```

**Commit:** `docs: align roadmap after blk-system 083`

### Task 004 — Hostile review and sprint closeout

**Objective:** Hostile-review the completed sprint and publish the closeout.

**Files:**

```text
docs/reviews/BLK-SYSTEM-083_hostile-review.md
docs/outcomes/BLK-SYSTEM-083_sprint-closeout.md
```

**Review focus:** decision package becoming publication approval; pilot request becoming pilot execution; approval envelope becoming publication authority; signer/storage/ledger/rollback side-effect smuggling; RTM/coverage/drift laundering; BLK-test/Codex/BLK-pipe/target authority inheritance; protected-body/path smuggling; proof-obligation weakness; stale roadmap guidance.

**Verification:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python3 -m unittest discover python 'test_*.py'
go test ./...
git diff --check
git status --short --branch
```

**Commit:** `docs: close blk-system 083 beo publication decision package`

---

## 7. Stop Conditions

Stop and require explicit human decision if implementation attempts to:

- publish any BEO or emit runtime `PUBLISHED` output;
- capture or accept live publication approval;
- access signer key material or generate cryptographic signatures;
- write immutable storage, append/mutate a public ledger, or execute rollback/revocation/supersession;
- generate RTM, reject drift, compare active-vault hashes, or claim coverage truth;
- invoke BLK-test, BLK-pipe, Codex, package managers, network/model/browser/cyber tooling, or arbitrary shell;
- scan or mutate any target repository;
- read protected BLK-req bodies;
- treat BLK-057, BLK-060, BLK-077, BLK-079, BLK-081, BLK-082, BLK-083, or a decision-package PASS as publication approval or runtime authority.
