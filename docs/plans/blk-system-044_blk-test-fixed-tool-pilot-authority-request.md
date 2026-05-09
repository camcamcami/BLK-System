# BLK-SYSTEM-044 — BLK-test Fixed-Tool Pilot Authority Request Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `code-review` when executing. This plan is guided by `docs/BLK-045_blk-system-post-042-roadmap.md` as the current post-BLK-SYSTEM-042 roadmap, with `docs/BLK-024_blk-system-development-roadmap.md` retained for maturity-model lineage, then BLK-001 through BLK-006 as applicable.

**Goal:** Package the BLK-test fixed-tool pilot authority request boundary and deterministic review fixture without starting BLK-test transport or granting runtime pilot authority.

**BLK-045 fork:** Fork C — Complete the Right Side of the V-Model, first frontier: BLK-test fixed-tool pilot authority request.

**BLK-024 maturity lineage:** L0 doctrine plus L1 fixture/request gates only. This is not L2 transport enablement, not L3 synthetic smoke, not L4 pilot runtime, and not L5 production BLK-test authority.

**Architecture:** BLK-045 says the next productive V-model completion step is BLK-test fixed-tool pilot authority before BEO publication or runtime RTM work. The operator asked for BLK-SYSTEM-044 execution but did not explicitly grant runtime BLK-test authority, so this sprint must stop at a review-only authority request package. The package names the exact future approval envelope, physical/isolation proof obligations, fixed-tool constraints, replay/expiry behavior, excluded adjacent authorities, and hostile-review gates needed before a later L3/L4 BLK-test pilot sprint.

**Tech Stack:** Markdown doctrine, Python deterministic fixture/tests, active doctrine gates.

**Authority boundary:** Review/request fixture only. No production BLK-test MCP, no live BLK-test server/client startup, no new smoke run, no replay of BLK-SYSTEM-014/BLK-020, no fixed-tool execution, no arbitrary shell, no package-manager/network/model/cyber/browser tooling, no source mutation/staging/commit/push/reset/stash/checkout/revert by BLK-test, no protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation, no authoritative BEO publication, no runtime RTM generation, no RTM drift rejection, no public ledger mutation, no signer/storage/rollback/revocation/supersession/release authority, and no production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claim.

---

## 0. Current Repository State at Planning

```text
Date: 2026-05-09T19:28:48+10:00
Branch: main...origin/main
HEAD: 3c51ced docs: close blk-system sprint 043 current state authority index
Existing highest system plan: docs/plans/blk-system-043_current-state-authority-index.md
Existing highest BLK boundary/index doc: docs/BLK-046_blk-system-current-state-authority-index.md
```

Discovery found no existing `BLK-SYSTEM-044`, `blk-system-044`, or `BLK-047` owner in `docs/plans/`, `docs/outcomes/`, or `docs/BLK-*.md`.

---

## 1. Roadmap Selection and Scope Decision

BLK-045 supersedes BLK-024 for post-BLK-SYSTEM-042 roadmap selection and BLK-046 completed the short current-state index. BLK-045 then recommends choosing exactly one frontier:

1. Codex live-dispatch activation, only with explicit live Codex approval.
2. BLK-test fixed-tool pilot authority, only with explicit verification frontier approval.
3. Further consolidation/remediation, only if a concrete blocker is demonstrated.

This request did not explicitly grant live Codex execution or live BLK-test pilot runtime. Therefore BLK-SYSTEM-044 must not activate either frontier. To still make forward V-model progress, the sprint selects the BLK-test frontier but executes only the review/request package that a later human can approve or reject.

This sprint advances BLK-045 Fork C by turning BLK-025's prerequisite checklist into a machine-checkable future-authority request package. It does not start BLK-test transport, execute fixed tools, or produce PASS/FAIL verification evidence.

---

## 2. Governing Documents and Obligations

- **BLK-045:** Current roadmap selector. This sprint follows Fork C but stops at review/request fixture because no runtime approval was granted.
- **BLK-046:** Current-state index. It identifies BLK-test as disabled/gated evidence only and requires explicit approval before activation.
- **BLK-024:** Historical maturity vocabulary. This sprint remains L0/L1 and does not claim L2/L3/L4/L5.
- **BLK-017 / BLK-018 / BLK-019 / BLK-020 / BLK-025:** BLK-test transport remains disabled; workspace/process probes are inert; approval/source evidence remains local validation only; the first live fixed-tool smoke remains a one-run historical exception; BLK-025 prerequisites remain non-authorizing.
- **BLK-001:** Preserve BLK-test as evidence oracle only, not planner, source mutator, publisher, or ledger generator.
- **BLK-002 / BLK-005 / BLK-006:** Preserve BLK-req staging, active-vault immutability, canonical hash binding, and protected-vault hard-deny semantics. This sprint must not read protected BLK-req bodies.
- **BLK-003:** Preserve human gates, bounded context, hostile audit, and separation between execution, verification, publication, and RTM.
- **BLK-004:** Preserve BLK-pipe as source mutation/Git authority. BLK-test cannot broaden mutation allowlists or validation command authority.

