# BLK-SYSTEM-016 — Authoritative BEO Publication Design Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `writing-plans`, and strict TDD to implement this plan task-by-task. If delegating implementation work to Codex CLI, use model `gpt-5.4` and run a hostile audit after every execution packet before accepting changes. Any Codex/Hermes delegation is project-maintenance support only; it must not become BLK-test MCP, BEO publication evidence, approval evidence, public-ledger evidence, signer evidence, storage evidence, rollback evidence, or RTM evidence.

**Goal:** Define and mechanically guard the future authoritative BEO publication authority envelope without actually publishing BEOs, mutating public ledgers, adding signer/storage/rollback authority, or generating RTM.

**Architecture:** Sprint 016 is a design-and-gate sprint only. It promotes the Sprint 015 handoff into a review artifact plus an active non-executing doctrine contract for a future publication-authority sprint, while preserving every existing runtime BEO output as `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`. The safe implementation surface is Markdown doctrine/review/outcome docs and persistent static/import tests proving no publisher, signer, ledger writer, storage writer, rollback executor, live BLK-test rerun, RTM generator, or protected active-vault body read was introduced.

**Tech Stack:** Python standard library only (`unittest`, `pathlib`, `re`, optional `ast`), existing BEO projection modules/tests, active doctrine review gates, Markdown doctrine/review/outcome docs, Go verification gates.

---

## 0. Live preflight facts

Captured before writing this plan:

```text
Date: Thu May  7 08:10:33 AM AEST 2026
Repository: /home/dad/BLK-System
Branch/status: ## main...origin/main
HEAD: 4b9b72e docs: close out blk-system sprint 015
Plan file: docs/plans/blk-system-016_authoritative-beo-publication-design.md
```

Sprint ID ownership check:

