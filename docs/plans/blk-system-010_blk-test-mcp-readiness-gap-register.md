# blk-system-010 — BLK-test MCP Target-State Readiness Review and Fixture-to-Live Gap Register

> **For Hermes:** Use `blk-system-sprint-execution` to implement this plan task-by-task. This is a deterministic local review/design sprint. Do not use Hindsight. Do not run live Codex, live tactical LLMs, network model services, cyber tooling, live BLK-test MCP, RTM generation, RTM authority, active BLK-req vault reads, or authoritative BEO publication.

**Sprint ID:** `blk-system-010`
**Component emphasis:** BLK-test MCP readiness and system authority boundaries, not a `blk-pipe` component sprint.
**Goal:** Produce a BLK-001-aligned readiness review and fixture-to-live gap register for future BLK-test MCP work without authorizing live MCP, BEO, RTM, Codex, tactical LLM, cyber, or active-vault behavior.

**Architecture:** This sprint treats BLK-test as the BLK-001 right-side Physics Oracle and audits the current fixture-only chain against the future target-state MCP server. The deliverable is a set of deterministic review artifacts and persistent gates that say exactly what must be true before a later sprint may implement or authorize live BLK-test MCP. The sprint deliberately preserves BLK-001 separation of concerns: `blk-req` is the legislative gateway, Hermes is the architect/router, `blk-pipe` is the deterministic forge/blast shield, `blk-test` is the physics oracle, and RTM generation is a separate ledger.

**Tech Stack:** Markdown review/design artifacts, dependency-free Python `unittest` gates, existing BLK-System Python fixture modules, Go verification for `blk-pipe` regression guard only.

---

## 0. Current Known State

Repository:

```text
/home/dad/BLK-System
```

Planning preflight when this document was authored:

```text
date                         -> 2026-05-06 08:11:14 AEST
git status --short --branch  -> ## main...origin/main
HEAD                         -> 1e96d5c docs: close out blk-pipe sprint 009
```

Naming correction:

- The Sprint 009 closeout recommended `BLK-PIPE-010` as a seed, but the next sprint scope is system-level BLK-test MCP readiness, not `blk-pipe` component work.
- This plan therefore uses `blk-system-010` / `BLK-SYSTEM-010` naming for files and outcome artifacts.
- `BEB` remains the BLK-native execution brief artifact type and `beb_id` remains the payload/trace field, but the sprint itself is not named `BEB_010`.

Source doctrine to align:

```text
docs/BLK-001_blk-system-master-architecture.md
docs/BLK-003_blk-pipe-blk-test-orchestration.md
docs/BLK-008_blk-test-mcp-execution-server.md
docs/BLK-013_blk-test-handoff-fixture-contract.md
docs/BLK-014_blk-execution-outcome-fixture-shape.md
docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md
docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md
docs/outcomes/BLK-PIPE-008_sprint-closeout.md
docs/outcomes/BLK-PIPE-009_sprint-closeout.md
```

---

## 1. BLK-001 Intent Alignment Contract

Sprint 010 must explicitly preserve the intent of BLK-001:

| BLK-001 domain | Intent to preserve | Sprint 010 implication |
| --- | --- | --- |
| `blk-req` Legislative Gateway | Requirements/use cases are HITL-authorized, linted, baselined, and stored as immutable active-vault artifacts. | Do not read or parse protected active vault bodies in this sprint. Treat trace metadata as opaque unless future RTM work explicitly authorizes vault comparison. |
| Architecture & Feature Planning | Hermes translates baselined laws into bounded BEB and `l2_packet` payloads. | Do not make BLK-test an architect, router, scope decider, or requirement interpreter. BLK-test readiness artifacts only define verification mechanics. |
| `blk-pipe` Blast Shield & Forge | `blk-pipe` is deterministic transport, isolation, timebox, and Git allowlist enforcement. | Do not ask BLK-test MCP to mutate source, stage files, commit, or replace `blk-pipe` authority. BLK-test consumes already-produced execution evidence. |
| `blk-test` Physics Oracle | BLK-test verifies physical reality and returns deterministic PASS/FAIL evidence with compressed logs. | Future live MCP must be a fixed-tool, no-arbitrary-shell physics oracle only. Sprint 010 may review/design this; it must not run live MCP. |
| RTM Aggregator Ledger | Offline RTM generation compares BEO trace hashes against active-vault hashes and flags drift. | Do not generate RTM, publish authoritative BEOs, or grant drift rejection authority. Record gaps and prerequisites for a later RTM sprint. |
| Cryptographic baton | `version_hash` is the only bridge across isolated domains. | Preserve non-empty canonical `trace_artifacts[*].version_hash == sha256:<64-lowercase-hex>` for PASS/FAIL-shaped evidence and exact source binding across request/response/BEO fixture paths. |

