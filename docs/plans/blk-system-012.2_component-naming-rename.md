# BLK-System 012.2 Component Naming Rename Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task. Preserve BLK-System exact-path commit discipline and hostile-review the result after each task.

**Sprint ID:** `BLK-SYSTEM-012.2`

**Goal:** Rename the Traceability Aggregator brand to `blk-link` and introduce explicit `blk-id` and `blk-relay` component names for identification and communication without changing runtime authority.

**Architecture:** This is a doctrine/naming sprint, not a behavior-enablement sprint. It updates BLK-001 vocabulary so the core components share a consistent lowercase `blk-*` naming theme, while preserving existing boundaries: `blk-id` records identity/provenance, `blk-relay` carries authenticated typed messages, `blk-link` names the future/offline RTM traceability ledger, and no component receives new live execution, publication, approval, active-vault mutation, or active-vault read authority.

**Tech Stack:** Markdown doctrine, Python repository text gates, Git.

---

## Live Preflight Facts

Captured before this reviewed/renamed plan revision:

```text
Date: 2026-05-06T19:17:02+10:00
Git status: ## main...origin/main
Untracked at capture:
  ?? docs/plans/blk-system-011.1_disabled-transport-metadata-hardening.md
  ?? docs/plans/blk-system-013_component-naming-rename.md
  ?? docs/reviews/BLK-SYSTEM-011.1_disabled-transport-hardening-source-review.md
HEAD: ef1574d docs: close out blk-system sprint 012
```

This plan supersedes the local untracked draft:

```text
docs/plans/blk-system-013_component-naming-rename.md
```

The implementation must use the renamed plan path:

```text
docs/plans/blk-system-012.2_component-naming-rename.md
```

## Existing Sprint-ID Reservation Guard

`BLK-SYSTEM-013` is already reserved by current doctrine for approval-channel and source-evidence authorization mechanics. This naming sprint MUST NOT reuse, overwrite, weaken, or reinterpret that reservation.

Known current references that must remain semantically intact:

```text
python/test_active_doctrine_review_gates.py:254-255
python/test_active_doctrine_review_gates.py:307-308
python/test_active_doctrine_review_gates.py:335
python/test_active_doctrine_review_gates.py:383
docs/reviews/BLK-SYSTEM-010_future-sprint-slicing.md:39
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md:22
docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md:64
```

## Non-Goals / Authority Guardrails

This sprint MUST NOT:

- implement live `blk-link` RTM generation;
- create, rename, or require existence of `generate_rtm.py`;
- grant `blk-test` active-vault read authority;
- grant `blk-relay` planning, approval, mutation, verification, or trace authority;
- grant `blk-id` authentication-provider implementation authority beyond doctrine naming;
- publish authoritative BEOs;
- create drift-rejection behavior outside the existing future/offline RTM boundary;
- rewrite historical review/outcome/plan artifacts solely to update old vocabulary;
- alter the existing `BLK-SYSTEM-013` approval/source-evidence handoff contract.

## Standard Execution / Git Guards

Before every task, run:

```bash
git fetch origin main
git status --short --branch
git diff --quiet
git diff --cached --quiet
```

Abort if there are staged changes or unexpected tracked edits. Known unrelated untracked files may exist and MUST NOT be staged unless their own sprint explicitly authorizes them:

```text
docs/plans/blk-system-011.1_disabled-transport-metadata-hardening.md
docs/reviews/BLK-SYSTEM-011.1_disabled-transport-hardening-source-review.md
```

Use exact-path staging only. Never use `git add .`. Avoid broad wildcard staging of current-doctrine files unless the cached file list is checked immediately and exactly matches the intended task files.

