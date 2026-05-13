# BLK-System Post-103 All-Codebase Hostile Review and Completion Roadmap

**Status:** Hostile review report and roadmap input — not sprint authority
**Date:** 2026-05-13T22:14:48+10:00
**Repository:** `/home/dad/BLK-System`
**Reviewed HEAD:** `070510f feat: execute blk-system 103 rtm trace closure`
**Scope:** All current BLK-System source and active doctrine surfaces: Go `blk-pipe`, Python fixtures/adapters/runtimes, active BLK docs, plans/outcomes/reviews used as current authority evidence, and roadmap/current-state indexes.

## 0. Non-Authority Boundary

This report is evidence and roadmap input only. It does not authorize source mutation, BLK-pipe execution, BLK-test runtime, Codex dispatch, BEB dispatch, BEO publication, RTM generation, RTM drift rejection, protected BLK-req body reads, public ledger mutation, signer/storage/rollback operations, target-repo scans, or Kuronode mutation. Every patch or higher-authority milestone below requires a separately approved plan/sprint boundary.

## 1. Executive Verdict

BLK-System is **not yet fit for the full BLK-001 target architecture as a production autonomous V-model system**.

It is, however, a strong L0/L1/L2-style authority-ladder codebase with many good local fixtures, closed-schema validators, hash-bound packages, explicit denial flags, and a working Go mutation blast shield. The main problem is that the codebase now contains both:

1. genuinely useful implementation evidence through BLK-SYSTEM-103, and
2. stale or incomplete authority surfaces that still describe older draft-only/offline-only states or leave critical guardrails as trusted-local assumptions.

The most serious implementation blocker is in Go `blk-pipe`: physical worktree snapshots read every regular file body, which can include protected BLK-req bodies. That violates the BLK-001/BLK-006 separation doctrine if `blk-pipe` is run against a repository containing `docs/active`, `docs/requirements`, or `docs/use_cases`.

The most serious doctrine blocker is that active BLK-001/003/005/006 and BLK-077/079 are no longer coherent after BLK-SYSTEM-100 and BLK-SYSTEM-103. They preserve old “draft-only” / “RTM disabled” wording while also recording exact record-only external BEO publication and local non-authoritative RTM trace closure. Future agents can quote the stale lines and make the wrong decision.

## 2. Review Evidence Captured

### 2.1 Repository inventory

At review time:

| Surface | Files | Lines |
| --- | ---: | ---: |
| Go | 32 | 13,088 |
| Python | 147 | 65,233 |
| Markdown | 937 | 133,884 |

### 2.2 Verification run

The following passed from `/home/dad/BLK-System`:

~~~text
python3 -m unittest discover -s python -p 'test_*.py'
Ran 982 tests in 30.840s
OK

go test ./...
PASS across cmd/blk-pipe and internal packages

go vet ./...
exit 0, no output

git diff --check
exit 0, no output
~~~

Final pre-report repository state before writing this file was clean at `main...origin/main`.

### 2.3 Methodology

- Read BLK-001 through BLK-006 first, then current roadmap/current-state docs BLK-024, BLK-077, BLK-079, BLK-080, and BLK-103.
- Ran full Python and Go test/vet verification.
- Ran static scans over `.go`, `.py`, and active docs for authority terms, subprocess/shell/eval/network/Git/protected-path patterns.
- Used independent focused review for Go `blk-pipe` and active roadmap/docs; Python review was completed locally with static scans and targeted source reads after an independent Python specialist review timed out.
- Classified findings as blocking authority drift, high-risk hardening, medium/low doctrine/test coverage debt, or positive alignment evidence.

## 3. Positive Alignment Evidence

These should be preserved while patching.

