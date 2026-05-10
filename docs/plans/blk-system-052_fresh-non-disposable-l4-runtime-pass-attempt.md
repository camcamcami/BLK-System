# BLK-SYSTEM-052 — Fresh Non-Disposable L4 Runtime PASS Attempt Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as current roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity vocabulary, then BLK-001 through BLK-006 as applicable.

**Goal:** Execute exactly one fresh, non-disposable L4 BLK-test fixed-tool `run_ast_validation` pilot against the current BLK-System target HEAD and record evidence without expanding BLK-test authority.
**BLK-024 / BLK-045 track:** Track F / Fork C — BLK-test production-readiness ladder; maturity level L4 pilot runtime.
**Architecture:** BLK-SYSTEM-052 is a fresh exact-target successor to BLK-SYSTEM-051. BLK-SYSTEM-051 proved the wrapper blocks stale HEADs and then hardened replay/path/mutation/evidence controls; BLK-SYSTEM-052 consumes a new operator-approved envelope naming the current HEAD and fresh replay IDs. The runtime must remain one-run, evidence-only, fixed-tool-only, and non-reusable.
**Tech Stack:** Markdown doctrine/outcomes, Python runtime wrapper, local Git state, Python `ast.parse` fixed tool.
**Authority boundary:** One exact non-disposable L4 pilot runtime only; evidence-only; no production/generic BLK-test MCP; no BEO publication; no RTM generation; no source/Git mutation authority.

---

## 0. Operator-Approved Fresh Envelope

The operator explicitly approved this envelope on 2026-05-10:

```text
target_repo_path: /home/dad/BLK-System
source_subtree_path: /home/dad/BLK-System/python
branch_or_worktree: main at 2b5e2054422cace5cd0f003b5c5f4713bba64bbf
workspace_clone_path: /tmp/blk-system-052-non-disposable-l4-runtime-workspace
approval_id: APPROVAL-BLK-SYSTEM-052-001
run_id: RUN-BLK-SYSTEM-052-001
expires_at: 1 hour from now
fixed_tool: run_ast_validation
```

Concrete expiry resolved during preflight:

```text
expires_at: 2026-05-10T12:25:01+10:00
```

Any mismatch in spelling, resolved target, HEAD, approval ID, run ID, workspace, expiry, or tool is a stop condition.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T11:24:04+10:00
git status --short --branch: ## main...origin/main
git log -1 --oneline: 2b5e205 docs: close blk-system sprint 051 runtime pilot
git rev-parse HEAD: 2b5e2054422cace5cd0f003b5c5f4713bba64bbf
```

Prior replay ledger state:

```json
{"approval_ids": ["APPROVAL-BLK-SYSTEM-051-001"], "run_ids": ["RUN-BLK-SYSTEM-051-001"]}
```

BLK-SYSTEM-052 must use a separate durable ledger path and fresh process-local replay state. It must not reuse BLK-SYSTEM-051 replay IDs.

---

## 2. Governing Doctrine Alignment

- **BLK-045 / BLK-024:** This is controlled activation under Fork C / Track F. It is a narrow L4 pilot, not production BLK-test authority.
- **BLK-001:** Preserves Hermes as architect/auditor and BLK-test as evidence oracle only. A PASS is evidence, not publication, mutation, or trace closure authority.
- **BLK-002 / BLK-005 / BLK-006:** No protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, active-vault comparison, or drift decision are authorized.
- **BLK-003:** Generic/live BLK-test MCP remains disabled except this wrapper-mediated fixed-tool pilot. The fixed tool is `run_ast_validation`; no caller-supplied command execution is allowed.
- **BLK-004:** BLK-pipe source mutation and Git authority remain separate. BLK-SYSTEM-052 must not stage, commit, push, reset, stash, checkout, revert, or autofix as BLK-test behavior.
- **BLK-054 / BLK-SYSTEM-051:** Reuse only the hardened safety pattern and committed wrapper implementation. Do not reuse BLK-SYSTEM-051 IDs or workspace. BLK-SYSTEM-052 gets fresh exact constants and its own evidence artifact.

---

## 3. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, arbitrary repositories, arbitrary shell, caller-supplied commands, dynamic tool expansion, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, package-manager/network/model/browser/cyber tooling, live Codex execution, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## 4. Execution Discipline

To preserve the approved HEAD, the plan and boundary docs may be written before runtime but must not be committed or staged before the one real pilot. `git add` mutates `.git`; no staging occurs until after runtime evidence is captured.

The real runtime should use the committed hardened BLK-SYSTEM-051 implementation at HEAD `2b5e2054422cace5cd0f003b5c5f4713bba64bbf`, with fresh BLK-SYSTEM-052 constants bound in the controller process:

```text
SPRINT: BLK-SYSTEM-052
APPROVAL_ID: APPROVAL-BLK-SYSTEM-052-001
RUN_ID: RUN-BLK-SYSTEM-052-001
EXPECTED_HEAD: 2b5e2054422cace5cd0f003b5c5f4713bba64bbf
APPROVED_TARGET_REPO: /home/dad/BLK-System
APPROVED_SOURCE_SUBTREE: /home/dad/BLK-System/python
APPROVED_WORKSPACE: /tmp/blk-system-052-non-disposable-l4-runtime-workspace
REPLAY_LEDGER_PATH: /tmp/blk-system-052-non-disposable-l4-runtime-replay-ledger.json
```

This avoids changing the approved target HEAD before runtime while still applying the hardened exact-target/replay/path/mutation/evidence logic already committed in BLK-SYSTEM-051.

---

## 5. Task Plan

### Task 000 — Plan and pre-runtime boundary capture

Deliverables:

```text
docs/plans/blk-system-052_fresh-non-disposable-l4-runtime-pass-attempt.md
docs/BLK-055_blk-test-fresh-non-disposable-l4-runtime-pass-boundary.md
docs/outcomes/BLK-SYSTEM-052_task-000-outcome.md
```

Actions:

1. Record preflight state and the exact approved envelope.
2. Write BLK-055 as a fresh one-run boundary for BLK-SYSTEM-052.
3. Do not stage or commit before runtime, because staging mutates `.git` and committing changes the approved HEAD.
4. Verify docs with fence checks and `git diff --check` before later final commit.

### Task 001 — Execute the one approved runtime pilot

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-052_runtime-evidence.json
docs/outcomes/BLK-SYSTEM-052_task-001-outcome.md
```

