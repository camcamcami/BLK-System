# BLK-SYSTEM-013 — Approval-Channel and Source-Evidence Authorization Mechanics Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution` and strict TDD to implement this plan task-by-task. If delegating to Codex CLI, use model `gpt-5.4` and run a hostile audit after every execution packet before accepting changes.

**Goal:** Implement deterministic BLK-test-specific approval validation and source-evidence binding mechanics for future live BLK-test MCP readiness, without starting live transport or executing fixed tools.

**Architecture:** Add a dependency-free Python approval authorization module that validates a human approval record against an exact BLK-pipe source evidence envelope, fixed-tool request profile, workspace identity, timeout/output profile, and replay/expiry policy. Keep BLK-017 disabled transport and BLK-018 inert workspace/process probes intact; Sprint 013 may emit source-bound approval/preflight evidence, but Sprint 014 still owns any first live fixed-tool BLK-test MCP smoke.

**Tech Stack:** Python standard library only (`unittest`, `dataclasses`, `datetime`, `hashlib`, `json`, `re`, `copy`), Markdown doctrine/review/outcome docs, existing BLK-System test gates.

---

## 0. Live preflight facts

Captured before writing this plan:

```text
Date: 2026-05-06T20:13:24+10:00
Repository: /home/dad/BLK-System
Branch/status: ## main...origin/main
HEAD: d344dc2 docs: finalize blk-system sprint 011.1 closeout metadata
Plan file: docs/plans/blk-system-013_approval-source-evidence-authorization.md
```

Sprint ID ownership check:

- `BLK-SYSTEM-013` is already reserved by active tests/docs for `Approval-channel and source-evidence authorization mechanics`.
- The existing `docs/BLK-013_blk-test-handoff-fixture-contract.md` is a BLK doctrine document, not a system sprint plan. Do not confuse it with `BLK-SYSTEM-013`.
- Key owner artifacts found during preflight:
  - `python/test_active_doctrine_review_gates.py` requires `BLK-SYSTEM-013` and `Approval-channel and source-evidence authorization mechanics`.
  - `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` line 39 defines the Sprint 013 scope.
  - `docs/outcomes/BLK-SYSTEM-012_sprint-closeout.md` lines 163-177 seed Sprint 013 handoff constraints.
  - `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md` and `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md` both preserve Sprint 013 as approval/source-evidence owner.

---

## 1. BLK-001 domain matrix

| Domain/component | Sprint 013 relationship | Authority statement |
| --- | --- | --- |
| `blk-req` | Approval validation may bind opaque `trace_artifacts[*].version_hash` metadata only. | Does not read protected BLK-req vault bodies, parse active requirements, promote requirements, or mutate requirement docs. |
| Architecture & Feature Planning / HITL | Approval record must carry explicit operator identity and approval timestamp. | Human authorization must be explicit and scoped; no ambient approval is inferred from prior sprint docs or agent action. |
| `blk-id` | Approval/source evidence gets deterministic identity hashes for audit/replay comparison. | Identity hashes are evidence identifiers only; they do not create truth, mutation, publication, or RTM authority. |
| `blk-relay` | No live relay/transport startup is authorized. | No network callbacks, HTTP/WebSocket/TCP/UDP listeners, MCP SDK startup, live stdio server/client, or Discord-mediated approval token execution. |
| `blk-pipe` | Source evidence envelope is copied from BLK-pipe report/request metadata: `beb_id`, source `commit_hash`, `pre_engine_hash`, and canonical `trace_artifacts`. | Source mutation, staging, commit, push, and allowlist authority remain exclusively outside BLK-test approval validation. |
| `blk-test` | Adds approval validator and source-bound startup preflight evidence for future physics-oracle use. | Does not execute fixed tools, invoke live BLK-test MCP, run against real repos, or emit live PASS/FAIL verdicts. |
| `blk-link` | Approval evidence must preserve `rtm_status: NOT_GENERATED` and no RTM fields. | Does not generate RTM, make drift decisions, or claim traceability closure beyond opaque source-bound metadata. |
| BEO/outcomes | Approval evidence may be documented in sprint outcomes. | Does not publish authoritative BEOs; any BEO-shaped fixture remains `DRAFT_ONLY`. |
| Cryptographic `version_hash` baton | Canonical trace hashes must match `sha256:<64-lowercase-hex>` and be copied exactly. | Hashes are opaque metadata; Sprint 013 does not verify them against protected requirement bodies. |

