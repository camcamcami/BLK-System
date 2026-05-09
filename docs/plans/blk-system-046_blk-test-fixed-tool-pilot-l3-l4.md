# BLK-SYSTEM-046 — BLK-test Fixed-Tool Pilot L3/L4 Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, `systematic-debugging`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as the current roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity lineage, then BLK-001 through BLK-006 and BLK-047/BLK-048 as applicable.

**Goal:** Activate the selected `blk_test_fixed_tool_pilot_l3_l4` frontier in the narrowest safe form: one approval-bound synthetic L3 fixed-tool pilot and an L4 real-repo preflight that remains blocked until a later exact target approval exists.

**BLK-045 fork:** Fork C — Complete the Right Side of the V-Model, first verification frontier.

**BLK-024 maturity lineage:** L3 approved synthetic fixed-tool smoke for this sprint's executable portion; L4 pilot runtime is represented only as a fail-closed preflight boundary because no exact real target repository/path approval was supplied. This is not L5 production BLK-test MCP authority.

**Architecture:** BLK-SYSTEM-045 created a selection gate and the operator explicitly selected `blk_test_fixed_tool_pilot_l3_l4` in the current Discord session. BLK-047 requires a separate BLK-test-specific approval envelope plus proof obligations before any fixed-tool pilot can execute. BLK-SYSTEM-046 therefore creates BLK-049, validates a source-bound one-run L3 synthetic approval envelope, runs only a dependency-free fixed tool against an isolated synthetic workspace, returns evidence only, and leaves L4 real-repo pilot execution blocked pending a later exact target approval.

**Tech Stack:** Markdown doctrine, Python deterministic envelope/preflight/runner fixture, stdio fixed-tool synthetic workspace harness, unittest, Go verification.

