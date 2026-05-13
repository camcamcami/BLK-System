# BLK-SYSTEM-097 — Bounded BLK-test Evidence Refresh Request / Exact-Target Frontier Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, and `test-driven-development` while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first for maturity vocabulary, then by current selectors `docs/BLK-077_blk-system-post-078-roadmap.md` and `docs/BLK-079_post-078-current-state-authority-index.md`, and by BLK-001 through BLK-006 as applicable.

**Goal:** Execute exactly one bounded, evidence-only BLK-test functional-module refresh over the current exact Kuronode target and record the resulting PASS/FAIL/BLOCKED evidence without granting source mutation, publication, RTM, coverage, protected-body, tooling, or production MCP authority.
**BLK-024 track:** Track F — BLK-test production-readiness ladder; Track J — security, sandbox, and capability hardening / maturity level L4 bounded real-repo evidence refresh, evidence-only and one-run.
**Architecture:** This is a single-frontier BLK-System evidence refresh sprint. Hermes plans and audits; the deterministic Python wrapper validates exact target identity, fresh IDs, replay, source/Git sterility, workspace cleanup, and fixed-tool-only semantics; BLK-test returns evidence only. The run copies the approved source subtree into a wrapper-owned workspace and evaluates static descriptors; it does not run Electron, smoke tests, TypeScript tooling, package managers, BLK-pipe, Codex, MCP transport, BEO publication, or RTM.
**Tech Stack:** Markdown doctrine/outcome docs, Python unittest gates, `python/blk_test_kuronode_workspace_bounded_evidence_refresh.py`, existing Kuronode static-profile evaluator.
**Authority boundary:** One exact evidence-only BLK-test refresh run. No production/generic BLK-test MCP, reusable BLK-test service startup, arbitrary shell, dynamic tool expansion, Electron/smoke/TypeScript/package-manager execution, network/model/browser/cyber tooling, Kuronode source/Git mutation, BLK-pipe/Codex execution, protected BLK-req body reads/hashing/scanning, BEO publication, runtime `PUBLISHED` BEO output, RTM generation, RTM drift rejection, coverage truth, active-vault comparison, public ledger mutation, signer/storage/rollback/release authority, target-repo push, or production-isolation claim.

---

## Current Known State

Captured before plan writing:

```text
2026-05-13T14:51:39+10:00
BLK-System: ## main...origin/main
BLK-System HEAD: 0422508 feat: reconcile post-local rtm ladder
BLK-System remote main: 0422508e89ad76ea78944bc0382d3d5f92a0c22e refs/heads/main
Kuronode: ## main...origin/main
Kuronode HEAD: aebea51bed911c781a537d84d38b2dcb838b1368
Kuronode origin/main: aebea51bed911c781a537d84d38b2dcb838b1368
Kuronode HEAD subject: aebea51 test: seed smoke model deterministically
```

Operator authorization captured in this sprint request:

```text
source_system: Discord DM current session
operator_identity: discord:684235178083745819:camcamcami
operator_text: plan and then execute all tasks in BLK-SYSTEM-097 - Bounded BLK-test Evidence Refresh Request / Exact-Target Frontier. I authorize 097 as one exact evidence-only BLK-test refresh run with fresh IDs and exact target boundaries.
```

The current roadmap/current-state surfaces after BLK-SYSTEM-096 list one bounded BLK-test evidence refresh as a valid candidate frontier after explicit operator selection. This plan consumes that selection for exactly one run.

---

## Exact Runtime Identity

```text
sprint: BLK-SYSTEM-097
approval_id: APPROVAL-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001
run_id: RUN-BLK-SYSTEM-097-KURONODE-EVIDENCE-REFRESH-001
target_repo_path: /home/dad/code/Kuronode-v1
source_subtree_path: /home/dad/code/Kuronode-v1/scripts
target_branch: main
target_head_sha: aebea51bed911c781a537d84d38b2dcb838b1368
observed_remote_head_required: aebea51bed911c781a537d84d38b2dcb838b1368
workspace_clone_path: /tmp/blk-system-097-kuronode-evidence-refresh-workspace
replay_ledger_path: /tmp/blk-system-097-kuronode-evidence-refresh-replay-ledger.json
fixed_tool: run_ast_validation
output_byte_limit: 16384
```