---

## 2. Scope boundary

### Allowed scope

- Dependency-free local Python validator functions and tests.
- A BLK-test-specific approval record schema with explicit required fields.
- Exact source-evidence binding against existing disabled request/source report shapes.
- Rejection tests for missing fields, extra tools, mismatched source evidence, stale expiry, replayed approval IDs, `codex-live` token misuse, unsafe capabilities, and protected-vault body references.
- Deterministic audit evidence: approval record hash, source evidence hash, normalized decision, non-authority flags.
- Disabled transport preflight integration that records approval validation but still refuses live startup until Sprint 014.
- Active doctrine update documenting Sprint 013 as an approval/source-evidence contract, not live transport authorization.
- Outcome docs after each task, committed and pushed separately under current BLK-System policy.

### Hard blocks / stop conditions

Stop and escalate if any implementation attempts to:

- start live BLK-test MCP;
- start an MCP server or client;
- initialize JSON-RPC or perform a live tool listing;
- execute fixed BLK-test tools;
- create arbitrary shell/dynamic command execution;
- run against a real project repository as BLK-test behavior;
- mutate, stage, commit, push, reset, stash, or checkout source as BLK-test behavior;
- publish authoritative BEOs;
- generate RTM or make drift decisions;
- read protected BLK-req vault body text;
- accept `BLK_APPROVE_CODEX_LIVE` or `codex-live` as BLK-test MCP approval;
- create reusable ambient approvals not bound to one exact source/request/workspace/profile envelope;
- claim production sandbox/container/cgroup/VM/seccomp/AppArmor/SELinux or host-secret isolation enforcement.

---

## 3. Decision register

| ID | Decision | Rationale | Mechanical gate |
| --- | --- | --- | --- |
| S13-AUTH-001 | Sprint 013 approval is BLK-test-specific, not `codex-live`. | Tactical LLM approval and physics-oracle startup approval are different authority surfaces. | Reject any `approval_kind`, token, or profile that equals `codex-live` / `BLK_APPROVE_CODEX_LIVE`. |
| S13-AUTH-002 | Approval records bind a complete source-evidence envelope. | Partial evidence allows stale commit or missing trace laundering. | Require exact `beb_id`, `source_report_identity`, `commit_hash`, `pre_engine_hash`, and canonical `trace_artifacts`. |
| S13-AUTH-003 | Approval records bind one requested fixed-tool set and profile. | Broad reusable approvals become ambient execution authority. | Reject missing/extra tools, unknown tool names, wildcard tools, and mismatched `test_profile`. |
| S13-AUTH-004 | Approval records bind one workspace and timeout/output profile. | Resource/workspace substitution changes the approved risk surface. | Reject changed branch, workspace clone id, source path policy, timeout class, output byte budget, or compression budget. |
| S13-AUTH-005 | Approval records are one-run, expiry-bound, and replay-checked by supplied state. | Replay can silently reauthorize later runs. | Reject expired records and `approval_id` values present in caller-supplied used-ID sets. |
| S13-AUTH-006 | Validation may produce audit/preflight evidence but not live startup. | Sprint 014 owns first live smoke after accepted gates. | Assert `server_started == client_started == network_called == subprocess_called == False`, `tools_executed == []`, `live_mcp_authorized == False`. |
| S13-AUTH-007 | Approval evidence must not carry publication/RTM/active-vault authority. | BLK-test approval must not absorb BEO/RTM/BLK-req authority. | Assert `beo_publication == DRAFT_ONLY`, `rtm_status == NOT_GENERATED`, `active_vault_read == False`. |

---

## 4. Controller workflow for execution

1. Create an implementation branch, for example `sprint/blk-system-013`.
2. Commit this plan first if it is still uncommitted.
3. For every task below:
   1. Write/patch the failing test first.
   2. Run the focused RED command and confirm expected failure.
   3. Implement the smallest code/doc change.
   4. Run focused GREEN verification.
   5. Run task shared gates.
   6. Stage exact paths only.
   7. Verify `git diff --cached --name-only` contains only expected files.
   8. Commit implementation/doc change.
   9. Push the implementation/doc commit to GitHub.
   10. Create `docs/outcomes/BLK-SYSTEM-013_task-00N-outcome.md` with pre-commit verification evidence only.
   11. Commit and push the outcome doc as a separate docs commit.
   12. Send concise Discord summary with `MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-013_task-00N-outcome.md` after push.
