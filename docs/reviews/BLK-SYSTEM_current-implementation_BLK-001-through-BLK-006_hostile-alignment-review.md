# BLK-System Current Implementation — Hostile Alignment Review Against BLK-001 through BLK-006

**Status:** Review report — hostile audit complete  
**Date:** 2026-05-07T16:40:36+10:00  
**Repository:** `/home/dad/BLK-System`  
**Reviewed baseline:** `main` at `3a23275 docs: close out blk-system sprint 017`  
**Requested scope:** current BLK-System implementation/docs alignment against `BLK-001` through `BLK-006`  
**Review mode:** hostile authority-boundary review; no remediation performed

---

## 1. Executive Verdict

The current BLK-System implementation is **mostly aligned in intent** with BLK-001 through BLK-006, but it is **not cleanly aligned**.

Two blocking alignment findings were found:

1. Protected BLK-req vault allowlist violations are rejected as invalid payloads instead of returning the BLK-006-mandated POSIX Exit 3 unauthorized-mutation route.
2. The `revert`/failure-ceiling recovery route is gated behind normal clean-preflight checks, making the BLK-003/BLK-004 abort-and-revert authority unreachable in dirty workspaces — precisely the condition it may need to recover from.

A third blocking documentation/doctrine ambiguity exists:

3. Active doctrine still says live BLK-test MCP remains disabled/non-executing, while BLK-020 records one accepted first live fixed-tool smoke. The later smoke is narrow and explicitly non-production, but the active doctrine set is internally contradictory.

No evidence was found that current runtime paths authorize broad live BLK-test MCP, authoritative BEO publication, RTM generation, RTM drift rejection authority, or BLK-test/BEO/RTM protected BLK-req vault body reads. Those boundaries are generally well guarded.

---

## 2. Governing Doctrine Reviewed

Primary doctrine reviewed:

- `docs/BLK-001_blk-system-master-architecture.md`
- `docs/BLK-002_blk-req-artifact-lifecycle.md`
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md`
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- `docs/BLK-005_blk-req-specification.md`
- `docs/BLK-006_blk-req-implementation-brief.md`

Important doctrine boundaries tested:

- `blk-req` is the legislative/HITL-authorized requirements vault; tactical/probe code must not read, copy, parse, or mutate protected BLK-req vault bodies.
- `blk-pipe` is the blast shield/forge and owns source mutation, staging, Git allowlists, and POSIX routing.
- `blk-test` is a physics oracle, not a planner, source-of-truth selector, Git actor, RTM generator, or BEO publisher.
- `blk-link` owns offline RTM/ledger authority; RTM generation and drift rejection must not be hidden inside BLK-test or BEO fixture code.
- The cryptographic baton (`version_hash`, canonical `trace_artifacts`) must not launder missing/malformed trace context into authority.
- BLK-006 specifically requires protected vault allowlist hits to abort and return POSIX Exit 3.

---

## 3. Implementation Surfaces Reviewed

Representative current implementation surfaces reviewed:

- Go `blk-pipe` payload, runner, validation, Git guard, revert, and report code under:
  - `cmd/blk-pipe/`
  - `internal/contracts/`
  - `internal/pipe/`
  - `internal/gitguard/`
  - `internal/validation/`
  - `internal/engine/`
  - `internal/execguard/`
- Python adapter/probe/fixture surfaces under:
  - `python/blk_pipe_adapter.py`
  - `python/blk_orchestrator_gate.py`
  - `python/blk_test_mcp_disabled_transport.py`
  - `python/blk_test_mcp_workspace_process_probes.py`
  - `python/blk_test_mcp_approval_authorization.py`
  - `python/blk_test_mcp_fixed_tool_live_smoke.py`
  - `python/beo_fixture_projection.py`
  - `python/beo_rtm_interface_fixtures.py`
- Active post-BLK-006 doctrine and review docs that affect current authority interpretation, especially `BLK-017` through `BLK-023`.

Searches targeted authority drift terms including: `authorize`, `live`, `execute`, `stage`, `commit`, `push`, `BEO`, `RTM`, `active vault`, `sandbox`, `host-secret`, `approval`, `shell=True`, `os.system`, `eval`, `exec`, `socket`, `requests`, `urllib`, `git add`, `git commit`, `git push`, `generate_rtm`, and `rtm_id`.

---

## 4. Blocking Findings

### BLOCKING-1 — Protected BLK-req vault allowlist violations route as Exit 2, not BLK-006 Exit 3

**Verdict:** Not aligned with BLK-006.

BLK-006 requires `blk-pipe` to scan both `allowed_modified_files` and `allowed_new_files` before tactical execution. If either allowlist targets protected vault paths under `docs/active/`, `docs/requirements/`, or `docs/use_cases/`, `blk-pipe` must instantly abort, wipe the workspace, and return POSIX Exit 3.

Current implementation does reject protected paths, but it does so inside payload validation. Payload validation errors are mapped to `INVALID_PAYLOAD` / Exit 2, not `UNAUTHORIZED_FILE_MUTATION` / Exit 3.

**Doctrine evidence:**

- `docs/BLK-006_blk-req-implementation-brief.md:15-17`
  - BLK-006 says the compiled Go binary must scan both allowlists and return POSIX Exit 3 on protected BLK-req vault path hits.

**Implementation evidence:**

- `internal/contracts/payload.go:321-340`
  - `validateAllowlist(...)` rejects protected docs paths with a validation error.
- `internal/pipe/run.go:589-603`
  - `parseAndValidatePayload(...)` maps decode/validation errors to `report.Status = "INVALID_PAYLOAD"` and `ExitInvalidPayload`.
- `internal/pipe/exitcodes.go`
  - Exit 2 is invalid payload; Exit 3 is unauthorized mutation.

**Why this matters:**

Hermes routing relies on POSIX status semantics. A protected vault allowlist attempt is not just malformed syntax; it is an attempted authority-boundary violation. Routing it as Exit 2 can cause the control loop to treat a vault attack or planning failure as a payload-shape issue instead of a blast-shield violation.

**Expected remediation direction:**

Move protected-vault allowlist classification to a pre-execution authority check that returns `UNAUTHORIZED_FILE_MUTATION` / Exit 3, or preserve early validation while explicitly mapping protected-vault validation errors to Exit 3. The report should also record the protected prefix hit without exposing protected body contents.

---

### BLOCKING-2 — `revert` recovery is blocked by normal clean-preflight checks

**Verdict:** Not aligned with BLK-003/BLK-004 failure-ceiling recovery intent.

BLK-003 and BLK-004 define the failure-ceiling path as a physical abort-and-revert route. On failure ceiling, Hermes invokes BLK-pipe using the `sprint_base_hash` to eradicate broken commits and halt/escalate safely. That path must be robust when the workspace is dirty or damaged, because that is exactly when revert may be needed.

Current `run(...)` calls `cleanPreflight(...)` before checking whether `payload.Action == "revert"`. If the workspace contains pre-existing dirty/untracked/ignored/nested-git residue, `cleanPreflight` returns a dirty-worktree status and `runRevert(...)` is never reached.

**Doctrine evidence:**

- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:161-165`
  - On failure ceiling, Hermes invokes `abort_sprint_and_revert` via BLK-pipe using the `sprint_base_hash`.