- `BLK-SYSTEM-016` is not currently used as a system sprint plan/outcome ID.
- Existing `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md` is active BLK doctrine for Sprint 007 disabled adapter fixtures. It is not the Sprint 016 plan and must not be renamed or repurposed.
- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md` names `BLK-SYSTEM-016` as `BEO publication design, not implementation` for GAP-009.
- Sprint 015 closeout hands off: `Later explicit BEO publication sprint — authoritative BEO publication authority, signer/storage/rollback design, and public ledger mutation remain unapproved until a separate human-approved sprint.`
- `docs/BLK-021_beo-draft-publication-gate-review.md` is active draft-only doctrine and explicitly says any future authoritative BEO publication sprint requires separate human approval, signer/storage/rollback design, public ledger mutation rules, and rollback evidence.

---

## 1. BLK-001 domain matrix

| Domain/component | Sprint 016 relationship | Authority statement |
| --- | --- | --- |
| `blk-req` | Supplies opaque trace identifiers already embedded in draft BEO evidence. | Sprint 016 does not read protected BLK-req vault bodies, parse active requirement text, promote requirements, or create RTM coverage claims. |
| `blk-id` | Designs future identity/provenance fields for publication authorization, signer identity, BEO hash, source evidence hash, operator identity, storage target identity, and rollback event identity. | Identity records are design-only; they do not grant publication, signing, storage, rollback, ledger, RTM, or approval authority in Sprint 016. |
| `blk-relay` | May be referenced as the future carrier of human publication approval messages. | Sprint 016 does not implement relay messages, start listeners, call Discord APIs, or accept live approval tokens. |
| Architecture & Feature Planning / HITL | Owns design review and future human approval prerequisites for publication. | Sprint 016 may define prerequisites, but it does not approve publication and does not publish any BEO. |
| `blk-pipe` | Source evidence remains immutable source-bound input inherited by draft BEOs. | Sprint 016 does not mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test/BEO behavior. |
| `blk-test` | Existing PASS/FAIL evidence remains physical verification input for draft BEO fixtures. | Sprint 016 does not start live BLK-test MCP, rerun BLK-SYSTEM-014 first smoke, broaden tools, run real target repositories, or convert BLOCKED/FATAL/transport evidence into success. |
| BEO/outcomes | Designs the future boundary between draft BEO fixtures and authoritative publication. | No authoritative BEO publication, public outcome ledger mutation, signer, storage write, rollback executor, release authority, or `PUBLISHED` runtime output is implemented. |
| `blk-link` / RTM | Receives future handoff constraints for after publication authority is separately approved. | Sprint 016 does not generate RTM, make drift decisions, claim coverage, compare active-vault hashes, or read active-vault bodies. |
| Cryptographic `version_hash` baton | Requires future publication design to preserve canonical trace hashes and BEO/source evidence hashes. | Hashes remain opaque evidence identifiers only; Sprint 016 does not verify protected requirement bodies. |

---

## 2. Scope boundary

### Allowed scope

- Preserve a Sprint 016 boundary review artifact in `docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md`.
- Add persistent tests proving the review artifact exists and uses the exact design-only/non-authority language.
- Add an active non-executing doctrine contract, expected path `docs/BLK-022_authoritative-beo-publication-design-boundary.md`, only if tests prove active doctrine is required to prevent Sprint 015 draft-only projection from being mistaken as publication authority.
- Define future publication-authority prerequisites at design level only:
  - explicit human publication approval separate from BLK-test MCP approval and separate from `codex-live` approval;
  - source-bound draft BEO identity/hash;
  - source BLK-pipe evidence identity/hash;
  - BLK-020/021 evidence lineage;
  - operator/signer identity policy;
  - storage target policy;
  - public ledger mutation schema;
  - rollback and revocation policy;
  - failure/status vocabulary that preserves PASS as PASS, FAIL as FAIL, and rejects BLOCKED/FATAL/transport/interrupted/unknown as success;
  - RTM handoff boundary that remains later/offline and outside Sprint 016.
- Add static/import tests proving existing runtime projectors still output `DRAFT_ONLY`/`NOT_GENERATED` and reject publication/RTM authority fields.
- Patch narrow cross-references in `docs/BLK-021_beo-draft-publication-gate-review.md` and, only if necessary, `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md` to point to the Sprint 016 design boundary without implying implementation authority.
- Produce matching outcome docs after every task and a sprint closeout.

### Hard blocks / stop conditions

Stop and escalate if any implementation attempts to:

- add a runtime BEO publisher, public ledger writer, signer, storage writer, rollback executor, release publisher, or publication daemon;
- emit runtime `beo_publication: "PUBLISHED"` from production BEO projection code;
- mutate public outcome ledgers or write publication records outside Markdown review/doctrine/outcome docs;
- accept live approval tokens, use `codex-live` as BEO publication approval, call Discord APIs, or implement relay transport;
- generate RTM, emit coverage matrices, make drift decisions, compare active-vault hashes, or claim coverage;
- read protected BLK-req vault bodies under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- rerun BLK-SYSTEM-014 first live smoke, start live BLK-test MCP, start MCP server/client transport, use arbitrary shell as BLK-test behavior, or run against real target repositories;
- mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test/BEO behavior;
- claim production sandbox/container/cgroup/VM/seccomp/AppArmor/SELinux or host-secret isolation enforcement;
- leak host secrets, active-vault body text, approval secrets, signer secrets, storage credentials, or unbounded logs.

---

## 3. Decision register

| ID | Decision | Rationale | Mechanical gate |
| --- | --- | --- | --- |
| S16-BEO-001 | Sprint 016 is design-only. | Sprint 015 preserved draft-only projection and explicitly handed off publication as later work. | Active tests require `design only`, `does not authorize authoritative BEO publication`, and no runtime `PUBLISHED` output. |
| S16-BEO-002 | Authoritative publication requires a separate future human-approved sprint after Sprint 016. | Publication changes public truth and must not be inherited from BLK-test PASS or Codex/Hermes execution support. | Doctrine/review tests require separate human approval, signer/storage/rollback design, and public ledger mutation rules. |
| S16-BEO-003 | `codex-live` and BLK-test MCP approvals are insufficient for BEO publication. | Execution approval and publication approval are different HITL acts. | Static tests require rejection wording: `codex-live approval is not BEO publication approval` and `BLK-test MCP approval is not BEO publication approval`. |
| S16-BEO-004 | PASS/FAIL draft BEOs may be future publication candidates; neither can be mutated into a different status. | Outcomes should record physical reality, not launder failures or infrastructure states. | Status matrix requires PASS stays PASS, FAIL stays FAIL, and BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success. |
| S16-BEO-005 | RTM remains later/offline and separate. | BLK-link owns trace ledger/drift work; BEO publication does not equal RTM coverage. | Tests reject `rtm`, `rtm_id`, `requirements`, `coverage_matrix`, `coverage_status`, `drift`, and `drift_decision` in Sprint 016 authority. |
| S16-BEO-006 | Active-vault body reads remain prohibited. | Publication design should preserve opaque trace hashes; active-vault access policy belongs to later BLK-link/RTM work. | Review/doctrine tests require protected-body exclusion and no active-vault reads. |
| S16-BEO-007 | Active doctrine number is `BLK-022` if a doctrine doc is added. | `BLK-016` and `BLK-021` already have active meanings. | Test path and cross-reference markers point to `docs/BLK-022_authoritative-beo-publication-design-boundary.md`. |

---

## 4. Controller workflow for execution

1. Create an implementation branch, for example `sprint/blk-system-016`.
2. Commit this plan first if it is still uncommitted.
3. For every task below:
   1. Write/patch the failing test first.
   2. Run the focused RED command and confirm expected failure.
   3. Implement the smallest doc/test change.
   4. Run focused GREEN verification.
   5. Run task shared gates.
   6. Remove Python/pytest caches.
   7. Stage exact paths only.
   8. Verify `git diff --cached --name-only` contains only expected files.
   9. Commit the implementation/doc change.
   10. Push the implementation/doc commit to GitHub.
   11. Create `docs/outcomes/BLK-SYSTEM-016_task-00N-outcome.md` with RED/GREEN and pre-commit verification evidence.
   12. Commit and push the outcome doc separately.
   13. Send concise Discord summary with `MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-016_task-00N-outcome.md` after push.
4. Close the sprint with `docs/outcomes/BLK-SYSTEM-016_sprint-closeout.md`, committed and pushed separately.

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

## 5. Task 0 — Commit the plan before implementation

**Objective:** Make this reviewed plan durable before implementation starts.

**Files:**

- Add: `docs/plans/blk-system-016_authoritative-beo-publication-design.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-016_task-000-outcome.md`

**Step 1: Verify plan markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/plans/blk-system-016_authoritative-beo-publication-design.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-016',
    'Authoritative BEO Publication Design',
    'design-only',
    'does not authorize authoritative BEO publication',
    'does not generate RTM',
    'codex-live approval is not BEO publication approval',
    'docs/BLK-022_authoritative-beo-publication-design-boundary.md',
    'beo_publication: "DRAFT_ONLY"',
    'rtm_status: "NOT_GENERATED"',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing plan markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-016 plan markers: PASS')
PY
```

