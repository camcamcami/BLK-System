# BLK-SYSTEM-015 — Draft BEO Publication Gate Review Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `writing-plans`, and strict TDD to implement this plan task-by-task. Any Codex/Hermes delegation is project-maintenance implementation support only; it must not be used by BLK-test MCP, live-smoke evidence, BEO projection evidence, approval evidence, publication evidence, or RTM evidence. If delegating implementation work to Codex CLI, use model `gpt-5.4` and run a hostile audit after every execution packet before accepting changes.

**Goal:** Review and harden whether source-bound BLK-SYSTEM-014 live BLK-test smoke evidence may feed draft BEO fixture projection while keeping `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"` until a later explicit publication sprint grants authority.

**Architecture:** Sprint 015 adds only a draft-only BEO gate on top of BLK-020 first-smoke evidence. It must not rerun BLK-test MCP, broaden BLK-020, publish authoritative BEOs, mutate public ledgers, generate RTM, read protected BLK-req vault bodies, or imply signer/storage/rollback authority. The safe implementation surface is a deterministic local projection/review path, persistent tests, a boundary review artifact, and an active doctrine document that records the draft-only gate.

**Tech Stack:** Python standard library only (`unittest`, `copy`, `hashlib` if needed, `re`, `pathlib`, `typing`), existing BEO fixture modules, existing BLK-test first-smoke evidence modules/docs, Markdown doctrine/review/outcome docs, Go verification gates.

---

## 0. Live preflight facts

Captured before writing this plan:

```text
Date: Thu May  7 07:26:06 AM AEST 2026
Repository: /home/dad/BLK-System
Branch/status: ## main...origin/main
HEAD: ff3c5a6 docs: record blk-system sprint 014 hardening review
Plan file: docs/plans/blk-system-015_draft-beo-publication-gate-review.md
```

Sprint ID ownership check:

- `BLK-SYSTEM-015` is reserved by `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` for `Draft BEO publication gate review, still not authoritative unless explicitly approved`.
- The existing `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md` is a BLK doctrine document, not this system sprint plan. Do not rename or repurpose it.
- Sprint 014 closeout explicitly hands off to BLK-SYSTEM-015 with prerequisites: BLK-020 first-smoke evidence remains source-bound/replayable; draft projection preserves `beo_publication: "DRAFT_ONLY"`; BLOCKED evidence does not project to success; RTM remains disabled; active BLK-req vault bodies remain unread.
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md` exists and records exactly one approved PASS first smoke with cleanup verified. Sprint 015 must not rerun that first-smoke path.

---

## 1. BLK-001 domain matrix

| Domain/component | Sprint 015 relationship | Authority statement |
| --- | --- | --- |
| `blk-req` | Carries opaque `trace_artifacts[*].version_hash` metadata from source-bound evidence into draft BEO fixtures only. | Does not read protected BLK-req vault bodies, parse active requirements, promote requirements, or create coverage claims. |
| Architecture & Feature Planning / HITL | Reviews whether draft-only BEO projection is safe after BLK-020 first-smoke evidence. | Does not grant authoritative BEO publication; any future publication authority requires a separate explicit human-approved sprint. |
| `blk-id` | May validate canonical `sha256:<64-lowercase-hex>` hashes for approval/source/request/transcript/evidence identifiers. | Hashes are evidence identifiers only; they do not create signer, storage, rollback, ledger, RTM, or active-vault authority. |
| `blk-relay` | No new transport. Consumes existing recorded BLK-020 evidence shape only. | Does not start MCP, stdio child processes, HTTP/WebSocket/TCP/UDP, daemons, listeners, callbacks, or live replay services. |
| `blk-pipe` | Source report identity, `beb_id`, `commit_hash`, `pre_engine_hash`, and trace metadata remain source-bound inputs. | BLK-test/BEO projection must not mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test behavior. |
| `blk-test` | Provides previously recorded first-smoke PASS/FAIL/BLOCKED/FATAL evidence vocabulary. | Sprint 015 must not rerun live smoke, broaden tools, run real target repositories, or convert BLOCKED/FATAL evidence into success. |
| BEO/outcomes | Owns draft BEO fixture projection and publication gate review. | Outputs remain `DRAFT_ONLY`; no authoritative BEO publication, signer identity, public outcome ledger mutation, storage contract, or rollback authority. |
| `blk-link` / RTM | May carry `rtm_status: NOT_GENERATED` and reject RTM/coverage fields. | Does not generate RTM, make drift decisions, claim coverage, or read active-vault bodies. |
| Cryptographic `version_hash` baton | Requires canonical trace hashes in draft BEO projection. | Hashes remain opaque and source-bound; Sprint 015 does not verify protected requirement bodies. |

---

## 2. Scope boundary

### Allowed scope

- Preserve a Sprint 015 boundary review artifact in `docs/reviews/`.
- Add persistent active-doctrine gates proving Sprint 015 remains draft-only and non-authoritative.
- Extend or wrap `python/beo_fixture_projection.py` with a deterministic local projector for source-bound BLK-020 live-smoke evidence into a **draft** BEO candidate.
- Add tests in `python/test_beo_fixture_projection.py` proving:
  - PASS live-smoke evidence can project only to a draft PASS BEO fixture;
  - FAIL live-smoke evidence can project only to a draft FAIL BEO fixture;
  - BLOCKED, FATAL, TRANSPORT_ERROR, OPERATOR_INTERRUPTED, unknown, or missing evidence cannot project to success;
  - source/request/approval/transcript hashes are required and canonical;
  - `trace_artifacts` must be non-empty and canonical;
  - publication/ledger/signer/storage/rollback fields are rejected;
  - `rtm_status` remains `NOT_GENERATED` and RTM/coverage fields are rejected;
  - protected BLK-req vault bodies are never read.
- Create a new active doctrine document only if the test gate proves it is necessary, expected path: `docs/BLK-021_beo-draft-publication-gate-review.md`.
- Patch BLK-016 and BLK-020 narrowly to cross-reference the Sprint 015 draft-only BEO gate without implying publication authority.
- Produce matching outcome docs after every task and a sprint closeout.

### Hard blocks / stop conditions

Stop and escalate if any implementation tries to:

- rerun BLK-SYSTEM-014 first live smoke or start any live BLK-test MCP process;
- start a live MCP server/client, stdio child process, HTTP/WebSocket/TCP/UDP listener, daemon, callback, or replay service;
- authorize authoritative BEO publication or public outcome ledger mutation;
- add signer identity, publication timestamp, storage location, rollback authority, ledger ID, or release authority to draft BEO outputs;
- convert `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, `OPERATOR_INTERRUPTED`, unknown, or missing evidence into PASS/success;
- generate RTM, emit coverage matrices, make drift decisions, or claim requirement coverage;
- read protected BLK-req vault bodies from `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- run against `/home/dad/BLK-System` or another real target repository as BLK-test behavior;
- mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test behavior;
- claim production sandbox/container/cgroup/VM/seccomp/AppArmor/SELinux or host-secret isolation enforcement;
- leak host secrets, environment dumps, approval secrets, active-vault body text, or unbounded logs.

---

## 3. Decision register

| ID | Decision | Rationale | Mechanical gate |
| --- | --- | --- | --- |
| S15-BEO-001 | Sprint 015 is a draft-only review/projection gate, not a publication sprint. | Future slicing reserves Sprint 015 for review and explicitly blocks authoritative BEO publication. | Tests assert every projected BEO has `beo_publication == "DRAFT_ONLY"` and rejects `PUBLISHED`, `published_at`, `approved_by`, `signature`, storage, rollback, and ledger fields. |
| S15-BEO-002 | Source-bound BLK-020 PASS/FAIL evidence may feed draft BEO fixtures only. | BLK-020 first-smoke evidence is replayable, but not publication authority. | Projection requires source/report fields, approval/request/source/transcript hashes, trace artifacts, checks, and `source == "blk-test-mcp-first-live-smoke"`; outputs remain draft-only. |
| S15-BEO-003 | BLOCKED/FATAL/transport/operator-interrupted evidence never projects to success. | BLOCKED is not-run/non-authoritative and fatal/transport statuses are infrastructure evidence. | Status matrix tests reject non-PASS/FAIL statuses and assert no BEO object is returned. |
| S15-BEO-004 | RTM remains disabled. | Future RTM work is separate and may require active-vault hash policy. | Tests assert `rtm_status == "NOT_GENERATED"`, no `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, `drift`, or coverage fields. |
| S15-BEO-005 | Active-vault bodies remain unread. | BLK-test/BEO draft projection should not interpret requirements. | Path read monkeypatch/source scan gates fail on protected prefixes/body reads. |
| S15-BEO-006 | Sprint 015 does not rerun first smoke. | Sprint 014 already recorded exactly one approved smoke; replaying would violate one-run approval semantics. | Source scan and tests keep the projector pure/local; no import/use of `run_sprint014_first_live_smoke`, `subprocess.Popen`, sockets, or live transport entrypoints. |
| S15-BEO-007 | Active doctrine may be `BLK-021`, not `BLK-015`. | `docs/BLK-015...` already exists with different doctrine semantics. | Active doctrine gate points to `docs/BLK-021_beo-draft-publication-gate-review.md` and explicitly distinguishes it from `BLK-SYSTEM-015`. |