Sprint 010 passes alignment only if every deliverable says what authority it does **not** grant.

---

## 2. Decision Register

| Decision ID | Question | Decision | Rationale | Implementation effect |
| --- | --- | --- | --- | --- |
| DEC-001 | Is Sprint 010 a `blk-pipe` component sprint? | **No. It is `blk-system-010`.** | The next frontier crosses BLK-test, BEO, RTM, approval, sandbox, and source-binding boundaries. It is system-level readiness, not `blk-pipe` implementation. | Use `BLK-SYSTEM-010` prefixes for review/outcome docs. Do not create `BLK-PIPE-010` artifacts. |
| DEC-002 | Does Sprint 010 authorize live BLK-test MCP? | **No.** | BLK-008 is target-state planning doctrine; BLK-013/014/015/016 keep current operation fixture-only/disabled. | Write readiness/gap artifacts and gates only. |
| DEC-003 | Should Sprint 010 create an MCP server skeleton? | **No, not in this sprint.** | A skeleton can silently become authority if transport, approval, workspace, and secret boundaries are not settled first. | Treat implementation as a later sprint candidate after the gap register is approved. |
| DEC-004 | Should BLK-test MCP approval reuse `codex-live` approval semantics? | **No direct reuse.** | BLK-test is a physics oracle, not tactical implementation. Its approval token/channel must bind source evidence and MCP tool profile, not just tactical BEB dispatch. | Produce an approval-gap section and future token-shape requirements; do not implement a token yet. |
| DEC-005 | Should BLOCKED evidence be allowed to feed BEO/RTM success paths? | **No.** | BLK-001's trace ledger must not launder failed or incomplete source evidence. | Persistent gates should preserve the PASS/FAIL vs BLOCKED distinction. |

---

## 3. Non-Goals and Hard Blocks

Sprint 010 must not implement, invoke, or imply:

- live BLK-test MCP transport;
- live MCP client/server startup;
- authoritative BLK-test verdict authority;
- authoritative BEO publication;
- RTM generation;
- RTM drift rejection authority;
- active BLK-req vault reads or requirement-body parsing;
- live Codex execution;
- live tactical LLM API calls;
- network model services;
- cyber tooling or cyber execution;
- execution against real cyber-program repositories or live targets;
- production sandbox/container/cgroup/VM enforcement claims;
- production host-secret isolation claims;
- production approval-channel mechanics.

Allowed work:

```text
deterministic local Python gates
Markdown readiness review artifacts
fixture-to-live gap register
BLK-001 alignment matrix
source-binding and approval-boundary decision records
future-sprint decomposition
outcome documents and closeout evidence
```

---

## 4. Invariants to Preserve

1. BLK-System sprint naming uses `BLK-SYSTEM-###` / `blk-system-###` for system-level work. Use `BLK-PIPE-###` only for `blk-pipe` component-specific sprints.
2. `BEB` and `BEO` are artifact types, not sprint IDs.
3. `blk-test` remains the deterministic physics oracle; it does not mutate source, choose architecture, publish BEOs, generate RTM, or read active vault bodies.
4. BLK-test MCP target-state tools must be fixed, validated, and bounded. No arbitrary shell tool.
5. Live MCP remains disabled until a later sprint explicitly authorizes transport and mechanically enforces that boundary.
6. PASS/FAIL-shaped evidence requires exact source binding: `beb_id`, source `commit_hash`, `pre_engine_hash`, `trace_artifacts`, test profile, and non-empty checks.
7. PASS/FAIL-shaped evidence requires non-empty canonical trace artifacts with `sha256:<64-lowercase-hex>` hashes.
8. BLOCKED may preserve trace absence only as blocked/non-authoritative evidence and must not project to success BEO or RTM evidence.
9. Draft-only BEO fixtures remain `beo_publication: "DRAFT_ONLY"` and `rtm_status: "NOT_GENERATED"`.
10. RTM generation and drift rejection remain separate future authority, not hidden inside BLK-test MCP.
11. New docs must preserve BLK-001's isolated-domain model and the cryptographic `version_hash` baton.
12. No production `git add .`, `git add -u`, `git stash`, broad staging, or unreviewed generated cache commits.