Expected: `BLK-SYSTEM-016 plan markers: PASS`.

**Step 2: Stage exact path and commit**

Run:

```bash
git add docs/plans/blk-system-016_authoritative-beo-publication-design.md
git diff --cached --name-only
git commit -m "docs: plan blk-system sprint 016 beo publication design"
git push
```

Expected staged path only:

```text
docs/plans/blk-system-016_authoritative-beo-publication-design.md
```

**Step 3: Outcome doc**

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-016_task-000-outcome.md`.

---

## 6. Task 1 — Preserve Sprint 016 design review artifact

**Objective:** Add the Sprint 016 review artifact and a persistent gate proving the design boundary is explicit and non-authorizing.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Add: `docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-016_task-001-outcome.md`

**Step 1: Write failing test**

Add constants near the Sprint 015 constants:

```python
SPRINT016_BEO_PUBLICATION_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-016_authoritative-beo-publication-design-review.md"
```

Add a focused test:

```python
def test_sprint016_beo_publication_design_review_preserves_non_authority(self):
    self.assertTrue(SPRINT016_BEO_PUBLICATION_REVIEW.exists(), "Sprint 016 BEO publication design review missing")
    text = SPRINT016_BEO_PUBLICATION_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-016",
        "BEO publication design, not implementation",
        "design only",
        "does not authorize authoritative BEO publication",
        "does not mutate public outcome ledgers",
        "does not grant signer/storage/rollback authority",
        "codex-live approval is not BEO publication approval",
        "BLK-test MCP approval is not BEO publication approval",
        "public ledger mutation rules remain future authority",
        "RTM generation remains disabled",
        "does not read protected BLK-req vault bodies",
        "PASS stays PASS",
        "FAIL stays FAIL",
        "BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 016 BEO publication review markers missing: {missing}")