---

## 3. Proposed Implementation Surface

### New Boundary Document

```text
docs/BLK-047_blk-test-fixed-tool-pilot-authority-request-boundary.md
```

Required markers:

```text
BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE
BLK_TEST_PILOT_REQUEST_REVIEW_ONLY_NOT_RUNTIME_AUTHORITY
FIXED_TOOL_PILOT_APPROVAL_REQUIRED_BEFORE_TRANSPORT
PRODUCTION_BLK_TEST_MCP_REMAINS_DISABLED
BLK_TEST_EVIDENCE_ONLY_NO_SOURCE_MUTATION
PROTECTED_BLK_REQ_BODY_READS_FORBIDDEN
BEO_PUBLICATION_AND_RTM_REMAIN_SEPARATE_AUTHORITIES
PHYSICAL_ISOLATION_PROOF_REQUIRED_BEFORE_PILOT
REPLAY_EXPIRY_AND_SOURCE_BINDING_REQUIRED
PERSISTENT_DOCTRINE_GATE_BLK_SYSTEM_044
```

### New Python Fixture

```text
python/blk_test_fixed_tool_pilot_authority_request.py
```

Proposed functions:

```text
build_blk_test_fixed_tool_pilot_authority_request(...)
validate_blk_test_fixed_tool_pilot_authority_request(...)
simulate_disabled_blk_test_pilot_adapter(record)
```

The fixture must produce a deterministic local request package. It must not import or invoke subprocess, live MCP, socket/network clients, package managers, model services, browser/cyber tools, Git, BLK-pipe, BEO publication, RTM generation, protected-vault readers, or filesystem mutation helpers.

### New Tests

```text
python/test_blk_test_fixed_tool_pilot_authority_request.py
```

Required test scope:

1. a complete review-only package evaluates to `BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME`;
2. the package requires a separate BLK-test-specific future approval grant and never reuses Codex, BLK-pipe, BEO, RTM, or BLK-020 approval;
3. production BLK-test MCP, live transport, fixed-tool execution, arbitrary shell, source mutation, protected-body access, BEO publication, RTM generation, drift rejection, package/network/model/cyber/browser tooling, and production isolation claims are all denied;
4. physical/isolation proof obligations, replay/expiry behavior, fixed-tool registry constraints, timeout/output caps, operator stop controls, and hostile-review checklist are required;
5. recursive authority-laundering keys/strings fail closed;
6. the disabled adapter path returns `BLK_TEST_PILOT_DISABLED_NOT_AUTHORIZED` and no side-effect flags;
7. source AST contains no live imports/calls for subprocess, shell, network, Git, package managers, `exec`, or `eval`.

### Doctrine Gate Update

```text
python/test_active_doctrine_review_gates.py
```

Add a persistent gate requiring BLK-047 to preserve BLK-test pilot request non-execution scope and the exact markers above.

---

## 4. Exact Allowed Implementation Paths

```text
docs/plans/blk-system-044_blk-test-fixed-tool-pilot-authority-request.md
docs/outcomes/BLK-SYSTEM-044_task-000-outcome.md
docs/BLK-047_blk-test-fixed-tool-pilot-authority-request-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-044_task-001-outcome.md
python/blk_test_fixed_tool_pilot_authority_request.py
python/test_blk_test_fixed_tool_pilot_authority_request.py
docs/outcomes/BLK-SYSTEM-044_task-002-outcome.md
docs/reviews/BLK-SYSTEM-044_blk-test-fixed-tool-pilot-authority-request-hostile-review.md
docs/outcomes/BLK-SYSTEM-044_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-044_sprint-closeout.md
```

No `docs/active/`, `docs/requirements/`, `docs/use_cases/`, real target repository, `.git`, protected-vault, root, or home path may be used as BLK-test runtime input. This sprint does not run BLK-test runtime at all.

---

## 5. Task Breakdown

### Task 0 — Plan Publication

