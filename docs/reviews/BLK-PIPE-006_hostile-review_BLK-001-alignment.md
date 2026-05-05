# BLK-PIPE-006 Hostile Review — Outcomes and BLK-001 Alignment

**Repository:** `/home/dad/BLK-System`
**Review date:** 2026-05-05
**Scope:** `docs/plans/BLK-PIPE-006_blk001-alignment-remediation.md`, `docs/outcomes/BLK-PIPE-006*.md`, Sprint 006 commits `e0d8718..23f1a4a`, BLK-001, and current/as-closeout runtime + doctrine surfaces relevant to Sprint 006.
**No repo edits made.** Temporary probes only; repo ended clean/aligned with `origin/main`.

---

## Verdict

**Conditional pass, not clean.** BLK-PIPE-006 materially improved BLK-001 alignment by closing the Sprint 005 blockers: `codex-live` exact-token approvals are no longer executable, trace hash syntax is canonical where validated, disabled BLK-test MCP mappings are source-bound, active vocabulary/hard-deny docs were remediated, and outcome metadata is now gated.

But the sprint should **not** be treated as a full BLK-001 traceability signoff. The cryptographic baton is still optional at the BLK-pipe execution boundary, one BLK-test PASS/FAIL fixture path still accepts noncanonical trace hashes, and active doctrine still contains schema examples/escalation language that can seed invalid or authority-confusing future work.

---

## What passed

- Full current verification stack passed:
  - `python3 -m unittest discover -s python -p 'test_*.py'` → `Ran 113 tests`, `OK`
  - `go test ./...` → PASS
  - `go vet ./...` → PASS
  - `go run ./cmd/blk-pipe --health` → `{"status":"OK","component":"blk-pipe"}`
  - `git diff --check` → PASS
  - final repo status → `## main...origin/main`
- Sprint 006 outcome commit references are real: `COMMIT_REF_PASS 17 refs`.
- Outcome remote metadata gate passed for Sprint 005/006 headers: `OUTCOME_REMOTE_METADATA_PASS`.
- Active BLK-native vocabulary gate passed: `ACTIVE_DOC_VOCAB_PASS`.
- Sprint 006 no-live-token gate passed over the scoped runtime/design files: `NO_LIVE_EXECUTION_PASS`.
- Sprint 006 commit chain is coherent:
  - `555a872` Task 1 implementation
  - `5d6a823` Task 1 outcome
  - `890fa29` Task 2 implementation
  - `7cd2e11` Task 2 outcome
  - `ec34932` Task 3 implementation
  - `bac61a5` Task 3 outcome
  - `98939fe` Task 4 implementation
  - `58fad2b` Task 4 outcome
  - `52c1899` Task 5 implementation
  - `5f0559c` Task 5 outcome
  - `23f1a4a` sprint closeout

---

## Critical / high findings

### HIGH-1 — BLK-pipe still executes successfully with an empty `trace_artifacts` baton

**Why this matters:** BLK-001 says the system’s integrity relies on the unbroken canonical `version_hash` chain. Sprint 006 canonicalized trace hash syntax, but it did **not** require the trace baton to exist at the BLK-pipe execution boundary. A successful BLK-pipe run can still produce `trace_artifacts: []`.

**Evidence:**

- `internal/contracts/payload.go:183` validates `ValidateTraceArtifacts(p.TraceArtifacts)`.
- `internal/contracts/payload.go:217-244` rejects malformed entries but returns nil for zero entries.
- `internal/contracts/payload_test.go:9-19` defines `validPayload()` with no `TraceArtifacts`.
- `internal/contracts/payload_test.go:22-25` asserts that payload is valid.
- `internal/contracts/payload_test.go:353-358` accepts a clean V47 payload with no `trace_artifacts` field.
- This behavior existed at Sprint 006 closeout (`git show 23f1a4a:internal/contracts/payload.go`).

**Physical probe:**

```text
EMPTY_TRACE_EXECUTION_STATUS SUCCESS
EMPTY_TRACE_EXECUTION_TRACE_ARTIFACTS []
EMPTY_TRACE_EXECUTION_STAGED_FILES ['dry_run_output.txt']
```

**Impact:** A successful execution can be sterile from an allowlist perspective but untraceable from a BLK-001/RTM perspective. That means Sprint 006 fixed *syntax of supplied trace metadata*, not *presence of the cryptographic baton*.