```

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint016_beo_publication_design_review_preserves_non_authority
```

Expected: FAIL because the review artifact is missing.

**Step 2: Add review artifact**

Create `docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md` with these sections:

- source documents reviewed: BLK-001, BLK-014, BLK-016, BLK-020, BLK-021, Sprint 010 gap/slicing, Sprint 015 review/closeout;
- positive design scope;
- exact non-authority markers;
- future publication authority prerequisites;
- approval separation (`codex-live` and BLK-test MCP approval are insufficient);
- status matrix;
- signer/storage/rollback/public-ledger design checklist;
- RTM and active-vault exclusion;
- handoff to future publication implementation sprint and later RTM sprint.

**Step 3: Run GREEN**

Run the focused test again. Expected: PASS.

**Step 4: Shared gates**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint016_beo_publication_design_review_preserves_non_authority
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git diff --check
git status --short --branch
```

**Step 5: Commit/push and outcome**

Stage exact paths only:

```bash
git add python/test_active_doctrine_review_gates.py docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md
git diff --cached --name-only
git commit -m "docs: define blk-system sprint 016 beo publication design review"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-016_task-001-outcome.md`.

---

## 7. Task 2 — Add active non-executing BLK-022 publication boundary

**Objective:** Make the design boundary active doctrine without implementing a publisher.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Add: `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-016_task-002-outcome.md`

**Step 1: Write failing test**

Add constant:

```python
BLK022 = ROOT / "docs" / "BLK-022_authoritative-beo-publication-design-boundary.md"
```

Add focused test:

```python
def test_blk022_records_design_only_authoritative_beo_publication_boundary(self):
    self.assertTrue(BLK022.exists(), "BLK-022 BEO publication design boundary missing")
    text = BLK022.read_text()
    required = [
        "**Status:** Active design-only boundary contract",
        "BLK-SYSTEM-016",
        "does not authorize authoritative BEO publication",
        "does not implement BEO publication",
        "does not mutate public outcome ledgers",
        "does not grant signer/storage/rollback authority",
        "does not emit runtime PUBLISHED BEOs",
        "beo_publication: \"DRAFT_ONLY\" remains the only current runtime output",
        "rtm_status: \"NOT_GENERATED\" remains mandatory",
        "codex-live approval is not BEO publication approval",
        "BLK-test MCP approval is not BEO publication approval",
        "PASS stays PASS",
        "FAIL stays FAIL",
        "BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success",
        "protected BLK-req vault bodies remain unread",
        "Later RTM sprint",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-022 boundary markers missing: {missing}")
```

Run focused test. Expected: FAIL because BLK-022 does not exist.

**Step 2: Add BLK-022 active doctrine**

Create `docs/BLK-022_authoritative-beo-publication-design-boundary.md` with:

- purpose and status as active design-only boundary;
- current runtime boundary: all existing projectors remain draft-only;
- future publication authorization envelope;
- future publication candidate schema fields at prose level only;
- explicit approval separation;
- status matrix;
- signer/storage/rollback/public-ledger checklist;
- RTM exclusion and active-vault body exclusion;
- implementation/testing mapping pointing to static gates, not publisher code;
- stop conditions.

Do not add a runtime function, storage adapter, signer, ledger writer, or `PUBLISHED` BEO output.

**Step 3: Run GREEN and shared gates**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk022_records_design_only_authoritative_beo_publication_boundary
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint016_beo_publication_design_review_preserves_non_authority
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git diff --check
```

Expected: PASS.

**Step 4: Commit/push and outcome**

```bash
git add python/test_active_doctrine_review_gates.py docs/BLK-022_authoritative-beo-publication-design-boundary.md
git diff --cached --name-only
git commit -m "docs: add blk-022 beo publication design boundary"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-016_task-002-outcome.md`.

---

## 8. Task 3 — Add runtime non-publication guard tests

**Objective:** Prove Sprint 016 did not accidentally introduce publication, RTM, active-vault, or live-MCP behavior.

**Files:**

- Create: `python/test_beo_publication_design_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-016_task-003-outcome.md`

**Step 1: Write tests**

Create tests that import existing projectors and scan production Python files. Suggested assertions:

```python
from pathlib import Path
import unittest

from beo_fixture_projection import project_live_smoke_evidence_to_draft_beo

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "python"

class BeoPublicationDesignGateTest(unittest.TestCase):
    def _live_smoke_evidence(self, **overrides):
        evidence = {
            "sprint": "BLK-SYSTEM-014",
            "source": "blk-test-mcp-first-live-smoke",
            "run_id": "BLK-SYSTEM-014-SMOKE-001",
            "tool_name": "run_ast_validation",
            "status": "PASS",
            "beb_id": "BEB_S14_SYNTHETIC_SMOKE",
            "commit_hash": "synthetic-fixture-no-git-commit",
            "pre_engine_hash": "sha256:" + "3" * 64,
            "test_profile": "bounded-live-smoke-short",
            "trace_artifacts": [{"kind": "REQ", "id": "REQ-S14-SMOKE-001", "version_hash": "sha256:" + "1" * 64}],
            "checks": [{"name": "run_ast_validation", "status": "PASS", "summary": "AST validation passed"}],
            "approval_record_hash": "sha256:" + "4" * 64,
            "authorization_request_hash": "sha256:" + "5" * 64,
            "source_evidence_hash": "sha256:" + "6" * 64,
            "transcript_hash": "sha256:" + "7" * 64,
            "cleanup_status": "CLEANED",
            "beo_publication": "DRAFT_ONLY",
            "rtm_status": "NOT_GENERATED",
            "active_vault_read": False,
        }
        evidence.update(overrides)
        return evidence

    def test_existing_live_smoke_projection_remains_draft_only(self):
        beo = project_live_smoke_evidence_to_draft_beo(self._live_smoke_evidence(), beo_id="BEO_S16_GUARD_001")
        self.assertEqual(beo["beo_publication"], "DRAFT_ONLY")
        self.assertEqual(beo["rtm_status"], "NOT_GENERATED")
        self.assertNotIn("published_at", beo)
        self.assertNotIn("signature", beo)
        self.assertNotIn("ledger_id", beo)
        self.assertNotIn("rollback_authority", beo)

    def test_published_runtime_input_still_rejects(self):
        with self.assertRaisesRegex(ValueError, "DRAFT_ONLY"):
            project_live_smoke_evidence_to_draft_beo(
                self._live_smoke_evidence(beo_publication="PUBLISHED"),
                beo_id="BEO_S16_GUARD_002",
            )

    def test_production_python_does_not_define_beo_publisher(self):
        forbidden = ["publish_authoritative_beo", "public outcome ledger writer", "beo_publication = \"PUBLISHED\""]
        offenders = []
        for path in PYTHON.glob("*.py"):
            if path.name.startswith("test_"):
                continue
            text = path.read_text()
            for marker in forbidden:
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual(offenders, [], f"Sprint 016 introduced runtime publisher markers: {offenders}")
```

Run focused test. Expected: PASS once test is created, because Sprint 016 must not introduce runtime publisher code.

**Step 2: Shared gates**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_beo_publication_design_gates
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_beo_fixture_projection.py python/test_beo_publication_design_gates.py
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git diff --check
```

**Step 3: Commit/push and outcome**

```bash
git add python/test_beo_publication_design_gates.py
git diff --cached --name-only
git commit -m "test: guard beo publication design as non-runtime"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-016_task-003-outcome.md`.

---

## 9. Task 4 — Cross-reference Sprint 016 without broadening authority

**Objective:** Patch existing active docs so readers discover BLK-022 while retaining draft-only runtime boundaries.

**Files:**

- Modify: `docs/BLK-021_beo-draft-publication-gate-review.md`
- Modify only if needed: `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-016_task-004-outcome.md`

**Step 1: Write failing cross-reference test**

Add or extend a test to require:

```python
def test_blk021_hands_off_publication_design_to_blk022_without_authority(self):
    text = BLK021.read_text()
    required = [
        "BLK-022",
        "authoritative BEO publication design boundary",
        "does not authorize authoritative BEO publication",
        "beo_publication: \"DRAFT_ONLY\" remains mandatory",
        "rtm_status: \"NOT_GENERATED\" remains mandatory",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-021 to BLK-022 handoff markers missing: {missing}")
```

Run focused test. Expected: FAIL until BLK-021 is patched.

**Step 2: Patch docs narrowly**

Patch BLK-021 handoff with a short paragraph:

```text
BLK-022 records the BLK-SYSTEM-016 authoritative BEO publication design boundary. BLK-022 is design-only: it does not authorize authoritative BEO publication, does not implement BEO publication, does not mutate public outcome ledgers, does not grant signer/storage/rollback authority, and keeps `beo_publication: "DRAFT_ONLY"` plus `rtm_status: "NOT_GENERATED"` mandatory for current runtime outputs.
```

Patch BLK-016 only if a focused test or hostile review proves the old document is misleading after BLK-022 exists. If patched, repeat the same non-authority language and avoid implying Sprint 007 fixtures can publish.

**Step 3: Run GREEN and shared gates**

Run focused cross-reference test, then:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
git diff --check
```

**Step 4: Commit/push and outcome**

Stage exact paths only:

```bash
git add docs/BLK-021_beo-draft-publication-gate-review.md python/test_active_doctrine_review_gates.py
# Add docs/BLK-016... only if it was actually changed.
git diff --cached --name-only
git commit -m "docs: cross-reference blk-022 publication design boundary"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-016_task-004-outcome.md`.

---

## 10. Task 5 — Full verification and sprint closeout

**Objective:** Verify the full repository and record Sprint 016 closeout.

**Files:**

- Add: `docs/outcomes/BLK-SYSTEM-016_sprint-closeout.md`

**Step 1: Full verification**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
go test ./...
go vet ./...
rm -rf python/__pycache__ python/.pytest_cache .pytest_cache
find python -type d -name __pycache__ -prune -exec rm -rf {} +
git diff --check
git status --short --branch
```

Expected: all tests pass; status clean except closeout file before commit.

**Step 2: Create closeout**

Create `docs/outcomes/BLK-SYSTEM-016_sprint-closeout.md` with:

- status complete;
- task commit table;
- outcome document table;
- accepted design-only boundary;
- non-authority boundary;
- full verification evidence;
- handoff seed for a later explicit BEO publication implementation sprint;
- handoff seed for later RTM/offline ledger sprint.

Required closeout markers:

```text
BLK-SYSTEM-016 was design-only.
Sprint 016 does not authorize authoritative BEO publication.
Sprint 016 does not implement BEO publication.
Sprint 016 does not mutate public outcome ledgers.
Sprint 016 does not grant signer/storage/rollback authority.
Sprint 016 does not generate RTM.
Current runtime BEO outputs remain DRAFT_ONLY and NOT_GENERATED.
```

**Step 3: Commit/push closeout**

```bash
git add docs/outcomes/BLK-SYSTEM-016_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system sprint 016"
git push
```

---

## 11. Final acceptance criteria

Sprint 016 is complete only if:

- `docs/plans/blk-system-016_authoritative-beo-publication-design.md` was committed before implementation.
- `docs/reviews/BLK-SYSTEM-016_authoritative-beo-publication-design-review.md` exists and passes its persistent review gate.
- `docs/BLK-022_authoritative-beo-publication-design-boundary.md` exists and passes active doctrine gates.
- Existing runtime BEO projection remains draft-only: `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`.
- No runtime BEO publisher, public ledger writer, signer, storage writer, rollback executor, RTM generator, active-vault body reader, live BLK-test rerun, or approval relay implementation was introduced.
- `codex-live approval is not BEO publication approval` and `BLK-test MCP approval is not BEO publication approval` are both mechanically guarded.
- PASS stays PASS; FAIL stays FAIL; BLOCKED/FATAL/TRANSPORT/INTERRUPTED/unknown cannot publish success.
- `docs/BLK-021_beo-draft-publication-gate-review.md` hands off to BLK-022 without broadening authority.
- Every task has a committed and pushed outcome doc.
- Sprint closeout is committed and pushed.
- Final Python unittest, pytest, Go test, Go vet, `git diff --check`, and cache cleanup gates pass.

---

## 12. Execution handoff

Plan complete when committed. Ready execution pattern:

```text
Execute BLK-SYSTEM-016 using blk-system-sprint-execution. This is design-only and gate-only: do not implement runtime publication, signing, storage, rollback, ledger mutation, RTM generation, active-vault reads, live BLK-test reruns, or relay/approval transports. Commit/push after each task and after each matching outcome doc.
```