---

## 4. Controller workflow for execution

1. Create an implementation branch, for example `sprint/blk-system-015`.
2. Commit this plan first if it is still uncommitted.
3. For every task below:
   1. Write/patch the failing test first.
   2. Run the focused RED command and confirm expected failure.
   3. Implement the smallest code/doc change.
   4. Run focused GREEN verification.
   5. Run task shared gates.
   6. Remove Python/pytest caches.
   7. Stage exact paths only.
   8. Verify `git diff --cached --name-only` contains only expected files.
   9. Commit implementation/doc change.
   10. Push the implementation/doc commit to GitHub.
   11. Create `docs/outcomes/BLK-SYSTEM-015_task-00N-outcome.md` with RED/GREEN and pre-commit verification evidence.
   12. Commit and push the outcome doc separately.
   13. Send concise Discord summary with `MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-015_task-00N-outcome.md` after push.
4. Close the sprint with `docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md`, committed and pushed separately.

Cache-safe command pattern:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git diff --check
git status --short --branch
```

---

## 5. Shared deterministic fixture values

Use these values across Sprint 015 tests unless a task says otherwise:

```python
TRACE_S15 = {
    "kind": "REQ",
    "id": "REQ-S14-SMOKE-001",
    "version_hash": "sha256:" + "1" * 64,
}
LIVE_SMOKE_EVIDENCE_S15 = {
    "sprint": "BLK-SYSTEM-014",
    "source": "blk-test-mcp-first-live-smoke",
    "run_id": "BLK-SYSTEM-014-SMOKE-001",
    "tool_name": "run_ast_validation",
    "status": "PASS",
    "beb_id": "BEB_S14_SYNTHETIC_SMOKE",
    "commit_hash": "synthetic-fixture-no-git-commit",
    "pre_engine_hash": "sha256:" + "3" * 64,
    "test_profile": "bounded-live-smoke-short",
    "trace_artifacts": [TRACE_S15],
    "checks": [
        {
            "name": "run_ast_validation",
            "status": "PASS",
            "summary": "AST validation passed for synthetic isolated workspace",
        }
    ],
    "approval_record_hash": "sha256:" + "4" * 64,
    "authorization_request_hash": "sha256:" + "5" * 64,
    "source_evidence_hash": "sha256:" + "6" * 64,
    "transcript_hash": "sha256:" + "7" * 64,
    "cleanup_status": "CLEANED",
    "beo_publication": "DRAFT_ONLY",
    "rtm_status": "NOT_GENERATED",
    "active_vault_read": False,
}
```

---

## 6. Task 0 — Commit the plan before implementation

**Objective:** Make this reviewed plan durable before implementation starts.

**Files:**

- Add: `docs/plans/blk-system-015_draft-beo-publication-gate-review.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-015_task-000-outcome.md`

**Step 1: Verify plan file markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/plans/blk-system-015_draft-beo-publication-gate-review.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-015',
    'Draft BEO Publication Gate Review',
    'beo_publication: "DRAFT_ONLY"',
    'rtm_status: "NOT_GENERATED"',
    'BLK-020 first-smoke evidence',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'does not read protected BLK-req vault bodies',
    'BLOCKED, FATAL, TRANSPORT_ERROR, OPERATOR_INTERRUPTED',
    'docs/BLK-021_beo-draft-publication-gate-review.md',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing plan markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-015 plan markers: PASS')
PY
```