4. Close the sprint with `docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md`, committed and pushed separately.

Cache-safe command pattern:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
```

Before every final status/commit:

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git diff --check
git status --short --branch
```

---

## 5. Shared test fixtures and constants

Use these values across Sprint 013 tests to keep evidence deterministic:

```python
TRACE_A = {
    "kind": "REQ",
    "id": "REQ-S13-001",
    "version_hash": "sha256:" + "a" * 64,
}
SOURCE_REPORT_IDENTITY = {
    "report_path": "reports/BEB_013/source-report.json",
    "report_hash": "sha256:" + "b" * 64,
    "report_id": "source-report-BEB_013",
}
WORKSPACE_IDENTITY = {
    "target_branch": "sprint/blk-system-013-fixture",
    "workspace_clone_id": "workspace-BEB_013-run-001",
    "source_path_policy": "isolated-copy-only",
}
TIMEOUT_OUTPUT_PROFILE = {
    "timeout_class": "bounded-short",
    "timeout_seconds": 30,
    "output_byte_limit": 8192,
    "compression": "line-dedupe-byte-bound",
}
REQUESTED_TOOLS = ["run_ast_validation"]
ISSUED_AT = "2026-05-06T10:00:00Z"
EXPIRES_AT = "2026-05-06T10:15:00Z"
NOW = "2026-05-06T10:05:00Z"
```

---

## 6. Task 0 — Commit the plan before implementation

**Objective:** Make this reviewed plan durable before implementation starts.

**Files:**

- Add: `docs/plans/blk-system-013_approval-source-evidence-authorization.md`

**Step 1: Verify plan file markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/plans/blk-system-013_approval-source-evidence-authorization.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-013',
    'Approval-Channel and Source-Evidence Authorization Mechanics',
    'does not authorize live BLK-test MCP',
    'codex-live',
    'source_report_identity',
    'operator identity',
    'Sprint 014 still owns any first live fixed-tool BLK-test MCP smoke',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing plan markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-013 plan markers: PASS')
PY
```

Expected: `BLK-SYSTEM-013 plan markers: PASS`.

**Step 2: Stage exact path and commit**

Run:

```bash
git add docs/plans/blk-system-013_approval-source-evidence-authorization.md
git diff --cached --name-only
git commit -m "docs: plan blk-system sprint 013 approval authorization"
git push
```

Expected staged path only:

```text
docs/plans/blk-system-013_approval-source-evidence-authorization.md
```

**Step 3: Outcome doc**

Create `docs/outcomes/BLK-SYSTEM-013_task-000-outcome.md`, then exact-path commit and push it.

---

## 7. Task 1 — Boundary review artifact and persistent doctrine gate

**Objective:** Preserve the Sprint 013 authority boundary in a review artifact and add a test gate before implementation code exists.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-013_approval-source-evidence-boundary-review.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-013_task-001-outcome.md`

**Step 1: Write failing test**

Add constants near the existing Sprint 011/012 review constants:

```python
SPRINT013_APPROVAL_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-013_approval-source-evidence-boundary-review.md"
```

Add test:

```python
def test_sprint013_approval_source_evidence_review_is_source_bound_and_non_executing(self):
    self.assertTrue(SPRINT013_APPROVAL_REVIEW.exists(), "Sprint 013 approval/source-evidence review missing")
    text = SPRINT013_APPROVAL_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-013",
        "Approval-channel and source-evidence authorization mechanics",
        "codex-live approval is not BLK-test MCP approval",
        "source BLK-pipe report identity",
        "beb_id",
        "source commit_hash",
        "pre_engine_hash",
        "canonical trace_artifacts",
        "requested fixed BLK-test tool(s)",
        "test profile",
        "workspace identity",
        "timeout/output profile",
        "operator identity/approval timestamp",
        "does not authorize live BLK-test MCP",
        "does not authorize live MCP client/server startup",
        "does not execute fixed-tool tests",
        "does not mutate primary repo",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not read protected BLK-req vault bodies",
        "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 013 approval/source-evidence markers missing: {missing}")
```

