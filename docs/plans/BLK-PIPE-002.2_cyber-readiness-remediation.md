# BLK-pipe Sprint 002.2 — Cyber Readiness Remediation and Usability Guardrails

> **For Hermes / LLM implementer:** Use `blk-system-sprint-execution`, `test-driven-development`, and `subagent-driven-development` for every code-producing task. Implement task-by-task with strict TDD, local fake engines only, two-stage review after each task, and one outcome document per task. Do not run Codex, do not call live LLM APIs, do not perform offensive cyber activity, and do not connect this sprint to a real cyber-program repository. This sprint is defensive hardening of BLK-pipe itself.

**Status:** Planned
**Date:** 2026-05-04
**Repository:** `/home/dad/BLK-System`
**Target Component:** `blk-pipe`
**Primary Doctrine:** `docs/BLK-001_blk-system-master-architecture.md`, `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
**Input Context:** `docs/plans/BLK-PIPE-002.1_hostile-review-remediation.md`, `docs/outcomes/BLK-PIPE-002.1_task-001-outcome.md`, `docs/outcomes/BLK-PIPE-001_sprint-001-closeout.md`, `docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md`

**Goal:** Close the remaining post-Sprint-002 hostile-review safety gaps while preserving enough usability that BLK-pipe remains operable for legitimate defensive development workflows.

**Architecture:** Sprint 002.2 keeps BLK-pipe as a deterministic local transport and repository mutation gate. It does not add live Codex/LLM execution or a full OS sandbox. It remediates the remaining process-lifetime, validation-authority, validation-classification, and V47 packet-transport gaps, then documents cyber-use boundaries and usability guardrails so future sandbox/orchestration work does not weaken the blast shield.

**Tech Stack:** Go 1.22 module semantics with local Go toolchain (`/home/dad/.local/bin/go`, currently `go1.26.2 linux/amd64`), Go standard library only for production code, POSIX shell fixtures for hostile regression tests, Git CLI only through bounded helpers, Python standard library adapter tests.

---

## 0. Current Known State

Preflight observed while drafting this plan:

```text
Date: 2026-05-04
Branch: main
Remote: origin/main
HEAD: f850eee docs: record BLK-pipe task 1 outcome
Working tree: clean and aligned with origin/main
Go toolchain: go version go1.26.2 linux/amd64
```

Always run Go commands with:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Current normal gates observed before drafting:

```text
PASS go test ./...
PASS python3 -m unittest discover -s python -p 'test_*.py'
PASS go vet ./...
PASS production broad-staging grep
PASS production direct-Git-call grep
PASS triple-dot diff grep across reviewed BLK-pipe code/docs
PASS git diff --check
```

Sprint 002.1 Task 1 is complete:

```text
277501b fix: block blk-pipe success with physical residue
f850eee docs: record BLK-pipe task 1 outcome
```

Task 1 fixed the hostile finding that `SUCCESS` could leave physical residue such as `ghostdir/` behind. Verified current behavior: physical residue routes to `UNAUTHORIZED_FILE_MUTATION` / exit `3`, cleans residue, preserves `HEAD`, and leaves repo clean.

Remaining hostile-review findings to carry forward:

```text
B. Timeout/flood/cancel escaped descendant can mutate after BLK-pipe returns.
C. Validation can author the committed diff.
D. Validation safety violations can be misclassified as SYNTAX_GATE_FAILED.
E. V47 l2_packet is accepted but dropped instead of delivered to engine stdin.
F. Full cyber execution still requires a real sandbox boundary beyond BLK-pipe.
```

---

## 1. Sprint 002.2 Non-Goals

Do **not** implement any of the following in Sprint 002.2 unless the user explicitly revises this plan:

- live Codex invocation,
- OpenAI/local LLM API calls,
- offensive cyber tooling or target interaction,
- execution against a real cyber-program repository,
- Discord/HITL integration,
- BLK-req authoring or promotion,
- BLK-test MCP integration,
- RTM generation,
- BEB/BEO lifecycle automation,
- Windows support,
- daemon/service mode,
- broad orchestrator rewrite,
- full container/VM/cgroup sandbox implementation.

Sprint 002.2 may add code hooks or documentation that make a future sandbox easier, but it must not pretend BLK-pipe alone is a complete cyber sandbox.

**Sprint 002.2 does not run Codex. Sprint 002.2 does not run live tactical LLMs. Sprint 002.2 does not authorize live cyber execution.**

---

## 2. Non-Negotiable Invariants To Preserve

1. No production `git add .`.
2. No production `git add -u`.
3. Stage only explicit allowlisted file paths with `git add -- <file>`.
4. Reject allowlist paths that are absolute, unclean, `.`, traversal, Git pathspec/glob, directory, missing/deleted, or protected BLK-req artifact paths.
5. Clean preflight must reject pre-existing tracked, untracked, ignored, empty-directory, nested-Git, and hidden physical residue before destructive execution/revert behavior.
6. No `SUCCESS` may leave unauthorized physical residue.
7. Engine output and validation logs remain bounded.
8. Timeout/flood/cancel must not leave discoverable BLK-pipe-owned process groups, visible descendants, inherited-output pipe holders, or visible descendants of those pipe holders alive after return. Arbitrary fully detached daemon containment remains future sandbox/capability-profile scope and must not be claimed as solved in Sprint 002.2.
9. `.git` mutations are unauthorized and restored where possible.
10. Safety violations outrank syntax/validation failure classification.
11. Validation is a read-only gate relative to the post-engine worktree unless doctrine explicitly grants validator mutation authority later.
12. Revert remains a fast path and must not run branch prep, engine, validation, staging, or commit.
13. Commit hooks remain disabled for BLK-pipe-created commits, including orphan initialization commits.
14. V47 `l2_packet` must be delivered to the engine when present; accepting and dropping it is forbidden after Task 4.
15. Local extension exit codes (`6`, `7`, `9`) must remain clearly separated from strict V47 codes (`0`-`5`) until doctrine changes.
16. Cyber use must require a future sandbox/capability boundary; BLK-pipe alone is not enough.

Copy-pasteable safety checks:

```bash
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md 'docs/outcomes/BLK-PIPE-002.2_task-*-outcome.md' docs/outcomes/BLK-PIPE-002.2_sprint-closeout.md
```

---

## 3. Usability Guardrails For Paranoid Security

Do not weaken safety to improve usability. Instead make strict failures explainable and operable.

### 3.1 Security controls that must remain strict

- dirty/pre-existing residue preflight,
- `.git` mutation denial,
- no broad staging,
- no validation-authored production diffs,
- no discoverable BLK-pipe-owned post-return process mutation from timeout/flood/cancel paths,
- no inherited Git/SSH credential/control environment for BLK-pipe subprocesses; do not claim general host-secret isolation until future sandbox/capability-profile work,
- no live Codex/LLM in this sprint.

### 3.2 Usability patterns to preserve or add

- Failure reports should identify actionable paths in `destroyed_files` / `error` without leaking secrets.
- Validation commands may use external caches/temp dirs, but not mutate production worktree files.
- Tests should use controlled temp repos and fake engines, not brittle real project state.
- If strict file-mode checks reject generated files, the error must make the mode problem discoverable.
- Documentation must tell operators how to fix legitimate failures rather than encouraging bypasses.
- Documentation must warn that Sprint 002.2 is not a host-secret sandbox: current subprocess environment scrubbing is Git/SSH-focused, and sensitive runs should use a minimal non-secret environment or future sandbox profile rather than live host secrets.

---

## 4. Standard Controller Workflow For Each Task

For every implementation task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   git status --short --branch
   git fetch origin main
   git status --short --branch
   export PATH="$HOME/.local/bin:$PATH"
   go version
   go test ./...
   python3 -m unittest discover -s python -p 'test_*.py'
   ```

