# BLK-SYSTEM-098 — BEO Publication Prerequisite Request After Evidence Refresh Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first for maturity vocabulary, then by current selectors `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md`, and by BLK-001 through BLK-006 as applicable.

**Goal:** Package the fresh BLK-SYSTEM-097 BLK-test evidence refresh together with the BLK-SYSTEM-087 local BEO publication-pilot evidence into a deterministic human-review request for a future exact external BEO publication decision, without granting or performing publication.
**BLK-024 track:** Track G — BEO publication path; Track F — BLK-test evidence ladder; Track H — BLK-link offline RTM ledger prerequisites / maturity level L0/L1 review-only prerequisite request.
**Architecture:** This sprint creates a BLK-System-local request fixture and boundary document. The fixture validates the exact BLK-SYSTEM-097 evidence hash and the exact BLK-SYSTEM-087 local pilot package/hash, then emits a request-readiness package for human review only. It does not execute signer/storage/ledger/rollback paths, does not publish a BEO, does not generate RTM, does not read protected BLK-req bodies, and does not mutate Kuronode or BLK-System source outside the approved sprint files.
**Tech Stack:** Markdown doctrine/outcome docs, Python unittest gates, deterministic Python fixture package, active doctrine/current-state gates.
**Authority boundary:** Review-only request package. No external authoritative BEO publication, no runtime `PUBLISHED` BEO output, no live publication approval capture, no signer key-material access, no cryptographic signing, no immutable storage write, no public ledger append/mutation, no rollback/revocation/supersession execution, no RTM generation, no RTM drift rejection, no active-vault hash comparison, no coverage truth, no protected BLK-req body reads/hashing/scanning, no BLK-pipe/BLK-test/Codex runtime, no package/network/model/browser/cyber tooling, no source/Git or target-repo mutation, and no production isolation claim.

---

## Current Known State

Captured before plan writing:

```text
2026-05-13T16:59:21+10:00
BLK-System: ## main...origin/main
BLK-System HEAD: 3db0e7c feat: run bounded blk-test evidence refresh
BLK-System commit: 3db0e7c184eeae3970305f6fb63980574ce69d61
BLK-System remote main: 3db0e7c184eeae3970305f6fb63980574ce69d61 refs/heads/main
BLK-SYSTEM-098 existing ID search: no existing docs, plans, outcomes, tests, or source found
BLK-SYSTEM-097 evidence canonical hash: sha256:ebf3121a3a62dabaea589dc796ad645ef56d71d59574326bf278fbf563b66580
BLK-SYSTEM-087 local pilot package hash: sha256:78df1c4420bebd3da4e568bff8dd9f424f093e2548248b2825f2781ab8f31a7e
BLK-SYSTEM-087 local pilot artifact hash: sha256:6ee76d749bdb809bb39ae2f6f26c22c302370f9bf30da54acfc208a6661e875a
```

Operator request captured in this sprint plan:

```text
source_system: Discord DM current session
operator_identity: discord:684235178083745819:camcamcami
operator_text: write the plan for the next logical blk-system sprint and then execute all tasks
```

The operator selected the next logical sprint after BLK-SYSTEM-097, not publication itself. This plan therefore executes only the request-readiness fixture for a later explicit decision.

---

## Exact Package Identity