---

## 5. Controller Workflow for Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   ```

2. Read the task's exact source docs before editing.
3. Use deterministic RED/GREEN gates for every persistent doctrine/review invariant.
4. Write or patch only the files named in the task.
5. Run focused verification listed in the task.
6. Run shared verification before each implementation commit:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   python3 -m unittest discover -s python -p 'test_*.py'
   go test ./...
   go vet ./...
   git diff --check
   ```

7. Create a matching outcome document for Tasks 1-5:

   ```text
   docs/outcomes/BLK-SYSTEM-010_task-00N-outcome.md
   ```

8. Use the sprint closeout document as Task 6 outcome:

   ```text
   docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md
   ```

9. Remove generated Python caches before exact-path staging:

   ```bash
   rm -rf python/__pycache__
   ```

10. Commit each task after verification with the listed commit message. Do not push until closeout unless the human explicitly asks.

---

## 6. Task 1 — Add BLK-001 Alignment Gate and Review Artifact

### Objective

Create the sprint's governing BLK-001 alignment review so all later tasks are judged against the V-Model separation of concerns and cryptographic baton intent.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-010_blk001-alignment-review.md`
- `docs/outcomes/BLK-SYSTEM-010_task-001-outcome.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

### Required behavior

The review artifact must include:

- all five BLK-001 operational domains;
- the phrase `cryptographic version_hash baton`;
- a clear statement that Sprint 010 does not authorize live BLK-test MCP;
- a clear statement that Sprint 010 does not authorize authoritative BEO publication;
- a clear statement that Sprint 010 does not authorize RTM generation or drift rejection;
- a clear statement that BLK-test must not mutate source or replace `blk-pipe`;
- a clear statement that BLK-test must not read protected BLK-req vault bodies in this sprint.

### TDD steps

#### Step 1 — RED: add the BLK-001 alignment artifact gate

Add constants and a test similar to:

```python
SPRINT010_ALIGNMENT = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_blk001-alignment-review.md"