- `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
  - Defines the revert/rollback path as part of BLK-pipe’s blast-shield safety role.

**Implementation evidence:**

- `internal/pipe/run.go:40-52`
  - `cleanPreflight(payload.Workdir, report)` executes before the `payload.Action == "revert"` branch.
- `internal/pipe/run.go:390-431`
  - `cleanPreflight` can reject the workspace before revert.
- `internal/pipe/run.go:496-525`
  - `runRevert(...)` contains the actual verified reset/clean behavior, but it is unreachable if preflight rejects first.

**Why this matters:**

The revert route is supposed to be the emergency brake. If normal cleanliness gates block the emergency brake, BLK-pipe can fail closed in a way that preserves broken residue rather than eradicating it.

**Expected remediation direction:**

Handle `payload.Action == "revert"` before ordinary execute-mode cleanliness checks. Revert should still validate target branch/hash/ancestry and protected anchors, but it should not require the workspace to be clean before cleanup. Add regression tests proving dirty/untracked residue does not prevent a valid revert from running.

---

### BLOCKING-3 — Active doctrine contradicts accepted first live fixed-tool BLK-test smoke authority

**Verdict:** Not cleanly aligned as a current doctrine set.

The current doc set contains an internal authority contradiction. `BLK-020` records an accepted first live fixed-tool BLK-test MCP smoke under explicit human approval with no production authority. However, active older doctrine still states that live BLK-test MCP remains disabled/non-executing without qualifying the one accepted BLK-020 exception.

**Doctrine evidence for accepted narrow smoke:**

- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md:3-4`
  - Status and scope record an accepted first live fixed-tool smoke under explicit human approval, with no production authority.
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md:10-20`
  - Records the approved first run, its PASS result, and its narrow synthetic fixed-tool scope.

**Contradictory doctrine evidence:**

- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:150`
  - Says Phase 4.2 is represented only by fixture/disabled stubs and that `live BLK-test MCP remains disabled`.
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:186`
  - Repeats that live BLK-test MCP remains disabled.
- `docs/BLK-017_blk-test-mcp-disabled-transport-skeleton.md:136-140`
  - Says BLK-test MCP remains non-executing until later sprints complete, without acknowledging BLK-020’s completed first-smoke exception.

**Why this matters:**

This is not broad live BLK-test authority drift: BLK-020 is narrow and repeatedly denies production authority. The problem is current-doctrine ambiguity. A reader cannot tell whether the one accepted BLK-020 evidence path is valid or impossible under BLK-003/BLK-017.

**Expected remediation direction:**

Patch active doctrine overlays to say: generic/production BLK-test MCP remains disabled; the only accepted live exception is the BLK-020 first fixed-tool synthetic smoke evidence contract; that exception grants no production MCP authority, no source mutation, no protected vault body reads, no BEO publication, and no RTM generation.

---

## 5. Non-Blocking Findings / Alignment Risks

### RISK-1 — Validation commands are arbitrary shell strings from payload

**Classification:** Non-blocking risk under current BLK-004 design, but high-value hardening target.

Validation commands are accepted as payload-provided strings and executed through `sh -c`. They are bounded by `execguard`, timeouts, output caps, scrubbed environment, and post-run mutation checks. Still, this is a shell-capable subprocess surface and can attempt network access or host inspection if an untrusted payload is allowed to supply validation commands.

**Evidence:**

- `internal/contracts/payload.go:306-317`
  - Validation command validation checks count/emptiness/length, not semantic allowlists.
- `internal/validation/validation.go:29-32`
  - Commands are interpreted exactly as payload-provided shell commands.
- `internal/validation/validation.go:65-70`
  - Commands execute as `[]string{"sh", "-c", command}`.

**Why non-blocking:**

BLK-004 historically includes validation command execution as part of BLK-pipe’s bounded execution sequence, and current tests pass. However, from a BLK-001 blast-shield perspective, a future hardening sprint should consider fixed validation profiles or explicit command allowlists.

---

### RISK-2 — Python `BlkPipeAdapter` is a pass-through, not an authority layer

**Classification:** Non-blocking if callers treat Go `blk-pipe` as the authority; risky if callers treat the Python adapter as policy enforcement.

`python/blk_pipe_adapter.py` forwards caller-supplied `engine`, `engine_args`, `validation_commands`, and allowlists into BLK-pipe. It does not independently enforce BLK-003 tactical constraints such as specific engine deny-read flags or a global workspace syntax check.

**Evidence:**

- `python/blk_pipe_adapter.py:74-102`
  - Builds execute payload from caller-supplied fields.
- `python/blk_pipe_adapter.py:125-138`
  - Invokes the binary without adding independent authority checks.

**Why non-blocking:**

The compiled Go binary is the intended blast shield and does enforce many hard boundaries. This should remain documented clearly: the adapter is a transport convenience, not the policy authority.

---

### RISK-3 — BEO generation responsibility remains terminologically muddy in older doctrine

**Classification:** Non-blocking documentation risk.

BLK-001 says RTM cross-references BEOs generated by `blk-test`, while BLK-003 says target-state Hermes generates BEO documents after execution. Later docs correctly deny current authoritative BEO publication and constrain BEO-like outputs to draft fixtures/design-only boundaries.

**Evidence:**

- `docs/BLK-001_blk-system-master-architecture.md:66`
  - Mentions BEOs generated by `blk-test` in the RTM cross-reference context.
- `docs/BLK-003_blk-pipe-blk-test-orchestration.md:169-170`
  - Says Hermes generates the BEO document in the future approved target architecture.
- `docs/BLK-021_beo-draft-publication-gate-review.md`
  - Denies authoritative BEO publication and keeps current paths draft-only.
- `docs/BLK-022_authoritative-beo-publication-design-boundary.md`
  - Design-only authoritative BEO publication boundary; no publication authority.

**Why non-blocking:**

No current implementation path was found that publishes authoritative BEOs. The ambiguity is terminological and should be normalized before target-state publication work resumes.

---

### RISK-4 — Stale future-tense references remain after BLK-020

**Classification:** Non-blocking documentation hygiene risk.

Some docs still describe Sprint 014 first-smoke approval as future work even though BLK-020 records the first-smoke evidence contract as accepted.

**Evidence:**

- `docs/BLK-018_blk-test-mcp-workspace-process-control-probes.md`
  - Contains future-tense prerequisites for Sprint 014.
- `docs/BLK-020_blk-test-mcp-first-live-fixed-tool-smoke.md`
  - Records that the approved first smoke occurred and passed.

**Why non-blocking:**

BLK-020 is the newer active evidence contract and preserves non-production boundaries. The stale future tense should be patched to avoid future authority confusion.

---

## 6. Positive Alignment Evidence

The hostile review also found strong alignment in several important places:

1. **Protected vault paths are rejected at all.**
   - `internal/contracts/payload.go:321-340` rejects absolute paths, dirty paths, `..`, pathspec metacharacters, and protected BLK-req vault prefixes.
   - The routing code needs correction to Exit 3, but the protected-prefix check exists.

2. **Git staging is narrow.**
   - `internal/gitguard/stage.go` stages explicit files and documents avoidance of broad `git add .` / `git add -u` behavior.

3. **Trace artifacts are structurally guarded.**
   - `internal/contracts/payload.go` validates canonical trace artifact shape, including `sha256:<64-lowercase-hex>` style hashes.

4. **BEO/RTM runtime authority remains disabled.**
   - `python/beo_fixture_projection.py` and `python/beo_rtm_interface_fixtures.py` preserve draft-only / disabled-interface behavior.
   - `docs/BLK-021`, `docs/BLK-022`, and `docs/BLK-023` repeatedly deny current authoritative BEO publication, RTM generation, RTM drift rejection authority, and protected BLK-req body reads.

5. **BLK-test fixed-tool smoke is constrained.**
   - `docs/BLK-020` narrows the accepted live smoke to one fixed-tool synthetic evidence contract and denies production MCP authority, source mutation, protected vault body reads, authoritative BEO publication, and RTM generation.

---

## 7. Verification Evidence

Commands run from `/home/dad/BLK-System` with `PATH="$HOME/.local/bin:$PATH"` where applicable:

```text
git status --short --branch
## main...origin/main