```text
sprint: BLK-SYSTEM-098
boundary_doc: docs/BLK-098_beo-publication-prerequisite-request-after-evidence-refresh.md
fixture_module: python/beo_publication_prerequisite_request_after_evidence_refresh.py
focused_test: python/test_beo_publication_prerequisite_request_after_evidence_refresh.py
request_package_id: BEO-PUBLICATION-PREREQUISITE-REQUEST-098-001
selected_frontier: external_beo_publication_prerequisite_request_after_blk_test_refresh
request_status: BEO_PUBLICATION_PREREQUISITE_REQUEST_READY_AFTER_BLK_TEST_REFRESH_NOT_GRANTED
next_required_authority: EXPLICIT_HUMAN_EXTERNAL_BEO_PUBLICATION_APPROVAL_REQUIRED_NOT_GRANTED
upstream_blk097_evidence_hash: sha256:ebf3121a3a62dabaea589dc796ad645ef56d71d59574326bf278fbf563b66580
upstream_blk087_execution_package_hash: sha256:78df1c4420bebd3da4e568bff8dd9f424f093e2548248b2825f2781ab8f31a7e
upstream_blk087_pilot_artifact_hash: sha256:6ee76d749bdb809bb39ae2f6f26c22c302370f9bf30da54acfc208a6661e875a
exact_target_repo_path: /home/dad/code/Kuronode-v1
exact_target_head: aebea51bed911c781a537d84d38b2dcb838b1368
beo_id: BEO-054-001
beo_hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

No approval ID or run ID is consumed by BLK-SYSTEM-098. Any later approval/execution sprint must mint fresh IDs and bind its own approval window, signer/storage/ledger/rollback policy, replay controls, and hostile review criteria.

---

## BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-SYSTEM-098 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Advance the V-model toward the BEO publication side by packaging verified evidence for human review, while preserving separation between BLK-test evidence, BEO publication, and blk-link trace closure. |
| BLK-002 — Artifact Lifecycle | Do not read, copy, parse, hash, summarize, scan, compare, or mutate protected BLK-req bodies. The request may bind opaque hashes and existing fixture identifiers only. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates and hostile audit. This sprint creates no BEB dispatch and no BEO closeout execution. |
| BLK-004 — BLK-pipe V47 Suite | Do not invoke BLK-pipe. No source mutation, staging, commit, revert, push, or target-repo cleanup occurs as fixture behavior. |
| BLK-005 — BLK-Req Specification | Preserve version-hash trace semantics without claiming coverage truth, drift truth, or RTM closure. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny behavior and no protected-body reads. |

---

## Tasks

### Task 0 — Publish the plan and plan outcome locally

**Deliverables:**

- `docs/plans/blk-system-098_beo-publication-prerequisite-request-after-evidence-refresh.md`
- `docs/outcomes/BLK-SYSTEM-098_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-098_beo-publication-prerequisite-request-after-evidence-refresh.md docs/outcomes/BLK-SYSTEM-098_task-000-outcome.md`
- Markdown fence balance check for both files.

### Task 1 — RED request fixture gates

Add failing tests before implementation to require:

- `python/beo_publication_prerequisite_request_after_evidence_refresh.py` exposes the BLK-SYSTEM-098 constants above.
- A deterministic request package binds the exact BLK-SYSTEM-097 evidence canonical hash and the exact BLK-SYSTEM-087 execution package/hash.
- The request rejects forged/self-consistent upstream evidence, mismatched target HEADs, non-PASS BLK-test evidence, findings, source/Git mutation flags, protected-body reads, coverage/drift claims, publication side effects, RTM generation, signer/storage/ledger/rollback side effects, target/source mutation, BLK-pipe/BLK-test/Codex runtime, tooling, and production-isolation claims.
- The request requires exact proof obligations, exact denied authorities, no duplicates, and strict closed schemas.
- The request recursively scans allowed strings and nested structures for compact/camel/allcaps/percent authority laundering and protected path variants.
- Returned hash-bound nested structures are defensively copied.

**Expected RED:** focused tests fail because the BLK-SYSTEM-098 fixture module does not exist yet.

### Task 2 — GREEN fixture and doctrine boundary

Implement the smallest changes that satisfy Task 1:

- Add `python/beo_publication_prerequisite_request_after_evidence_refresh.py`.
- Add `docs/BLK-098_beo-publication-prerequisite-request-after-evidence-refresh.md`.
- Update `python/test_active_doctrine_review_gates.py` with persistent markers for BLK-098.
- Preserve no-publication/no-RTM/no-protected-body/no-target-mutation/no-tooling false side-effect flags.

### Task 3 — Roadmap/current-state alignment

Update:

- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`

Required behavior:

1. Mark BLK-SYSTEM-098 as the completed request-readiness step after BLK-SYSTEM-097 once implemented.
2. Keep the current state explicit that external BEO publication, runtime `PUBLISHED` output, RTM generation, drift rejection, protected-body reads, signer/storage/ledger/rollback side effects, source/Git mutation, target-repo mutation, and tooling remain unauthorized.
3. Remove unqualified wording that treats BLK-SYSTEM-097 as the current open frontier after BLK-SYSTEM-098.

### Task 4 — Hostile review and remediation

Write and preserve:

- `docs/reviews/BLK-SYSTEM-098_hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-098_task-004-outcome.md`

Review for authority laundering, forged upstream evidence, stale evidence binding, missing denied-authority coverage, mutable nested aliasing, stale roadmap/index wording, publication/RTM/protected-body/signer/storage/ledger/rollback loopholes, and false implications that BLK-SYSTEM-098 grants publication or trace closure. Remediate blockers with tests first and re-run focused verification.

### Task 5 — Outcomes, closeout, verification, commit, and push

Write:

- `docs/outcomes/BLK-SYSTEM-098_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-098_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-098_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-098_task-005-outcome.md`
- `docs/outcomes/BLK-SYSTEM-098_sprint-closeout.md`

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beo_publication_prerequisite_request_after_evidence_refresh python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Check no repository-local `__pycache__` / `.pyc` artifacts remain. Commit with exact-path staging only, push to `origin main`, and verify local/remote heads match.

---

## Explicit Non-Authority Statement

BLK-SYSTEM-098 creates a deterministic review-only request package after the BLK-SYSTEM-097 evidence refresh. It does not authorize or perform external authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key-material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback, revocation, supersession, runtime RTM generation, RTM drift rejection, authoritative drift decision, active-vault hash comparison, coverage truth, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, BLK-pipe execution, BLK-test runtime, Codex execution, BEB dispatch, BEO closeout execution, Kuronode source/Git mutation, target-repo scan/mutation, package/network/model/browser/cyber tooling, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## Stop Conditions

Pause and split the sprint if any task attempts to:

1. perform or imply external BEO publication instead of request-readiness;
2. reuse BLK-SYSTEM-087, BLK-SYSTEM-095, or BLK-SYSTEM-097 run IDs as new publication execution authority;
3. treat BLK-SYSTEM-097 PASS evidence as approval for publication, RTM generation, coverage truth, drift truth, or signer/storage/ledger/rollback authority;
4. run BLK-pipe, BLK-test, Codex, package managers, network/model/browser/cyber tooling, Electron, Playwright, TypeScript tooling, or arbitrary shell as fixture behavior;
5. mutate Kuronode source/Git state or BLK-System source outside exact planned files;
6. read, hash, scan, compare, summarize, or mutate protected BLK-req bodies;
7. combine external BEO publication approval capture, publication execution, RTM generation, drift rejection, or trace closure into this request-only sprint.
