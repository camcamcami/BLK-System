# BLK-SYSTEM-099 — External BEO Publication Approval Decision Capture Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current sequencing in `docs/BLK-077_blk-system-post-078-roadmap.md`, current-state indexing in `docs/BLK-079_post-078-current-state-authority-index.md`, and BLK-001 through BLK-006 as applicable.

**Goal:** Capture the operator's explicit external BEO publication approval decision for the exact BLK-SYSTEM-098 prerequisite package, while preserving that approval capture is not publication execution.
**BLK-024 track:** Track G — BEO publication path / L0-L1 approval-decision capture fixture; future execution remains a separate higher-authority rung.
**Architecture:** BLK-SYSTEM-099 consumes the review-only prerequisite package `BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001`, validates its exact committed hash and authority-denial state, then emits a deterministic approval-decision package for one future external BEO publication execution sprint. The fixture records approval identity and decision metadata only; it does not publish, sign, write immutable storage, append a ledger, run rollback/revocation/supersession, generate RTM, read protected BLK-req bodies, scan/mutate target repos, run BLK-pipe/BLK-test/Codex, or consume a future execution run ID.
**Tech Stack:** Markdown doctrine/outcome docs, Python unittest gates, deterministic Python fixture package, active doctrine/current-state gates.
**Authority boundary:** Approval-decision capture only. External publication execution remains not run; signer/storage/ledger/rollback and all adjacent runtime/tooling authorities remain denied.

---

## Current Known State

Captured before plan writing:

```text
2026-05-13T19:03:14+10:00
BLK-System branch: main...origin/main
BLK-System HEAD: 8b4db6c [verified] BLK-SYSTEM-098 prerequisite request package
BLK-System commit: 8b4db6cd1fbcf2ab6bcdc3c2cb7518e96a7d4a72
BLK-System remote main: 8b4db6cd1fbcf2ab6bcdc3c2cb7518e96a7d4a72 refs/heads/main
BLK-SYSTEM-099 existing ID search: no existing BLK-SYSTEM-099 or BLK-099 sprint artifacts found
BLK-SYSTEM-098 request package id: BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001
BLK-SYSTEM-098 request package hash: sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041
BLK-SYSTEM-098 request status: BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED
BLK-SYSTEM-098 next authority: EXPLICIT_HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_REQUIRED_NOT_GRANTED
```

Operator approval captured as authority input for this sprint:

```text
source_system: Discord DM current session
operator_identity: discord:684235178083745819:camcamcami
operator_text_raw: I approve external BEO publication for BEO-PUBLICATION-PREREQUISITE-REQUEST-098- 001 under BLK-SYSTEM-099
operator_text_interpretation: explicit approval for exact normalized package id BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001 under BLK-SYSTEM-099
```

The raw operator text includes a whitespace anomaly in the package id (`098- 001`). BLK-SYSTEM-099 treats the operator text as provenance, normalizes the package id for exact artifact binding, and requires the structured approval package to bind the canonical `BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001` id and hash.

---

## Exact Package Identity

```text
sprint: BLK-SYSTEM-099
boundary_doc: docs/BLK-099_external-beo-publication-approval-decision.md
fixture_module: python/beo_external_publication_approval_decision.py
focused_test: python/test_beo_external_publication_approval_decision.py
approval_decision_package_id: BEO-PUBLICATION-APPROVAL-DECISION-099-001
selected_frontier: external_beo_publication_approval_decision_capture
decision_scope: EXTERNAL_BEO_PUBLICATION_APPROVAL_DECISION_ONLY_NOT_PUBLICATION_EXECUTION
decision_result: APPROVED_FOR_ONE_FUTURE_EXTERNAL_BEO_PUBLICATION_EXECUTION_NOT_PUBLISHED
approval_id: APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001
future_publication_execution_run_id: RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001
next_required_authority: SEPARATELY_SCOPED_EXTERNAL_BEO_PUBLICATION_EXECUTION_REQUIRED_NOT_RUN
upstream_request_package_id: BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001
upstream_request_package_hash: sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
exact_target_repo_path: /home/dad/code/Kuronode-v1
exact_target_head: aebea51bed911c781a537d84d38b2dcb838b1368
```

The future publication execution run ID is reserved as a candidate only. It is not consumed by BLK-SYSTEM-099 and cannot be used unless a later sprint is separately authorized to execute publication.

---

## BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-SYSTEM-099 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Bind who approved what, which artifact was approved, and which hash was used, without letting the approval record become execution or trace closure. |
| BLK-002 — Artifact Lifecycle | Treat human approval as structured provenance. Do not mutate active/protected BLK-req bodies or baseline artifacts. |
| BLK-003 — Orchestration Protocol | Preserve human gates and BEO/RTM separation. Approval capture does not dispatch a BEB, publish a BEO, run BLK-pipe, run BLK-test, or generate RTM. |
| BLK-004 — BLK-pipe V47 Suite | Do not invoke BLK-pipe or any target-repo mutation path. Approval capture is a deterministic local fixture only. |
| BLK-005 — BLK-Req Specification | Preserve hash trace semantics while avoiding active-vault hash comparison, coverage truth, drift truth, or RTM closure. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no protected-body reads/copying/parsing/hashing/scanning/mutation. |

