# BLK-SYSTEM-017 — Offline RTM Ledger Design Implementation Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `writing-plans`, and strict TDD to implement this plan task-by-task. If delegating implementation work to Codex CLI, use model `gpt-5.4` and run a hostile audit after every execution packet before accepting changes. Any Codex/Hermes delegation is project-maintenance support only; it must not become BLK-test MCP, BEO publication evidence, RTM generation evidence, active-vault-read evidence, drift-rejection evidence, approval evidence, or public-ledger mutation evidence.

**Goal:** Define and mechanically guard the future offline `blk-link` RTM ledger and drift-rejection authority envelope without generating RTM, reading protected BLK-req bodies, publishing BEOs, or mutating public ledgers.

**Architecture:** Sprint 017 is a design-and-gate sprint only. It promotes the Sprint 010 GAP-010 / Later RTM handoff plus Sprint 016 BLK-022 handoff into a review artifact and active non-executing doctrine contract for a future offline RTM implementation sprint. The safe implementation surface is Markdown doctrine/review/outcome docs and persistent static/import tests proving current runtime outputs remain `rtm_status: "NOT_GENERATED"`, `rtm_authority: "DISABLED_INTERFACE_ONLY"`, draft-only BEO interfaces, and no active-vault body reads or drift decisions were introduced.

**Tech Stack:** Python standard library only (`unittest`, `pathlib`, optional `ast`), existing BEO/RTM interface fixtures, active doctrine review gates, Markdown doctrine/review/outcome docs, Go verification gates.

---

## 0. Live preflight facts

Captured before writing this plan:

```text
Date: 2026-05-07T12:44:28+10:00
Repository: /home/dad/BLK-System
Branch/status: ## main...origin/main
HEAD: baa3c80 docs: close out blk-system sprint 016
Plan file: docs/plans/blk-system-017_offline-rtm-ledger-design.md
```

Sprint ID ownership check:

- `BLK-SYSTEM-017` is named in `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md` as `RTM ledger design` for GAP-010.
- No existing `docs/plans/blk-system-017_*.md`, `docs/outcomes/BLK-SYSTEM-017_*.md`, or `docs/reviews/BLK-SYSTEM-017_*.md` existed at preflight.
- Existing `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md` is active BLK doctrine for the Sprint 011 disabled transport contract. It is not the Sprint 017 plan and must not be renamed or repurposed.
- Active doctrine number `BLK-023` is unused at preflight and is reserved by this plan for the Sprint 017 offline RTM ledger design boundary if an active doctrine doc is added.
- Sprint 016 closeout hands off a Later RTM sprint that remains separate from BEO publication and must define offline traceability, active-vault hash policy, coverage, drift rejection, and rollback interactions independently.
- `docs/BLK-022_authoritative-beo-publication-design-boundary.md` keeps BEO publication design separate from RTM and states that a Later RTM sprint remains separate.

---

## 1. BLK-001 domain matrix

| Domain/component | Sprint 017 relationship | Authority statement |
| --- | --- | --- |
| `blk-req` | Supplies future hash-only active-vault comparison policy for RTM design. | Sprint 017 does not read, parse, quote, summarize, compare body text, promote, or mutate protected BLK-req vault bodies. It may design hash-only policy using opaque `version_hash` identifiers. |
| `blk-id` | Designs future ledger artifact identity, RTM ID, BEO identity, trace-artifact identity, drift event identity, operator identity, and source-system identity. | Identity records are design-only; they do not grant RTM generation, active-vault read, drift rejection, publication, signer, storage, rollback, source mutation, or approval authority in Sprint 017. |
| `blk-relay` | May be referenced as a future carrier for human RTM/drift review messages. | Sprint 017 does not implement relay messages, start listeners, call Discord APIs, accept live approval tokens, or route RTM decisions. |
| Architecture & Feature Planning / HITL | Owns design review and future human approval prerequisites for RTM/drift authority. | Sprint 017 may define prerequisites, but it does not approve RTM generation and does not reject drift. |
| `blk-pipe` | Existing source evidence remains immutable input to later traceability. | Sprint 017 does not mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as RTM behavior. |
| `blk-test` | Existing PASS/FAIL/BLOCKED evidence remains physical verification input only. | Sprint 017 does not start live BLK-test MCP, rerun BLK-SYSTEM-014 first smoke, broaden tools, run real target repositories, or emit RTM fields from BLK-test. |
| BEO/outcomes | Draft-only BEO and disabled BEO/RTM interface fixtures are RTM design inputs. | Sprint 017 does not authorize authoritative BEO publication, does not mutate public outcome ledgers, does not add signer/storage/rollback authority, and does not treat BEO publication as RTM approval. |
| `blk-link` / RTM | Designs the future offline RTM ledger, coverage, and drift-rejection envelope. | Sprint 017 does not implement `generate_rtm.py`, does not generate ledgers, does not emit `rtm_id`, does not claim coverage, and does not make drift decisions. |
| Cryptographic `version_hash` baton | Defines future hash-only comparison constraints between BEO trace artifacts and active vault hashes. | Hashes remain opaque evidence identifiers only; Sprint 017 does not verify protected requirement bodies. |