2. Read this plan plus:
   - `docs/BLK-001_blk-system-master-architecture.md`, especially BLK-pipe blast-shield scope.
   - `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, especially hard bans and execution sequence.
   - `docs/outcomes/BLK-PIPE-002.1_task-001-outcome.md`, especially physical residue lessons.
   - Current files named by the task.
3. Dispatch a fresh implementation subagent with complete task context.
4. Require RED evidence before implementation.
5. Implement minimal code.
6. Run focused tests, full Go tests, `go vet ./...`, Python adapter tests if relevant, safety greps from Section 2, `git diff --check`, and `git status --short --branch`.
7. Run two fresh review gates:
   - spec compliance review against this plan, BLK-001, BLK-004, and the cited hostile finding,
   - code-quality/security/usability review focused on bypasses, cyber risk, cleanup ordering, and operator ergonomics.
8. If either reviewer requests changes, amend the local unpushed task commit and rerun both reviews.
9. Only the controller pushes.
10. Create a matching outcome doc after each task:

    ```text
    docs/outcomes/BLK-PIPE-002.2_task-00N-outcome.md
    ```

Outcome docs must include RED evidence, GREEN evidence, review results, final verification, deviations, and next task.

---

## 5. Task 1 — Reap Escaped Descendants on Timeout, Flood, and Context Cancel

### Objective

Close hostile finding B: BLK-pipe must not return from timeout/flood/cancel paths while an escaped descendant can later mutate the repository.

### Files

Modify:

- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- `internal/engine/runner.go` only if API propagation is required
- `internal/engine/runner_test.go` only if API propagation is required
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "fix: reap blk-pipe escaped descendants before return"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.2_task-001-outcome.md
```