---

## Tasks

### Task 0 — Publish the plan and task-000 outcome locally

**Deliverables:**

- `docs/plans/blk-system-099_external-beo-publication-approval-decision-capture.md`
- `docs/outcomes/BLK-SYSTEM-099_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-099_external-beo-publication-approval-decision-capture.md docs/outcomes/BLK-SYSTEM-099_task-000-outcome.md`
- Markdown fence balance check.

### Task 1 — RED approval-decision capture gates

Add failing tests before implementation to require:

- `python/beo_external_publication_approval_decision.py` exposes the BLK-SYSTEM-099 constants above.
- A deterministic approval-decision package binds the exact BLK-SYSTEM-098 request package id/hash, BEO id/hash, target repo path, and target head.
- The fixture captures human external BEO publication approval for one future execution sprint only.
- The fixture preserves publication not executed, runtime `PUBLISHED` output not emitted, signer/storage/ledger/rollback not touched, RTM not generated, drift not decided, protected bodies not read, target/source/Git not mutated, BLK-pipe/BLK-test/Codex/tooling not run, and production isolation not claimed.
- Forged or self-consistently rehashed BLK-SYSTEM-098 request packages are rejected unless they match the canonical committed 098 package fields and hash.
- Decision scope, approval id, future run id, timestamp window, proof obligations, denied authorities, and false side-effect flags are exact.
- Compact/camel/allcaps/percent authority-laundering and protected path variants are rejected in caller-controlled decision fields.
- Returned hash-bound nested structures are defensively copied.

**Expected RED:** focused tests fail because the BLK-SYSTEM-099 fixture module does not exist yet.

### Task 2 — GREEN approval decision fixture and boundary document

Implement the smallest changes that satisfy Task 1:

- Add `python/beo_external_publication_approval_decision.py`.
- Add `docs/BLK-099_external-beo-publication-approval-decision.md`.
- Preserve exact proof/denial sets and all non-publication side-effect flags.
- Emit `approval_decision_package_hash` over the canonical output package.

### Task 3 — Roadmap/current-state alignment

Update:

- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_active_doctrine_review_gates.py`

Required behavior:

1. Mark BLK-SYSTEM-099 as completed approval-decision capture after BLK-SYSTEM-098.
2. Make clear that approval capture authorizes only one future separately scoped external publication execution sprint, not execution now.
3. Preserve denial of RTM, drift rejection, protected-body reads, signer/storage/ledger/rollback side effects, BLK-pipe/BLK-test/Codex runtime, tooling, target/source/Git mutation, and production-isolation claims.
4. Remove unqualified wording that leaves BLK-SYSTEM-098's prerequisite request as the current open frontier.

### Task 4 — Hostile review and remediation

Write and preserve:

- `docs/reviews/BLK-SYSTEM-099_hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-099_task-004-outcome.md`

Review for approval-to-execution laundering, forged upstream 098 packages, future run ID consumption, publication side effects, signer/storage/ledger/rollback implications, RTM/drift/protected-body leakage, target/source/Git mutation, tooling/runtime authority, stale roadmap wording, and false claims that approval capture already published the BEO. Remediate blockers with tests first and re-run focused verification.

### Task 5 — Outcomes, closeout, verification, commit, and push

Write:

- `docs/outcomes/BLK-SYSTEM-099_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-099_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-099_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-099_task-005-outcome.md`
- `docs/outcomes/BLK-SYSTEM-099_sprint-closeout.md`

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beo_external_publication_approval_decision python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover -s python -p 'test*.py'
go test ./...
go vet ./...
git diff --check
```

Check no repository-local `__pycache__` / `.pyc` artifacts remain. Run added-lines static security probes and independent staged-diff review. Stage exact paths only, commit, push to `origin main`, and verify local/remote heads match.

---

## Explicit Non-Authority Statement

BLK-SYSTEM-099 captures a human approval decision for one future external BEO publication execution sprint. It does not execute publication, emit runtime `PUBLISHED` BEO output, access signer key material, cryptographically sign, write immutable storage, append or mutate a public ledger, execute rollback/revocation/supersession, generate RTM, reject RTM drift, make an authoritative drift decision, compare active-vault hashes, promote coverage truth, read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies, dispatch a BEB, execute BEO closeout, run BLK-pipe, run BLK-test runtime, run Codex, invoke package/network/model/browser/cyber tooling, scan or mutate the target repo, mutate source/Git, or claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret isolation.

---

## Stop Conditions

Pause and split the sprint if any task attempts to:

1. perform external BEO publication instead of approval capture;
2. consume `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001` or any execution run ID;
3. call signer, storage, ledger, rollback, revocation, supersession, network, package-manager, model, browser, cyber, BLK-pipe, BLK-test, Codex, or arbitrary shell pathways as fixture behavior;
4. read, hash, scan, summarize, compare, or mutate protected BLK-req bodies;
5. scan/mutate Kuronode or any target repo;
6. collapse approval capture and publication execution into one frontier;
7. claim RTM generation, drift rejection, active-vault comparison, coverage truth, or trace closure from the approval decision.