The run ID and approval ID are fresh for BLK-SYSTEM-097 and are not a reuse of BLK-SYSTEM-073, BLK-SYSTEM-076, BLK-SYSTEM-077, BLK-SYSTEM-078, or any BEO/RTM local pilot IDs.

---

## BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-SYSTEM-097 obligation |
| --- | --- |
| BLK-001 — Master Architecture | Advance the Physics Oracle side of the V-model by refreshing BLK-test evidence while preserving separation from BLK-pipe mutation, BEO publication, and blk-link trace closure. |
| BLK-002 — Artifact Lifecycle | Do not read, hash, compare, summarize, or mutate protected BLK-req bodies. Evidence may cite source hashes and artifact IDs only. |
| BLK-003 — Orchestration Protocol | Preserve human dispatch gates and hostile audit. This sprint creates no BEB dispatch and no BEO closeout execution; BLK-test evidence remains input to later review only. |
| BLK-004 — BLK-pipe V47 Suite | Do not invoke BLK-pipe. No source mutation, staging, commit, revert, or push may occur as BLK-test behavior. |
| BLK-005 — BLK-Req Specification | Do not promote coverage truth or drift truth from BLK-test evidence. Version-hash style source evidence is not requirement trace closure. |
| BLK-006 — BLK-Req Implementation Brief | Preserve protected-vault hard-deny behavior and no protected-body reads. Path checks must reject protected descendants and secret-like files. |

---

## Tasks

### Task 0 — Publish the plan and plan outcome locally

**Deliverables:**

- `docs/plans/blk-system-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md`
- `docs/outcomes/BLK-SYSTEM-097_task-000-outcome.md`

**Verification:**

- `git diff --check -- docs/plans/blk-system-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md docs/outcomes/BLK-SYSTEM-097_task-000-outcome.md`
- Markdown fence balance check for both files.

### Task 1 — RED exact-target evidence-refresh gates

Add failing tests before implementation to require:

- `docs/BLK-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md` exists and pins the exact runtime identity above.
- `python/blk_test_kuronode_workspace_bounded_evidence_refresh.py` exposes BLK-SYSTEM-097 constants, exact fresh IDs, exact target paths, exact HEAD, and denied-authority/false-side-effect sets.
- `docs/outcomes/BLK-SYSTEM-097_runtime-evidence.json` is produced by exactly one run and records PASS/FAIL/BLOCKED evidence only.
- BLK-077, BLK-079, and `python/blk_current_state_authority_index.py` record BLK-SYSTEM-097 after completion without promoting production MCP, source mutation, publication, RTM, coverage/drift truth, protected-body reads, tooling authority, or production isolation.
- Hostile laundering probes cover PASS-as-approval, BEO publication, RTM generation, coverage truth, drift decision, active-vault comparison, protected-body/secret strings, target mutation, BLK-pipe/Codex/runtime escalation, and compact/camel/percent variants where relevant.

**Expected RED:** focused tests fail because the BLK-SYSTEM-097 module, doctrine artifact, runtime evidence, and current-state surface do not exist yet.

### Task 2 — GREEN wrapper and doctrine implementation

Implement the smallest changes that satisfy Task 1:

- Write `docs/BLK-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md` as the active one-run boundary.
- Add `python/blk_test_kuronode_workspace_bounded_evidence_refresh.py` and focused tests.
- Keep the wrapper fixed-tool-only: copy `/home/dad/code/Kuronode-v1/scripts` into the wrapper-owned workspace and evaluate static descriptors using `run_ast_validation` semantics.
- Require exact raw path spelling, local HEAD and observed `origin/main`, fresh approval/run IDs, pre-owned workspace rejection, secret/protected descendant rejection, replay consumption before runtime, source/Git metadata snapshots, workspace cleanup, output byte bounds, and honest finding counts.
- Update BLK-077, BLK-079, and `python/blk_current_state_authority_index.py` only after runtime evidence exists.