Expected: `BLK-SYSTEM-015 plan markers: PASS`.

**Step 2: Stage exact path and commit**

Run:

```bash
git add docs/plans/blk-system-015_draft-beo-publication-gate-review.md
git diff --cached --name-only
git commit -m "docs: plan blk-system sprint 015 draft beo gate"
git push
```

Expected staged path only:

```text
docs/plans/blk-system-015_draft-beo-publication-gate-review.md
```

**Step 3: Outcome doc**

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-015_task-000-outcome.md`.

---

## 7. Task 1 — Boundary review artifact and persistent doctrine gate

**Objective:** Preserve Sprint 015 draft-only BEO publication boundaries before code changes.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-015_draft-beo-publication-gate-review.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-015_task-001-outcome.md`

**Step 1: Write failing test**

Add constant near existing Sprint review constants:

```python
SPRINT015_BEO_GATE_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-015_draft-beo-publication-gate-review.md"
```

Add test:

```python
def test_sprint015_draft_beo_publication_gate_review_is_draft_only(self):
    self.assertTrue(SPRINT015_BEO_GATE_REVIEW.exists(), "Sprint 015 BEO gate review missing")
    text = SPRINT015_BEO_GATE_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-015",
        "Draft BEO publication gate review",
        "BLK-020 first-smoke evidence",
        "beo_publication: \"DRAFT_ONLY\"",
        "rtm_status: \"NOT_GENERATED\"",
        "source-bound and replayable",
        "PASS/FAIL evidence may project only to draft BEO fixtures",
        "BLOCKED evidence must not project to success",
        "does not authorize authoritative BEO publication",
        "does not mutate public outcome ledgers",
        "does not grant signer/storage/rollback authority",
        "does not authorize RTM generation",
        "does not claim RTM coverage",
        "does not read protected BLK-req vault bodies",
        "does not rerun BLK-SYSTEM-014 first live smoke",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 015 BEO gate review markers missing: {missing}")
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint015_draft_beo_publication_gate_review_is_draft_only
```

Expected: FAIL because the review doc does not exist yet.

**Step 3: Create review doc**

Required sections:

1. Source docs reviewed: BLK-001, BLK-014, BLK-016, BLK-020, Sprint 010 future slicing/gap register, Sprint 014 closeout.
2. Positive authority: review/project source-bound PASS/FAIL first-smoke evidence into draft BEO fixtures only.
3. Non-authority: no authoritative BEO publication, ledger mutation, signer/storage/rollback authority, RTM, coverage, active-vault reads, live MCP reruns.
4. Status mapping: PASS -> draft PASS; FAIL -> draft FAIL; BLOCKED/FATAL/transport/operator-interrupted/unknown -> no draft BEO success projection.
5. Required source-bound fields and canonical hashes.
6. Handoff to a later explicit publication-authority sprint, not Sprint 015.