---

## 2. Scope boundary

### Allowed scope

- Preserve a Sprint 017 boundary review artifact in `docs/reviews/BLK-SYSTEM-017_offline-rtm-ledger-design-review.md`.
- Add persistent tests proving the review artifact exists and uses exact offline/design-only/non-authority language.
- Add an active non-executing doctrine contract at `docs/BLK-023_offline-rtm-ledger-design-boundary.md` only if tests prove active doctrine is required to prevent RTM fixture fields from being mistaken as RTM generation authority.
- Define future RTM implementation prerequisites at design level only:
  - explicit future RTM generation approval separate from BLK-test MCP approval, BEO publication approval, `codex-live` approval, and Hermes/Codex sprint execution;
  - source-bound BEO/outcome identity and canonical BEO hash policy;
  - source BLK-pipe evidence identity and BLK-test evidence identity;
  - hash-only active BLK-req vault comparison policy;
  - RTM ledger identity/schema at prose level only;
  - coverage vocabulary and unknown/missing/stale/replayed hash rejection policy;
  - drift-rejection review and rollback/supersession interaction policy;
  - secret/protected-body exclusion and bounded replay-bundle policy.
- Add static/import tests proving existing runtime interfaces still output `rtm_status: "NOT_GENERATED"`, `rtm_authority: "DISABLED_INTERFACE_ONLY"`, `active_vault_read: False`, and `requirements_resolved: False`.
- Patch narrow cross-references in `docs/BLK-022_authoritative-beo-publication-design-boundary.md` and, only if necessary, `docs/BLK-008_blk-test-mcp-execution-server.md` or `docs/BLK-001_blk-system-master-architecture.md` to point to BLK-023 without implying implementation authority.
- Produce matching outcome docs after every task and a sprint closeout.

### Hard blocks / stop conditions

Stop and escalate if any implementation attempts to:

- implement `generate_rtm.py`, an RTM ledger writer, a coverage matrix generator, an active-vault hash scanner, or a drift-rejection runtime;
- emit runtime `rtm_status: "GENERATED"`, `rtm_id`, `rtm`, `requirements`, `coverage_matrix`, `coverage_status`, `drift`, `drift_decision`, or `drift_status` from production code;
- read, parse, quote, summarize, compare body text, or expose protected paths under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`;
- treat BEO publication approval, BLK-test MCP approval, `codex-live` approval, or BLK-test PASS as RTM generation approval;
- mutate public outcome ledgers, publish authoritative BEOs, add signer/storage/rollback runtime authority, or write publication records;
- start live BLK-test MCP, rerun BLK-SYSTEM-014 first live smoke, start MCP server/client transport, use arbitrary shell as BLK-test behavior, or run against real target repositories;
- mutate, stage, commit, push, reset, stash, checkout, revert, or autofix source as BLK-test/BEO/RTM behavior;
- claim production sandbox/container/cgroup/VM/seccomp/AppArmor/SELinux or host-secret isolation enforcement;
- leak host secrets, active-vault body text, approval secrets, signer secrets, storage credentials, or unbounded logs.

---

## 3. Decision register

| ID | Decision | Rationale | Mechanical gate |
| --- | --- | --- | --- |
| S17-RTM-001 | Sprint 017 is design-only. | Sprint 010 GAP-010 and Sprint 016 handoff require RTM ledger design before implementation authority. | Tests require `design only`, `does not authorize RTM generation`, and no runtime generated RTM fields. |
| S17-RTM-002 | Active doctrine number is `BLK-023` if a doctrine doc is added. | `BLK-017` already means disabled transport and `BLK-022` already means BEO publication design boundary. | Tests point to `docs/BLK-023_offline-rtm-ledger-design-boundary.md`. |
| S17-RTM-003 | RTM generation approval is separate from BEO publication, BLK-test MCP, and `codex-live`. | Traceability is a separate `blk-link` authority and must not be inherited from execution or publication. | Review/doctrine tests require exact approval-separation markers. |
| S17-RTM-004 | Future active-vault comparison is hash-only until a later approved implementation grants specific access. | `blk-req` protected bodies must not leak into BLK-test, BEO, or planning contexts. | Tests require protected-body exclusion and no runtime active-vault reads. |
| S17-RTM-005 | Existing runtime outputs remain disabled. | Sprint 017 cannot become hidden RTM implementation. | Import/static tests require `NOT_GENERATED`, `DISABLED_INTERFACE_ONLY`, no `rtm_id`, no coverage matrix, and no drift decision. |
| S17-RTM-006 | Drift rejection remains future review authority, not a Sprint 017 decision. | Drift can invalidate execution evidence and must be explicitly approved and rollback-aware. | Doctrine markers state `does not authorize RTM drift rejection authority` and `does not make drift decisions`. |

---

## 4. Controller workflow for execution

1. Create an implementation branch, for example `sprint/blk-system-017`.
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
   11. Create `docs/outcomes/BLK-SYSTEM-017_task-00N-outcome.md` with RED/GREEN and pre-commit verification evidence.
   12. Commit and push the outcome doc separately.
   13. Send concise Discord summary with `MEDIA:/home/dad/BLK-System/docs/outcomes/BLK-SYSTEM-017_task-00N-outcome.md` after push.
4. Close the sprint with `docs/outcomes/BLK-SYSTEM-017_sprint-closeout.md`, committed and pushed separately.

Cache-safe command pattern:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
python - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
for p in Path('python').glob('**/__pycache__'):
    shutil.rmtree(p)
PY
git diff --check
git status --short --branch
```

---

## 5. Task 0 — Commit the plan before implementation

**Objective:** Make this reviewed plan durable before implementation starts.

**Files:**

- Add: `docs/plans/blk-system-017_offline-rtm-ledger-design.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-017_task-000-outcome.md`

**Step 1: Verify plan markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
path = Path('docs/plans/blk-system-017_offline-rtm-ledger-design.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-017',
    'Offline RTM Ledger Design',
    'design-only',
    'does not authorize RTM generation',
    'does not authorize RTM drift rejection authority',
    'docs/BLK-023_offline-rtm-ledger-design-boundary.md',
    'rtm_status: "NOT_GENERATED"',
    'rtm_authority: "DISABLED_INTERFACE_ONLY"',
    'protected BLK-req vault bodies remain unread',
    'RTM generation approval is separate from BEO publication approval',
]
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit(f'missing plan markers: {missing}')
fence = chr(96) * 3
if text.count(fence) % 2:
    raise SystemExit('unbalanced markdown fences')
print('BLK-SYSTEM-017 plan markers: PASS')
PY
```

Expected: `BLK-SYSTEM-017 plan markers: PASS`.

**Step 2: Stage exact path and commit**

Run:

```bash
git add docs/plans/blk-system-017_offline-rtm-ledger-design.md
git diff --cached --name-only
git commit -m "docs: plan blk-system sprint 017 rtm ledger design"
git push
```

Expected staged path only:

```text
docs/plans/blk-system-017_offline-rtm-ledger-design.md
```

**Step 3: Outcome doc**

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-017_task-000-outcome.md`.