python3 -m unittest discover -s python -p 'test_*.py'
Ran 310 tests in 6.368s
OK

go test ./...
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe              (cached)
ok  github.com/camcamcami/BLK-System/internal/contracts        (cached)
ok  github.com/camcamcami/BLK-System/internal/engine           (cached)
ok  github.com/camcamcami/BLK-System/internal/execguard        (cached)
ok  github.com/camcamcami/BLK-System/internal/gitguard         (cached)
ok  github.com/camcamcami/BLK-System/internal/pipe             (cached)
ok  github.com/camcamcami/BLK-System/internal/runtimeguard     (cached)
ok  github.com/camcamcami/BLK-System/internal/testutil         (cached)
ok  github.com/camcamcami/BLK-System/internal/validation       (cached)

go vet ./...
exit 0, no output

git diff --check
exit 0, no output
```

The passing test suite does not close the findings above; it indicates that the current tests encode the current behavior and need targeted hostile regressions for the blocked alignment gaps.

---

## 8. Recommended Remediation Slices

Recommended narrow follow-up slices:

1. **BLK-SYSTEM-018 — Protected-vault Exit 3 and revert emergency-path hardening**
   - Add RED tests for protected allowlist paths returning Exit 3.
   - Add RED tests for revert succeeding from dirty/untracked workspace residue when the target hash/branch/ancestry is valid.
   - Patch routing and revert action ordering.
   - Preserve no protected body reads, no broad Git staging, no live BLK-test authority.

2. **BLK-SYSTEM-019 — Active doctrine authority overlay cleanup**
   - Patch BLK-003 and BLK-017 to acknowledge BLK-020’s single accepted first-smoke exception.
   - Patch stale Sprint 014 future-tense references after BLK-020.
   - Normalize BEO wording so current docs do not imply BLK-test publishes or owns authoritative BEO generation.

3. **Later hardening candidate — validation command profile tightening**
   - Consider fixed validation profiles or explicit command allowlists if validation commands will ever cross a less-trusted boundary.

---

## 9. Non-Execution Statement

This review did not implement code changes, did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.