Use cache-safe pytest invocations and cleanup before final status checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider <test path> -q
rm -rf .pytest_cache python/__pycache__
git status --short --branch
```

Outcome docs should record verification performed before their commit. Do not try to embed the outcome doc's own final commit hash inside that same outcome doc; record post-push hash/status in the executor summary or later closeout.

---

## Desired Vocabulary

```text
blk-req    = requirements gateway / legislative source of truth
blk-id     = identity and provenance spine
blk-relay  = communication and authenticated signal routing
blk-pipe   = execution isolation / blast shield and forge
blk-test   = verification / physics oracle
blk-link   = offline traceability and RTM ledger closure
```

Short doctrine summary:

```text
blk-id establishes identity.
blk-relay carries authenticated typed messages.
blk-req baselines requirements.
blk-pipe isolates execution.
blk-test verifies reality.
blk-link proves traceability after authorized offline RTM implementation exists.
```

## Domain Matrix

| Domain | Owns | Must Not Own |
| --- | --- | --- |
| `blk-req` | Human-approved requirements and use-case baselines, linting, canonical hashing, active vault writes. | Tactical execution, test verdicts, RTM drift rejection. |
| Architecture & Feature Planning | Dependency mapping, BEB generation, `l2_packet` payload assembly. | Active-vault mutation, tactical code execution, authoritative test verdicts. |
| `blk-id` | Deterministic actor, artifact, source, approval, and provenance identity vocabulary. | Message transport, requirement mutation, execution, verification, RTM generation, approval decisions. |
| `blk-relay` | Typed payload routing, source-binding metadata preservation, communication events. | Planning, approval decisions, source-of-truth mutation, test verdicts, drift rejection, trace authority. |
| `blk-pipe` | POSIX isolation, allowlist enforcement, bounded tactical execution. | Requirement interpretation, HITL authorization, RTM generation. |
| `blk-test` | Native verification and deterministic PASS/FAIL/BLOCKED evidence. | Active-vault hash comparison, BEO publication, RTM generation, requirement mutation. |
| `blk-link` | Future/offline RTM generation, BEO trace hash to active-vault hash comparison, drift reporting. | Test execution, requirement approval, tactical mutation, message transport, BEO publication. |
| Cryptographic `version_hash` baton | Opaque source-bound trace evidence passed across isolated domains. | Body-derived inference outside the owning component; empty/malformed hash acceptance. |

---

## Task 0: Commit the renamed sprint plan

**Objective:** Make the reviewed `BLK-SYSTEM-012.2` plan durable before implementation and remove the stale local `BLK-SYSTEM-013` draft path.

**Files:**
- Add: `docs/plans/blk-system-012.2_component-naming-rename.md`
- Remove if present and untracked: `docs/plans/blk-system-013_component-naming-rename.md`

**Step 1: Verify only intended plan path is staged**

Run:

```bash
git status --short --branch
rm -f docs/plans/blk-system-013_component-naming-rename.md
git add -- docs/plans/blk-system-012.2_component-naming-rename.md
git diff --cached --name-only
```

Expected cached file list:

```text
docs/plans/blk-system-012.2_component-naming-rename.md
```

**Step 2: Commit and push the plan**

Run:

```bash
git commit -m "docs: plan blk-system component naming rename"
git push origin main
git rev-parse --short HEAD
git status --short --branch
```

Expected: push succeeds; remaining untracked files, if any, are only unrelated 011.1 artifacts.

---

## Task 1: Update BLK-001 component headings and traceability wording

**Objective:** Make `blk-link` the canonical current-doctrine name for the former Traceability Aggregator, add `blk-id` / `blk-relay`, and preserve the `version_hash` trust-baton invariant.

**Files:**
- Modify: `docs/BLK-001_blk-system-master-architecture.md`
- Create: `docs/outcomes/BLK-SYSTEM-012.2_task-001-outcome.md`

**Step 1: Preserve the trust-baton invariant while allowing identity/relay vocabulary**

Replace the current sentence:

```md
The only element bridging these isolated domains is the cryptographic `version_hash`.
```

with:

```md
The only trust-bearing trace baton crossing these isolated domains is the cryptographic `version_hash`; `blk-id` records identity/provenance and `blk-relay` carries typed messages, but neither creates truth, approval, mutation, verification, or trace authority.
```

**Step 2: Rename the Section 2 heading and update subsystem count wording**

Replace:

```md
## 2. Core Subsystems
```

with:

```md
## 2. Core Subsystems & Component Contracts
```

Then replace:

```md
The `blk-system` is composed of five strictly bounded operational domains:
```

with:

```md
The `blk-system` is composed of strictly bounded operational domains and named component contracts:
```

**Step 3: Insert `blk-id` and `blk-relay` as non-authorizing component contracts**

After `blk-req`, add:

```md
### 2.2. `blk-id` (The Identity Spine)
**Every actor and artifact has a stable name.**
* **Function:** Deterministic identity and provenance binding for humans, agents, requirements, use cases, briefs, outcomes, commits, approval events, and source systems.
* **Enforcement:** Canonical IDs, source-bound metadata, approved identity-provider references, and cryptographic hashes where applicable.
* **Mechanics:** Binds every meaningful action to an actor ID, artifact ID, source system, timestamp, and canonical hash without granting mutation or approval authority by itself.
* **Output:** Stable identity records that prove who approved what, which artifact was used, and which execution outcome inherited which requirement.

