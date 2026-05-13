# BLK-SYSTEM-100 — External BEO Publication Execution Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by historical maturity vocabulary in `docs/BLK-024_blk-system-development-roadmap.md`, current sequencing in `docs/BLK-077_blk-system-post-078-roadmap.md`, current-state indexing in `docs/BLK-079_post-078-current-state-authority-index.md`, and BLK-001 through BLK-006 as applicable.

**Goal:** Execute one exact BLK-SYSTEM-099-approved external BEO publication record for `BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001`, consume `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001`, and preserve all adjacent signer/storage/ledger/rollback/RTM/protected-body/runtime/tooling boundaries.
**BLK-024 track:** Track G — BEO publication path / L2-style exact externally-published record fixture; no signer key material, immutable storage, public ledger mutation, rollback, RTM, protected-body, target-repo, BLK-pipe, BLK-test, Codex, tooling, or production-isolation authority.
**Architecture:** BLK-SYSTEM-100 consumes the canonical BLK-SYSTEM-099 approval-decision package, validates the exact BLK-SYSTEM-098 request hash and BLK-SYSTEM-097/087 evidence hashes inherited through BLK-099, checks an execution request window within the approval window, consumes exactly one reserved run ID, and emits a deterministic hash-bound external BEO publication execution package plus a matching BEO publication execution outcome. The execution is repository-local and record-oriented: it does not access signer key material, cryptographically sign, write immutable storage, mutate a public ledger, run rollback/revocation/supersession, generate RTM, read protected BLK-req bodies, scan/mutate target repos, run BLK-pipe/BLK-test/Codex, invoke package/network/model/browser/cyber tooling, or claim production isolation.
**Tech Stack:** Markdown doctrine/outcome docs, Python unittest gates, deterministic Python fixture package, active doctrine/current-state gates.
**Authority boundary:** Exact external BEO publication execution record for the single approved BLK-SYSTEM-099 package/run ID only. Adjacent signer/storage/ledger/rollback, RTM, protected-body, target/source/Git, BEB/BEO closeout, BLK-pipe/BLK-test/Codex/tooling, and production-isolation authorities remain denied.

---

## Current Known State

Captured before plan writing:

```text
2026-05-13T20:13:25+10:00
BLK-System branch: main...origin/main
BLK-System HEAD: f1e7530 [verified] BLK-SYSTEM-099 external BEO approval capture
BLK-System commit: f1e75304fd7a3cfc6af4682cde92e6e2d7dce400
BLK-System remote main: f1e75304fd7a3cfc6af4682cde92e6e2d7dce400 refs/heads/main
BLK-SYSTEM-100 existing ID search: no existing BLK-SYSTEM-100 or BLK-100 sprint artifacts found
BLK-SYSTEM-099 approval decision package id: BEO-PUBLICATION-APPROVAL-DECISION-099-001
BLK-SYSTEM-099 approval decision package hash: sha256:c83ea7982632b587a8596550cfa0f1c36b546a70b8f2fa8cbefb4aedfeda383b
BLK-SYSTEM-099 approval id: APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001
BLK-SYSTEM-099 future execution run id: RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001
```

Operator sprint instruction captured as authority input for this sprint:

```text
source_system: Discord DM current session
operator_identity: discord:684235178083745819:camcamcami
operator_text_raw: plan and then execute all tasks for BLK-SYSTEM-100
operator_text_interpretation: proceed with a separately scoped BLK-SYSTEM-100 plan and execute its tasks for the already-approved exact BLK-SYSTEM-099 external BEO publication execution frontier
```

---

## Exact Package Identity

