# BLK-pipe Sprint 009 — BLK-001 / BLK-008 Doctrine Trace Gates

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This sprint is deterministic local remediation only. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication.

**Goal:** Close the Sprint 006 hostile-review doctrine and review-scope gaps that remain after BLK-PIPE-008’s code-bound trace-remediation plan, especially BLK-003 strict examples, BLK-006 draft hash lifecycle, BLK-008 current-boundary qualifiers, and outcome-amendment evidence.

**Architecture:** Sprint 009 is a documentation-and-gate hardening sprint. It does not supersede BLK-PIPE-008’s physical BLK-pipe / BLK-test boundary fixes; it adds active-doctrine overlays and deterministic tests so future BLK-test, BEO, RTM, and trace-baton planning cannot copy invalid hash examples or imply live authority before an explicit later sprint authorizes it.

**Tech Stack:** Dependency-free Python `unittest` doctrine gates, Markdown active doctrine documents, Markdown review/outcome documents, Go verification for no BLK-pipe regression.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Planning preflight when this document was authored:

```text
date                         -> 2026-05-05 19:27:20 AEST
git status --short --branch  -> ## main...origin/main
                               ?? docs/reviews/BLK-PIPE-006_BLK-008_review-scope-addendum.md
                               ?? docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md
HEAD                         -> 817d011 docs: add BLK-pipe sprint 008 plan
```

Source review artifacts introduced alongside this plan:

```text
docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md
docs/reviews/BLK-PIPE-006_BLK-008_review-scope-addendum.md
```

If either review artifact is still untracked at sprint start, include it in the sprint branch/commit stream before closeout so the remediation source is preserved in repository history.

Important dependency note:

- BLK-PIPE-008 already plans the physical boundary fixes for the Sprint 006 hostile review’s `HIGH-1` and `HIGH-2` findings:
  - mandatory non-empty canonical `trace_artifacts` for governed BLK-pipe `execute` payloads;
  - canonical hash validation in BLK-test PASS/FAIL handoff fixtures.
- Sprint 009 must **not** duplicate or weaken BLK-PIPE-008. If BLK-PIPE-008 has not been executed when Sprint 009 starts, Sprint 009 may still patch doctrine and gates, but all outcome language must say `HIGH-1` / `HIGH-2` are assigned to BLK-PIPE-008 and are not physically closed yet.

---

## 1. Review Findings Driving This Sprint

Sprint 009 is driven by these source artifacts:

```text
docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md
docs/reviews/BLK-PIPE-006_BLK-008_review-scope-addendum.md
```

Findings-to-task map:

| Review finding | Sprint 009 disposition |
| --- | --- |
| `HIGH-1` — BLK-pipe can execute successfully with empty `trace_artifacts`. | BLK-PIPE-008 dependency. Do not duplicate; reference honestly in Task 4 amendment. |
| `HIGH-2` — BLK-test PASS/FAIL handoff fixture accepts noncanonical hashes. | BLK-PIPE-008 dependency. Do not duplicate; reference honestly in Task 4 amendment. |
| `HIGH-3` — BLK-003 strict BEB frontmatter uses truncated `version_hash` examples. | Task 1. |
| `MEDIUM-1` — BLK-006 draft schema conflicts with BLK-002 hash lifecycle. | Task 2. |
| `MEDIUM-2` — BLK-003 §10 escalation implies current authoritative BEO / live BLK-test payload availability. | Task 1. |
| `MEDIUM-3` — Sprint 006 outcomes understate residual trace-readiness gaps. | Task 4. |
| BLK-008 addendum — BLK-008 must be secondary target-state BLK-test authority anchor for relevant reviews. | Task 3 and Task 5. |
| Recommended gate — fail on active strict YAML examples containing truncated `sha256` examples. | Tasks 1, 2, and 5. |

---

## 2. Decision Register