Create and publish this plan plus `docs/outcomes/BLK-SYSTEM-044_task-000-outcome.md`.

Verification:

```bash
git diff --check -- docs/plans/blk-system-044_blk-test-fixed-tool-pilot-authority-request.md docs/outcomes/BLK-SYSTEM-044_task-000-outcome.md
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('docs/plans/blk-system-044_blk-test-fixed-tool-pilot-authority-request.md'),
    Path('docs/outcomes/BLK-SYSTEM-044_task-000-outcome.md'),
]:
    text = path.read_text()
    fence = chr(96) * 3
    assert text.count(fence) % 2 == 0, path
print('markdown sanity PASS')
PY
```

Commit: `docs: plan blk-system sprint 044 blk-test pilot request`

### Task 1 — BLK-047 Boundary and Doctrine Gate

Add BLK-047 and persistent active doctrine gates. RED first: add the focused gate and verify failure before writing the doc.

Allowed files:

```text
docs/BLK-047_blk-test-fixed-tool-pilot-authority-request-boundary.md
python/test_active_doctrine_review_gates.py
docs/outcomes/BLK-SYSTEM-044_task-001-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- docs/BLK-047_blk-test-fixed-tool-pilot-authority-request-boundary.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-SYSTEM-044_task-001-outcome.md
```

Commit: `docs: define blk047 blk-test pilot request boundary`

### Task 2 — Deterministic Pilot Request Fixture

Implement the pure request fixture and tests. RED first: create tests and verify failure before implementing the helper.

Required record shape includes:

```text
request_id: BLK-SYSTEM-044-PILOT-REQUEST-001
request_status: BLK_TEST_FIXED_TOOL_PILOT_AUTHORITY_REQUEST_PACKAGE
review_status: BLK_TEST_PILOT_REQUEST_READY_FOR_HUMAN_REVIEW_NOT_RUNTIME or BLK_TEST_PILOT_REQUEST_BLOCKED_NOT_AUTHORIZED
maturity: L0_L1_REQUEST_FIXTURE_ONLY
separate_human_approval_required: true
production_blk_test_mcp_authorized: false
live_transport_authorized: false
fixed_tool_execution_authorized: false
source_mutation_authorized: false
protected_body_read_authorized: false
beo_publication_authorized: false
rtm_generation_authorized: false
drift_rejection_authorized: false
```

Allowed files:

```text
python/blk_test_fixed_tool_pilot_authority_request.py
python/test_blk_test_fixed_tool_pilot_authority_request.py
docs/outcomes/BLK-SYSTEM-044_task-002-outcome.md
```

Verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
git diff --check -- python/blk_test_fixed_tool_pilot_authority_request.py python/test_blk_test_fixed_tool_pilot_authority_request.py docs/outcomes/BLK-SYSTEM-044_task-002-outcome.md
```

Commit: `feat: add blk-test pilot authority request fixture`

### Task 3 — Hostile Review and Closeout

Perform hostile review, remediate blockers, write review and closeout docs, run final verification, commit, and push.

Hostile review questions:

1. Does BLK-047 or the fixture accidentally grant production BLK-test MCP, live transport, fixed-tool execution, source mutation, protected-body access, BEO publication, RTM generation, drift rejection, package/network/model/cyber/browser tooling, or production isolation authority?
2. Does the package keep BLK-test-specific approval separate from Codex, BLK-pipe, BLK-020 first-smoke, BEO, and RTM approvals?
3. Does it require physical/isolation proof, replay/expiry behavior, fixed-tool constraints, timeout/output caps, cleanup proof, operator stop controls, and hostile review before a later runtime sprint?
4. Can recursive generic authority-laundering keys/strings bypass validation?
5. Does the disabled adapter path prove no side effects rather than merely reporting blocked status?
6. Is the next-step recommendation honest: human approval required before any L3/L4 runtime pilot?

Final verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_pilot_authority_request -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
export PATH="$HOME/.local/bin:$PATH"; go test ./... && go vet ./...
git diff --check
```

Commit: `docs: close blk-system sprint 044 blk-test pilot request`

---

## 6. Expected Final State

BLK-SYSTEM-044 should leave the repository with a BLK-047 fixed-tool pilot authority request boundary, persistent doctrine gate, deterministic Python request fixture, hostile review, and closeout evidence. The sprint may report human-review readiness only. It must not report BLK-test runtime approval, transport startup, fixed-tool execution, source mutation, BEO publication, RTM generation, drift rejection, protected-body reads, or production isolation.