### Required behavior

When `execguard.Run` exits due to any of these conditions:

- timeout,
- output flood,
- parent context cancellation,

it must make a best-effort active cleanup pass before unregistering the active command and before returning to `engine.Run` / `pipe.Run`.

On Linux, the active cleanup pass must include:

- original process group,
- visible descendants,
- inherited stdout/stderr pipe holders discovered through `/proc`,
- visible descendants of inherited-output pipe holders.

On Darwin, preserve existing reduced process-tree/process-group behavior and document the limitation. Do not add Windows fallback code.

### TDD RED tests

Add or update tests in `internal/execguard/command_test.go`:

1. `TestRunTimeoutReapsEscapedDescendantBeforeReturn`

   Shape:

   ```go
   func TestRunTimeoutReapsEscapedDescendantBeforeReturn(t *testing.T) {
       if runtime.GOOS != "linux" {
           t.Skip("Linux /proc pipe-holder cleanup required for this hostile regression")
       }
       tempDir := t.TempDir()
       latePath := filepath.Join(tempDir, "late.txt")
       ctx := context.Background()
       result, err := Run(ctx, Options{
           Workdir: tempDir,
           Command: []string{"sh", "-c", "setsid sh -c 'sleep 1; printf late > late.txt' >/dev/null 2>&1 & sleep 10"},
           Timeout: 100 * time.Millisecond,
           MaxOutputBytes: 4096,
       })
       // Expected after fix: result.TimedOut true, err nil, and late.txt absent after a delay.
   }
   ```

   Translate into the existing helper style. Include a bounded post-return wait, e.g. poll for 2 seconds and fail if `late.txt` appears.

2. `TestRunOutputFloodReapsEscapedDescendantBeforeReturn`

   Use a command that starts an escaped delayed writer and also floods output. Expected: `Flooded == true`, returned promptly, delayed file absent after bounded wait.

3. `TestRunContextCancelReapsEscapedDescendantBeforeReturn`

   Use context cancellation instead of timeout. Expected: returned promptly, delayed file absent after bounded wait.

Add or update a pipe-level hostile regression in `internal/pipe/run_test.go`:

- `TestRunTimeoutEscapedDescendantCannotMutateAfterReturn`

Expected properties:

- report status `ENGINE_TIMEOUT`,
- exit code `ExitEngineTimeout`,
- immediate Git status clean,
- after bounded delay Git status still clean,
- `late.txt` absent,
- `HEAD` unchanged.

### Implementation guidance

Current code already has active registry and Linux pipe-holder discovery machinery. The likely fix is to call `killActiveProcessGroups(false)` from timeout/flood/cancel return paths before `defer unregisterActiveProcessGroup()` executes.