### Task 3 — Execute one exact evidence-only refresh run

Execute exactly once with the fresh BLK-SYSTEM-097 IDs and exact target above. Persist the raw evidence to:

```text
docs/outcomes/BLK-SYSTEM-097_runtime-evidence.json
```

Any result vocabulary is final evidence for this sprint:

```text
BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_PASS_EVIDENCE_ONLY
BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_FAIL_EVIDENCE_ONLY
BLK_TEST_KURONODE_WORKSPACE_BOUNDED_EVIDENCE_REFRESH_BLOCKED_EVIDENCE_ONLY
```

Do not rerun with the same IDs if the result is FAIL or BLOCKED.

### Task 4 — Hostile review and remediation

Run an adversarial review against the diff and persisted evidence for:

- target laundering, path aliases, workspace overlap, `.git`/secret/protected descendant gaps;
- replay bypass through caller-owned, process-local, durable, or committed-evidence ID reuse;
- source/Git mutation evidence gaps and workspace cleanup honesty;
- PASS-as-approval/publication/RTM/coverage/drift laundering in allowed strings and evidence;
- stale current-state wording after BLK-SYSTEM-097;
- false claims of production BLK-test MCP, sandbox/host-secret isolation, package/network/model/browser/cyber tooling, or target mutation authority.

Remediate blockers with tests first and re-run hostile review after remediation.

### Task 5 — Outcomes, closeout, and verification

Write:

- `docs/reviews/BLK-SYSTEM-097_hostile-review.md`
- `docs/outcomes/BLK-SYSTEM-097_task-001-outcome.md`
- `docs/outcomes/BLK-SYSTEM-097_task-002-outcome.md`
- `docs/outcomes/BLK-SYSTEM-097_task-003-outcome.md`
- `docs/outcomes/BLK-SYSTEM-097_task-004-outcome.md`
- `docs/outcomes/BLK-SYSTEM-097_task-005-outcome.md`
- `docs/outcomes/BLK-SYSTEM-097_sprint-closeout.md`

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_test_kuronode_workspace_bounded_evidence_refresh python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

Check no repository-local `__pycache__` / `.pyc` artifacts remain. Check Kuronode remains `## main...origin/main` at `aebea51bed911c781a537d84d38b2dcb838b1368`.

### Task 6 — Commit, push, and remote verification

Use exact-path staging only. Commit after all verification and closeout artifacts exist. Push to `origin main`, then verify local and remote heads match.

---

## Explicit Non-Authority Statement

BLK-SYSTEM-097 authorizes exactly one evidence-only BLK-test functional-module refresh run for the exact target named in this plan. It does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, arbitrary shell, dynamic tool expansion, Electron/smoke/TypeScript/package-manager execution, network/model/browser/cyber tooling, BLK-pipe execution, Codex execution, live tactical LLM dispatch, Kuronode source/Git mutation, target-repo cleanup/autofix/push, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer/storage/ledger/rollback/release authority, runtime RTM generation, RTM drift rejection, authoritative drift decision, coverage matrix/truth/claim promotion, active-vault hash comparison, public ledger mutation, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## Stop Conditions

Pause and split the sprint if any task attempts to:

1. broaden the exact target beyond `/home/dad/code/Kuronode-v1` at `aebea51bed911c781a537d84d38b2dcb838b1368` and `/home/dad/code/Kuronode-v1/scripts`;
2. reuse BLK-SYSTEM-073 or any BEO/RTM local pilot approval/run IDs;
3. run Electron, smoke tests, TypeScript tooling, package managers, network tooling, model services, browser/cyber tools, Codex, BLK-pipe, or MCP transport;
4. mutate Kuronode source/Git state, push, clean, stash, reset, checkout, revert, or autofix as BLK-test behavior;
5. inspect protected BLK-req bodies or active-vault contents;
6. treat PASS/FAIL/BLOCKED evidence as BEO publication, RTM generation, coverage truth, drift truth, source mutation authority, or production BLK-test MCP authority;
7. rerun the BLK-SYSTEM-097 exact evidence refresh after replay consumption without a new explicit sprint and fresh IDs.