def test_sprint010_blk001_alignment_review_preserves_v_model_intent(self):
    self.assertTrue(SPRINT010_ALIGNMENT.exists(), "Sprint 010 BLK-001 alignment review missing")
    text = SPRINT010_ALIGNMENT.read_text()
    required = [
        "blk-req",
        "Architecture & Feature Planning",
        "blk-pipe",
        "blk-test",
        "Traceability Aggregator",
        "cryptographic version_hash baton",
        "does not authorize live BLK-test MCP",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
        "does not authorize RTM drift rejection authority",
        "must not mutate source",
        "must not read protected BLK-req vault bodies",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 010 BLK-001 alignment markers missing: {missing}")
```

Run:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected RED: fails because `BLK-SYSTEM-010_blk001-alignment-review.md` does not exist.

#### Step 2 — GREEN: write the alignment review

Create `docs/reviews/BLK-SYSTEM-010_blk001-alignment-review.md` with sections:

1. Scope and source documents.
2. BLK-001 domain-by-domain intent summary.
3. Sprint 010 authority denied list.
4. BLK-test MCP readiness implications.
5. Pass/fail criteria for this sprint.

Rerun:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Expected GREEN: new Sprint 010 BLK-001 alignment test passes.

#### Step 3 — Outcome and shared verification

Create `docs/outcomes/BLK-SYSTEM-010_task-001-outcome.md` with RED/GREEN evidence and non-execution statement.

Run shared verification.

#### Step 4 — Commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-010_blk001-alignment-review.md \
  docs/outcomes/BLK-SYSTEM-010_task-001-outcome.md
git commit -m "docs: add blk-system sprint 010 alignment gate"
```

---

## 7. Task 2 — Build Fixture-to-Live Gap Register

### Objective

Document the exact gaps between current fixture-only BLK-test behavior and any future live BLK-test MCP path.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md`
- `docs/outcomes/BLK-SYSTEM-010_task-002-outcome.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

### Required gap categories

The register must include at least these categories:

1. MCP transport lifecycle.
2. Fixed tool registry and no arbitrary shell.
3. Workspace clone/isolation and teardown.
4. Locking and parallel execution prevention.
5. Process tree kill/timeout/flood behavior.
6. Output compression and token-flood bounds.
7. Source evidence binding from BLK-pipe report to BLK-test request.
8. PASS/FAIL/BLOCKED status mapping.
9. BEO draft-only boundary.
10. RTM non-generation and future ledger boundary.
11. Approval-channel mechanics.
12. Secret/network isolation policy.
13. Active BLK-req vault read prohibition/current limitation.
14. Audit logging and replay evidence.
15. Future implementation slice recommendations.

### TDD steps

#### Step 1 — RED: add gap-register coverage gate

Add a test requiring the categories above and denying authority expansion:

```python
SPRINT010_GAP_REGISTER = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_fixture-to-live-gap-register.md"


def test_sprint010_fixture_to_live_gap_register_is_complete(self):
    self.assertTrue(SPRINT010_GAP_REGISTER.exists(), "Sprint 010 fixture-to-live gap register missing")
    text = SPRINT010_GAP_REGISTER.read_text()
    required = [
        "MCP transport lifecycle",
        "Fixed tool registry",
        "no arbitrary shell",
        "Workspace clone/isolation and teardown",
        "Locking and parallel execution prevention",
        "Process tree kill/timeout/flood behavior",
        "Output compression",
        "Source evidence binding",
        "PASS/FAIL/BLOCKED",
        "BEO draft-only boundary",
        "RTM non-generation",
        "Approval-channel mechanics",
        "Secret/network isolation policy",
        "Active BLK-req vault read prohibition",
        "Audit logging and replay evidence",
        "does not authorize live BLK-test MCP",
    ]
    missing = [marker for marker in required if marker not in text]
    self.assertEqual(missing, [], f"Sprint 010 gap register markers missing: {missing}")
```

Expected RED: missing register.

#### Step 2 — GREEN: write the gap register

Create the register with one table:

```markdown
| Gap ID | Current fixture behavior | Target-state requirement | BLK-001 domain protected | Blocking risk | Required future gate | Candidate future sprint |
| --- | --- | --- | --- | --- | --- | --- |
```

Each row must separate current fixture evidence from future authority.

#### Step 3 — Outcome and shared verification

Create the Task 2 outcome doc and run shared verification.

#### Step 4 — Commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md \
  docs/outcomes/BLK-SYSTEM-010_task-002-outcome.md
git commit -m "docs: record blk-test fixture to live gap register"
```

---

## 8. Task 3 — Approval and Authority Boundary Decision Register

### Objective

Define what a future BLK-test MCP approval boundary must bind before live transport can be considered, without implementing approval mechanics.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md`
- `docs/outcomes/BLK-SYSTEM-010_task-003-outcome.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

### Required decisions

The decision register must state:

- `codex-live` approval is not BLK-test MCP approval;
- BLK-test MCP approval must bind the source BLK-pipe report identity and test profile;
- live BLK-test MCP approval must require human authorization before transport startup;
- approval must not grant arbitrary shell, source mutation, BEO publication, RTM generation, or active-vault read authority;
- approval record must include `beb_id`, source `commit_hash`, `pre_engine_hash`, canonical `trace_artifacts`, requested fixed BLK-test tool(s), target branch/workspace identity, timeout/output profile, and operator identity/approval timestamp when implemented;
- Sprint 010 records requirements only and does not implement approval-channel mechanics.

### TDD steps

#### Step 1 — RED: add approval-boundary gate

Add a test requiring the markers above.

Expected RED: missing decision register.

#### Step 2 — GREEN: write the decision register

Create a decision table:

```markdown
| Decision ID | Boundary question | Decision | BLK-001 rationale | Future mechanical gate |
| --- | --- | --- | --- | --- |
```

Include a blocked-token example for future design only, but do not define it as executable.

#### Step 3 — Outcome and shared verification

Create Task 3 outcome and run shared verification.

#### Step 4 — Commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md \
  docs/outcomes/BLK-SYSTEM-010_task-003-outcome.md
git commit -m "docs: define blk-test mcp authority boundaries"
```

---

## 9. Task 4 — Sandbox, Workspace, and Tool Capability Readiness Spec

### Objective

Produce a readiness spec for the future live BLK-test MCP environment without implementing or claiming production sandbox authority.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md`
- `docs/outcomes/BLK-SYSTEM-010_task-004-outcome.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

### Required content

The spec must cover:

- stdio-only MCP transport readiness;
- fixed tool list and Zod/schema validation;
- no dynamic command execution tool;
- hardlink/same-filesystem clone decision and fallback;
- startup purge, per-run teardown, stale lockfile behavior;
- single-run mutex/lock and parallel prevention;
- child process group kill behavior;
- timeout and output-flood response;
- cache jailing and environment scrubbing;
- network policy and secret exposure policy;
- primary repo corruption prevention;
- evidence artifacts required for replay;
- explicit statement that this spec is not production sandbox/cgroup/VM enforcement.

### TDD steps

#### Step 1 — RED: add sandbox-readiness gate

Add a test requiring all markers above.

Expected RED: missing spec.

#### Step 2 — GREEN: write the spec

Create sections:

1. Boundary statement.
2. Workspace lifecycle requirements.
3. Tool capability registry requirements.
4. Process/resource controls.
5. Cache/network/secret policy requirements.
6. Evidence and replay requirements.
7. Future implementation gates.

#### Step 3 — Outcome and shared verification

Create Task 4 outcome and run shared verification.

#### Step 4 — Commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md \
  docs/outcomes/BLK-SYSTEM-010_task-004-outcome.md
git commit -m "docs: specify blk-test mcp readiness controls"
```

---

## 10. Task 5 — Future Sprint Slicing and Doctrine Cross-Reference Gate

### Objective

Convert the gap register into safe future sprint candidates and add a persistent gate preventing docs from implying Sprint 010 authorized live BLK-test/BEO/RTM behavior.

### Files

Create:

- `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md`
- `docs/outcomes/BLK-SYSTEM-010_task-005-outcome.md`

Modify:

- `python/test_active_doctrine_review_gates.py`

Optionally modify if the deterministic gate proves a missing cross-reference:

- `docs/BLK-008_blk-test-mcp-execution-server.md`
- `docs/BLK-015_blk-pipe-approval-and-mcp-integration-design.md`
- `docs/BLK-016_disabled-blk-test-mcp-adapter-smoke-and-beo-rtm-interface-fixtures.md`

Do not patch active doctrine unless the RED gate proves the cross-reference is missing or misleading.

### Required future sprint candidates

The slicing document must separate at least these candidate future sprints:

1. `BLK-SYSTEM-011` — BLK-test MCP disabled live-transport skeleton, still non-executing.
2. `BLK-SYSTEM-012` — Workspace isolation and process-control implementation probes.
3. `BLK-SYSTEM-013` — Approval-channel and source-evidence authorization mechanics.
4. `BLK-SYSTEM-014` — First live fixed-tool BLK-test MCP smoke under explicit human approval.
5. `BLK-SYSTEM-015` — Draft BEO publication gate review, still not authoritative unless explicitly approved.
6. Later RTM sprint — offline RTM generation and drift rejection, separate from BLK-test MCP.

Each candidate must include:

- allowed scope;
- explicit non-goals;
- prerequisite gates;
- BLK-001 domain protected;
- stop condition.

### TDD steps

#### Step 1 — RED: add future-slicing and no-authority gate

Add tests requiring the future sprint candidates and verifying Sprint 010 docs include non-authorization markers.

Example gate:

```python
SPRINT010_SLICING = ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_future-sprint-slicing.md"
SPRINT010_REVIEW_DOCS = [
    SPRINT010_ALIGNMENT,
    SPRINT010_GAP_REGISTER,
    ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_approval-and-authority-decision-register.md",
    ROOT / "docs" / "reviews" / "BLK-SYSTEM-010_sandbox-capability-readiness-spec.md",
    SPRINT010_SLICING,
]


def test_sprint010_review_docs_do_not_authorize_live_authority(self):
    forbidden_missing = []
    required = [
        "does not authorize live BLK-test MCP",
        "does not authorize authoritative BEO publication",
        "does not authorize RTM generation",
    ]
    for path in SPRINT010_REVIEW_DOCS:
        text = path.read_text()
        missing = [marker for marker in required if marker not in text]
        if missing:
            forbidden_missing.append(f"{path.relative_to(ROOT)} missing {missing}")
    self.assertEqual(forbidden_missing, [])
```

Expected RED until all review docs exist and carry non-authorization markers.

#### Step 2 — GREEN: write future slicing and patch only proven cross-reference gaps

Create future slicing doc. If needed, patch active doctrine to reference the Sprint 010 gap register as a planning artifact, not authority.

#### Step 3 — Outcome and shared verification

Create Task 5 outcome and run shared verification.

#### Step 4 — Commit

```bash
git add python/test_active_doctrine_review_gates.py \
  docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md \
  docs/outcomes/BLK-SYSTEM-010_task-005-outcome.md
# Add active doctrine docs only if actually modified by a proven RED/GREEN gate.
git commit -m "docs: slice future blk-system readiness sprints"
```

---

## 11. Task 6 — Closeout and Final Verification

### Objective

Close Sprint 010 with audit-grade evidence, source artifact links, and a BLK-001 alignment verdict.

### Files

Create:

- `docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md`

Do not create `BLK-PIPE-010` or `BEB_010` sprint artifacts.

### Required closeout content

The closeout must include:

- status/date/sprint ID;
- commits for Tasks 1-5;
- BLK-001 alignment verdict;
- links to all Sprint 010 review artifacts;
- fixture-to-live gap summary;
- explicit non-execution statement;
- remaining blocked scope before live BLK-test MCP;
- recommended next sprint seed using `BLK-SYSTEM-011`, not `BLK-PIPE-011`;
- final verification evidence.

### RED/GREEN closeout gate

Before writing closeout:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md')
assert path.exists(), 'RED: Sprint 010 closeout doc missing'
PY
```

Expected RED.

After writing closeout, run:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md')
text = path.read_text()
required = [
    'BLK-SYSTEM-010',
    'BLK-001 alignment verdict',
    'does not authorize live BLK-test MCP',
    'does not authorize authoritative BEO publication',
    'does not authorize RTM generation',
    'BLK-SYSTEM-011',
]
missing = [marker for marker in required if marker not in text]
assert not missing, missing
print('SPRINT010_CLOSEOUT_CONTENT_PASS')
PY
```

Expected GREEN.

### Final verification

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
rm -rf python/__pycache__
git status --short --branch
```

### Commit and push discipline

Commit:

```bash
git add docs/outcomes/BLK-SYSTEM-010_sprint-closeout.md
git commit -m "docs: close out blk-system sprint 010"
```

Push only after final verification and human approval or explicit instruction:

```bash
git push origin main
git status --short --branch
```

---

## 12. Sprint 010 Acceptance Criteria

Sprint 010 is complete only when:

1. `docs/reviews/BLK-SYSTEM-010_blk001-alignment-review.md` exists and passes its gate.
2. `docs/reviews/BLK-SYSTEM-010_fixture-to-live-gap-register.md` exists and covers all required gap categories.
3. `docs/reviews/BLK-SYSTEM-010_approval-and-authority-decision-register.md` exists and separates BLK-test MCP approval from `codex-live` approval.
4. `docs/reviews/BLK-SYSTEM-010_sandbox-capability-readiness-spec.md` exists and explicitly avoids production sandbox claims.
5. `docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md` exists and uses `BLK-SYSTEM-011+` future sprint naming.
6. Persistent deterministic gates prevent Sprint 010 review docs from implying live BLK-test MCP, authoritative BEO, or RTM authority.
7. Outcome docs exist for Tasks 1-5 and closeout.
8. Shared verification passes.
9. The final closeout states that Sprint 010 is BLK-001-aligned because it preserves isolated domains and the cryptographic baton without expanding authority.

---

## 13. Recommended Next Sprint Seed After Closeout

If Sprint 010 closes cleanly, the next safe seed is probably:

```text
BLK-SYSTEM-011 — Disabled BLK-test MCP Live-Transport Skeleton and Non-Executing Handshake Gate
```

That future sprint should still be non-executing unless it separately proves and receives approval for live fixed-tool execution. It should create a stdio MCP server skeleton only if the Sprint 010 gap register, approval-boundary decisions, and sandbox/capability requirements are accepted.