**Step 2: Run RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint013_approval_source_evidence_review_is_source_bound_and_non_executing
```

Expected: FAIL because the review doc does not exist yet.

**Step 3: Create review doc**

Review doc required sections:

- Source docs reviewed: BLK-001, BLK-013, BLK-017, BLK-018, Sprint 010 approval register, Sprint 012 closeout.
- Scope: source-bound BLK-test approval validator only.
- Non-authority markers: no live MCP, no server/client startup, no fixed-tool execution, no source mutation/staging/commit/push, no BEO publication, no RTM generation, no protected vault body reads, no production sandbox/host-secret claims.
- Accepted evidence fields: source report identity, `beb_id`, commit/pre-engine evidence, canonical trace artifacts, tools, profile, workspace, timeout/output, operator identity/timestamp.
- Handoff: Sprint 014 owns first live fixed-tool BLK-test MCP smoke.

**Step 4: Run GREEN**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint013_approval_source_evidence_review_is_source_bound_and_non_executing
```

Expected: PASS.

**Step 5: Shared gates / commit / push / outcome**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
git diff --check
rm -rf python/__pycache__ .pytest_cache
git status --short --branch
git add docs/reviews/BLK-SYSTEM-013_approval-source-evidence-boundary-review.md python/test_active_doctrine_review_gates.py
git diff --cached --name-only
git commit -m "docs: define blk-system sprint 013 approval boundary"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-013_task-001-outcome.md`.

---

## 8. Task 2 — Approval record schema and fail-closed parser

**Objective:** Add a dependency-free module that normalizes a BLK-test approval record and rejects missing/unsafe fields before source binding.

**Files:**

- Create: `python/blk_test_mcp_approval_authorization.py`
- Create: `python/test_blk_test_mcp_approval_authorization.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-013_task-002-outcome.md`

**Step 1: Write failing tests**

Create `python/test_blk_test_mcp_approval_authorization.py` with tests for:

- valid approval record normalizes required fields;
- missing `operator_identity` rejects;
- missing `approval_timestamp` rejects;
- missing `approval_id` rejects;
- `approval_kind == "codex-live"` rejects;
- token text containing `BLK_APPROVE_CODEX_LIVE` rejects;
- unknown/wildcard/dynamic requested tools reject;
- protected-vault body path/reference rejects;
- output always carries non-authority flags.

Core test shape:

```python
import unittest

from blk_test_mcp_approval_authorization import (
    build_authorization_request,
    validate_blk_test_approval_record,
)

class ApprovalRecordSchemaTest(unittest.TestCase):
    def test_valid_record_normalizes_required_fields_without_live_authority(self):
        request = build_authorization_request(source_report=valid_source_report(), requested_tools=["run_ast_validation"])
        approval = valid_approval_record(request)
        decision = validate_blk_test_approval_record(approval, request, now="2026-05-06T10:05:00Z")

        self.assertEqual(decision["decision"], "APPROVAL_VALIDATED_SOURCE_BOUND")
        self.assertFalse(decision["live_mcp_authorized"])
        self.assertFalse(decision["server_started"])
        self.assertFalse(decision["client_started"])
        self.assertEqual(decision["tools_executed"], [])
        self.assertEqual(decision["rtm_status"], "NOT_GENERATED")
        self.assertEqual(decision["beo_publication"], "DRAFT_ONLY")
```

**Step 2: Run RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
```

Expected: FAIL because module/functions do not exist.

**Step 3: Implement minimal module**

Required public API:

```python
ALLOWED_FIXED_TOOLS = (
    "run_ast_validation",
    "run_ipc_race_test",
    "run_svg_export_purity_test",
    "run_architecture_lint",
)

def build_authorization_request(*, source_report, requested_tools, test_profile="strict-ci", workspace_identity=None, timeout_output_profile=None):
    """Return a normalized source/request envelope for BLK-test approval validation only."""


def validate_blk_test_approval_record(approval_record, authorization_request, *, now, used_approval_ids=None):
    """Return source-bound approval evidence or raise ValueError; never starts live transport."""
```

Implementation constraints:

- Use only standard library imports.
- Do not import `subprocess`, `socket`, `requests`, `http`, `urllib`, `asyncio`, MCP SDKs, or package managers.
- Deep-copy inbound data before returning it.
- Raise `ValueError` with specific messages for invalid approval data.
- Return non-authority fields: `live_mcp_authorized: False`, `server_started: False`, `client_started: False`, `network_called: False`, `subprocess_called: False`, `tools_executed: []`, `source_write_allowed: False`, `staging_allowed: False`, `commit_allowed: False`, `push_allowed: False`, `active_vault_read: False`, `rtm_status: NOT_GENERATED`, `beo_publication: DRAFT_ONLY`.