Do not simply sleep after timeout. Do not rely only on `killProcessGroup(cmd)`. The known bypass uses `setsid` to escape the original process group.

Preserve bounded return behavior. If cleanup cannot prove every possible escaped process was killed, document that limitation; but the specific inherited-output/visible-descendant regression must be closed.

Scope note: Sprint 002.2 must close the known BLK-pipe-owned process-group, visible-descendant, and inherited-output pipe-holder regressions. It must not claim full daemon containment for processes that completely detach beyond those discovery mechanisms; that remains future sandbox/capability-profile scope.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run_test.go
go test ./internal/execguard -run 'TestRun.*EscapedDescendant.*BeforeReturn|TestKillActive|TestActiveCleanup|TestRegistry' -v
go test -race ./internal/execguard
go test ./internal/engine -v
go test ./internal/pipe -run 'TestRun.*Timeout.*Escaped|TestRun.*OutputFlood|TestRun.*EngineTimeout' -v
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

- Confirm active registry entries remain live until cleanup has run.
- Confirm timeout/flood/cancel paths do not return before the hostile delayed mutation probe is safe.
- Confirm there is no unbounded hang waiting for invisible detached processes.
- Confirm Darwin limitations are explicit.

---

## 6. Task 2 — Enforce Read-Only Validation Semantics

### Objective

Close hostile finding C: validation commands must not author or alter the committed diff.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- optionally create small helper functions in `internal/pipe/run.go` for post-engine/post-validation state comparison

Expected implementation commit:

```bash
git commit -m "fix: prevent validation-authored blk-pipe diffs"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.2_task-002-outcome.md
```

### Required behavior

Validation is a read-only gate relative to the post-engine state.

After successful engine execution and after existing pre-validation `.git`/physical audits pass, BLK-pipe must snapshot the engine-produced candidate state before running validation. After validation finishes, BLK-pipe must reject any validation-induced mutation to:

- tracked files,
- allowed modified files,
- allowed new files,
- unallowlisted files,
- ignored files,
- empty directories,
- nested `.git` directories,
- root/worktree modes,
- `.git` metadata,
- staged/index state if applicable.

If validation changes anything, route to:

```text
UNAUTHORIZED_FILE_MUTATION / exit 3
```

No success commit may be created from validation-authored changes.

### TDD RED tests

Add tests in `internal/pipe/run_test.go`:

1. `TestRunValidationCannotCreateFirstCommitWorthyDiff`

   Scenario:

   - engine command: `true` or `printf noop`,
   - validation command: `printf validation > README.md`,
   - allowlist: `README.md`,
   - expected: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, `HEAD` unchanged, repo clean, `README.md` restored.

2. `TestRunValidationCannotAlterEngineProducedDiff`

   Scenario:

   - engine writes `engine` to `README.md`,
   - validation writes `validation` to `README.md`,
   - allowlist: `README.md`,
   - expected: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, no commit, repo clean.

3. `TestRunValidationCanReadWithoutMutating`

   Scenario:

   - engine writes allowlisted `README.md`,
   - validation reads/asserts content without writing,
   - expected: `SUCCESS`, committed engine content.

4. `TestRunValidationMayUseExternalTempWithoutWorktreeMutation`

   Scenario:

   - validation writes to `$TMPDIR` or a path outside repo passed by shell, not inside worktree,
   - expected: `SUCCESS` if engine diff is otherwise valid.

Do not permit validation scratch paths inside the repo in this task unless doctrine is explicitly amended.

### Implementation guidance

A practical approach:

1. After engine success and pre-validation safety audits pass, record a post-engine worktree/Git baseline.
2. Run validation commands.
3. Compare the post-validation state to the post-engine baseline.
4. If different, restore to `PreEngineHash`, restore `.git`, cleanup unauthorized residue, preserve validation logs, set `DestroyedFiles` or `Error` to actionable mutation detail, and return exit `3`.