```text
sprint: BLK-SYSTEM-100
boundary_doc: docs/BLK-100_external-beo-publication-execution.md
fixture_module: python/beo_external_publication_execution.py
focused_test: python/test_beo_external_publication_execution.py
execution_package_id: BEO-PUBLICATION-EXECUTION-100-001
execution_status: EXTERNAL_BEO_PUBLICATION_EXECUTED_FOR_EXACT_BLK099_APPROVAL_RECORD_ONLY
selected_frontier: external_beo_publication_execution
execution_scope: EXACT_EXTERNAL_BEO_PUBLICATION_EXECUTION_FOR_BLK099_APPROVAL_RECORD_ONLY_NO_SIGNER_STORAGE_LEDGER_RTM
approval_decision_package_id: BEO-PUBLICATION-APPROVAL-DECISION-099-001
approval_decision_package_hash: sha256:c83ea7982632b587a8596550cfa0f1c36b546a70b8f2fa8cbefb4aedfeda383b
approval_id: APPROVAL-BLK-SYSTEM-099-EXTERNAL-BEO-PUBLICATION-001
run_id: RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001
upstream_request_package_id: BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001
upstream_request_package_hash: sha256:a782b223c88ae155a37519b87313dd2085450515c78ba60e93277c636ba6e041
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
exact_target_repo_path: /home/dad/code/Kuronode-v1
exact_target_head: aebea51bed911c781a537d84d38b2dcb838b1368
```

The run ID is consumed exactly once by BLK-SYSTEM-100 fixture output. It is not reusable authority and does not authorize retargeting.

---

## BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-SYSTEM-100 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Preserve V-model separation while recording a single approved BEO publication execution record; do not convert the record into RTM/blk-link trace closure, target-repo mutation, or reusable runtime authority. |
| BLK-002 — Artifact Lifecycle | Treat the publication record as structured provenance and do not mutate active/protected BLK-req bodies or baseline artifacts. |
| BLK-003 — Orchestration Protocol | Preserve human gates and BEO/RTM separation. This sprint does not dispatch a BEB, run BLK-pipe, run BLK-test, start Codex, or generate RTM. |
| BLK-004 — BLK-pipe V47 Suite | Do not invoke BLK-pipe or any target-repo mutation path. |
| BLK-005 — BLK-Req Specification | Preserve hash trace semantics without promoting coverage truth, drift truth, or RTM closure. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny and no protected-body reads/copying/parsing/hashing/scanning/mutation. |

---

## Tasks

### Task 0 — Publish the plan and task-000 outcome locally

**Deliverables:**

- `docs/plans/blk-system-100_external-beo-publication-execution.md`
- `docs/outcomes/BLK-SYSTEM-100_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-100_external-beo-publication-execution.md docs/outcomes/BLK-SYSTEM-100_task-000-outcome.md`
- Markdown fence balance check.

### Task 1 — RED external publication execution gates

Add failing tests before implementation to require:

- `python/beo_external_publication_execution.py` exposes the BLK-SYSTEM-100 constants above.
- A deterministic execution package binds the exact BLK-SYSTEM-099 approval-decision package, BLK-SYSTEM-098 request hash, BLK-SYSTEM-097/087 evidence hashes inherited through BLK-099, BEO id/hash, target path/head, approval ID, and run ID.
- The fixture consumes `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001` exactly once and emits a hash-bound `PUBLISHED_EXTERNAL_BEO_RECORD` result.
- Signer key material, cryptographic signing, immutable storage write, public ledger mutation, rollback/revocation/supersession, RTM, drift, protected-body, target/source/Git, BLK-pipe, BLK-test, Codex, tooling, and production-isolation side-effect flags remain false.
- Forged or self-consistently rehashed BLK-SYSTEM-099 approval packages are rejected unless they match the canonical committed BLK-SYSTEM-099 package fields and hash.
- Execution scope, approval id, run id, timestamp window, proof obligations, denied authorities, and false side-effect flags are exact.
- Compact/camel/allcaps/percent authority-laundering and protected path variants are rejected in caller-controlled execution fields.
- Returned hash-bound nested structures are defensively copied.

**Expected RED:** focused tests fail because the BLK-SYSTEM-100 fixture module does not exist yet.

### Task 2 — GREEN execution fixture, package artifact, and boundary document

Implement the smallest changes that satisfy Task 1:

- Add `python/beo_external_publication_execution.py`.
- Add `docs/BLK-100_external-beo-publication-execution.md`.
- Add `docs/outcomes/BLK-SYSTEM-100_external-beo-publication-execution.json` generated from the deterministic fixture package.
- Preserve exact proof/denial sets and all adjacent-authority no-side-effect flags.
- Emit `execution_package_hash` over the canonical output package and `publication_record_hash` over the nested publication record.

### Task 3 — Roadmap/current-state alignment

Update:

- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_active_doctrine_review_gates.py`

Required behavior:

1. Mark BLK-SYSTEM-100 as completed external BEO publication execution record after BLK-SYSTEM-099.
2. Make clear that BLK-SYSTEM-100 consumes the exact run ID and does not authorize reuse, retargeting, signer/storage/ledger/rollback, RTM, protected-body reads, target/source/Git mutation, runtime/tooling, or production-isolation claims.
3. Remove unqualified wording that leaves BLK-SYSTEM-099 publication execution as the current open frontier.

### Task 4 — Hostile review and remediation

Write and preserve:

- `docs/reviews/BLK-SYSTEM-100_hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-100_task-004-outcome.md`

Review for approval-to-execution retargeting, replay/reuse, external-publication-to-signer/storage/ledger laundering, publication-to-RTM laundering, protected-body leakage, target/source/Git mutation, tooling/runtime authority, stale roadmap wording, and false claims that BLK-SYSTEM-100 created runtime `blk-link` trace closure. Remediate blockers with tests first and re-run focused verification.

### Task 5 — Outcomes, closeout, verification, commit, and push

Write:

- `docs/outcomes/BLK-SYSTEM-100_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-100_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-100_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-100_task-005-outcome.md`
- `docs/outcomes/BLK-SYSTEM-100_beo-publication-execution-outcome.md`
- `docs/outcomes/BLK-SYSTEM-100_sprint-closeout.md`

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beo_external_publication_execution python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover -s python -p 'test*.py'
go test ./...
go vet ./...
git diff --check
```

Check no repository-local `__pycache__` / `.pyc` artifacts remain. Run added-lines static security probes and independent staged-diff review. Stage exact paths only, commit, push to `origin main`, and verify local/remote heads match.

---

## Explicit Non-Authority Statement

BLK-SYSTEM-100 executes one exact approved external BEO publication record for the BLK-SYSTEM-099 package and consumes the exact BLK-SYSTEM-100 run ID once. It does not access signer key material, cryptographically sign, write immutable storage, append or mutate a public ledger, execute rollback/revocation/supersession, generate RTM, perform RTM drift rejection, make an authoritative drift decision, compare active-vault hashes, promote coverage truth, read/copy/parse/hash/summarize/scan/mutate protected BLK-req bodies, dispatch a BEB, execute BEO closeout, run BLK-pipe, run BLK-test runtime, run Codex, invoke package/network/model/browser/cyber tooling, scan or mutate the target repo, mutate source/Git, or claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret isolation.

---

## Stop Conditions

Pause and split the sprint if any task attempts to:

1. retarget the BLK-SYSTEM-099 approval, BLK-SYSTEM-098 request, BEO identity/hash, target path/head, approval ID, or run ID;
2. reuse `RUN-BLK-SYSTEM-100-EXTERNAL-BEO-PUBLICATION-001` after BLK-SYSTEM-100 consumes it;
3. access signer key material, cryptographically sign, write immutable storage, append or mutate a public ledger, or execute rollback/revocation/supersession;
4. generate RTM, perform RTM drift rejection, compare active-vault hashes, promote coverage truth, or make an authoritative drift decision;
5. read, hash, scan, summarize, compare, or mutate protected BLK-req bodies;
6. run BLK-pipe, BLK-test runtime, Codex, package managers, network/model/browser/cyber tooling, or arbitrary shell as fixture behavior;
7. scan or mutate Kuronode or any target repo;
8. claim production sandbox, cgroup, VM, namespace, seccomp, AppArmor, SELinux, firewall, or host-secret isolation.