**Step 4: Run GREEN**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
```

Expected: PASS.

**Step 5: Commit/push/outcome**

Stage exact paths only:

```bash
git add python/blk_test_mcp_approval_authorization.py python/test_blk_test_mcp_approval_authorization.py
git diff --cached --name-only
git commit -m "feat: add blk-test approval record validator"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-013_task-002-outcome.md`.

---

## 9. Task 3 — Exact source-evidence binding and mismatch rejection

**Objective:** Require approval records to match the full source/request envelope exactly.

**Files:**

- Modify: `python/blk_test_mcp_approval_authorization.py`
- Modify: `python/test_blk_test_mcp_approval_authorization.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-013_task-003-outcome.md`

**Step 1: Write failing tests**

Add tests for each mismatch class:

- approval `beb_id` differs from source/request;
- source `commit_hash` differs;
- `pre_engine_hash` differs;
- `trace_artifacts` differs in hash/case/order/content;
- `source_report_identity.report_hash` differs;
- requested tools contain extra/missing tool;
- `test_profile` differs;
- `workspace_identity.workspace_clone_id` differs;
- timeout/output profile differs.

Example:

```python
def test_rejects_mismatched_commit_hash(self):
    request = build_authorization_request(source_report=valid_source_report(), requested_tools=["run_ast_validation"])
    approval = valid_approval_record(request)
    approval["source_evidence"]["commit_hash"] = "deadbeef"

    with self.assertRaisesRegex(ValueError, "commit_hash"):
        validate_blk_test_approval_record(approval, request, now="2026-05-06T10:05:00Z")
```

**Step 2: Run RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
```

Expected: new mismatch tests fail until exact comparison exists.

**Step 3: Implement exact binding**

Implementation requirements:

- Normalize source evidence into a stable dict:
  - `source_report_identity`
  - `beb_id`
  - `commit_hash`
  - `pre_engine_hash`
  - `trace_artifacts`
- Normalize request evidence:
  - `requested_tools`
  - `test_profile`
  - `workspace_identity`
  - `timeout_output_profile`
- Reject unknown fields that imply authority, including `shell`, `command`, `exec`, `eval`, `source_mutation`, `staging`, `commit`, `push`, `publish_beo`, `generate_rtm`, `active_vault_body`.
- Preserve copied source evidence in the returned decision.

**Step 4: Run GREEN and gates**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
git add python/blk_test_mcp_approval_authorization.py python/test_blk_test_mcp_approval_authorization.py
git diff --cached --name-only
git commit -m "test: bind blk-test approval to exact source evidence"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-013_task-003-outcome.md`.

---

## 10. Task 4 — Expiry, replay, and deterministic audit hashes

**Objective:** Make approval evidence one-run/scoped with deterministic audit identities and fail-closed replay/expiry behavior.

**Files:**

- Modify: `python/blk_test_mcp_approval_authorization.py`
- Modify: `python/test_blk_test_mcp_approval_authorization.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-013_task-004-outcome.md`

**Step 1: Write failing tests**

Add tests for:

- expired approval rejects when `now > expires_at`;
- approval with `approval_id` in `used_approval_ids` rejects;
- malformed timestamps reject;
- missing `expires_at` rejects;
- returned `approval_record_hash` is stable across dict insertion order;
- returned `source_evidence_hash` changes when source evidence changes;
- audit evidence omits raw secrets and protected body text.

Example:

```python
def test_approval_record_hash_is_stable_across_key_order(self):
    request = build_authorization_request(source_report=valid_source_report(), requested_tools=["run_ast_validation"])
    approval_a = valid_approval_record(request)
    approval_b = dict(reversed(list(approval_a.items())))

    decision_a = validate_blk_test_approval_record(approval_a, request, now="2026-05-06T10:05:00Z")
    decision_b = validate_blk_test_approval_record(approval_b, request, now="2026-05-06T10:05:00Z")

    self.assertEqual(decision_a["approval_record_hash"], decision_b["approval_record_hash"])
```

**Step 2: Run RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
```

Expected: new tests fail until expiry/replay/hash logic exists.

**Step 3: Implement expiry/replay/audit**

Implementation requirements:

- Parse UTC ISO-8601 `Z` timestamps using standard library only.
- Enforce `issued_at <= approval_timestamp <= expires_at` where applicable.
- Reject `approval_id` reuse via caller-supplied `used_approval_ids` iterable.
- Build stable hashes with canonical JSON: `json.dumps(value, sort_keys=True, separators=(",", ":"))`, then `sha256:` + lowercase hexdigest.
- Return audit fields:
  - `approval_id`
  - `operator_identity`
  - `approval_timestamp`
  - `expires_at`
  - `approval_record_hash`
  - `source_evidence_hash`
  - `authorization_request_hash`
  - `decision: APPROVAL_VALIDATED_SOURCE_BOUND`
  - non-authority flags.

**Step 4: Run GREEN and gates**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_approval_authorization
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
git add python/blk_test_mcp_approval_authorization.py python/test_blk_test_mcp_approval_authorization.py
git diff --cached --name-only
git commit -m "feat: add blk-test approval replay and audit gates"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-013_task-004-outcome.md`.

---

## 11. Task 5 — Disabled transport preflight integration without live startup

**Objective:** Wire approval validation evidence into a disabled startup preflight while preserving BLK-017/018 non-execution boundaries and Sprint 014 handoff.

**Files:**

- Modify: `python/blk_test_mcp_disabled_transport.py`
- Modify: `python/test_blk_test_mcp_disabled_transport.py`
- Modify: `python/test_blk_test_mcp_approval_authorization.py` if shared helper imports need adjustment
- Outcome: `docs/outcomes/BLK-SYSTEM-013_task-005-outcome.md`

**Step 1: Write failing tests**

Add tests in `python/test_blk_test_mcp_disabled_transport.py`:

```python
def test_sprint013_validated_approval_still_blocks_live_startup_until_sprint014(self):
    approval_decision = {
        "decision": "APPROVAL_VALIDATED_SOURCE_BOUND",
        "approval_id": "BLKTEST-S13-APPROVAL-001",
        "approval_record_hash": "sha256:" + "c" * 64,
        "source_evidence_hash": "sha256:" + "d" * 64,
        "authorization_request_hash": "sha256:" + "e" * 64,
        "live_mcp_authorized": False,
    }
    descriptor = build_disabled_transport_descriptor(approval_record={"approval_id": "BLKTEST-S13-APPROVAL-001"})
    decision = evaluate_sprint013_approval_preflight(descriptor, approval_decision)

    self.assertEqual(decision["decision"], "STARTUP_BLOCKED_SPRINT014_REQUIRED")
    self.assertFalse(decision["server_started"])
    self.assertFalse(decision["client_started"])
    self.assertFalse(decision["network_called"])
    self.assertFalse(decision["subprocess_called"])
    self.assertEqual(decision["tools_executed"], [])
    self.assertFalse(decision["live_mcp_authorized"])
    self.assertIn("Sprint 014", decision["reason"])
```

Also add rejection tests for malformed approval decisions and for `decision != APPROVAL_VALIDATED_SOURCE_BOUND`.

**Step 2: Run RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_disabled_transport
```

Expected: FAIL because `evaluate_sprint013_approval_preflight` does not exist.

**Step 3: Implement preflight helper**

Add public helper:

```python
def evaluate_sprint013_approval_preflight(descriptor: dict[str, object], approval_decision: dict[str, object]) -> dict[str, object]:
    """Record validated Sprint 013 approval evidence but block live startup until Sprint 014."""
```

Behavior:

- Validate stdio-only descriptor with existing `_require_stdio_transport_metadata`.
- Require `approval_decision["decision"] == "APPROVAL_VALIDATED_SOURCE_BOUND"`.
- Require stable hash fields matching `sha256:<64-lowercase-hex>`.
- Return `STARTUP_BLOCKED_SPRINT014_REQUIRED` with all non-authority flags false/empty and copied hash evidence.
- Do not import approval module if that creates coupling issues; accept a plain decision dict.
- Do not start transport or execute tools.

**Step 4: Source scan gate**

Update the existing AST/source scan if needed so the new helper remains free of live imports/calls while allowing safe public evidence keys.