---

## 6. Task 1 — Preserve Sprint 017 RTM ledger design review artifact

**Objective:** Add the Sprint 017 review artifact and a persistent gate proving the offline RTM boundary is explicit and non-authorizing.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Add: `docs/reviews/BLK-SYSTEM-017_offline-rtm-ledger-design-review.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-017_task-001-outcome.md`

**Step 1: Write failing test**

Add constant near Sprint 016 constants:

```python
SPRINT017_RTM_LEDGER_REVIEW = ROOT / "docs" / "reviews" / "BLK-SYSTEM-017_offline-rtm-ledger-design-review.md"
```

Add focused test:

```python
def test_sprint017_offline_rtm_ledger_design_review_preserves_non_authority(self):
    self.assertTrue(SPRINT017_RTM_LEDGER_REVIEW.exists(), "Sprint 017 RTM ledger design review missing")
    text = SPRINT017_RTM_LEDGER_REVIEW.read_text()
    required = [
        "BLK-SYSTEM-017",
        "Offline RTM ledger design, not implementation",
        "design only",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "does not generate RTM",
        "does not emit rtm_id",
        "does not create coverage matrices",
        "does not make drift decisions",
        "RTM generation approval is separate from BEO publication approval",
        "RTM generation approval is separate from BLK-test MCP approval",
        "RTM generation approval is separate from codex-live approval",
        "protected BLK-req vault bodies remain unread",
        "hash-only active-vault comparison remains future authority",
        "beo_publication: \"DRAFT_ONLY\" remains mandatory",
        "rtm_status: \"NOT_GENERATED\" remains mandatory",
        "rtm_authority: \"DISABLED_INTERFACE_ONLY\" remains mandatory",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 017 RTM design review markers missing: {missing}")
```

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint017_offline_rtm_ledger_design_review_preserves_non_authority
```

Expected: FAIL because the review artifact is missing.

**Step 2: Add review artifact**

Create `docs/reviews/BLK-SYSTEM-017_offline-rtm-ledger-design-review.md` with these sections:

- source documents reviewed: BLK-001, BLK-008, BLK-014, BLK-016, BLK-020, BLK-021, BLK-022, Sprint 010 gap/slicing, Sprint 015 review/closeout, Sprint 016 review/closeout;
- positive design scope;
- exact non-authority markers;
- future RTM approval separation;
- hash-only active-vault policy;
- future ledger identity/schema checklist;
- coverage and drift vocabulary;
- forbidden runtime field matrix;
- BEO publication and BLK-test exclusion;
- handoff to a future explicit offline RTM implementation sprint.

**Step 3: Run GREEN**

Run the focused test again. Expected: PASS.

**Step 4: Shared gates**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint017_offline_rtm_ledger_design_review_preserves_non_authority
python - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
for p in Path('python').glob('**/__pycache__'):
    shutil.rmtree(p)
PY
git diff --check
git status --short --branch
```

**Step 5: Commit/push and outcome**

Stage exact paths only:

```bash
git add python/test_active_doctrine_review_gates.py docs/reviews/BLK-SYSTEM-017_offline-rtm-ledger-design-review.md
git diff --cached --name-only
git commit -m "docs: define blk-system sprint 017 rtm ledger design review"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-017_task-001-outcome.md`.

---

## 7. Task 2 — Add active non-executing BLK-023 RTM ledger design boundary

**Objective:** Make the RTM ledger design boundary active doctrine without implementing RTM generation.

**Files:**

- Modify: `python/test_active_doctrine_review_gates.py`
- Add: `docs/BLK-023_offline-rtm-ledger-design-boundary.md`
- Outcome: `docs/outcomes/BLK-SYSTEM-017_task-002-outcome.md`

**Step 1: Write failing test**

Add constant:

```python
BLK023 = ROOT / "docs" / "BLK-023_offline-rtm-ledger-design-boundary.md"
```

Add focused test:

```python
def test_blk023_records_design_only_offline_rtm_ledger_boundary(self):
    self.assertTrue(BLK023.exists(), "BLK-023 offline RTM ledger design boundary missing")
    text = BLK023.read_text()
    required = [
        "**Status:** Active design-only boundary contract",
        "BLK-SYSTEM-017",
        "offline RTM ledger design boundary",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "does not implement generate_rtm.py",
        "does not emit runtime rtm_id",
        "does not create coverage matrices",
        "does not make drift decisions",
        "RTM generation approval is separate from BEO publication approval",
        "RTM generation approval is separate from BLK-test MCP approval",
        "RTM generation approval is separate from codex-live approval",
        "hash-only active-vault comparison remains future authority",
        "protected BLK-req vault bodies remain unread",
        "beo_publication: \"DRAFT_ONLY\" remains mandatory",
        "rtm_status: \"NOT_GENERATED\" remains mandatory",
        "rtm_authority: \"DISABLED_INTERFACE_ONLY\" remains mandatory",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-023 boundary markers missing: {missing}")
```

Run focused test. Expected: FAIL because BLK-023 does not exist.

**Step 2: Add BLK-023 active doctrine**

Create `docs/BLK-023_offline-rtm-ledger-design-boundary.md` with:

- purpose and status as active design-only boundary;
- current runtime boundary: all existing projectors/interfaces remain RTM-disabled;
- future RTM authorization envelope;
- future ledger candidate schema fields at prose level only;
- explicit approval separation;
- hash-only active-vault policy and protected-body exclusion;
- coverage/drift vocabulary and rejection matrix;
- BEO publication / BLK-test / source mutation exclusions;
- implementation/testing mapping pointing to static gates, not RTM generator code;
- stop conditions.

Do not add `generate_rtm.py`, runtime ledger generators, coverage matrices, drift decision emitters, active-vault scanners, or requirement-body readers.

**Step 3: Run GREEN and shared gates**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk023_records_design_only_offline_rtm_ledger_boundary
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint017_offline_rtm_ledger_design_review_preserves_non_authority
python - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
for p in Path('python').glob('**/__pycache__'):
    shutil.rmtree(p)
PY
git diff --check
```

Expected: PASS.

**Step 4: Commit/push and outcome**

```bash
git add python/test_active_doctrine_review_gates.py docs/BLK-023_offline-rtm-ledger-design-boundary.md
git diff --cached --name-only
git commit -m "docs: add blk-023 rtm ledger design boundary"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-017_task-002-outcome.md`.

---

## 8. Task 3 — Add runtime non-RTM guard tests

**Objective:** Prove Sprint 017 did not accidentally introduce RTM generation, active-vault reading, coverage, drift, publication, or live-MCP behavior.

**Files:**

- Create: `python/test_rtm_ledger_design_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-017_task-003-outcome.md`

**Step 1: Write tests**

Create tests that import existing disabled interfaces and scan production Python files. Suggested assertions:

```python
from pathlib import Path
import unittest
from unittest.mock import patch

from beo_rtm_interface_fixtures import build_beo_rtm_interface_fixture

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "python"
TRACE_ARTIFACTS = [{"kind": "REQ", "id": "REQ-S17-001", "version_hash": "sha256:" + "1" * 64}]


def draft_beo(**overrides):
    beo = {
        "beo_id": "BEO_S17_GUARD_001",
        "beb_id": "BEB_S17_GUARD_001",
        "status": "PASS",
        "pre_engine_hash": "sha256:" + "2" * 64,
        "trace_artifacts": TRACE_ARTIFACTS,
        "beo_publication": "DRAFT_ONLY",
        "rtm_status": "NOT_GENERATED",
    }
    beo.update(overrides)
    return beo