**Step 4: Run GREEN and shared gate**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint015_draft_beo_publication_gate_review_is_draft_only
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add docs/reviews/BLK-SYSTEM-015_draft-beo-publication-gate-review.md python/test_active_doctrine_review_gates.py
git diff --cached --name-only
git commit -m "docs: define blk-system sprint 015 draft beo boundary"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-015_task-001-outcome.md`.

---

## 8. Task 2 — Source-bound live-smoke evidence to draft BEO projector

**Objective:** Add a deterministic local projector that converts source-bound BLK-020 PASS/FAIL first-smoke evidence into draft BEO fixture objects only.

**Files:**

- Modify: `python/beo_fixture_projection.py`
- Modify: `python/test_beo_fixture_projection.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-015_task-002-outcome.md`

**Step 1: Write failing tests**

Import the new function:

```python
from beo_fixture_projection import project_live_smoke_evidence_to_draft_beo
```

Add tests for:

- PASS evidence projects to a BEO fixture with `status == "PASS"`, source `blk-test-mcp-first-live-smoke`, `beo_publication == "DRAFT_ONLY"`, and `rtm_status == "NOT_GENERATED"`.
- FAIL evidence projects to a failed draft BEO and does not upgrade to success.
- Required source-bound fields are enforced: `beb_id`, `commit_hash`, `pre_engine_hash`, `trace_artifacts`, `checks`, `approval_record_hash`, `authorization_request_hash`, `source_evidence_hash`, `transcript_hash`, `run_id`, `tool_name`, `cleanup_status`.
- Required hashes must match `sha256:<64-lowercase-hex>`.
- `trace_artifacts[*].version_hash` must remain canonical.
- The function does not read protected active-vault paths.

Core test shape:

```python
def test_live_smoke_pass_projects_to_draft_beo_only(self):
    evidence = self._live_smoke_evidence(status="PASS")
    beo = project_live_smoke_evidence_to_draft_beo(evidence, beo_id="BEO_S15_DRAFT_001")

    self.assertEqual(beo["beo_id"], "BEO_S15_DRAFT_001")
    self.assertEqual(beo["beb_id"], evidence["beb_id"])
    self.assertEqual(beo["status"], "PASS")
    self.assertEqual(beo["source"], "blk-test-mcp-first-live-smoke")
    self.assertEqual(beo["commit_hash"], evidence["commit_hash"])
    self.assertEqual(beo["pre_engine_hash"], evidence["pre_engine_hash"])
    self.assertEqual(beo["trace_artifacts"], evidence["trace_artifacts"])
    self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
    self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
    self.assertEqual(beo["live_smoke_replay"]["run_id"], evidence["run_id"])
    self.assertEqual(beo["live_smoke_replay"]["transcript_hash"], evidence["transcript_hash"])
    self.assertNotIn("published_at", beo)
    self.assertNotIn("approved_by", beo)
    self.assertNotIn("signature", beo)
    self.assertNotIn("rtm", beo)
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_beo_fixture_projection.BeoFixtureProjectionTest
```

Expected: FAIL because `project_live_smoke_evidence_to_draft_beo` does not exist yet.

**Step 3: Implement minimal projector**

Add constants:

```python
_LIVE_SMOKE_SOURCE = "blk-test-mcp-first-live-smoke"
_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
_PUBLICATION_AUTHORITY_FIELDS = {
    "published_at",
    "approved_by",
    "signature",
    "signer",
    "storage_uri",
    "ledger_id",
    "rollback_plan",
    "publication_authority",
}
_RTM_AUTHORITY_FIELDS = {
    "rtm",
    "rtm_id",
    "requirements",
    "coverage_matrix",
    "coverage_status",
    "drift",
    "drift_decision",
}
```

Add public API:

```python
def project_live_smoke_evidence_to_draft_beo(
    live_smoke_evidence: dict[str, Any],
    *,
    beo_id: str,
) -> dict[str, Any]:
    """Project source-bound first-smoke PASS/FAIL evidence into a draft BEO fixture only."""
```

Implementation requirements:

- Require `source == "blk-test-mcp-first-live-smoke"`.
- Require `sprint == "BLK-SYSTEM-014"` or explicit BLK-020 evidence marker.
- Require `status` in `{"PASS", "FAIL"}` only.
- Require non-empty `checks` list and count PASS/FAIL checks via existing `_test_summary` logic.
- Require canonical hashes for `approval_record_hash`, `authorization_request_hash`, `source_evidence_hash`, and `transcript_hash`.
- Require `cleanup_status == "CLEANED"` for PASS; FAIL may carry deterministic cleanup evidence but still must not publish.
- Reject any publication authority or RTM authority fields in input.
- Return a draft-only BEO fixture with:
  - `beo_publication: "DRAFT_ONLY"`
  - `rtm_status: "NOT_GENERATED"`
  - `live_smoke_replay` containing bounded replay hashes and `run_id`/`tool_name`
  - no signer/storage/rollback/ledger fields.

**Step 4: Run GREEN and focused gates**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_beo_fixture_projection.BeoFixtureProjectionTest
python -m py_compile python/beo_fixture_projection.py
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add python/beo_fixture_projection.py python/test_beo_fixture_projection.py
git diff --cached --name-only
git commit -m "feat: project live smoke evidence to draft beo fixtures"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-015_task-002-outcome.md`.

---

## 9. Task 3 — Publication, BLOCKED, RTM, and active-vault negative gates

**Objective:** Harden the projector against authority creep and unsafe status projection.