**Authority boundary:** This sprint may execute one bounded L3 synthetic fixed-tool validation in tests/local fixture only. It does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary shell, caller-supplied commands, dynamic tool expansion, package-manager/network/model/browser/cyber tooling, execution against `/home/dad/BLK-System` as a target, execution against real repositories, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T20:38:30+10:00
Branch: main...origin/main
HEAD: 92f0b97 docs: close blk-system sprint 045 frontier selection gate
Remote HEAD: 92f0b9798189f2635b98a9286212dd9716b8b99c refs/heads/main
Existing highest system plan: docs/plans/blk-system-045_authority-frontier-selection-gate.md
Existing highest BLK boundary doc: docs/BLK-048_authority-frontier-selection-gate-boundary.md
```

Discovery found no existing `BLK-SYSTEM-046`, `blk-system-046`, or `BLK-049` owner in the repository.

---

## 1. Operator Selection and Approval Provenance

The current operator message explicitly selected the frontier by saying:

```text
write the plan for the blk_test_fixed_tool_pilot_l3_l4 sprint and then execute all tasks
```

This satisfies BLK-048's requirement to name exactly one frontier. It is not treated as broad production authority. For this sprint it grants only the following bounded approval envelope:

```text
source_system: Discord DM with Camcamcam
operator_identity: camcamcami / Discord user 684235178083745819
selected_frontier: blk_test_fixed_tool_pilot_l3_l4
approved_runtime_slice: L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY
approved_tool: run_ast_validation
approved_target_boundary: synthetic isolated workspace created by the test fixture
l4_real_repo_pilot: BLOCKED_PENDING_EXACT_TARGET_APPROVAL
excluded_authorities: production MCP, arbitrary shell, source/Git mutation, protected-body reads, BEO publication, RTM generation, drift rejection, network/model/browser/cyber/package-manager tooling, production isolation claims
```

If a future operator wants L4 real-repo pilot runtime, that later sprint must provide exact target repo/path, branch, workspace, rollback, cleanup, approval expiry, and output/timeout details.

---

## 2. Governing Documents and Obligations

| Governing doc | Obligation for BLK-SYSTEM-046 |
| --- | --- |
| BLK-045 | Use Fork C and activate only one bounded verification frontier. Do not pursue BEO publication or RTM before trustworthy verification evidence exists. |
| BLK-048 | The selected frontier is exactly `blk_test_fixed_tool_pilot_l3_l4`; do not inherit adjacent authority. |
| BLK-047 | Require BLK-test-specific approval, fixed-tool registry proof, source/evidence binding, isolation proof, replay protection, output bounds, cleanup, and operator stop controls. |
| BLK-017 / BLK-018 / BLK-019 / BLK-020 / BLK-025 | Preserve generic/production BLK-test disabled boundaries and historical first-smoke separation. |
| BLK-001 | BLK-test remains a verification evidence oracle only. |
| BLK-002 / BLK-005 / BLK-006 | Preserve protected-vault isolation and no protected body reads. |
| BLK-003 | Preserve human gates, hostile review, bounded context, and no implicit inheritance between execution, verification, publication, and RTM. |
| BLK-004 | Preserve BLK-pipe as source mutation/Git enforcement; BLK-test cannot mutate source or broaden allowlists. |

---

## 3. Implementation Surface

### New Boundary Document

```text
docs/BLK-049_blk-test-fixed-tool-pilot-l3-l4-boundary.md
```

Required markers:

```text
BLK_TEST_FIXED_TOOL_PILOT_L3_L4_BOUNDARY
BLK_TEST_FRONTIER_SELECTED_BY_OPERATOR
L3_SYNTHETIC_FIXED_TOOL_PILOT_ONLY_THIS_SPRINT
L4_REAL_REPO_PILOT_BLOCKED_PENDING_EXACT_TARGET_APPROVAL
FIXED_TOOL_REGISTRY_RUN_AST_VALIDATION_ONLY
SOURCE_BOUND_REPLAY_PROTECTED_APPROVAL_REQUIRED
SYNTHETIC_WORKSPACE_ISOLATION_REQUIRED
BLK_TEST_EVIDENCE_ONLY_NO_SOURCE_MUTATION
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_046
```

### New Python Fixture

```text
python/blk_test_fixed_tool_pilot_l3_l4.py
python/test_blk_test_fixed_tool_pilot_l3_l4.py
```

The fixture must provide:

- deterministic source report and approval envelope builders;
- preflight that refuses missing approval, wrong frontier, replay, mismatched tool/profile/workspace/source, real repo L4 targets, protected paths, adjacent approvals, authority-laundering fields, arbitrary shell, package/network/model/browser/cyber markers, BEO/RTM/coverage/drift claims, and production isolation claims;
- an L3 synthetic fixed-tool pilot runner that uses the existing fixed `run_ast_validation` stdio harness only against a synthetic workspace;
- evidence-only output: `PASS`, `FAIL`, `BLOCKED`, or `FATAL_*`, never BEO publication, RTM generation, drift rejection, source mutation, active coverage, or protected-vault truth;
- cleanup verification before success;
- exact replay tracking via caller-supplied used approval/run sets.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add BLK-049 and pin the L3-only/L4-blocked boundary markers above.

---

## 4. Exact Allowed Paths

```text
docs/plans/blk-system-046_blk-test-fixed-tool-pilot-l3-l4.md
docs/outcomes/BLK-SYSTEM-046_task-000-outcome.md
docs/BLK-049_blk-test-fixed-tool-pilot-l3-l4-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-046_task-001-outcome.md
python/blk_test_fixed_tool_pilot_l3_l4.py
python/test_blk_test_fixed_tool_pilot_l3_l4.py
docs/outcomes/BLK-SYSTEM-046_task-002-outcome.md
docs/reviews/BLK-SYSTEM-046_blk-test-fixed-tool-pilot-l3-l4-hostile-review.md
docs/outcomes/BLK-SYSTEM-046_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-046_sprint-closeout.md
```

---

## 5. Task Breakdown

### Task 0 — Plan Publication

Create and publish this plan plus `docs/outcomes/BLK-SYSTEM-046_task-000-outcome.md`.

Verification:

```bash
git diff --check -- docs/plans/blk-system-046_blk-test-fixed-tool-pilot-l3-l4.md docs/outcomes/BLK-SYSTEM-046_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-046_blk-test-fixed-tool-pilot-l3-l4.md'),
    Path('docs/outcomes/BLK-SYSTEM-046_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

Commit: `docs: plan blk-system sprint 046 blk-test pilot`

### Task 1 — BLK-049 Boundary and Doctrine Gate

Add BLK-049 and persistent active-doctrine gates. RED first: patch the doctrine test and verify failure because BLK-049 does not exist, then write BLK-049 and verify GREEN.

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-049_blk-test-fixed-tool-pilot-l3-l4-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-046_task-001-outcome.md
```

Commit: `docs: define blk049 blk-test pilot boundary`

### Task 2 — L3 Synthetic Fixed-Tool Pilot Fixture

Implement the fixture and tests with strict TDD. RED first: create tests that import missing functions and fail. GREEN: implement the minimal safe wrapper. The test suite must execute one synthetic L3 fixed-tool pilot in a temporary synthetic workspace and prove L4 real-repo pilot remains blocked.

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_l3_l4 -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_test_fixed_tool_pilot_l3_l4.py python/test_blk_test_fixed_tool_pilot_l3_l4.py docs/outcomes/BLK-SYSTEM-046_task-002-outcome.md
```

Commit: `feat: add blk-test fixed-tool pilot l3 fixture`

### Task 3 — Hostile Review, Remediation, Closeout

Perform hostile review against BLK-047/BLK-048/BLK-049. Remediate any blocker with RED/GREEN tests before closeout.

Hostile review questions:

1. Can sprint-dispatch wording, BLK-047 request readiness, BLK-048 selection readiness, Codex approval, BLK-pipe approval, BEO fixture readiness, RTM fixture readiness, or BLK-020 first-smoke evidence become BLK-test pilot approval?
2. Can L4 real-repo runtime start without exact target repository/path approval?
3. Can arbitrary shell, caller-supplied commands, wildcard tools, package managers, network/model/browser/cyber tooling, or dynamic tool expansion bypass the fixed registry?
4. Can protected-vault bodies or active-vault paths be read, copied, parsed, hashed, scanned, summarized, compared, or mutated?
5. Can PASS evidence publish BEOs, generate RTM, claim coverage/drift truth, mutate source, or claim production isolation?
6. Are replay state, output bounds, timeout handling, cleanup, and operator stop controls proven rather than self-reported?

Final verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_l3_l4 -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

Commit: `docs: close blk-system sprint 046 blk-test pilot`

---

## 6. Expected Final State

BLK-SYSTEM-046 should leave the repository with BLK-049 doctrine, persistent gates, a deterministic approval-bound synthetic L3 fixed-tool pilot fixture, L4 real-repo pilot blocked pending exact target approval, hostile review, outcome docs, and full verification evidence. The sprint may report synthetic L3 evidence only; it must not report production BLK-test MCP, generic live MCP, source mutation, BEO publication, RTM generation, drift rejection, protected-body reads, network/model/browser/cyber/package-manager use, or production isolation.