class RtmLedgerDesignGateTest(unittest.TestCase):
    def test_existing_beo_rtm_interface_remains_disabled_only(self):
        interface = build_beo_rtm_interface_fixture(draft_beo(), interface_id="RTM_IFACE_S17_GUARD_001")
        self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
        self.assertEqual(interface["rtm_authority"], "DISABLED_INTERFACE_ONLY")
        self.assertFalse(interface["active_vault_read"])
        self.assertFalse(interface["requirements_resolved"])
        forbidden = {"rtm", "rtm_id", "requirements", "coverage_matrix", "coverage_status", "drift", "drift_decision"}
        self.assertTrue(forbidden.isdisjoint(interface))

    def test_generated_rtm_fields_still_reject(self):
        for field in ("rtm", "rtm_id", "requirements", "coverage_matrix"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "generated RTM authority field"):
                    build_beo_rtm_interface_fixture(draft_beo(**{field: "forbidden"}), interface_id="RTM_IFACE_S17_GUARD_002")

    def test_active_vault_paths_are_not_read_by_disabled_interface(self):
        forbidden = ("docs/active", "docs/requirements", "docs/use_cases")
        def fail_forbidden_read(self_path, *args, **kwargs):
            as_text = str(self_path)
            if any(token in as_text for token in forbidden):
                raise AssertionError(f"forbidden active vault read: {as_text}")
            return ""
        with patch.object(Path, "read_text", fail_forbidden_read):
            interface = build_beo_rtm_interface_fixture(draft_beo(), interface_id="RTM_IFACE_S17_GUARD_003")
        self.assertEqual(interface["rtm_status"], "NOT_GENERATED")
        self.assertFalse(interface["active_vault_read"])

    def test_production_python_does_not_define_rtm_generator_or_drift_runtime(self):
        forbidden_markers = [
            "def generate_rtm",
            "class RtmLedger",
            "rtm_status = \"GENERATED\"",
            "rtm_status='GENERATED'",
            "coverage_matrix =",
            "drift_decision =",
            "active_vault_hash_compare",
        ]
        offenders = []
        for path in PYTHON.glob("*.py"):
            if path.name.startswith("test_"):
                continue
            text = path.read_text()
            for marker in forbidden_markers:
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual(offenders, [], f"Sprint 017 introduced runtime RTM markers: {offenders}")
```

Run focused test. Expected: PASS once test is created, because Sprint 017 must not introduce runtime RTM code.

**Step 2: Shared gates**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_rtm_ledger_design_gates
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_beo_rtm_interface_fixtures.py python/test_rtm_ledger_design_gates.py
python - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
for p in Path('python').glob('**/__pycache__'):
    shutil.rmtree(p)
PY
git diff --check
```

**Step 3: Commit/push and outcome**

```bash
git add python/test_rtm_ledger_design_gates.py
git diff --cached --name-only
git commit -m "test: guard rtm ledger design as non-runtime"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-017_task-003-outcome.md`.

---

## 9. Task 4 — Cross-reference Sprint 017 without broadening authority

**Objective:** Patch existing active docs so readers discover BLK-023 while retaining disabled RTM runtime boundaries.

**Files:**

- Modify: `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
- Modify only if needed: `docs/BLK-008_blk-test-mcp-execution-server.md`
- Modify only if needed: `docs/BLK-001_blk-system-master-architecture.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Outcome: `docs/outcomes/BLK-SYSTEM-017_task-004-outcome.md`

**Step 1: Write failing cross-reference test**

Add or extend a test to require:

```python
def test_blk022_hands_off_later_rtm_design_to_blk023_without_authority(self):
    text = BLK022.read_text()
    required = [
        "BLK-023",
        "offline RTM ledger design boundary",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "rtm_status: \"NOT_GENERATED\" remains mandatory",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"BLK-022 to BLK-023 handoff markers missing: {missing}")
```

Run focused test. Expected: FAIL until BLK-022 is patched.

**Step 2: Patch docs narrowly**

Patch BLK-022 handoff with a short paragraph:

```text
BLK-023 records the BLK-SYSTEM-017 offline RTM ledger design boundary. BLK-023 is design-only: it does not authorize RTM generation, does not authorize RTM drift rejection authority, does not implement `generate_rtm.py`, does not emit runtime `rtm_id`, does not create coverage matrices, does not make drift decisions, keeps `rtm_status: "NOT_GENERATED"` mandatory for current runtime outputs, and keeps protected BLK-req vault bodies unread.
```

Patch BLK-008 or BLK-001 only if a focused test or hostile review proves the old document is misleading after BLK-023 exists. If patched, repeat the same non-authority language and avoid implying current `blk-link` can generate RTM.