**Files:**

- Modify: `python/beo_fixture_projection.py`
- Modify: `python/test_beo_fixture_projection.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-015_task-003-outcome.md`

**Step 1: Write failing tests**

Add table-driven tests for:

- `BLOCKED`, `FATAL_TIMEOUT`, `FATAL_OUTPUT_FLOOD`, `TRANSPORT_ERROR`, `OPERATOR_INTERRUPTED`, `UNKNOWN`, and empty status all reject with no BEO output.
- Input containing `beo_publication: "PUBLISHED"`, `published_at`, `approved_by`, `signature`, `signer`, `storage_uri`, `ledger_id`, `rollback_plan`, or `publication_authority` rejects.
- Input containing `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, `coverage_status`, `drift`, or `drift_decision` rejects.
- Source scans prove no live smoke rerun or transport is reachable from the BEO projector.

Example test:

```python
def test_live_smoke_blocked_and_fatal_statuses_do_not_project_to_success(self):
    for status in [
        "BLOCKED",
        "FATAL_TIMEOUT",
        "FATAL_OUTPUT_FLOOD",
        "TRANSPORT_ERROR",
        "OPERATOR_INTERRUPTED",
        "UNKNOWN",
        "",
    ]:
        with self.subTest(status=status):
            evidence = self._live_smoke_evidence(status=status, checks=[])
            with self.assertRaisesRegex(ValueError, "PASS/FAIL"):
                project_live_smoke_evidence_to_draft_beo(evidence, beo_id="BEO_S15_DRAFT_001")
```

Source-scan gate shape:

```python
def test_beo_projector_does_not_import_or_call_live_smoke_runner(self):
    source = (self.root / "python" / "beo_fixture_projection.py").read_text()
    forbidden = [
        "run_sprint014_first_live_smoke",
        "subprocess.Popen",
        "socket",
        "http.server",
        "requests",
        "urllib",
        "tools/call",
        "--sprint014-stdio-child",
    ]
    violations = [marker for marker in forbidden if marker in source]
    self.assertEqual(violations, [])
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_beo_fixture_projection.BeoFixtureProjectionTest
```

Expected: FAIL until negative gates are implemented.

**Step 3: Implement hardening**

Implementation requirements:

- Check for forbidden publication/RTM fields before normalizing output.
- Keep status validation fail-closed.
- Keep all output fields deterministic and bounded.
- Use only local dictionary validation and existing helper functions; do not import Sprint 014 live-smoke runner.
- Do not read files except tests reading source for scan gates.

**Step 4: Run GREEN and gates**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_beo_fixture_projection
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_beo_rtm_interface_fixtures
python -m py_compile python/beo_fixture_projection.py
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add python/beo_fixture_projection.py python/test_beo_fixture_projection.py
git diff --cached --name-only
git commit -m "test: harden draft beo publication gates"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-015_task-003-outcome.md`.

---

## 10. Task 4 — Active BLK-021 draft BEO doctrine and cross-reference gates

**Objective:** Publish Sprint 015 draft-only BEO gate doctrine without granting authoritative BEO publication or RTM authority.

**Files:**