| Decision ID | Question | Decision | Rationale | Implementation effect |
| --- | --- | --- | --- | --- |
| DEC-001 | Should strict YAML/frontmatter examples use placeholder ellipses? | **No. Use real synthetic canonical fixture hashes or explicit non-runtime placeholders that cannot be mistaken for valid hashes.** For BLK-003 strict frontmatter, use real synthetic canonical hashes. | BLK-003 says the YAML block is mandatory strict frontmatter. Ellipsis hashes are copy-paste hazards. | Replace `sha256:7f8b9...`, `sha256:1a2b3...`, and other strict-hash shorthand inside strict YAML examples. |
| DEC-002 | Should BLK-006 show one universal DRAFT schema with `sha256:...` values? | **No. Split new-draft and staged-revision examples.** | BLK-002 says new drafts use `parent_hash: ""` and `version_hash: "PENDING"`; staged revisions carry a canonical parent hash and still use `version_hash: "PENDING"` until promotion. | Patch BLK-006 §B and keep BLK-006 §C consistent. |
| DEC-003 | Should BLK-008 be treated as currently live BLK-test MCP authority? | **No. BLK-008 is active target-state planning doctrine only until a later sprint authorizes live BLK-test MCP.** | Sprint 006/007/008 keep live MCP, authoritative BEO, and RTM authority disabled. | Add BLK-008 current-boundary overlay and cross-links to BLK-013/014/015/016. |
| DEC-004 | Should Sprint 006 closeout be rewritten as if it failed? | **No. Preserve the historical closeout and add a post-closeout amendment.** | Sprint 006 materially improved alignment but was later reviewed as conditional/not-clean. History should remain audit-grade, not back-edited into fiction. | Create an amendment outcome and add a short cross-link to the closeout. |
| DEC-005 | Should the new doctrine gate globally ban every narrative `sha256:...` shorthand in all historical docs? | **No. Gate active strict YAML/code-fence examples first.** | Historical plans/outcomes and narrative BLK-001 examples may use shorthand for exposition. The immediate unsafe copy-paste risk is strict YAML/frontmatter examples in active doctrine. | Scan active `docs/BLK-*.md` YAML fences for truncated `sha256` patterns; do not rewrite historical plans/outcomes in this sprint. |

---

## 3. Non-Goals and Hard Blocks

Sprint 009 must not implement, invoke, or imply:

- live Codex invocation;
- live tactical LLM API calls;
- network model services;
- `codex-live` runtime execution;
- cyber tooling or cyber execution;
- execution against real cyber-program repositories or live targets;
- live BLK-test MCP calls;
- live MCP client transport;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- complete RTM generation as a traceability ledger;
- RTM drift rejection authority;
- full sandbox/container/cgroup/VM enforcement;
- production host-secret isolation claims;
- production approval-channel mechanics;
- active BLK-req vault reads or requirement-body parsing.

Allowed work:

```text
deterministic local tests
active doctrine text patching
post-closeout amendment documentation
review-source preservation
fixture-only / disabled-boundary wording
gate tests that inspect Markdown text only
outcome documents and closeout evidence
```

Do not broaden this sprint into a wholesale rewrite of BLK-001 or historical plans/outcomes. Patch only the active-doctrine and Sprint 006 closeout surfaces named by the review findings unless a deterministic gate proves a directly equivalent active-doc issue.

---

## 4. Invariants to Preserve

1. BLK-pipe remains a deterministic transport/mutation gate, not an architect, requirement parser, live LLM caller, BLK-test authority, BEO publisher, RTM generator, or sandbox.
2. BLK-test remains disabled/fixture-only in current implementation unless a future sprint explicitly authorizes live MCP transport and mechanically enforces it.
3. BLK-008 can describe target-state MCP architecture, but must clearly distinguish target-state architecture from current disabled/fixture-only operation.
4. PASS/FAIL-shaped BLK-test data must require non-empty canonical `trace_artifacts[*].version_hash` at every current fixture and future target-state contract surface.
5. BLOCKED-shaped data may preserve trace absence only when the source failed before canonical trace decode; it must not launder malformed trace metadata.
6. Draft-only BEO fixture projection is not authoritative BEO publication.
7. RTM interface fixtures preserve opaque trace metadata only; they do not generate RTM ledgers, read active vault bodies, or compare hashes against files.
8. BLK-002 draft lifecycle remains authoritative for `parent_hash` / `version_hash` semantics.
9. New BLK-System plans and active docs use BLK-native BEB/BEO terminology and `beb_id`, not legacy execution-brief/outcome vocabulary.
10. No production `git add .`, `git add -u`, `git stash`, relative revert anchors, or triple-dot report diffs.