1. **Go `blk-pipe` preserves strong mutation-enforcement shape.** Exact allowlist staging is used instead of broad `git add .`/`git add -u`; revert validates target hash and ancestry; reports preserve trace and validation evidence.
2. **Trace artifact presence/shape is enforced for execute payloads.** `internal/contracts/payload.go` requires non-empty execute `trace_artifacts` and canonical `sha256:<64-lowercase-hex>` values.
3. **Protected allowlist descendants generally route to Exit 3.** Paths such as `docs/active/REQ-001.md` are rejected as `UNAUTHORIZED_FILE_MUTATION`, matching the Sprint 018/BLK-006 route requirement.
4. **Go process/environment hygiene is materially stronger than early doctrine.** Process groups, timeout/flood cleanup, Git env scrubbing, and SSH askpass/socket stripping are implemented. Do not overstate this as production sandboxing.
5. **Python authority fixtures are generally disciplined.** Many modules use closed schemas, exact ID/hash checks, exact denied-authority sets, false side-effect flags, bounded output, percent-decoding/normalization, and no live network/model/browser/cyber tooling.
6. **Current-state index has detailed BLK-100/101/102/103 surfaces.** The stale generic summaries need repair, but the detailed late surfaces do record the new local/non-authoritative boundaries.

## 4. Findings

### HR-001 — Critical — Go `blk-pipe` reads protected BLK-req body content during physical snapshots

**Evidence:**

- `internal/pipe/run.go:92` calls `snapshotPhysicalWorktree(...)` before engine execution.
- `internal/pipe/run.go:1354` calls `snapshotPhysicalWorktree(...)` for validation baseline.
- `internal/pipe/run.go:1410-1455` recursively walks the whole worktree except root `.git`.
- `internal/pipe/run.go:1471-1472` calls `os.ReadFile(entryPath)` for every regular file.
- BLK-006 lines 16-19 require protected BLK-req vault paths under `docs/active/`, `docs/requirements/`, and `docs/use_cases/` to be hard-denied without authorizing body reads.
- BLK-004 lines 12-13 say BLK-pipe validates trace metadata shape only and does not parse requirement/use-case bodies or verify hashes against BLK-req files.

**Why this is blocking:** BLK-001’s central promise is physical separation between requirements truth and tactical execution/mutation. A mutation guard that snapshots/copies protected bodies is still reading protected bodies, even if it does not parse them semantically. This violates the “no protected-body reads/copying/parsing/hashing” boundary and blocks using `blk-pipe` against any repo that contains a real protected BLK-req vault.

**Patch plan:**

1. Replace full-content physical snapshots with metadata-only snapshots for protected BLK-req prefixes.
2. Explicitly skip or hard-deny reads under `docs/active`, `docs/requirements`, and `docs/use_cases`, including exact directory roots and descendants.
3. Detect protected path mutation via Git/status/path metadata, not body reads.
4. Add regression tests using protected files with unreadable permissions and prove `blk-pipe` does not call `os.ReadFile` on them.
5. Add doctrine gate asserting “mutation detection never copies protected BLK-req body bytes.”

### HR-002 — Disposition updated — BLK-pipe timeout/output caps are caller-tunable defaults, not doctrine hard caps

**Evidence:**

- Defaults: `internal/contracts/payload.go:16-17` (`900` seconds, `52428800` bytes).
- Validation only rejects non-positive values: `internal/contracts/payload.go:222-227`.
- Runtime uses caller values: `internal/pipe/run.go:99-101` for engine timeout/output and `internal/pipe/run.go:201` for validation.
- Pre-disposition doctrine wording in BLK-003/004 described 15 minutes / 50MB as hard caps, while code already treated them as defaults.

**Operator disposition, 2026-05-14:** Keep caller-tunable caps as an intentional feature. The correct remediation is doctrine alignment, not rejecting/clamping values above 900 seconds or 52,428,800 bytes. BLK-003 and BLK-004 now state that 15 minutes / 50MB are defaults and that explicit finite `timeout_seconds` / `max_output_bytes` values may raise or lower caps for a bounded run.

**Residual guardrail:** Cap tuning is operational sizing only. It must remain visible in payload/report evidence and must not authorize broader file allowlists, protected BLK-req body reads, live BLK-test MCP, authoritative BEO publication, RTM generation, RTM drift rejection, or source mutation outside exact BLK-pipe allowlists.

### HR-003 — High — Execute payloads can run and commit with no validation gate

**Evidence:**

- Empty `validation_profiles` is accepted: `internal/contracts/payload.go:343-345`.
- Empty `validation_commands` is accepted: `internal/contracts/payload.go:353-365`.
- Empty commands resolve as success: `internal/contracts/payload.go:248-250` and `internal/validation/validation.go:47-52,100-101`.
- Python adapter also defaults missing validation to an empty list: `python/blk_pipe_adapter.py:243-247`.
- BLK-003 lines 120 and 127-128 require a global workspace syntax check and mechanical validation before commit.