- Create: `docs/BLK-021_beo-draft-publication-gate-review.md`
- Modify: `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- Modify: `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-015_task-004-outcome.md`

**Step 1: Write failing doctrine gates**

Add constant:

```python
BLK021 = ROOT / "docs" / "BLK-021_beo-draft-publication-gate-review.md"
```

Add test:

```python
def test_blk021_records_sprint015_draft_beo_gate_without_publication_authority(self):
    self.assertTrue(BLK021.exists(), "BLK-021 draft BEO gate doctrine missing")
    text = BLK021.read_text()
    required = [
        "**Status:** Active draft-only BEO gate review contract",
        "BLK-SYSTEM-015",
        "Draft BEO publication gate review",
        "BLK-020 first-smoke evidence",
        "source-bound and replayable",
        "beo_publication: \"DRAFT_ONLY\"",
        "rtm_status: \"NOT_GENERATED\"",
        "PASS/FAIL evidence may project only to draft BEO fixtures",
        "BLOCKED evidence must not project to success",
        "does not authorize authoritative BEO publication",
        "does not mutate public outcome ledgers",
        "does not grant signer/storage/rollback authority",
        "does not authorize RTM generation",
        "does not claim RTM coverage",
        "does not read protected BLK-req vault bodies",
        "does not rerun BLK-SYSTEM-014 first live smoke",
        "python/beo_fixture_projection.py",
        "python/test_beo_fixture_projection.py",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-021 markers missing: {missing}")
```

Add cross-reference test:

```python
def test_blk016_020_021_cross_reference_draft_beo_without_publication_authority(self):
    expectations = {
        BLK016: ["BLK-021", "DRAFT_ONLY", "does not authorize authoritative BEO publication"],
        BLK020: ["BLK-021", "Draft BEO publication gate review", "does not authorize authoritative BEO publication"],
        BLK021: ["BLK-016", "BLK-020", "BLK-SYSTEM-015"],
    }
    for path, markers in expectations.items():
        text = path.read_text()
        missing = [marker for marker in markers if marker not in text]
        self.assertEqual(missing, [], f"{path.relative_to(ROOT)} missing {missing}")
```

**Step 2: Run RED**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
```

Expected: FAIL because BLK-021 and cross-references are missing.

**Step 3: Create BLK-021 and patch cross-references narrowly**

BLK-021 required sections:

1. Purpose.
2. Draft-only BEO gate boundary.
3. Accepted source evidence: BLK-020 first-smoke PASS/FAIL evidence only.
4. Projection status matrix.
5. Required replay/source fields and canonical hashes.
6. Publication non-authority checklist.
7. RTM non-generation and active-vault exclusion.
8. Implementation and tests.
9. Stop conditions.
10. Handoff to a later explicit authoritative BEO publication sprint, if ever approved.

Patch BLK-016 and BLK-020 only to say:

- BLK-021 records the Sprint 015 draft-only BEO gate review.
- Draft BEO fixture projection remains `DRAFT_ONLY`.
- BLK-021 does not authorize authoritative BEO publication, signer/storage/rollback authority, public ledger mutation, RTM generation, RTM coverage, active-vault body reads, or live-smoke reruns.

**Step 4: Run GREEN and gates**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
git diff --check
```

Expected: PASS.

**Step 5: Commit/push/outcome**

```bash
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git add docs/BLK-021_beo-draft-publication-gate-review.md docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md python/test_active_doctrine_review_gates.py
git diff --cached --name-only
git commit -m "docs: define draft beo publication gate contract"
git push
```

Then create, validate, commit, and push `docs/outcomes/BLK-SYSTEM-015_task-004-outcome.md`.

---

## 11. Task 5 — Full-suite verification and closeout

**Objective:** Close BLK-SYSTEM-015 with full verification evidence and a narrow handoff seed for a later explicit publication or RTM sprint.

**Files:**

- Create: `docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md`
- Optionally modify: `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` only if a RED gate proves stale post-Sprint-015 wording; otherwise preserve history.

**Step 1: Full verification**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git status --short --branch
```

Expected:

- Python `unittest` suite passes.
- Python pytest suite passes with cache provider disabled.
- `go test ./...` passes.
- `go vet ./...` passes.
- `git diff --check` passes.
- No `python/__pycache__` or pytest cache remains staged/untracked.

**Step 2: Create closeout doc**

`docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md` must include:

- sprint ID and timestamp;
- task commit table;
- outcome doc table;
- exact verification commands and results;
- explicit statement that Sprint 015 did not rerun BLK-SYSTEM-014 first live smoke;
- explicit statement that Sprint 015 projects source-bound PASS/FAIL first-smoke evidence only into draft BEO fixtures;
- explicit statement that Sprint 015 does not authorize authoritative BEO publication, public outcome ledger mutation, signer/storage/rollback authority, RTM generation, RTM coverage claims, active BLK-req vault body reads, live MCP startup, arbitrary shell, real target execution, source mutation, production sandbox claims, or host-secret isolation claims;
- evidence that BLOCKED/FATAL/transport/operator-interrupted/unknown statuses cannot project to success;
- handoff seed:

```text
Later explicit BEO publication sprint — authoritative BEO publication authority, signer/storage/rollback design, and public ledger mutation remain unapproved until a separate human-approved sprint.
Later RTM sprint — offline RTM generation and drift rejection remain separate from BLK-test MCP and draft BEO projection.
```

**Step 3: Validate closeout**

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-015',
    'Draft BEO publication gate review',
    'did not rerun BLK-SYSTEM-014 first live smoke',
    'beo_publication: "DRAFT_ONLY"',
    'rtm_status: "NOT_GENERATED"',
    'does not authorize authoritative BEO publication',
    'does not mutate public outcome ledgers',
    'does not grant signer/storage/rollback authority',
    'does not authorize RTM generation',
    'does not claim RTM coverage',
    'does not read protected BLK-req vault bodies',
    'BLOCKED',
    'Later explicit BEO publication sprint',
    'Later RTM sprint',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing closeout markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-015 closeout markers: PASS')
PY
```

Expected: PASS.

**Step 4: Commit/push closeout**

```bash
git add docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system sprint 015"
git push
```

Then send concise Discord summary with:

```text
MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md
```

---

## 12. Final acceptance criteria

BLK-SYSTEM-015 is complete only when all are true:

- `docs/plans/blk-system-015_draft-beo-publication-gate-review.md` is committed.
- `docs/reviews/BLK-SYSTEM-015_draft-beo-publication-gate-review.md` exists and passes the active doctrine gate.
- `python/beo_fixture_projection.py` contains a deterministic local projector for BLK-020 source-bound live-smoke PASS/FAIL evidence to draft BEO fixture objects.
- `python/test_beo_fixture_projection.py` proves:
  - PASS evidence projects only to draft PASS BEO;
  - FAIL evidence projects only to draft FAIL BEO;
  - BLOCKED/FATAL/transport/operator-interrupted/unknown evidence does not project to success;
  - canonical replay/source hashes are required;
  - canonical trace artifacts are required;
  - publication, signer, storage, rollback, ledger, RTM, coverage, and drift fields are rejected;
  - protected BLK-req vault bodies are not read;
  - the projector does not import/call live-smoke runner or transport code.
- `docs/BLK-021_beo-draft-publication-gate-review.md` exists as active draft-only BEO gate doctrine.
- BLK-016 and BLK-020 cross-reference BLK-021 without implying authoritative BEO publication, RTM generation, or live-smoke rerun authority.
- Every task has a matching pushed `docs/outcomes/BLK-SYSTEM-015_task-00N-outcome.md`.
- Sprint closeout is pushed.
- Final verification passes:
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'`
  - `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python`
  - `go test ./...`
  - `go vet ./...`
  - `git diff --check`
- Final worktree is clean except any deliberate, reported, user-approved untracked files.

---

## 13. Expected artifact set

```text
docs/plans/blk-system-015_draft-beo-publication-gate-review.md
docs/reviews/BLK-SYSTEM-015_draft-beo-publication-gate-review.md
python/beo_fixture_projection.py
python/test_beo_fixture_projection.py
python/test_active_doctrine_review_gates.py
docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md
docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md
docs/BLK-021_beo-draft-publication-gate-review.md
docs/outcomes/BLK-SYSTEM-015_task-000-outcome.md
docs/outcomes/BLK-SYSTEM-015_task-001-outcome.md
docs/outcomes/BLK-SYSTEM-015_task-002-outcome.md
docs/outcomes/BLK-SYSTEM-015_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-015_task-004-outcome.md
docs/outcomes/BLK-SYSTEM-015_sprint-closeout.md
```

---

## 14. Executor notes

- Do not stage with `git add .`, `git add -A`, or broad wildcards.
- Remove `python/__pycache__`, `python/.pytest_cache`, and `.pytest_cache` before status/commit.
- Do not rerun `BLK-SYSTEM-014-SMOKE-001`; Sprint 015 consumes recorded/replayable evidence shape only.
- Do not import `run_sprint014_first_live_smoke` from `beo_fixture_projection.py`.
- Do not add authoritative BEO publication fields to any output.
- Do not make outcome docs self-referential with their own final commit hash. Record pre-commit verification in the doc; record post-push hash/status in executor summary or sprint closeout.
- If a required source-bound hash or trace artifact is absent or malformed, fail closed; do not synthesize authority.
- Keep Discord updates concise and only after meaningful task completion/push events.