Avoid duplicating enormous snapshot code if existing `gitSnapshot`, directory-mode snapshot, physical-residue helpers, and `git diff`/status helpers can be composed safely.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/pipe -run 'TestRunValidationCannot|TestRunValidationCanRead|TestRunValidationMayUseExternalTemp' -v
go test ./internal/pipe -run 'TestRun.*Validation' -v
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

- Confirm validation cannot create the first diff.
- Confirm validation cannot alter engine-produced allowed diffs.
- Confirm legitimate read-only validation still succeeds.
- Confirm no broad cleanup deletes pre-existing user work because clean preflight still happens first.
- Confirm diagnostics are actionable enough for normal operators.

---

## 7. Task 3 — Route Validation Safety Violations Above Syntax Failure

### Objective

Close hostile finding D: if validation fails and also mutates `.git` or worktree state, BLK-pipe must report the safety violation, not merely `SYNTAX_GATE_FAILED`.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "fix: prioritize blk-pipe validation safety failures"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.2_task-003-outcome.md
```

### Required behavior

After validation commands run, BLK-pipe must audit `.git`, worktree, physical residue, and validation-read-only state regardless of whether validation commands returned success or failure.

Classification precedence:

1. infrastructure/reporting failure that prevents safe cleanup/reporting,
2. `.git` mutation or unauthorized physical/worktree mutation: `UNAUTHORIZED_FILE_MUTATION` / exit `3`,
3. validation command failure with no safety mutation: `SYNTAX_GATE_FAILED` / exit `2`,
4. otherwise proceed to staging/commit.

### TDD RED tests

Add tests in `internal/pipe/run_test.go`:

1. `TestRunValidationFailureWithGitMutationReportsUnauthorized`

   Scenario:

   - engine writes allowed `README.md`,
   - validation command writes `.git/hooks/post-commit` and exits `1`,
   - expected: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, destroyed/error mentions `.git/hooks/post-commit`, no commit, repo clean.

2. `TestRunValidationFailureWithUnauthorizedWorktreeMutationReportsUnauthorized`

   Scenario:

   - engine writes allowed `README.md`,
   - validation command writes `rogue.txt` and exits `1`,
   - expected: `UNAUTHORIZED_FILE_MUTATION`, exit `3`, `rogue.txt` absent after return, no commit.

3. `TestRunValidationFailureWithoutMutationStillReportsSyntaxGateFailed`

   Scenario:

   - engine writes allowed `README.md`,
   - validation command exits `1` without mutating,
   - expected: `SYNTAX_GATE_FAILED`, exit `2`, no commit, repo clean, validation logs preserved.

### Implementation guidance

Do not short-circuit immediately on `validationResult.HasFailure`. Audit safety first, then choose status.

Preserve validation logs even when classification changes to unauthorized mutation.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/pipe -run 'TestRunValidationFailure.*Unauthorized|TestRunValidationFailureWithoutMutation' -v
go test ./internal/pipe -run 'TestRun.*Validation' -v
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

- Confirm safety violation status outranks syntax failure.
- Confirm normal failing validation still routes to code `2`.
- Confirm `.git` restore still tolerates unsupported entries from prior Sprint 002 hardening.
- Confirm no success commit is created on any validation failure.

---

## 8. Task 4 — Deliver V47 `l2_packet` to Engine Stdin

### Objective

Close hostile finding E: V47 `l2_packet` must be normalized into the payload and delivered to the engine process via stdin.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/execguard/command.go`
- `internal/execguard/command_test.go`
- `internal/engine/runner.go`
- `internal/engine/runner_test.go`
- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `python/blk_pipe_adapter.py`
- `python/test_blk_pipe_adapter.py`

Expected implementation commit:

```bash
git commit -m "feat: deliver blk-pipe l2 packet to engine stdin"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.2_task-004-outcome.md
```

### Required behavior