Canonical trace artifact shape:

```yaml
trace_artifacts:
  - kind: "REQ"
    id: "REQ-042"
    version_hash: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
```

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Use strict TDD for code/gate changes: write a failing deterministic gate first, capture RED, patch the docs, capture GREEN.
3. Use deterministic local review gates only. Do not dispatch live Codex, live tactical LLM, network model, cyber, or live BLK-test MCP reviewers.
4. Run focused tests listed in the task.
5. Run shared verification before each implementation commit:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```

6. Create a matching outcome document for Tasks 1-5:

   ```text
   docs/outcomes/BLK-PIPE-009_task-00N-outcome.md
   ```

7. Use the sprint closeout document as Task 6 outcome:

   ```text
   docs/outcomes/BLK-PIPE-009_sprint-closeout.md
   ```

8. Commit each task after verification with the listed commit message.
9. Push only after verification passes and `git status --short --branch` is clean/aligned.

---

## 6. Task 1 — Patch BLK-003 Strict Trace Examples and Escalation Boundary

### Objective

Close `HIGH-3` and `MEDIUM-2` by making BLK-003’s strict BEB frontmatter example copy-paste-safe and by qualifying §10 escalation as current disabled/draft-only behavior, not live BLK-test or authoritative BEO authority.

### Files

Modify:

- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `python/test_active_doctrine_review_gates.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-009_task-001-outcome.md`

### Required behavior

- The strict BEB YAML frontmatter example in BLK-003 must not contain truncated hash examples:
  - replace `sprint_base_hash: "a1b2c3d4..."` with a deterministic synthetic full-length Git hash such as `0123456789abcdef0123456789abcdef01234567`;
  - replace `sha256:7f8b9...` and `sha256:1a2b3...` with real synthetic `sha256:` + 64 lowercase hex fixture hashes.
- BLK-003 must explicitly state that synthetic fixture hashes in examples are not live BLK-req vault values.
- BLK-003 §10 must state the current behavior:
  - halt the loop;
  - write a human escalation package;
  - create only a `draft-only BEO`-shaped fixture if a BEO-shaped artifact is needed;
  - include BLK-test payloads only when a source-bound fixture exists now or a future sprint authorizes live BLK-test;
  - authoritative BEO publication and RTM generation remain disabled.

### TDD steps

#### Step 1 — RED: add BLK-003 doctrine gate

Create or extend `python/test_active_doctrine_review_gates.py` with tests similar to:

```python
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK003 = ROOT / "docs" / "BLK-003_blk-pipe-blk-test-orchestration.md"
TRUNCATED_SHA_RE = re.compile(r"sha256:(?:[0-9a-fA-F]{1,63})?\.\.\.")
YAML_FENCE_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def yaml_fences(path: Path) -> list[str]:
    return YAML_FENCE_RE.findall(path.read_text())