**Why this is high risk:** `blk-pipe` can produce a commit without a syntax/validation command. That is incompatible with BLK-003’s “Syntax Gate” and undermines hostile audit reliability.

**Patch plan:** Require at least one repository-owned `validation_profiles` entry for execute payloads by default. If legacy `validation_commands` must remain, require an explicit trusted-local override field that is visible in reports and denied in autonomous/less-trusted boundaries.

### HR-004 — High — Active doctrine/current-state docs are stale and contradictory after BLK-SYSTEM-100/103

**Evidence:**

- `docs/BLK-001_blk-system-master-architecture.md:62` still says current BEO handling remains draft-only/design-only until later publication authority.
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:48,152,172` still frame current BEO handling as draft-only fixture output.
- `docs/BLK-005_blk-req-specification.md:30` states target drift rejection as an unconditional current `MUST`.
- `docs/BLK-006_blk-req-implementation-brief.md:80` says `generate_rtm.py` compares BEO hashes against live artifact files.
- BLK-SYSTEM-100 records exact external BEO publication execution as a record-only publication surface.
- BLK-SYSTEM-103 records exact local RTM trace-closure execution as non-authoritative local evidence.
- `docs/BLK-103_exact-local-rtm-trace-closure-execution.md:63-78` explicitly denies reusable/production `blk-link`, active-vault comparison, protected-body reads, and drift authority.

**Why this is blocking for roadmap clarity:** Master/orchestration docs can mislead future agents into thinking BEO handling is still only draft-only, or conversely that target RTM/drift mechanics are already active. The correct post-103 state is narrower and more nuanced.

**Patch plan:** Create a post-103 reconciliation sprint/doc update that patches BLK-001/003/005/006 overlays to distinguish:

- target architecture;
- BLK-SYSTEM-100 exact record-only external BEO publication;
- BLK-SYSTEM-103 exact local non-authoritative trace closure;
- still-denied authoritative signed/storage/ledger publication;
- still-denied reusable production `blk-link`, active-vault comparison, protected-body reads, and drift authority.

### HR-005 — High — BLK-077/BLK-079 lack a clean post-103 frontier and retain stale generic BEO/RTM summaries

**Evidence:**

- `docs/BLK-077_blk-system-post-078-roadmap.md:344` labels the “current roadmap status snapshot” as after BLK-SYSTEM-096.
- `docs/BLK-077...:452-454` frames gaps as after BLK-SYSTEM-096/098.
- `docs/BLK-077...:461` says “external publication and RTM remain unauthorized,” while lines 760-788 record BLK-SYSTEM-100 and 103.
- `docs/BLK-079_post-078-current-state-authority-index.md:24-25` still has `BEO_PUBLICATION_DISABLED_DRAFT_AND_FIXTURE_ONLY` and `RTM_RUNTIME_GENERATION_AND_DRIFT_REJECTION_DISABLED` top markers.
- `docs/BLK-079...:267-268` generic BEO/RTM rows omit the BLK-100 record-only external publication and BLK-103 local trace-closure evidence.
- `python/blk_current_state_authority_index.py:467-478` still models generic BEO/RTM surfaces as `draft_and_fixture_only` and `offline_fixture_only` even though lines 629-654 add detailed BLK-100/103 surfaces.

**Why this is high risk:** The operator-facing index has both stale and current facts. A future sprint selector can quote stale generic rows and select the wrong frontier.

**Patch plan:** Make **BLK-SYSTEM-104 — Post-103 Current-State Reconciliation and Frontier Selection Gate** the next safe sprint. It should update BLK-077/079 and `python/blk_current_state_authority_index.py`, add a post-103 frontier/stop-condition section, and move old post-096/post-098 guidance into historical appendix wording.

### HR-006 — Medium/High — Validation profiles and legacy validation commands still execute through `sh -c`

**Evidence:**

- `internal/validation/validation.go:29-32` documents shell interpretation.
- `internal/validation/validation.go:65-68` executes validation as `[]string{"sh", "-c", command}`.
- Repository profiles are shell command strings: `internal/validationprofiles/profiles.go:5-12`.
- Legacy `validation_commands` are explicitly retained as trusted-local compatibility: `internal/contracts/payload_test.go:224-236`.
- BLK-004 lines 16-17 say less-trusted/autonomous boundaries must use profiles and that profiles do not authorize arbitrary shell, network, package-manager, secret-reading, or protected-body reads.

**Why this matters:** Shell strings are acceptable only as a trusted-local compatibility rung. They are not fit for a production autonomous payload boundary without structured argv profiles and stricter capability controls.

**Patch plan:** Convert validation profile registry values from strings to structured argv/env specs. Keep shell-string legacy only behind a named trusted-local override that cannot appear in autonomous payloads.

### HR-007 — Medium — Protected exact directory roots slip through Go allowlist classification

**Evidence:**

- `internal/contracts/payload.go:418-419` only checks prefixes with trailing slash, e.g. `docs/active/`, not exact `docs/active`.
- `internal/contracts/payload.go:368-387` rejects `.` but not arbitrary directory entries.
- `internal/pipe/run.go:489-524` wrong-class preflight treats any `git ls-files -- <rel>` output as tracked, so tracked directories can pass preflight.
- `internal/gitguard/stage.go:41-49` rejects directories only at staging time, after engine execution.
- BLK-006 lines 16-18 require protected allowlist violations to abort before tactical spawn.

**Why this matters:** Exact protected directory roots and tracked directories should fail before engine execution, not later. This is the same authority-class bug shape as HR-001, but at allowlist validation time.

**Patch plan:** Treat exact protected roots and descendants as protected. Require allowlist entries to be exact file paths before engine execution. Use exact `git ls-files -z` equality or `os.Lstat`/tree checks rather than “any output means tracked.”

### HR-008 — Medium — Python BLK-test runtime source-scope guards accept exact protected directory roots

**Evidence:**

- `python/blk_test_kuronode_workspace_read_only_pilot_runtime.py:627-640` rejects descendants whose relative `joined` path starts with `docs/active`, `docs/requirements`, or `docs/use_cases`, but the protected directory itself has empty relative parts and is accepted.
- Same pattern: `python/blk_test_kuronode_workspace_bounded_evidence_refresh.py:654-667`.
- Same pattern: `python/blk_test_non_disposable_l4_runtime_pilot.py:397-403`.
- Same pattern with substring matching: `python/blk_test_fixed_tool_l4_disposable_repo_runtime.py:327-331`.
- Local reproduction during review called the private source-scope functions on temp `docs/active`, `docs/requirements`, and `docs/use_cases` roots; all four helpers accepted the exact protected roots.

**Current-state nuance:** Existing approved constants for BLK-SYSTEM-073 and 097 point at `/home/dad/code/Kuronode-v1/scripts`, so this is not current evidence that protected bodies were read in those runs. It is a latent parameterization/hardening defect that blocks generalizing these helpers safely.

**Patch plan:** Add a shared protected-path predicate that rejects exact roots and descendants after resolving against the target repo. Add tests where `source_subtree_path` is exactly `docs/active`, `docs/requirements`, and `docs/use_cases`.

### HR-009 — Medium — Invalid payload shares POSIX Exit 2 with syntax/validation failure

**Evidence:**

- `internal/pipe/exitcodes.go:6-7` sets both `ExitInvalidPayload` and `ExitValidationFailed` to `2`.
- `internal/pipe/run.go` maps generic invalid payload to `ExitInvalidPayload` while the adapter and doctrine route Exit 2 as syntax/validation failure.
- `python/blk_pipe_adapter.py:52-56` permits both `INVALID_PAYLOAD` and `SYNTAX_GATE_FAILED` for code 2.
- BLK-003 lines 141-145 route Exit 2 as `SYNTAX_GATE_FAILED`.

**Why this matters:** Invalid payload and validation failure are different failure classes. Sharing the POSIX code weakens automation, retry policy, and operator diagnostics.

**Patch plan:** Allocate a distinct invalid-payload exit code, or route invalid payload to a fatal/internal code with explicit report status. Preserve protected BLK-req allowlist violations as Exit 3.

### HR-010 — Medium — Tests pass while stale current-state prose remains allowed

**Evidence:**

- Full Python suite passed 982 tests.
- `python/test_active_doctrine_review_gates.py:2689-2732` still asserts stale markers such as `BEO_PUBLICATION_DISABLED_DRAFT_AND_FIXTURE_ONLY` and `RTM_RUNTIME_GENERATION_AND_DRIFT_REJECTION_DISABLED`.
- `docs/BLK-079...:321` and surrounding decision guidance still require careful manual interpretation after BLK-100/103.
- No search hit found a post-103/BLK-SYSTEM-104 frontier marker before this report.

**Why this matters:** Doctrine gates are green but not strong enough to detect stale authority wording after the latest ladder movement.

**Patch plan:** Add regression gates that fail if BLK-077/079 lack a post-103 boundary/frontier section, if BLK-001/003 still describe current BEO handling as only draft-only, or if generic BEO/RTM rows omit BLK-100/103 distinctions.

### HR-011 — Low/Medium — BLK-test functional-module warning is under-propagated

**Evidence:**

- BLK-097 correctly states “BLK-test is a BLK-System functional module, not BLK-System's test suite” at `docs/BLK-097...:14`.
- BLK-079 generic BLK-test rows at `docs/BLK-079...:264` and `:287` do not carry the exact warning.

**Why this matters:** The repository also has normal Python/Go test suites. Future agents can confuse “run tests” with BLK-test module authority.

**Patch plan:** Add the exact warning to BLK-077/079 operator-facing current-state surfaces and pin it in active doctrine tests.

### HR-012 — Low — Operator runbook vocabulary lags post-100/post-103 evidence states

**Evidence:**

- `docs/BLK-031_operator-ux-observability-runbook-boundary.md:46-47` still uses `DRAFT_ONLY_BEO` and `RTM_NOT_GENERATED` as primary status vocabulary.
- Later BLK-100/103 introduce `PUBLISHED_EXTERNAL_BEO_RECORD` and `PILOT_LOCAL_RTM_TRACE_CLOSURE_RECORDED_NOT_AUTHORITATIVE`.

**Why this matters:** This is not an authority grant, but it will confuse operators during diagnostics.

**Patch plan:** Add non-authoritative “record-only external BEO publication” and “local trace-closure evidence only” statuses while preserving denial of production publication/`blk-link` authority.

## 5. Completion Gaps Against BLK-001

These are not all bugs; many are expected unfinished organs of the BLK-001 V-model.

| BLK-001 subsystem | Current reviewed state | Fit for final target? | Gap |
| --- | --- | --- | --- |
| `blk-req` legislative gateway | Doctrine and fixtures exist; no `lint_artifacts.py` found; no active/staging promotion backend found in repo search. | No | Implement actual staging, lint, HITL promotion, revision, canonical hashing, and protected retrieval tooling. |
| `blk-id` identity spine | Many packages carry IDs/hashes; not yet a unified identity service. | Partial | Define a canonical identity/provenance store/schema across approvals, actors, artifacts, and events. |
| `blk-relay` signal bus | Described in BLK-001; not implemented as service here. | No | Implement typed message routing and source binding, or explicitly scope it outside this repo. |
| Hermes planning/BEB | Doctrine and dry-run fixtures exist; no fully automated BLK-002 `fetch_requirements_context` + dependency graph authority in repo. | Partial | Build real requirement retrieval and dependency analysis handoff. |
| `blk-pipe` forge | Real Go implementation exists and passes tests. | Partial | Fix protected-body reads, hard caps, validation gate, directory roots, exit taxonomy, validation shell profile model. |
| `blk-test` physics oracle | Multiple evidence-only/runtime pilots and fixtures exist; production MCP/generic service remains denied. | Partial | Productize as a reusable fixed-tool verification module with explicit approvals/isolation/replay/output/cleanup. |
| BEO publication | BLK-100 record-only external publication exists; signer/storage/ledger/rollback remain denied. | Partial | Implement authoritative publication path after separate approval. |
| `blk-link` / RTM | Local non-authoritative trace closure exists after BLK-103; production `blk-link` remains denied. | Partial | Implement production trace closure using published BEO metadata and approved hash-only active-vault metadata. |
| Drift rejection | Local non-authoritative evidence exists; authoritative drift decision remains denied. | No | Add explicit human-reviewed drift detection/recommendation/rejection workflow. |
| Operations/security | Health checks and runbooks exist; no production isolation claim. | Partial | Hardening, monitoring, recovery, release governance, and audited sandbox/capability evidence. |

## 6. Patch Plan From This Hostile Review

### P0 — Blocking authority reconciliation and protected-body patch set

1. **Post-103 current-state reconciliation (recommended BLK-SYSTEM-104).**
   - Patch BLK-001/003/005/006, BLK-077, BLK-079, and `python/blk_current_state_authority_index.py`.
   - Add post-103 frontier/stop-condition language.
   - Split “record-only external BEO publication exists” from “authoritative signed/storage/ledger publication remains disabled.”
   - Split “local non-authoritative trace closure exists” from “production/reusable blk-link remains disabled.”

2. **Go protected-body no-read remediation.**
   - Remove body reads from physical snapshots for protected BLK-req roots.
   - Add unreadable protected-file regression tests.
   - Confirm mutation detection remains effective without copying bodies.

3. **Timeout/output-cap doctrine alignment.**
   - Treat 900 seconds / 15 minutes and 52,428,800 bytes / 50MB as defaults, not hard maxima.
   - Preserve caller-tunable finite `timeout_seconds` / `max_output_bytes` values as intentional operational sizing, with selected caps visible in payload/report evidence.

4. **Mandatory validation gate.**
   - Require validation profiles or explicit trusted-local override.
   - Reject no-validation execute payloads by default.

### P1 — Safety-hardening patch set

5. **Validation profile argv conversion.**
   - Replace shell strings with structured argv/env profile registry.
   - Keep legacy shell only as visible trusted-local exception.

6. **Protected directory/file exactness.**
   - Fix Go exact protected root/directory allowlist loopholes.
   - Fix Python exact protected source-scope root loopholes.
   - Add shared tests for `docs/active`, `docs/requirements`, and `docs/use_cases` exact roots and descendants.

7. **Exit-code taxonomy.**
   - Split invalid payload from syntax/validation failure or document an explicit compatibility transition.

8. **Doctrine gate coverage.**
   - Add tests that stale post-099/post-103 wording fails.
   - Add tests pinning BLK-test as functional module, not BLK-System test suite.
   - Add tests for BLK-077/079 post-103 frontier presence.

### P2 — Operator and roadmap cleanup

9. **Runbook vocabulary update.**
   - Add BLK-100/103 non-authoritative states to BLK-031.

10. **Report/result publication hygiene.**
   - Decide whether future all-codebase hostile reviews should be committed/pushed by default and whether they should trigger a follow-on plan/outcome document.

## 7. High-Level Roadmap to Complete BLK-System

### Milestone 0 — Hostile-review patch closure

**Goal:** Make current authority surfaces coherent and eliminate protected-body read drift.

**Exit criteria:** HR-001 through HR-010 are patched or explicitly deferred with doctrine; full Python/Go suites and doctrine gates pass; current-state docs have a single post-103 frontier selector.

### Milestone 1 — BLK-req legislative gateway implementation

**Goal:** Implement the left side of the V-model as real infrastructure, not just doctrine.

**Work:**

- Staging directories for requirements/use cases.
- Version-aware schema validation.
- Requirement atomicity and use-case narrative bounds.
- HITL approval capture with source system/operator/message/timestamp.
- Atomic promotion/revision/concurrency lock.
- Canonical `version_hash` generation.
- Read-only, exact-ID requirement retrieval for Hermes; no tactical/probe protected-body access.

**Exit criteria:** Real REQ/UC artifacts can be baselined/revised and retrieved for BEB trace binding without bypassing HITL or leaking protected bodies to tactical/probe code.

### Milestone 2 — BLK-pipe production hardening

**Goal:** Turn the Go blast shield into a production-grade deterministic mutation forge.

**Work:**

- Resolve HR-001/002/003/006/007/009.
- Structured validation profiles.
- Strong report evidence for target hash, branch, profiles, exact staged paths, cleanup, and denial routes.
- Audit-safe distinction between trusted-local and autonomous payloads.

**Exit criteria:** BLK-pipe can safely run approved source mutation payloads with exact allowlists and validation gates, without protected-body reads or authority drift.

### Milestone 3 — Hermes planning/BEB generation and dependency routing

**Goal:** Implement the BLK-001 planning translation layer.

**Work:**

- `fetch_requirements_context` equivalent for exact baselined artifacts.
- Dependency graph analysis with inbound/outbound limitations documented.
- BEB authoring with trace artifacts, exact allowlists, denied actions, validation profiles, and human dispatch gate.
- Three-iteration hostile-audit loop with failure ceiling and revert.

**Exit criteria:** Hermes can produce a BEB/L2 payload from real requirements and approved dependency evidence without guessing constraints or paths.

### Milestone 4 — BLK-test production functional module

**Goal:** Promote BLK-test from evidence-only pilots to a reusable fixed-tool physics oracle.

**Work:**

- Keep BLK-test as functional module, not repo test suite.
- Fixed-tool registry, no arbitrary shell.
- Source/Git mutation detection.
- Ephemeral workspace ownership/cleanup.
- Replay/expiry/operator-stop controls.
- Output caps and deduplication.
- Protected-body and secret descendant denial.

**Exit criteria:** BLK-test can return production verification evidence without becoming planner, mutation authority, BEO publisher, RTM generator, or drift authority.

### Milestone 5 — Authoritative BEO publication

**Goal:** Move from record-only/local publication evidence to authoritative BEO publication.

**Work:**

- Publication approval capture separate from BLK-test PASS and BLK-pipe success.
- Signer identity and key-material policy.
- Immutable storage/ledger append policy.
- Revocation, rollback, supersession, and audit trail.
- BEO frontmatter trace inheritance from BEB.

**Exit criteria:** BEOs can be authoritatively published, audited, and superseded without implying RTM generation or drift decisions.

### Milestone 6 — Production `blk-link` RTM trace closure

**Goal:** Implement reusable production RTM closure using approved metadata only.

**Work:**

- Consume authoritative published BEO metadata.
- Consume approved hash-only active-vault metadata without protected-body reads.
- Generate coverage/trace closure matrix.
- Record exact package hashes and source evidence.

**Exit criteria:** `blk-link` can produce trace-closure evidence that proves BEO-to-requirement hash binding without reading protected bodies or issuing drift rejection.

### Milestone 7 — Drift detection and rejection authority

**Goal:** Add an explicit human-reviewed drift workflow.

**Work:**

- Separate detection, recommendation, approval, rejection, and supersession.
- Never auto-reject solely from local trace closure.
- Add appeal/audit and rollback/supersession links.

**Exit criteria:** Drift rejection can become authoritative only through explicit review and cannot be laundered from RTM generation or BLK-test PASS/FAIL evidence.

### Milestone 8 — Integrated autonomous V-model operations

**Goal:** Operate the full BLK-001 target architecture under HITL gates.

**End-to-end chain:**

1. BLK-req baselines REQ/UC artifacts and hashes.
2. Hermes retrieves exact constraints and generates BEB/L2 payload.
3. Human approves dispatch.
4. BLK-pipe performs bounded mutation.
5. BLK-test verifies physical reality.
6. Human separately approves BEO publication.
7. `blk-link` separately generates RTM trace closure.
8. Human separately handles drift decisions.

**Exit criteria:** The system can run one complete approved BLK-System-governed change from requirement to trace closure with no authority laundering between components.

### Milestone 9 — Operations, security, and release governance

**Goal:** Make BLK-System operable without tribal knowledge.

**Work:**

- Operator UX/runbooks and status vocabulary.
- Monitoring and audit dashboards.
- Backup/recovery/revocation procedures.
- Release/version governance.
- Threat model and isolation evidence.
- Scheduled all-codebase hostile reviews.

**Exit criteria:** Operators can diagnose, approve, halt, recover, and audit BLK-System safely in normal and failure modes.

## 8. Recommended Immediate Next Action

Create and execute a narrow documentation/test sprint:

**BLK-SYSTEM-104 — Post-103 Current-State Reconciliation and Hostile-Review Patch Plan**

Minimum scope:

1. Save this review as source evidence.
2. Patch BLK-001/003/005/006, BLK-077, BLK-079, and current-state index code/tests for post-103 coherence.
3. Add doctrine gates for stale post-100/post-103 wording.
4. Plan the Go protected-body no-read remediation as the first implementation patch sprint after reconciliation.

This should remain L0/L1 documentation/test/doctrine-gate work. It must not authorize BLK-pipe runtime, BLK-test runtime, BEO publication, RTM generation, drift rejection, protected-body reads, or target-repo mutation.