**Step 3: Run GREEN and shared gates**

Run focused cross-reference test, then:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates
python - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
for p in Path('python').glob('**/__pycache__'):
    shutil.rmtree(p)
PY
git diff --check
```

**Step 4: Commit/push and outcome**

Stage exact paths only:

```bash
git add docs/BLK-022_authoritative-beo-publication-design-boundary.md python/test_active_doctrine_review_gates.py
# Add docs/BLK-008... or docs/BLK-001... only if actually changed.
git diff --cached --name-only
git commit -m "docs: cross-reference blk-023 rtm ledger design boundary"
git push
```

Create, validate, exact-path commit, and push `docs/outcomes/BLK-SYSTEM-017_task-004-outcome.md`.

---

## 10. Task 5 — Full verification and sprint closeout

**Objective:** Verify the full repository and record Sprint 017 closeout.

**Files:**

- Add: `docs/outcomes/BLK-SYSTEM-017_sprint-closeout.md`

**Step 1: Full verification**

Run:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s python -p 'test_*.py'
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python
go test ./...
go vet ./...
python - <<'PY'
from pathlib import Path
import shutil
for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
    if p.exists():
        shutil.rmtree(p)
for p in Path('python').glob('**/__pycache__'):
    shutil.rmtree(p)
PY
git diff --check
git status --short --branch
```

Expected: all tests pass; status clean except closeout file before commit.

**Step 2: Create closeout**

Create `docs/outcomes/BLK-SYSTEM-017_sprint-closeout.md` with:

- status complete;
- task commit table;
- outcome document table;
- accepted design-only RTM ledger boundary;
- non-authority boundary;
- full verification evidence;
- handoff seed for a later explicit offline RTM implementation sprint;
- handoff seed for future BEO publication implementation interaction only if still relevant and separately approved.

Required closeout markers:

```text
BLK-SYSTEM-017 was design-only.
Sprint 017 does not authorize RTM generation.
Sprint 017 does not authorize RTM drift rejection authority.
Sprint 017 does not implement generate_rtm.py.
Sprint 017 does not emit runtime rtm_id.
Sprint 017 does not create coverage matrices.
Sprint 017 does not make drift decisions.
Protected BLK-req vault bodies remain unread.
Current runtime RTM outputs remain NOT_GENERATED and DISABLED_INTERFACE_ONLY.
```

**Step 3: Validate and commit closeout**

Run a marker check, stage exact path, commit, and push:

```bash
git add docs/outcomes/BLK-SYSTEM-017_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system sprint 017"
git push
```

---

## 11. Final verification checklist

Before final closeout, all must be true:

- [ ] `docs/plans/blk-system-017_offline-rtm-ledger-design.md` committed first.
- [ ] `docs/reviews/BLK-SYSTEM-017_offline-rtm-ledger-design-review.md` exists and is gated.
- [ ] `docs/BLK-023_offline-rtm-ledger-design-boundary.md` exists and is gated.
- [ ] Existing runtime outputs remain `rtm_status: "NOT_GENERATED"` and `rtm_authority: "DISABLED_INTERFACE_ONLY"`.
- [ ] No production Python module implements `generate_rtm.py`, RTM ledger writer, coverage matrix generator, active-vault scanner, or drift-decision runtime.
- [ ] BLK-022 cross-references BLK-023 without broadening authority.
- [ ] Every task has a matching pushed outcome doc.
- [ ] Full Python unittest, Python pytest, Go test, Go vet, `git diff --check`, cache cleanup, and clean status verified.

## 12. Explicit non-goals recap

Sprint 017 does not authorize RTM generation, does not authorize RTM drift rejection authority, does not implement RTM generation, does not emit runtime `rtm_id`, does not create coverage matrices, does not compare active-vault hashes at runtime, does not read protected BLK-req vault bodies, does not publish authoritative BEOs, does not mutate public outcome ledgers, does not grant signer/storage/rollback authority, does not start BLK-test MCP, does not rerun BLK-SYSTEM-014 first live smoke, does not run against real target repositories, does not mutate source, and does not claim production sandbox or host-secret isolation.