**Recommended fix:** Add a dedicated execution-mode gate: for BEB/L2 execution payloads, require non-empty `trace_artifacts` with canonical hashes. If legacy/revert/dev-smoke paths must remain trace-optional, encode that exception explicitly by action/profile and make outcome docs stop implying universal trace-baton strictness.

---

### HIGH-2 — BLK-test PASS/FAIL handoff fixtures still accept noncanonical `version_hash` values

**Why this matters:** Sprint 006 invariant: PASS/FAIL-shaped BLK-test data must never exist without non-empty canonical trace evidence. The older `python/blk_test_handoff_fixtures.py` path still allows PASS-shaped handoff output with uppercase/noncanonical hashes.

**Evidence:**

- `python/blk_test_handoff_fixtures.py:118-119` requires non-empty trace artifacts for PASS/FAIL but does not validate canonical hash syntax.
- `python/blk_test_handoff_fixtures.py:154-173` copies `kind`, `id`, and `version_hash` without regex validation.
- `python/test_blk_test_handoff_fixtures.py` has preservation tests but no short/uppercase/nonhex negative tests for this path.

**Physical probe:**

```text
BLK_TEST_HANDOFF_CANONICAL_HASH_GAP accepted= sha256:AAAAAAAAAAAAA...
```

A downstream shield does exist:

```text
HANDOFF_STATUS PASS
BEO_PROJECTION_REJECTS_BAD_HANDOFF_TRACE trace_artifacts.version_hash must match sha256:<64-lowercase-hex>
```

So BEO projection rejects the bad handoff, but the PASS-shaped BLK-test handoff already existed, violating the stricter Sprint 006 invariant.

**Recommended fix:** Add canonical trace validation to `blk_test_handoff_fixtures._trace_artifacts(...)`, add tests for short/uppercase/nonhex hashes, and document that all BLK-test handoff surfaces share the same `sha256:<64-lowercase-hex>` contract.

---

### HIGH-3 — Active BLK-003 strict BEB frontmatter still shows invalid truncated `version_hash` examples

**Why this matters:** BLK-003 presents this as mandatory strict YAML frontmatter. Sprint 006 explicitly made `trace_artifacts[*].version_hash` canonical, but the active doctrine example still teaches invalid hashes.

**Evidence:**

```text
NONCANONICAL_ACTIVE_HASH_EXAMPLES_FOUND
docs/BLK-003_blk-pipe-blk-test-orchestration.md | 71 | sha256:7f8b9... | version_hash: "sha256:7f8b9..."
docs/BLK-003_blk-pipe-blk-test-orchestration.md | 74 | sha256:1a2b3... | version_hash: "sha256:1a2b3..."
```

This was also present at Sprint 006 closeout:

```text
git show 23f1a4a:docs/BLK-003_blk-pipe-blk-test-orchestration.md
70 version_hash: "sha256:7f8b9..."
73 version_hash: "sha256:1a2b3..."
```

**Recommended fix:** Replace with `sha256:<64-lowercase-hex>` placeholders or real 64-lowercase fixture hashes. Because this is strict frontmatter, do not use ellipsis examples.

---

## Medium findings

### MEDIUM-1 — BLK-006’s draft schema still conflicts with BLK-002 hashing lifecycle

**Why this matters:** BLK-002 says new drafts use `parent_hash: ""` and `version_hash: "PENDING"` until human approval/baseline promotion. BLK-006 shows a DRAFT schema with `parent_hash: "sha256:..."` and `version_hash: "sha256:..."`, which blurs new-draft vs staged-revision semantics and uses noncanonical placeholder hashes.

**Evidence:**

- BLK-002 draft schema: `docs/BLK-002_blk-req-artifact-lifecycle.md:24-28`
  - `parent_hash: ""`
  - `version_hash: "PENDING"`
  - `status: "DRAFT"`
- BLK-006 conflicting schema: `docs/BLK-006_blk-req-implementation-brief.md:24-30`
  - `parent_hash: "sha256:..."`
  - `version_hash: "sha256:..."`
  - `status: "DRAFT"`

**Recommended fix:** Split BLK-006 into two explicit schema examples:

1. New draft: `parent_hash: ""`, `version_hash: "PENDING"`.
2. Staged revision: canonical `parent_hash: "sha256:<64-lowercase-hex>"`, `version_hash: "PENDING"` until promotion.