### 2.3. `blk-relay` (The Signal Bus)
**Controlled communication without authority.**
* **Function:** Routes authenticated messages, execution requests, status payloads, and HITL approvals between humans, Hermes, tactical agents, and BLK-System services.
* **Enforcement:** Typed payload schemas, deterministic routing rules, source binding, and metadata preservation.
* **Mechanics:** Accepts only structured payloads from approved sources, forwards them to the correct component, and records enough identity/provenance metadata for later traceability.
* **Output:** Validated communication events consumable by `blk-req`, Architecture & Feature Planning, `blk-pipe`, `blk-test`, and `blk-link`; `blk-relay` does not authorize the payload it carries.
```

**Step 4: Renumber the existing sections**

Use this final order:

```text
2.1 blk-req
2.2 blk-id
2.3 blk-relay
2.4 Architecture & Feature Planning
2.5 blk-pipe
2.6 blk-test
2.7 blk-link
```

**Step 5: Rename Traceability Aggregator to `blk-link`**

Rename the existing traceability heading to:

```md
### 2.7. `blk-link` (The Ledger)
```

Update its body to preserve future/offline implementation boundaries:

```md
**Closing the V-Model. Proving the trace.**
* **Function:** Offline Requirements Traceability Matrix (RTM) generation.
* **Enforcement:** Deterministic Python script contract (`generate_rtm.py`, future/offline implementation target) operating under the `blk-link` component name.
* **Mechanics:** Sweeps the repository post-execution. It cross-references the canonical hashes embedded in the Blk Execution Outcomes (BEOs) generated by `blk-test` against the live cryptographic hashes in the `blk-req` vault.
* **Output:** A mathematically proven RTM. It mechanically flags any BEO as a "Drift Rejection" if the underlying architectural constraint was altered mid-sprint.
```

Do not create `generate_rtm.py` and do not add a file-existence gate for it in this sprint.

**Step 6: Update the cryptographic baton reference**

Change:

```md
5. **Verification:** The RTM Aggregator confirms `BEO_010` matches the live vault hash for `REQ-042`.
```

to:

```md
5. **Verification:** `blk-link` confirms `BEO_010` matches the live vault hash for `REQ-042` after authorized offline RTM implementation exists.
```

**Step 7: Verify BLK-001 markers**

Run:

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/BLK-001_blk-system-master-architecture.md').read_text()
required = [
    '## 2. Core Subsystems & Component Contracts',
    'strictly bounded operational domains and named component contracts',
    'The only trust-bearing trace baton crossing these isolated domains is the cryptographic `version_hash`',
    '### 2.2. `blk-id` (The Identity Spine)',
    '### 2.3. `blk-relay` (The Signal Bus)',
    '### 2.7. `blk-link` (The Ledger)',
    'Deterministic Python script contract (`generate_rtm.py`, future/offline implementation target) operating under the `blk-link` component name',
    '`blk-link` confirms `BEO_010` matches the live vault hash for `REQ-042` after authorized offline RTM implementation exists',
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit('missing required BLK-001 markers: ' + repr(missing))
for forbidden in [
    '## 2. Core Subsystems\n',
    'five strictly bounded operational domains',
    'The only element bridging these isolated domains is the cryptographic `version_hash`.',
    '### 2.5. Traceability Aggregator (The Ledger)',
    'RTM Aggregator confirms',
    'BLK-Link',
]:
    if forbidden in text:
        raise SystemExit('stale BLK-001 wording remains: ' + forbidden)
print('BLK-001 naming markers OK')
PY
```

Expected: `BLK-001 naming markers OK`.

**Step 8: Create outcome, verify, commit, push**

Create `docs/outcomes/BLK-SYSTEM-012.2_task-001-outcome.md` with:

- summary of BLK-001 vocabulary changes;
- exact files changed;
- verification commands and PASS/BLOCKED state;
- statement that no live RTM, BEO publication, new transport, or identity-provider implementation was authorized.

Then run:

```bash
git diff --check
rm -rf .pytest_cache python/__pycache__
git add -- docs/BLK-001_blk-system-master-architecture.md docs/outcomes/BLK-SYSTEM-012.2_task-001-outcome.md
git diff --cached --name-only
git commit -m "docs: name blk-system identity relay and link components"
git push origin main
git rev-parse --short HEAD
git status --short --branch
```

Expected cached files only:

```text
docs/BLK-001_blk-system-master-architecture.md
docs/outcomes/BLK-SYSTEM-012.2_task-001-outcome.md
```

---

## Task 2: Add a current-doctrine-only naming drift gate