class ActiveDoctrineReviewGateTest(unittest.TestCase):
    def test_blk003_strict_yaml_examples_do_not_use_truncated_trace_hashes(self):
        offenders = []
        for block in yaml_fences(BLK003):
            if "trace_artifacts:" not in block:
                continue
            for match in TRUNCATED_SHA_RE.finditer(block):
                offenders.append(match.group(0))
        self.assertEqual(offenders, [], f"BLK-003 strict YAML uses truncated hashes: {offenders}")

    def test_blk003_escalation_is_current_boundary_safe(self):
        text = BLK003.read_text()
        required = [
            "human escalation package",
            "draft-only BEO",
            "source-bound fixture",
            "live BLK-test MCP remains disabled",
            "authoritative BEO publication remains disabled",
            "RTM generation remains disabled",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-003 escalation boundary missing: {missing}")
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected RED: BLK-003 truncated hash and/or §10 boundary markers fail against current `main`.

#### Step 2 — GREEN: patch BLK-003

Patch the YAML block near BLK-003 State 1 to use full synthetic values:

```yaml
sprint_base_hash: "0123456789abcdef0123456789abcdef01234567"
trace_artifacts:
  - kind: "REQ"
    id: "REQ-042"
    version_hash: "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  - kind: "UC"
    id: "UC-004"
    version_hash: "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
```

Add a sentence immediately after the block:

```text
The hash values above are synthetic fixture values for example shape only; a real BEB must use the canonical hashes returned by the BLK-002 retrieval/baseline path.
```

Patch §10 to say, in current-boundary language, that the escalation package is human-facing and that any BEO-shaped artifact is draft-only unless a future sprint explicitly authorizes authoritative publication.

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected GREEN.

#### Step 3 — Verify and document

Run shared verification. Then create `docs/outcomes/BLK-PIPE-009_task-001-outcome.md` with:

- RED evidence;
- GREEN evidence;
- exact BLK-003 sections patched;
- explicit non-execution statement.

Commit:

```bash
git add docs/BLK-003_blk-pipe-blk-test-orchestration.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-PIPE-009_task-001-outcome.md
git commit -m "docs: align blk-003 trace examples and escalation boundary"
```

---

## 7. Task 2 — Split BLK-006 Draft and Revision Hash Lifecycle Examples

### Objective

Close `MEDIUM-1` by making BLK-006’s DRAFT schema examples match BLK-002’s new-draft and staged-revision hash lifecycle.

### Files

Modify:

- `docs/BLK-006_blk-req-implementation-brief.md`
- `python/test_active_doctrine_review_gates.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-009_task-002-outcome.md`

### Required behavior

BLK-006 §B must no longer present a single universal DRAFT schema with fake `sha256:...` values.

It must show two explicit examples:

1. New draft intake:

   ```yaml
   ---
   id: "TBD"
   schema_version: "1.0"
   parent_hash: ""
   version_hash: "PENDING"
   status: "DRAFT"
   rationale: "Justification text..."
   linked_nodes:
     - "[[REQ-012]]"
   ---
   ```

2. Staged revision draft:

   ```yaml
   ---
   id: "REQ-042"
   schema_version: "1.0"
   parent_hash: "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
   version_hash: "PENDING"
   status: "DRAFT"
   rationale: "Revision justification text..."
   linked_nodes:
     - "[[REQ-012]]"
   ---
   ```

BLK-006 must state that promotion/baseline mechanics assign the final canonical `version_hash`; DRAFT documents must not invent future hashes.

### TDD steps

#### Step 1 — RED: extend doctrine gate for BLK-006

Extend `python/test_active_doctrine_review_gates.py` with tests similar to:

```python
BLK006 = ROOT / "docs" / "BLK-006_blk-req-implementation-brief.md"

class ActiveDoctrineReviewGateTest(unittest.TestCase):
    # keep Task 1 tests...

    def test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders(self):
        offenders = []
        for block in yaml_fences(BLK006):
            for match in TRUNCATED_SHA_RE.finditer(block):
                offenders.append(match.group(0))
        self.assertEqual(offenders, [], f"BLK-006 YAML uses truncated hashes: {offenders}")

    def test_blk006_documents_new_draft_and_staged_revision_lifecycles(self):
        text = BLK006.read_text()
        required = [
            'parent_hash: ""',
            'version_hash: "PENDING"',
            'parent_hash: "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"',
            "promotion",
            "DRAFT documents must not invent future hashes",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-006 lifecycle markers missing: {missing}")
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected RED: current BLK-006 still contains `sha256:...` and lacks split lifecycle examples.

#### Step 2 — GREEN: patch BLK-006

Patch `docs/BLK-006_blk-req-implementation-brief.md` §B to replace the universal schema with the two examples above. Keep §C staged-revision language consistent with the staged-revision example.

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected GREEN.

#### Step 3 — Verify and document

Run shared verification. Then create `docs/outcomes/BLK-PIPE-009_task-002-outcome.md` with RED/GREEN evidence and the BLK-002 lifecycle alignment rationale.

Commit:

```bash
git add docs/BLK-006_blk-req-implementation-brief.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-PIPE-009_task-002-outcome.md
git commit -m "docs: align blk-006 draft hash lifecycle"
```

---

## 8. Task 3 — Add BLK-008 Current-Boundary and Trace Contract Overlay

### Objective

Close the BLK-008 review-scope addendum by making BLK-008 explicitly target-state/planning-only until live BLK-test MCP is separately authorized, while still making it a secondary authority anchor for future BLK-test/BEO/RTM reviews.

### Files

Modify:

- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `python/test_active_doctrine_review_gates.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-009_task-003-outcome.md`

### Required behavior

BLK-008 must explicitly state:

- BLK-008 is active target-state planning doctrine, not current live MCP authorization.
- Current implementation remains disabled/fixture-only under BLK-013/BLK-014/BLK-015/BLK-016 unless a future sprint authorizes live BLK-test MCP.
- PASS/FAIL payload shapes require non-empty canonical `trace_artifacts[*].version_hash` values matching `sha256:<64-lowercase-hex>`.
- BLOCKED payload shapes may preserve trace absence only with an explicit source-failure reason; malformed trace hashes are rejected rather than laundered.
- BLK-008 cannot imply authoritative BEO publication, RTM generation, or RTM drift rejection authority.
- MCP output/status vocabulary must align with BLK-013/014/015/016 current fixture vocabulary and source-binding requirements.
- The test server is a deterministic physics oracle only; it must not grant arbitrary shell access or architectural authority.

Do not implement the MCP server in this sprint. Do not perform a wholesale rewrite of the TypeScript design unless needed to add the boundary overlay.

### TDD steps

#### Step 1 — RED: extend doctrine gate for BLK-008

Extend `python/test_active_doctrine_review_gates.py` with a BLK-008 marker test:

```python
BLK008 = ROOT / "docs" / "BLK-008_blk-test-mcp-execution-server.md"

class ActiveDoctrineReviewGateTest(unittest.TestCase):
    # keep prior tests...

    def test_blk008_declares_target_state_boundary_and_trace_contract(self):
        text = BLK008.read_text()
        required = [
            "target-state planning doctrine",
            "not current live MCP authorization",
            "BLK-013",
            "BLK-014",
            "BLK-015",
            "BLK-016",
            "PASS/FAIL payload shapes require non-empty canonical trace_artifacts",
            "sha256:<64-lowercase-hex>",
            "malformed trace hashes are rejected",
            "authoritative BEO publication remains disabled",
            "RTM generation remains disabled",
            "RTM drift rejection authority remains disabled",
            "source-binding requirements",
        ]
        missing = [marker for marker in required if marker not in text]
        self.assertEqual(missing, [], f"BLK-008 boundary markers missing: {missing}")
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected RED: current BLK-008 lacks the current-boundary overlay and trace-contract markers.

#### Step 2 — GREEN: patch BLK-008

Add a new section near the top, before Phase 1:

```markdown
## 0. Current Implementation Boundary and Authority

BLK-008 is active target-state planning doctrine for a future BLK-test MCP physics oracle. It is not current live MCP authorization. Current BLK-System operation remains disabled/fixture-only under BLK-013, BLK-014, BLK-015, and BLK-016 unless a later sprint explicitly authorizes live BLK-test MCP and mechanically enforces the authorization boundary.

Current and future BLK-test PASS/FAIL payload shapes require non-empty canonical trace_artifacts entries. Each `trace_artifacts[*].version_hash` must match `sha256:<64-lowercase-hex>`. BLOCKED payload shapes may preserve trace absence only with an explicit source-failure reason; malformed trace hashes are rejected rather than laundered into BEO/RTM fixture paths.

BLK-008 does not authorize authoritative BEO publication, RTM generation, or RTM drift rejection authority. MCP output/status vocabulary must align with BLK-013/014/015/016 current fixture vocabulary and source-binding requirements.
```

If necessary, lightly qualify the existing Objective/Purpose so it says future target-state server rather than current live server.

Run the focused doctrine gate again and then shared verification.

#### Step 3 — Verify and document

Create `docs/outcomes/BLK-PIPE-009_task-003-outcome.md` with:

- RED/GREEN evidence;
- exact BLK-008 current-boundary clauses added;
- statement that no live BLK-test MCP was implemented or invoked.

Commit:

```bash
git add docs/BLK-008_blk-test-mcp-execution-server.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-PIPE-009_task-003-outcome.md
git commit -m "docs: qualify blk-008 target-state test authority"
```

---

## 9. Task 4 — Add Sprint 006 Post-Closeout Trace-Readiness Amendment

### Objective

Close `MEDIUM-3` by adding a post-closeout amendment that records the Sprint 006 hostile review verdict without rewriting historical closeout evidence.

### Files

Create:

- `docs/outcomes/BLK-PIPE-006_post-closeout-hostile-review-amendment.md`

Modify:

- `docs/outcomes/BLK-PIPE-006_sprint-closeout.md`
- `python/test_active_doctrine_review_gates.py`

Create outcome:

- `docs/outcomes/BLK-PIPE-009_task-004-outcome.md`

### Required behavior

The new amendment must state:

- Sprint 006 is a conditional pass, not clean, per `docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md`.
- Sprint 006 improved syntax validation and source binding but did not constitute full BLK-001 traceability signoff.
- `HIGH-1` / `HIGH-2` are assigned to BLK-PIPE-008. If BLK-PIPE-008 has not been implemented at execution time, state they are planned/open rather than closed.
- `HIGH-3`, `MEDIUM-1`, `MEDIUM-2`, `MEDIUM-3`, and the BLK-008 addendum are assigned to BLK-PIPE-009.
- No live Codex, live BLK-test MCP, authoritative BEO, or RTM authority is authorized by the amendment.

The Sprint 006 closeout must get a short cross-link to the amendment, preferably in `## 10. Deviations / Notes` or immediately after the objective, without rewriting historical task evidence.

### TDD steps

#### Step 1 — RED: extend doctrine gate for the amendment

Extend `python/test_active_doctrine_review_gates.py`:

```python
SPRINT006_CLOSEOUT = ROOT / "docs" / "outcomes" / "BLK-PIPE-006_sprint-closeout.md"
SPRINT006_AMENDMENT = ROOT / "docs" / "outcomes" / "BLK-PIPE-006_post-closeout-hostile-review-amendment.md"

class ActiveDoctrineReviewGateTest(unittest.TestCase):
    # keep prior tests...

    def test_sprint006_post_closeout_amendment_records_residual_trace_gaps(self):
        self.assertTrue(SPRINT006_AMENDMENT.exists(), "Sprint 006 post-closeout amendment missing")
        amendment = SPRINT006_AMENDMENT.read_text()
        required = [
            "conditional pass, not clean",
            "not a full BLK-001 traceability signoff",
            "HIGH-1",
            "HIGH-2",
            "BLK-PIPE-008",
            "HIGH-3",
            "MEDIUM-1",
            "MEDIUM-2",
            "MEDIUM-3",
            "BLK-PIPE-009",
            "does not authorize live Codex",
            "does not authorize live BLK-test MCP",
            "does not authorize authoritative BEO publication",
            "does not authorize RTM generation",
        ]
        missing = [marker for marker in required if marker not in amendment]
        self.assertEqual(missing, [], f"Sprint 006 amendment markers missing: {missing}")

    def test_sprint006_closeout_links_post_closeout_amendment(self):
        text = SPRINT006_CLOSEOUT.read_text()
        self.assertIn("BLK-PIPE-006_post-closeout-hostile-review-amendment.md", text)
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected RED: amendment missing and closeout does not link it.

#### Step 2 — GREEN: create amendment and patch closeout

Create the amendment with sections:

```markdown
# BLK-pipe Sprint 006 — Post-Closeout Hostile Review Amendment

**Status:** Post-closeout amendment
**Date:** <execution date>
**Source review:** docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md
**Scope addendum:** docs/reviews/BLK-PIPE-006_BLK-008_review-scope-addendum.md

## Verdict

Sprint 006 remains accepted as an improvement sprint, but the post-closeout hostile verdict is conditional pass, not clean. It is not a full BLK-001 traceability signoff.
```

Add the required finding disposition and non-authorization sections. Then patch the Sprint 006 closeout with a short note linking the amendment.

Run focused gate and shared verification.

#### Step 3 — Verify and document

Create `docs/outcomes/BLK-PIPE-009_task-004-outcome.md` with RED/GREEN evidence and a note that the original Sprint 006 closeout was not rewritten into a false clean pass.

Commit:

```bash
git add docs/outcomes/BLK-PIPE-006_post-closeout-hostile-review-amendment.md docs/outcomes/BLK-PIPE-006_sprint-closeout.md python/test_active_doctrine_review_gates.py docs/outcomes/BLK-PIPE-009_task-004-outcome.md
git commit -m "docs: amend sprint 006 trace readiness closeout"
```

---

## 10. Task 5 — Harden Persistent Active-Doctrine Review Gates and Source Preservation

### Objective

Make the Sprint 009 gates reusable so active strict YAML examples and BLK-008 review-scope obligations cannot silently regress.

### Files

Modify:

- `python/test_active_doctrine_review_gates.py`

Verify/source-preserve:

- `docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md`
- `docs/reviews/BLK-PIPE-006_BLK-008_review-scope-addendum.md`

Create outcome:

- `docs/outcomes/BLK-PIPE-009_task-005-outcome.md`

### Required behavior

The final persistent gate file must check:

1. Every active `docs/BLK-*.md` YAML fence is free of truncated SHA-256 examples matching `sha256:...` or `sha256:<short>...`.
2. BLK-003 strict trace examples and §10 current-boundary markers remain present.
3. BLK-006 draft/revision lifecycle markers remain present.
4. BLK-008 current-boundary / trace-contract / BLK-013-016 cross-link markers remain present.
5. Sprint 006 post-closeout amendment exists and is linked from the Sprint 006 closeout.
6. The two Sprint 006 hostile-review source artifacts exist under `docs/reviews/` and contain their expected titles.

### TDD steps

#### Step 1 — RED/GREEN gate finalization

Extend `python/test_active_doctrine_review_gates.py` with a global active-doc YAML scan and source-artifact checks:

```python
ACTIVE_BLK_DOCS = sorted((ROOT / "docs").glob("BLK-*.md"))
SPRINT006_REVIEW = ROOT / "docs" / "reviews" / "BLK-PIPE-006_hostile-review_BLK-001-alignment.md"
SPRINT006_SCOPE_ADDENDUM = ROOT / "docs" / "reviews" / "BLK-PIPE-006_BLK-008_review-scope-addendum.md"

class ActiveDoctrineReviewGateTest(unittest.TestCase):
    # keep prior tests...

    def test_active_yaml_fences_do_not_use_truncated_sha256_examples(self):
        offenders = []
        for path in ACTIVE_BLK_DOCS:
            text = path.read_text()
            if "**Status:** Active" not in text:
                continue
            for block in yaml_fences(path):
                for match in TRUNCATED_SHA_RE.finditer(block):
                    offenders.append(f"{path.relative_to(ROOT)}: {match.group(0)}")
        self.assertEqual(offenders, [], "truncated SHA examples in active YAML fences: " + repr(offenders))

    def test_sprint006_review_sources_are_preserved(self):
        self.assertTrue(SPRINT006_REVIEW.exists(), "Sprint 006 hostile review source missing")
        self.assertTrue(SPRINT006_SCOPE_ADDENDUM.exists(), "Sprint 006 BLK-008 addendum source missing")
        self.assertIn("BLK-PIPE-006 Hostile Review", SPRINT006_REVIEW.read_text())
        self.assertIn("BLK-008 Scope Check", SPRINT006_SCOPE_ADDENDUM.read_text())
```

If the source docs are not present, copy them from the provided review artifacts before continuing. Do not reference `/home/dad/.hermes/cache/documents/...` as the primary long-term source in the repo plan/outcome docs.

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
python3 -m unittest discover -s python -p 'test_*.py'
```

Expected GREEN after Tasks 1-4 and source preservation are complete.

#### Step 2 — Verify and document

Run shared verification. Create `docs/outcomes/BLK-PIPE-009_task-005-outcome.md` with:

- list of persistent gate checks;
- evidence that source review docs are committed under `docs/reviews/`;
- evidence that the active-doc YAML fence scan passes;
- explicit non-execution statement.

Commit:

```bash
git add python/test_active_doctrine_review_gates.py docs/reviews/BLK-PIPE-006_hostile-review_BLK-001-alignment.md docs/reviews/BLK-PIPE-006_BLK-008_review-scope-addendum.md docs/outcomes/BLK-PIPE-009_task-005-outcome.md
git commit -m "test: harden active doctrine trace review gates"
```

---

## 11. Task 6 — Sprint Closeout

### Objective

Close Sprint 009 with audit-grade evidence, preserving the exact commit chain, gates, non-execution statements, and remaining blocked live scope.

### Files

Create:

- `docs/outcomes/BLK-PIPE-009_sprint-closeout.md`

### Required content

The closeout must include:

- sprint objective summary;
- Task 1-5 implementation commits and outcome commits;
- findings-to-task disposition table;
- statement that BLK-PIPE-008 owns physical `HIGH-1` / `HIGH-2` closure and Sprint 009 owns doctrine/gate closure;
- final persistent gate evidence;
- final whole-repo verification evidence;
- explicit non-execution statement:
  - no Hindsight;
  - no live Codex;
  - no live tactical LLM;
  - no network model services;
  - no cyber tooling;
  - no live BLK-test MCP;
  - no RTM generation;
  - no authoritative BEO publication;
- remaining blocked scope before live BLK-test MCP / BEO / RTM authority;
- recommended next sprint seed, if any, without authorizing live execution.

### Closeout gates

Before writing the closeout, run a RED existence/content gate so the closeout has evidence:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-PIPE-009_sprint-closeout.md')
assert path.exists(), 'RED: Sprint 009 closeout doc missing'
PY
```

Expected RED before the closeout exists.

After writing the closeout, run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('docs/outcomes/BLK-PIPE-009_sprint-closeout.md').read_text()
required = [
    'BLK-pipe Sprint 009',
    'Task 1',
    'Task 2',
    'Task 3',
    'Task 4',
    'Task 5',
    'BLK-PIPE-008 owns physical HIGH-1 / HIGH-2 closure',
    'Sprint 009 owns doctrine/gate closure',
    'python3 -m unittest discover -s python -p',
    'go test ./...',
    'go vet ./...',
    'git diff --check',
    'No Hindsight tools were used',
    'Sprint 009 did not run Codex',
    'Sprint 009 did not call live BLK-test MCP',
    'Sprint 009 did not generate RTM or publish authoritative BEOs',
]
missing = [item for item in required if item not in text]
assert not missing, f'SPRINT009_CLOSEOUT_CONTENT_FAIL missing={missing}'
print('SPRINT009_CLOSEOUT_CONTENT_PASS')
PY
```

Then run final verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
git diff --check
git status --short --branch
```

Commit:

```bash
git add docs/outcomes/BLK-PIPE-009_sprint-closeout.md
git commit -m "docs: close out blk-pipe sprint 009"
```

Push only after final verification passes and the local branch is ready:

```bash
git push origin main
```

---

## 12. Final Acceptance Criteria

Sprint 009 is complete only when all criteria are true:

- `docs/BLK-003_blk-pipe-blk-test-orchestration.md` uses full synthetic canonical hashes in strict BEB YAML examples and has safe §10 escalation boundary language.
- `docs/BLK-006_blk-req-implementation-brief.md` separates new-draft and staged-revision hash lifecycle examples and no longer teaches fake DRAFT `sha256:...` values.
- `docs/BLK-008_blk-test-mcp-execution-server.md` says BLK-008 is target-state planning doctrine, not current live MCP authorization, and cross-links current disabled/source-bound fixture docs.
- Sprint 006 has a post-closeout hostile-review amendment linked from the original closeout.
- The Sprint 006 hostile-review source docs are committed under `docs/reviews/`.
- Persistent doctrine gates pass:

  ```bash
  python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
  ```

- Full verification passes:

  ```bash
  python3 -m unittest discover -s python -p 'test_*.py'
  go test ./...
  go vet ./...
  go run ./cmd/blk-pipe --health
  git diff --check
  ```

- Task outcome documents exist for Tasks 1-5.
- `docs/outcomes/BLK-PIPE-009_sprint-closeout.md` exists and records final evidence.
- No live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication occurred.

---

## 13. Recommended Next Sprint Seed

Only after BLK-PIPE-008 and BLK-PIPE-009 are both closed should planning consider the next narrow slice.

Recommended next seed, if all physical and doctrine trace gates are green:

```text
BLK-PIPE-010 — BLK-test MCP Target-State Readiness Review and Fixture-to-Live Gap Register
```

That future sprint should still be a review/design sprint unless it explicitly adds mechanical authorization, sandbox/capability controls, and live-MCP safety gates. It must not silently enable live BLK-test MCP, authoritative BEO publication, or RTM authority.