- `contracts.Payload` must include `L2Packet string`.
- `DecodePayload` must preserve V47 `l2_packet` into normalized `Payload.L2Packet`.
- `execguard.Options` must support bounded stdin input, likely `Stdin []byte` or `Stdin string`.
- `engine.Run` must accept stdin payload and pass it to `execguard.Run`.
- `pipe.Run` must pass `payload.L2Packet` to the engine.
- Empty `l2_packet` means empty stdin, not an error.
- Define and enforce a maximum `l2_packet`/stdin size, for example `DefaultMaxL2PacketBytes` in `internal/contracts`. Oversized packets must be rejected during payload validation before engine start, must not be truncated silently, and must not be echoed into reports.
- Legacy Sprint 001 `engine_command` payloads continue to work with empty stdin.
- Python adapter already accepts an `l2_packet` parameter; preserve that API and add tests proving it writes the field.

### TDD RED tests

Add tests:

1. `internal/contracts/payload_test.go`

   - `TestPayloadDecodePreservesL2Packet`
   - input V47 JSON with `l2_packet: "EXPECTED_PACKET"`, expected `payload.L2Packet == "EXPECTED_PACKET"`.
   - `TestPayloadDecodeRejectsOversizedL2Packet`
   - input V47 JSON with `l2_packet` one byte over the configured maximum, expected decode/validation error, no packet body in the error string.

2. `internal/execguard/command_test.go`

   - `TestRunWritesConfiguredStdinToCommand`
   - command: `sh -c 'cat > packet.txt'`, stdin `EXPECTED_PACKET`, expected file content.

3. `internal/engine/runner_test.go`

   - `TestRunPassesStdinToEngine`
   - fake engine reads stdin and writes file.

4. `internal/pipe/run_test.go`

   - `TestRunV47L2PacketDeliveredToEngineStdin`
   - payload uses V47 shape: `engine: "sh"`, `engine_args: ["-c", "umask 022; cat > packet.txt; chmod 0644 packet.txt"]`, `l2_packet: "EXPECTED_PACKET"`, allowed new `packet.txt`.
   - expected `SUCCESS`, committed `packet.txt` exactly equals `EXPECTED_PACKET`.

5. `python/test_blk_pipe_adapter.py`

   - prove `execute_sprint(..., l2_packet="EXPECTED_PACKET", ...)` writes JSON with `l2_packet` intact.

### Implementation guidance

For stdin plumbing, avoid shell string interpolation. Use `cmd.Stdin = bytes.NewReader(opts.Stdin)` or equivalent in `execguard.Run`.

Do not log the full `l2_packet` by default. It may contain task context or sensitive planning data. The packet should be transported, not echoed into reports.

### Focused verification

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w internal/contracts/payload.go internal/contracts/payload_test.go internal/execguard/command.go internal/execguard/command_test.go internal/engine/runner.go internal/engine/runner_test.go internal/pipe/run.go internal/pipe/run_test.go
go test ./internal/contracts -run 'TestPayloadDecode.*L2|TestPayloadDecodeV47|TestPayloadDecodeRejectsOversizedL2Packet' -v
go test ./internal/execguard -run 'TestRunWritesConfiguredStdin|TestRun.*Timeout|TestRun.*OutputFlood' -v
go test ./internal/engine -run 'TestRunPassesStdin|TestRun' -v
go test ./internal/pipe -run 'TestRunV47L2Packet|TestRunSuccess' -v
python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

### Review gate focus

- Confirm `l2_packet` is preserved and delivered exactly.
- Confirm no report logs leak full packet content by default.
- Confirm empty stdin does not regress legacy payloads.
- Confirm stdin delivery does not break timeout/flood cleanup.

---

## 9. Task 5 — Cyber-Usability Failure Reporting and Operator Guidance

### Objective

Make the stricter security behavior usable: failures must tell operators what happened and how to fix legitimate local workflow issues without encouraging unsafe bypasses.

### Files

Modify:

- `internal/pipe/run.go`
- `internal/pipe/run_test.go`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `README.md` if needed for links

Optionally create:

- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

Expected implementation commit:

```bash
git commit -m "docs: describe blk-pipe cyber readiness guardrails"
```

If code changes are required for diagnostics, use:

```bash
git commit -m "feat: improve blk-pipe safety diagnostics"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-002.2_task-005-outcome.md
```

### Required behavior / documentation

Document and, where low-risk, improve failure diagnostics for:

- pre-existing untracked/ignored/empty directory residue,
- validation attempting to mutate production files,
- validation attempting to mutate `.git`,
- unsafe generated file modes such as `0600`, setuid/setgid/sticky, or unsafe parent directory modes,
- post-return process safety expectations,
- `l2_packet` stdin delivery,
- bounded `l2_packet` size and non-logging expectations,
- current host-secret limitation: BLK-pipe scrubs Git/SSH control variables but is not a general host-secret isolation boundary,
- why BLK-pipe is not a full cyber sandbox.

The docs must distinguish three operational profiles without implementing them yet:

```text
dev-smoke: local fake-engine work only; verbose diagnostics acceptable; no live secrets.
strict-ci: ephemeral clean clone, no pre-existing residue, minimal non-secret environment, fake or deterministic local tools.
cyber-execution: future profile; requires sandbox/container/VM/cgroup/network/secret controls before live use.
```

Do not claim that `cyber-execution` is implemented in Sprint 002.2.

### TDD / docs-validation RED tests

For documentation-only portions, add a validation script or inline Python check in the task execution evidence requiring the new doc text to include these phrases:

- `Sprint 002.2 does not run Codex`
- `BLK-pipe is not a complete sandbox`
- `validation commands are read-only gates`
- `l2_packet is delivered to engine stdin`
- `l2_packet is bounded and not logged by default`
- `cyber-execution requires a future sandbox boundary`
- `BLK-pipe does not provide general host-secret isolation`
- `do not bypass clean preflight`

If code diagnostics change, add targeted tests in `internal/pipe/run_test.go` that assert useful error substrings without making tests brittle on full prose.

### Verification

```bash
export PATH="$HOME/.local/bin:$PATH"
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/BLK-010_blk-pipe-v47-hardening-cli.md'),
    Path('docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md'),
]
required = [
    'Sprint 002.2 does not run Codex',
    'BLK-pipe is not a complete sandbox',
    'validation commands are read-only gates',
    'l2_packet is delivered to engine stdin',
    'l2_packet is bounded and not logged by default',
    'cyber-execution requires a future sandbox boundary',
    'BLK-pipe does not provide general host-secret isolation',
    'do not bypass clean preflight',
]
text = '\n'.join(p.read_text() for p in paths if p.exists())
for phrase in required:
    assert phrase in text, phrase
fence = chr(96) * 3
assert text.count(fence) % 2 == 0
for p in paths:
    if p.exists():
        for i, line in enumerate(p.read_text().splitlines(), 1):
            assert line.rstrip() == line, f'{p}:{i}: trailing whitespace'
PY
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go vet ./...
git diff --check
```

### Review gate focus

- Confirm docs do not overclaim cyber readiness.
- Confirm docs improve usability without weakening security.
- Confirm operators are told how to fix strict failures safely.
- Confirm no live Codex/LLM/cyber execution is introduced.

---

## 10. Task 6 — Sprint 002.2 Closeout and Hostile Probe Re-Run

### Objective

Close Sprint 002.2 with evidence that findings B-E are fixed and that Sprint 002.2 still does not authorize live cyber execution.

### Files

Create:

- `docs/outcomes/BLK-PIPE-002.2_sprint-closeout.md`

Modify if needed:

- `README.md`
- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`
- `docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md`

Expected implementation commit:

```bash
git commit -m "docs: close out blk-pipe sprint 002.2"
```

Expected closeout doc:

```text
docs/outcomes/BLK-PIPE-002.2_sprint-closeout.md
```

### Required closeout content

Include:

- final task-line commit before closeout,
- all Sprint 002.2 task commits and outcome docs,
- hostile finding status table:
  - A physical residue fixed in Sprint 002.1 Task 1,
  - B timeout/flood/cancel escaped descendants fixed in Sprint 002.2 Task 1,
  - C validation cannot author diffs fixed in Sprint 002.2 Task 2,
  - D validation safety precedence fixed in Sprint 002.2 Task 3,
  - E `l2_packet` stdin transport fixed in Sprint 002.2 Task 4,
  - F full sandbox still deferred,
- verification commands and outputs,
- explicit statement: `Sprint 002.2 does not run Codex`,
- explicit statement: `BLK-pipe is not a complete sandbox`,
- explicit statement: `BLK-pipe does not provide general host-secret isolation`,
- recommended next sprint scope for actual sandbox/capability profile work.

### Hostile probe re-run

Create a temporary local script during closeout execution only. Do not commit it unless the user asks for a reusable audit harness.

The probe must build a temp binary and verify:

1. Physical residue remains blocked.
2. Timeout escaped descendant cannot mutate after return.
3. Output flood escaped descendant cannot mutate after return.
4. Validation cannot create the first diff.
5. Validation cannot alter engine-produced diff.
6. Validation `.git` mutation plus non-zero exit returns unauthorized mutation.
7. `l2_packet` delivered exactly to engine stdin and committed file content.
8. Oversized `l2_packet` is rejected before engine start and without logging the packet body.

Expected verification commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
go build -o /tmp/blk-pipe-0022-closeout ./cmd/blk-pipe
python3 /tmp/blk_pipe_0022_hostile_probe.py
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go vet ./...
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n -E 'exec\.Command(Context)?\("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
! git grep -n -E 'git[^\n]*diff[^\n]*\.\.\.' -- '*.go' ':!*_test.go' docs/BLK-009_blk-pipe-sprint-001-cli.md docs/BLK-010_blk-pipe-v47-hardening-cli.md docs/BLK-011_blk-pipe-cyber-readiness-and-usability.md docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md docs/outcomes/BLK-PIPE-002.2_task-001-outcome.md docs/outcomes/BLK-PIPE-002.2_task-002-outcome.md docs/outcomes/BLK-PIPE-002.2_task-003-outcome.md docs/outcomes/BLK-PIPE-002.2_task-004-outcome.md docs/outcomes/BLK-PIPE-002.2_task-005-outcome.md docs/outcomes/BLK-PIPE-002.2_sprint-closeout.md
git diff --check
git status --short --branch
rm -f /tmp/blk-pipe-0022-closeout /tmp/blk_pipe_0022_hostile_probe.py
rm -rf python/__pycache__
git status --short --branch
```

### Review gate focus

- Confirm the closeout does not claim live cyber readiness.
- Confirm all hostile probes are represented.
- Confirm all outcome docs exist and point to actual commits.
- Confirm no docs introduce unsafe bypass instructions.

---

## 11. Recommended Future Sprint After 002.2

After Sprint 002.2, the next sprint should not be live Codex. It should be a sandbox/capability profile sprint.

Recommended next scope:

```text
BLK-PIPE-003 — Sandbox and Capability Profiles
```

Candidate objectives:

- ephemeral clone/worktree execution by default,
- no general host-secret isolation claims until sandbox work exists; use minimal non-secret environments,
- optional network-denied/default profile,
- explicit toolchain profile mounts,
- process containment stronger than POSIX process groups,
- cgroup/container/namespace/VM feasibility decision,
- report and artifact handoff from sandbox back to BLK-pipe,
- dry-run-only integration tests.

Do not begin this future sprint until Sprint 002.2 closeout says B-E are fixed and the user explicitly approves sandbox/capability-profile planning.

---

## 12. Quick Resume Prompt For Future Hermes / LLM

```text
You are implementing BLK-pipe Sprint 002.2 in /home/dad/BLK-System. Read docs/plans/BLK-PIPE-002.2_cyber-readiness-remediation.md, docs/BLK-001_blk-system-master-architecture.md, docs/BLK-004_blk-pipe-v47-architecture-suite.md, docs/outcomes/BLK-PIPE-002.1_task-001-outcome.md, and the current source files named by the task. Use strict TDD. Implement only the next incomplete task. Do not run Codex, do not use live LLM APIs, do not execute offensive cyber activity, and do not connect to real cyber-program repositories. Commit locally with the task's expected commit message but do not push. After implementation, run focused tests, go test ./..., Python adapter tests if relevant, go vet ./..., safety greps, and git diff --check. Then run spec-compliance and code-quality/security reviews before the controller pushes and writes the outcome doc.
```