**Objective:** Prevent active/current doctrine from reverting to `BLK-Link`, `RTM Aggregator`, or unbranded `Traceability Aggregator` while preserving historical review/outcome wording.

**Files:**
- Create: `python/test_blk_component_naming.py`
- Create: `docs/outcomes/BLK-SYSTEM-012.2_task-002-outcome.md`

**Important historical-preservation rule:** Do not replace the `Traceability Aggregator` marker in `python/test_active_doctrine_review_gates.py:test_sprint010_blk001_alignment_review_preserves_v_model_intent`. That test preserves historical Sprint 010 review wording and is not the current-doctrine naming gate.

**Step 1: Create the focused naming test**

Create `python/test_blk_component_naming.py`:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLK001 = ROOT / "docs" / "BLK-001_blk-system-master-architecture.md"
CURRENT_DOCTRINE = sorted((ROOT / "docs").glob("BLK-*.md"))


def test_blk001_declares_canonical_component_names():
    text = BLK001.read_text(encoding="utf-8")
    required = [
        "`blk-id` (The Identity Spine)",
        "`blk-relay` (The Signal Bus)",
        "`blk-link` (The Ledger)",
        "version_hash",
        "does not authorize the payload it carries",
    ]
    missing = [marker for marker in required if marker not in text]
    assert missing == []


def test_current_blk_doctrine_uses_blk_link_not_stale_aggregator_names():
    assert CURRENT_DOCTRINE, "expected current BLK doctrine files"
    stale_terms = ("BLK-Link", "RTM Aggregator", "Traceability Aggregator")
    stale_hits = []
    for path in CURRENT_DOCTRINE:
        text = path.read_text(encoding="utf-8")
        for term in stale_terms:
            if term in text:
                stale_hits.append(f"{path.relative_to(ROOT)}: {term}")
    assert stale_hits == []
```

**Step 2: Run focused and related gates**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_blk_component_naming.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_active_doctrine_review_gates.py -q
rm -rf .pytest_cache python/__pycache__
git diff --check
```

Expected: PASS.

**Step 3: Create outcome, commit, push**

Create `docs/outcomes/BLK-SYSTEM-012.2_task-002-outcome.md` with:

- summary that a current-doctrine-only naming drift gate was added;
- explicit note that historical Sprint 010 review wording was preserved;
- verification results.

Then run:

```bash
git add -- python/test_blk_component_naming.py docs/outcomes/BLK-SYSTEM-012.2_task-002-outcome.md
git diff --cached --name-only
git commit -m "test: guard canonical blk component naming"
git push origin main
git rev-parse --short HEAD
git status --short --branch
```

Expected cached files only:

```text
python/test_blk_component_naming.py
docs/outcomes/BLK-SYSTEM-012.2_task-002-outcome.md
```

---

## Task 3: Verify/update narrow current-doctrine cross-references

**Objective:** Update any remaining current active-doctrine references to the old traceability name, while leaving historical reviews/outcomes/plans intact.

**Files:**
- Modify only exact current `docs/BLK-*.md` files that still contain stale current-doctrine names after Task 1.
- Create: `docs/outcomes/BLK-SYSTEM-012.2_task-003-outcome.md`
- Do not modify historical files under `docs/reviews/`, `docs/outcomes/`, or older `docs/plans/` just to modernize vocabulary.

**Step 1: Find current doctrine references**

Run:

```bash
python - <<'PY'
from pathlib import Path
terms = ['Traceability Aggregator', 'RTM Aggregator', 'BLK-Link']
for path in sorted(Path('docs').glob('BLK-*.md')):
    text = path.read_text(errors='replace')
    hits = [term for term in terms if term in text]
    if hits:
        print(path, hits)
PY
```

Expected after Task 1: no output. If there is output, update only the exact printed current-doctrine file paths.

**Step 2: Apply conservative replacements if needed**

Use these replacement rules only in current doctrine files:

```text
Traceability Aggregator -> `blk-link` ledger
RTM Aggregator -> `blk-link`
BLK-Link -> `blk-link`
```

Keep explanatory references to RTM generation, BEO hashes, active-vault hashes, and the future/offline `generate_rtm.py` contract intact.

**Step 3: Verify no stale current-doctrine naming remains**

Run:

```bash
python - <<'PY'
from pathlib import Path
bad = []
for path in sorted(Path('docs').glob('BLK-*.md')):
    text = path.read_text(errors='replace')
    for term in ['Traceability Aggregator', 'RTM Aggregator', 'BLK-Link']:
        if term in text:
            bad.append(f'{path}: {term}')
if bad:
    raise SystemExit('stale current doctrine naming remains:\n' + '\n'.join(bad))
print('current doctrine blk-link naming OK')
PY
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_blk_component_naming.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_active_doctrine_review_gates.py -q
rm -rf .pytest_cache python/__pycache__
git diff --check
```