**Step 5: Run GREEN and gates**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_mcp_disabled_transport python.test_blk_test_mcp_approval_authorization
git diff --check
```

Expected: PASS.

**Step 6: Commit/push/outcome**

```bash
git add python/blk_test_mcp_disabled_transport.py python/test_blk_test_mcp_disabled_transport.py python/test_blk_test_mcp_approval_authorization.py
git diff --cached --name-only
git commit -m "feat: bind sprint 013 approval preflight without live startup"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-013_task-005-outcome.md`.

---

## 12. Task 6 — Active BLK-019 doctrine and cross-reference gates

**Objective:** Publish Sprint 013 behavior as active doctrine without superseding BLK-017 disabled transport or BLK-018 workspace/process probes.

**Files:**

- Create: `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md`
- Modify: `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md`
- Modify: `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-013_task-006-outcome.md`

**Step 1: Write failing doctrine gates**

Add constants:

```python
BLK019 = ROOT / "docs" / "BLK-019_blk-test-mcp-approval-source-evidence-authorization.md"
```

Add test for BLK-019 markers:

```python
def test_blk019_records_sprint013_approval_source_evidence_without_live_startup(self):
    self.assertTrue(BLK019.exists(), "BLK-019 approval/source-evidence doctrine missing")
    text = BLK019.read_text()
    required = [
        "**Status:** Active approval/source-evidence authorization contract",
        "BLK-SYSTEM-013",
        "codex-live approval is not BLK-test MCP approval",
        "source BLK-pipe report identity",
        "beb_id",
        "source commit_hash",
        "pre_engine_hash",
        "canonical trace_artifacts",
        "requested fixed BLK-test tool(s)",
        "workspace identity",
        "timeout/output profile",
        "operator identity/approval timestamp",
        "one-run/scoped",
        "replay",
        "does not authorize live BLK-test MCP",
        "does not authorize live MCP client/server startup",
        "does not execute fixed-tool tests",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not read protected BLK-req vault bodies",
        "Sprint 014 owns any future first live fixed-tool BLK-test MCP smoke",
        "python/blk_test_mcp_approval_authorization.py",
        "python/test_blk_test_mcp_approval_authorization.py",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-019 markers missing: {missing}")
```

Add cross-reference test:

```python
def test_blk017_018_019_cross_reference_approval_contract_without_live_authority(self):
    expectations = {
        BLK017: ["BLK-019", "Sprint 013", "approval/source-evidence"],
        BLK018: ["BLK-019", "approval/source-evidence authorization", "before Sprint 014"],
        BLK019: ["BLK-017", "BLK-018", "Sprint 014"],
    }
    for path, markers in expectations.items():
        text = path.read_text()
        missing = [marker for marker in markers if marker not in text]
        self.assertEqual(missing, [], f"{path.relative_to(ROOT)} missing {missing}")
```

**Step 2: Run RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
```

Expected: FAIL because BLK-019 and cross-references are missing.

**Step 3: Create BLK-019 and patch cross-references**

BLK-019 required sections:

1. Purpose.
2. Current authority boundary.
3. Approval record required fields.
4. Source-evidence binding rules.
5. Expiry/replay/audit evidence.
6. Relationship to BLK-017 and BLK-018.
7. Non-authority checklist.
8. Stop conditions.
9. Implementation and tests.

Patch BLK-017/018 narrowly:

- BLK-017 remains active disabled transport contract until live authority is separately approved.
- BLK-018 remains inert workspace/process-control probe contract.
- BLK-019 adds approval/source-evidence authorization validation evidence only.
- Sprint 014 still owns first live fixed-tool BLK-test MCP smoke.

**Step 4: Run GREEN and gates**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
git add docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md python/test_active_doctrine_review_gates.py
git diff --cached --name-only
git commit -m "docs: define blk-test approval source evidence contract"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-013_task-006-outcome.md`.

---

## 13. Task 7 — Full-suite verification and Sprint 014 handoff closeout

**Objective:** Close BLK-SYSTEM-013 with full verification evidence and a narrow Sprint 014 handoff seed.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md`
- Optionally modify: `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` only if a RED gate proves stale post-Sprint-013 wording; otherwise preserve history.

**Step 1: Full verification**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git status --short --branch
```

Expected:

- Python `unittest` suite passes.
- Python pytest suite passes (or same tests collected successfully with no cache provider).
- `go test ./...` passes.
- `go vet ./...` passes.
- `git diff --check` passes.
- No `python/__pycache__` or pytest cache remains staged/untracked.

**Step 2: Create closeout doc**

`docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md` must include:

- sprint ID and timestamp;
- task commit table;
- outcome doc table;
- exact verification commands and results;
- explicit statement that Sprint 013 implemented approval/source-evidence validation only;
- explicit statement that Sprint 013 does not authorize live BLK-test MCP, live MCP client/server startup, fixed-tool execution, arbitrary shell, source mutation/staging/commit/push as BLK-test behavior, authoritative BEO publication, RTM generation, RTM drift rejection, active BLK-req vault body reads, production sandbox/host-secret claims, or first live smoke;
- Sprint 014 handoff seed:

```text
BLK-SYSTEM-014 — First live fixed-tool BLK-test MCP smoke under explicit human approval
```

Narrow Sprint 014 prerequisites:

1. BLK-017 disabled transport contract remains intact or is explicitly superseded by Sprint 014 plan and human approval.
2. BLK-018 workspace/process controls must pass.
3. BLK-019 approval/source-evidence validation must pass for the exact source/request/workspace/profile envelope.
4. Human approval must be explicit and current.
5. Still no arbitrary shell, source mutation, BEO publication, RTM generation, or active-vault body reads unless a later sprint explicitly grants those authorities.

**Step 3: Validate closeout**

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-013',
    'approval/source-evidence validation only',
    'does not authorize live BLK-test MCP',
    'does not authorize live MCP client/server startup',
    'does not execute fixed-tool tests',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'does not read protected BLK-req vault bodies',
    'BLK-SYSTEM-014',
    'First live fixed-tool BLK-test MCP smoke under explicit human approval',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing closeout markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-013 closeout markers: PASS')
PY
```

Expected: PASS.

**Step 4: Commit/push closeout**

```bash
git add docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system sprint 013"
git push
```

Then send concise Discord summary with:

```text
MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
```

---

## 14. Final acceptance criteria

BLK-SYSTEM-013 is complete only when all are true:

- `docs/plans/blk-system-013_approval-source-evidence-authorization.md` is committed.
- `docs/reviews/BLK-SYSTEM-013_approval-source-evidence-boundary-review.md` exists and passes the active doctrine gate.
- `python/blk_test_mcp_approval_authorization.py` exists and is dependency-free.
- `python/test_blk_test_mcp_approval_authorization.py` proves:
  - exact source-evidence binding;
  - fixed-tool/profile/workspace/timeout-output binding;
  - operator identity/timestamp requirements;
  - `codex-live` rejection;
  - missing/extra/mismatched field rejection;
  - expiry/replay rejection;
  - deterministic audit hashes;
  - non-authority flags.
- `python/blk_test_mcp_disabled_transport.py` records Sprint 013 validated approval preflight evidence but still blocks live startup until Sprint 014.
- `docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md` exists as active doctrine.
- BLK-017, BLK-018, and BLK-019 cross-reference each other without implying live authority.
- Every task has a matching pushed `docs/outcomes/BLK-SYSTEM-013_task-00N-outcome.md`.
- Sprint closeout is pushed.
- Final verification passes:
  - `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'`
  - `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python`
  - `go test ./...`
  - `go vet ./...`
  - `git diff --check`
- Final worktree is clean except any deliberate, reported, user-approved untracked files.

---

## 15. Expected artifact set

```text
docs/plans/blk-system-013_approval-source-evidence-authorization.md
docs/reviews/BLK-SYSTEM-013_approval-source-evidence-boundary-review.md
python/blk_test_mcp_approval_authorization.py
python/test_blk_test_mcp_approval_authorization.py
python/blk_test_mcp_disabled_transport.py
python/test_blk_test_mcp_disabled_transport.py
python/test_active_doctrine_review_gates.py
docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md
docs/BLK-019_blk-test-mcp-approval-source-evidence-authorization.md
docs/outcomes/BLK-SYSTEM-013_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-005-outcome.md
docs/outcomes/BLK-SYSTEM-013_task-006-outcome.md
docs/outcomes/BLK-SYSTEM-013_sprint-closeout.md
```

---

## 16. Executor notes

- Do not stage with `git add .`.
- Do not broaden source scans to rewrite historical Sprint 010/011/012 review/outcome wording unless a current-doctrine gate requires it.
- Do not make outcome docs self-referential with their own final commit hash. Record pre-commit verification in the doc; report post-push commit/status in the executor summary or later closeout.
- Keep Discord updates concise and only after meaningful task completion/push events.
- If a subagent/Codex run attempts live transport, shell execution inside BLK-test approval code, source mutation as BLK-test behavior, BEO publication, RTM generation, or active-vault body reads, reject the run and retry with a narrower packet.