---

### MEDIUM-2 — BLK-003 escalation procedure still implies BEO creation and BLK-test payload availability without current-boundary qualifiers

**Why this matters:** BLK-003 now correctly states that live BLK-test MCP, authoritative BEO publication, and RTM generation are disabled. But §10 still instructs Hermes to create a BEO document and include raw payloads from both `blk-pipe` and `blk-test` when the loop escalates. That is too authoritative/live-looking for the current disabled/draft-only boundary.

**Evidence:**

- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:186`: `Create the BEO document`.
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:187`: include raw JSON payloads from both `blk-pipe` and `blk-test`.
- Also present at closeout (`git show 23f1a4a:...` lines 185-186).

**Recommended fix:** Qualify §10: current implementation writes a human escalation package and, if needed, a draft-only BEO-shaped fixture. Include `blk-test` payload only when a source-bound fixture exists now or a future sprint authorizes live BLK-test.

---

### MEDIUM-3 — Outcome docs understate residual trace-readiness gaps

**Why this matters:** The closeout language is mostly careful (“improved alignment”, “non-live”), but the trace-baton section can be read as stronger than what code enforces. The true statement is: canonical syntax is required where the trace baton is supplied to the Sprint 006 hardened paths. It is not universally mandatory at all successful execution/PASS-shaped boundaries.

**Evidence:**

- Closeout says trace-baton strictness improved: `docs/outcomes/BLK-PIPE-006_sprint-closeout.md:49-56`, `75-77`.
- Findings HIGH-1 and HIGH-2 show residual optional/noncanonical paths.

**Recommended fix:** Add a follow-up note/outcome amendment or next sprint objective: “Make trace baton presence mandatory for BEB/L2 execution and all BLK-test PASS/FAIL handoff paths.”

---

## Alignment assessment against BLK-001

| BLK-001 principle | Sprint 006 status | Hostile verdict |
| --- | --- | --- |
| Hermes/Codex/compiled tools have separated authority | Improved: `codex-live` exact token is audit-only and non-executable. | Pass for Sprint 006 scope. |
| Tactical agent locked out of BLK-req vault | Improved: docs and Go allowlist hard-deny cover `docs/active/`, `docs/requirements/`, `docs/use_cases/`. | Pass. |
| Cryptographic `version_hash` baton bridges domains | Improved syntax validation, but baton is optional at BLK-pipe execution and malformed in BLK-test handoff fixture path. | Not clean. |
| BLK-test/BEO/RTM cannot self-authorize live authority | Improved: docs and stubs say disabled/draft-only. | Mostly pass; BLK-003 §10 needs qualifier. |
| Audit trail/outcome integrity | Good: commit refs exist, metadata gate passes, outcomes are coherent. | Pass with trace-readiness caveat. |

---

## Recommended next remediation slice

Create a narrow BLK-PIPE follow-up task:

**BLK-PIPE-00X — Mandatory Trace Baton Enforcement Across Execution and Handoff Boundaries**

Scope:

1. Make BEB/L2 execution payloads require non-empty `trace_artifacts` unless an explicitly named legacy/revert exception applies.
2. Add canonical hash validation to `python/blk_test_handoff_fixtures.py`.
3. Patch BLK-003 strict frontmatter examples and §10 escalation language.
4. Patch BLK-006 schema examples to match BLK-002 draft/revision lifecycle.
5. Add gates that fail on active strict YAML examples containing `sha256:...` or `sha256:<short/ellipsis>`.

---

## Commands/probes used

```text
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
go run ./cmd/blk-pipe --health
git diff --check
git status --short --branch
```

Custom probes:

```text
COMMIT_REF_PASS 17 refs
OUTCOME_REMOTE_METADATA_PASS
ACTIVE_DOC_VOCAB_PASS
NO_LIVE_EXECUTION_PASS
NONCANONICAL_ACTIVE_HASH_EXAMPLES_FOUND
EMPTY_TRACE_EXECUTION_STATUS SUCCESS
BLK_TEST_HANDOFF_CANONICAL_HASH_GAP accepted= sha256:AAAAAAAAAAAAA...
BEO_PROJECTION_REJECTS_BAD_HANDOFF_TRACE trace_artifacts.version_hash must match sha256:<64-lowercase-hex>
```