Actions:

1. Ensure current HEAD still equals `2b5e2054422cace5cd0f003b5c5f4713bba64bbf`.
2. Ensure `/tmp/blk-system-052-non-disposable-l4-runtime-workspace` does not pre-exist.
3. Ensure fresh BLK-SYSTEM-052 replay ledger does not already contain the fresh IDs.
4. Run exactly one wrapper-mediated fixed-tool pilot.
5. Persist the evidence JSON verbatim.
6. Stop on PASS, FAIL, or BLOCKED; do not rerun the same approval/run IDs.

### Task 002 — Hostile review and remediation

Deliverables:

```text
docs/reviews/BLK-SYSTEM-052_fresh-non-disposable-l4-runtime-hostile-review.md
docs/outcomes/BLK-SYSTEM-052_task-002-outcome.md
```

Actions:

1. Hostile-review the evidence and execution path for authority laundering, replay bypass, HEAD/path mismatch, source/Git mutation, cleanup failure, output-bound bypass, or adjacent BEO/RTM/source-mutation claims.
2. Use synthetic tests only for any remediation; do not rerun the real pilot.
3. Record final verdict.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-052_sprint-closeout.md
```

Actions:

1. Run focused BLK-SYSTEM-051 hardened-wrapper tests, doctrine gate tests, full Python discovery, Go tests, Go vet, and `git diff --check`.
2. Record final verification output.
3. Stage exact paths only.
4. Commit and push to `origin/main`.
5. Report final commit hash.

---

## 6. Stop Conditions

Stop and report without rerun if any of these occur:

1. current HEAD no longer equals the approved HEAD before runtime;
2. the BLK-SYSTEM-052 workspace already exists;
3. the BLK-SYSTEM-052 durable replay ledger already contains the fresh approval/run IDs;
4. wrapper evidence is larger than its output cap;
5. source or `.git` mutation is detected;
6. workspace cleanup is not verified;
7. evidence claims BEO publication, RTM generation, drift rejection, source/Git mutation authority, production BLK-test MCP, generic MCP, live Codex, arbitrary shell, network/package/model/browser/cyber authority, or production isolation;
8. hostile review finds an unremediated authority or safety bypass.