Expected: PASS.

**Step 4: Create outcome, commit, push**

Create `docs/outcomes/BLK-SYSTEM-012.2_task-003-outcome.md` with:

- summary of any exact current-doctrine files updated, or explicit statement that no extra current-doctrine files required edits after Task 1;
- verification results;
- statement that historical artifacts were intentionally left untouched.

Stage exact touched files only. If no extra doctrine files were modified, stage only the outcome doc:

```bash
git add -- docs/outcomes/BLK-SYSTEM-012.2_task-003-outcome.md
```

If exact current-doctrine files were modified, stage only those exact paths plus the outcome doc:

```bash
git add -- <exact touched docs/BLK-*.md paths> docs/outcomes/BLK-SYSTEM-012.2_task-003-outcome.md
```

Then run:

```bash
git diff --cached --name-only
git commit -m "docs: verify blk-link active doctrine references"
git push origin main
git rev-parse --short HEAD
git status --short --branch
```

---

## Task 4: Create mandatory sprint closeout

**Objective:** Close the doctrine-only naming sprint with final verification evidence and an explicit non-authority statement.

**Files:**
- Create: `docs/outcomes/BLK-SYSTEM-012.2_sprint-closeout.md`

**Step 1: Run final verification**

Run:

```bash
git status --short --branch
git log -4 --oneline
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_blk_component_naming.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python/test_active_doctrine_review_gates.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider python -q
rm -rf .pytest_cache python/__pycache__
git diff --check
python - <<'PY'
from pathlib import Path
current = '\n'.join(p.read_text(errors='replace') for p in sorted(Path('docs').glob('BLK-*.md')))
required = ['`blk-id`', '`blk-relay`', '`blk-link`']
missing = [r for r in required if r not in current]
stale = [s for s in ['BLK-Link', 'RTM Aggregator', 'Traceability Aggregator'] if s in current]
if missing or stale:
    raise SystemExit(f'missing={missing} stale={stale}')
print('BLK-SYSTEM-012.2 closeout naming gate OK')
PY
```

Expected: PASS, or document exact unrelated/pre-existing failures as BLOCKED with output.

**Step 2: Write closeout**

Create `docs/outcomes/BLK-SYSTEM-012.2_sprint-closeout.md` with:

- sprint ID `BLK-SYSTEM-012.2`;
- plan path and plan commit hash if Task 0 committed it;
- task commit table for Tasks 1-3;
- final verification command list and PASS/BLOCKED state;
- final pre-closeout `git status --short --branch`;
- explicit statement that this sprint renamed doctrine vocabulary only and did not authorize live RTM, BEO publication, new message transport, identity-provider implementation, active-vault reads, or drift-rejection behavior;
- explicit statement that `BLK-SYSTEM-013` remains reserved for approval/source-evidence authorization mechanics.

Do not attempt to embed the closeout doc's own final commit hash inside itself. The executor summary after push should record the closeout commit hash.

**Step 3: Commit and push closeout**

Run:

```bash
git add -- docs/outcomes/BLK-SYSTEM-012.2_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close out blk-system component naming sprint"
git push origin main
git rev-parse --short HEAD
git status --short --branch
```

Expected cached files only:

```text
docs/outcomes/BLK-SYSTEM-012.2_sprint-closeout.md
```

---

## Expected End State

- The sprint is named `BLK-SYSTEM-012.2`, not `BLK-SYSTEM-013`.
- Existing `BLK-SYSTEM-013` future approval/source-evidence authorization semantics remain intact.
- BLK-001 names the canonical traceability component as `blk-link`, not `BLK-Link`, `RTM Aggregator`, or unbranded `Traceability Aggregator`.
- BLK-001 contains explicit `blk-id` and `blk-relay` component contracts with non-authority guardrails.
- BLK-001 no longer contradicts itself with "five strictly bounded operational domains" after adding new component contracts.
- BLK-001 preserves the `version_hash` trust-baton invariant while clarifying that `blk-id` and `blk-relay` do not create truth or authority.
- Current active doctrine references use `blk-link` for the traceability ledger.
- Historical reviews/plans/outcomes remain historically accurate unless they are active gates/templates.
- A deterministic current-doctrine-only test prevents naming drift without breaking historical preservation tests.
