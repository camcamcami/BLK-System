# BLK-pipe Sprint 002 — Sprint Closeout

**Status:** Complete
**Date:** 2026-05-03
**Sprint:** BLK-pipe Sprint 002 — V47 Hardening Layer
**Plan:** `docs/plans/BLK-PIPE-002_v47-hardening-layer.md`
**Primary Doctrine:** `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
**Final task-line commit:** `a1c0d73c5a197edbe9b5b66050d4e692662fe3ba docs: describe blk-pipe v47 hardening layer`
**Sprint closeout commit:** `PENDING_CLOSEOUT_COMMIT_HASH docs: close out blk-pipe sprint 002`
**Remote target:** `origin/main`

---

## 1. Objective

Sprint 002 hardened the Sprint 001 deterministic `blk-pipe` kernel toward the BLK-004/V47 interface without invoking Codex or any live tactical LLM engine.

The sprint reconciled exit-code routing, added V47-compatible payload/report contracts, centralized bounded command execution, improved process and Git safety, added validation/revert/branch handling, introduced the local Python adapter, and documented the resulting contract.

**Sprint 002 does not run Codex.** Codex/live LLM integration remains deferred until a later sprint after deterministic file-boundary, validation, revert, branch, signal, and adapter behavior remain stable under continued review.

---

## 2. Implemented Task Line

| Task | Implementation Commit | Outcome |
|---|---|---|
| 1 — Reconcile Exit-Code Registry | `f30ead8 feat: reconcile blk-pipe v47 exit codes` | `docs/outcomes/BLK-PIPE-002_task-001-outcome.md` |
| 2 — Add V47 Payload and Stable Report Contracts With Legacy Normalization | `b123772 feat: add blk-pipe v47 contracts` | `docs/outcomes/BLK-PIPE-002_task-002-outcome.md` |
| 3 — Add Reusable Bounded Command Guard, Engine Log Capture, and Environment Scrub | `871f3a9 feat: add bounded command guard` | `docs/outcomes/BLK-PIPE-002_task-003-outcome.md` |
| 4 — Add Main-Level Signal Trap, Panic Recovery, and Active Process Reaping | `4a2ce0f feat: add blk-pipe fatal signal guard` | `docs/outcomes/BLK-PIPE-002_task-004-outcome.md` |
| 5 — Route Git Calls Through a Bounded Git Helper | `4dd0bb7 feat: bound blk-pipe git commands` | `docs/outcomes/BLK-PIPE-002_task-005-outcome.md` |
| 6 — Add Pre-Engine Hash, Mandatory Zero-Diff Abort, Diff Summary, Git Diff, and Untracked Report Fields | `9819f01 feat: report blk-pipe v47 execution details` | `docs/outcomes/BLK-PIPE-002_task-006-outcome.md` |
| 7 — Add Sequential Validation Command Gate | `2168a4f feat: add blk-pipe validation gate` | `docs/outcomes/BLK-PIPE-002_task-007-outcome.md` |
| 8 — Add Revert Escape Hatch | `22b08e0 feat: add blk-pipe revert action` | `docs/outcomes/BLK-PIPE-002_task-008-outcome.md` |
| 9 — Add Branch/Fetch/Orphan Workspace Preparation For Execute | `2d7582c feat: add blk-pipe branch preparation` | `docs/outcomes/BLK-PIPE-002_task-009-outcome.md` |
| 10 — Add Python Adapter Skeleton and Tests | `91aa93b feat: add blk-pipe python adapter` | `docs/outcomes/BLK-PIPE-002_task-010-outcome.md` |
| 11 — Sprint 002 Documentation and Closeout | `a1c0d73 docs: describe blk-pipe v47 hardening layer` | this closeout document |

---

## 3. Files Added or Changed in Task 11

Task 11 documentation commit:

```text
a1c0d73 docs: describe blk-pipe v47 hardening layer
 README.md                                  |   5 +
 docs/BLK-010_blk-pipe-v47-hardening-cli.md | 252 +++++++++++++++++++++++++++++
 2 files changed, 257 insertions(+)
```

Added:

- `docs/BLK-010_blk-pipe-v47-hardening-cli.md`

Modified:

- `README.md`

Closeout commit adds:

- `docs/outcomes/BLK-PIPE-002_sprint-002-closeout.md`

---

## 4. Behavior and Contract Now Documented

`docs/BLK-010_blk-pipe-v47-hardening-cli.md` documents the completed Sprint 002 behavior only:

- supported local commands:
  - `go run ./cmd/blk-pipe --health`,
  - `go run ./cmd/blk-pipe --payload /tmp/payload.json` with a prepared absolute payload file,
  - optional/internal `go run ./cmd/blk-pipe --payload-stdin`,
- V47-compatible payload fields:
  - `action`,
  - `target_hash`,
  - `ceb_id`,
  - `work_dir`,
  - `target_branch`,
  - `engine`,
  - `engine_args`,
  - `l2_packet`,
  - `validation_commands`,
  - `allowed_modified_files`,
  - `allowed_new_files`,
- legacy migration fields still accepted where implemented:
  - `workdir`,
  - `engine_command`,
  - `timeout_seconds`,
  - `max_output_bytes`,
- stable report fields:
  - `status`,
  - `exit_code`,
  - `action`,
  - `workdir` / `work_dir`,
  - `target_branch`,
  - `ceb_id`,
  - `commit_hash`,
  - `pre_engine_hash`,
  - `git_diff`,
  - `engine_logs`,
  - `validation_logs`,
  - `diff_summary`,
  - `untracked_files`,
  - `staged_files`,
  - `destroyed_files`,
  - `engine_exit_code`,
  - `engine_output_bytes`,
  - `error`,
- strict V47 router codes `0-5`, separated from local extension codes `6`, `7`, and `9`,
- fatal signal and panic behavior,
- sequential validation gate behavior,
- verified revert escape hatch behavior,
- branch/fetch/orphan preparation behavior,
- Python adapter path and API surface,
- remaining deferrals and recommended Sprint 003 seed scope.

The README now links `docs/BLK-010_blk-pipe-v47-hardening-cli.md` beside the prior doctrine documents and calls out the Sprint 002 hardening layer.

---

## 5. TDD / RED-GREEN Evidence for Task 11

Task 11 was documentation-only, but the implementation subagent still used docs-validation-first discipline before writing the new contract document.

### 5.1 RED

Before creating `docs/BLK-010_blk-pipe-v47-hardening-cli.md`, the implementer ran a validation check that required the file and expected contract phrases to exist.

Observed RED evidence:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'docs/BLK-010_blk-pipe-v47-hardening-cli.md'
```

This was the expected failure because the Task 11 contract document did not exist yet.

### 5.2 GREEN

After writing `docs/BLK-010_blk-pipe-v47-hardening-cli.md` and updating `README.md`, validation passed for:

- required contract phrases,
- balanced Markdown fences,
- no trailing whitespace,
- final newlines,
- `git diff --check`,
- `git diff --cached --check` before commit.

The implementation subagent also ran the required regression commands before committing:

```text
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
git diff --check
```

The initial documentation commit was amended once after review found wording overclaims.

---

## 6. Review Results

### 6.1 First Review Gate

Spec-compliance reviewer found three documentation gaps:

1. `validation_logs` was described as keyed by command strings, but implementation uses deterministic keys such as `validation_001`.
2. The exit-code table included `VALIDATION_FAILED`, which is not emitted by the completed implementation.
3. `allowed_modified_files` was described as tracked-file-only, while current implementation treats the allowlist arrays as a combined explicit staging boundary.

Code-quality/doc reviewer requested changes for the same overclaims and also noted that the `/tmp/payload.json` command needed to be marked as illustrative or prepared rather than universally copy-pasteable.

### 6.2 Fix Commit Amendment

The fix subagent amended the unpushed documentation commit and corrected:

- `validation_logs` wording to deterministic sequential keys,
- current Sprint 002 exit-code/status wording,
- allowlist boundary wording,
- `/tmp/payload.json` illustrative/prepared wording,
- heading capitalization.

Amended implementation commit:

```text
a1c0d73c5a197edbe9b5b66050d4e692662fe3ba docs: describe blk-pipe v47 hardening layer
```

### 6.3 Final Review Gate

Spec-compliance re-review result:

```text
PASS
```

Code-quality/doc re-review result:

```text
Critical: None.
Important: None.
Minor: None.
Verdict: APPROVED.
```

The final reviewer confirmed:

- README links resolve,
- Markdown fences and whitespace are clean,
- the previous wording overclaims were fixed,
- no broad staging examples were introduced,
- no `git stash` instruction was introduced,
- no triple-dot diff instruction was introduced,
- no relative revert-anchor example was introduced,
- Codex/LLM references are negative/deferred rather than invocation instructions.

---

## 7. Final Verification Evidence

Controller verification before pushing the implementation commit:

```text
Command:
set -e
export PATH="$HOME/.local/bin:$PATH"
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
go run ./cmd/blk-pipe --health
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
git diff --check
git status --short --branch
git log --oneline --decorate -4
git push origin main
git status --short --branch

Result:
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
.........
----------------------------------------------------------------------
Ran 9 tests in 0.249s

OK
{"status":"OK","component":"blk-pipe"}
## main...origin/main [ahead 1]
?? python/__pycache__/
a1c0d73 (HEAD -> main) docs: describe blk-pipe v47 hardening layer
4399973 (origin/main) docs: record BLK-pipe sprint 002 task 10 outcome
91aa93b feat: add blk-pipe python adapter
7464eff docs: record BLK-pipe sprint 002 task 9 outcome
To https://github.com/camcamcami/BLK-System.git
   4399973..a1c0d73  main -> main
## main...origin/main
?? python/__pycache__/
```

Python tests generated `python/__pycache__/`; the controller removed it after verification and confirmed the worktree was clean:

```text
rm -rf python/__pycache__
git status --short --branch

## main...origin/main
```

Controller verification repeated before writing this closeout document:

```text
Command:
set -e
export PATH="$HOME/.local/bin:$PATH"
go test ./...
python3 -m unittest discover -s python -p 'test_*.py'
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
git diff --check
go run ./cmd/blk-pipe --health
git status --short --branch

Result:
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
.........
----------------------------------------------------------------------
Ran 9 tests in 0.254s

OK
{"status":"OK","component":"blk-pipe"}
## main...origin/main
?? python/__pycache__/
```

The second Python run also generated `python/__pycache__/`; it was removed before this closeout file was committed, leaving:

```text
## main...origin/main
```

---

## 8. Production Safety Grep Results

Production broad-staging grep:

```bash
! git grep -n -E '"add",[[:space:]]*"(\\.|-u)"' -- '*.go' ':!*_test.go'
```

Result: no matches, exit status `0` under shell negation.

Production direct-Git-call grep:

```bash
! git grep -n 'exec.Command("git"' -- '*.go' ':!*_test.go' ':!internal/gitguard/command.go' ':!internal/testutil/**'
```

Result: no matches, exit status `0` under shell negation.

---

## 9. Sprint 002 Acceptance Criteria Status

| Criterion | Status |
|---|---|
| `go test ./...` passes | Complete |
| `go run ./cmd/blk-pipe --health` remains deterministic | Complete |
| `--payload /absolute/path` still works | Complete |
| Sprint 001 payloads remain supported during migration | Complete |
| V47-compatible payloads are accepted for local fake-engine execution | Complete |
| Strict V47 router codes `0-5` are documented separately from local extensions | Complete |
| Exit code `4` is reserved for invalid revert anchor only | Complete |
| Engine non-zero exits no longer use code `4` | Complete |
| Signal/panic paths emit fatal behavior and exit `1` | Complete |
| Validation command failures restore the repo and exit `2` | Complete |
| Validation never runs after detected `.git` mutation | Complete |
| Unauthorized mutations exit `3` and leave the repo clean | Complete |
| Zero-diff/no-staged-allowed-change exits `3` and leaves the repo clean | Complete |
| Output floods exit `5` and leave the repo clean | Complete |
| Timeouts remain bounded and leave the repo clean | Complete |
| Production Git calls route through the bounded Git helper | Complete |
| Production code contains no broad staging commands | Complete |
| Final diff extraction uses `git diff <Hash> HEAD --`, not triple-dot diff | Complete |
| Revert uses verified `target_hash`, rejects relative anchors, and refuses dirty pre-existing work | Complete |
| Branch/orphan handling initializes orphan branches before capturing HEAD and does not inherit previous branch files | Complete |
| Python adapter shells out without shell and cleans temp payloads | Complete |
| No Codex/live LLM integration is introduced | Complete |

---

## 10. Remaining BLK-004/V47 Deviations and Deferrals

Sprint 002 intentionally stops before live tactical-engine integration. Remaining or deferred work includes:

1. **No live Codex invocation.** `blk-pipe` can execute payload-provided local commands, but Sprint 002 does not wire the adapter or a higher-level orchestrator to live Codex.
2. **No CEB/L2 orchestration lifecycle.** `l2_packet` is transported in the payload contract, but Sprint 002 does not implement CEB packet generation, Discord HITL, BEB/BEO lifecycle automation, or RTM generation.
3. **No BLK-test MCP integration.** Validation commands are local bounded commands; future work may route validation through BLK-test if doctrine is ready.
4. **No daemon/service mode.** `blk-pipe` remains an explicit CLI binary.
5. **POSIX scope only.** Windows support remains out of scope.
6. **Process containment is still process-group/procfs based.** Sprint 002 hardened signal cleanup and inherited-pipe process discovery on Linux, but full sandbox containment of hostile descendants that escape process groups and close inherited FDs remains future OS-level supervision work.
7. **Allowlist names preserve intent, not tracked/new semantics.** `allowed_modified_files` and `allowed_new_files` are validated explicit path boundaries, but Sprint 002 still treats them as a combined staging boundary rather than enforcing tracked-vs-new semantics separately.
8. **Local extension exit codes remain documented.** Strict V47 router codes are `0-5`; local extensions `6`, `7`, and `9` are retained defensively until doctrine decides whether to collapse them.

---

## 11. Recommended Sprint 003 Seed Scope

Recommended Sprint 003 work should remain controlled and test-first:

1. Decide whether tactical execution invokes Codex directly through `engine`/`engine_args` or through a higher-level Hermes/Python orchestrator.
2. Add Codex dry-run/fake-engine parity tests before any live Codex run.
3. Add CEB/L2 packet fixture tests around payload construction.
4. Add operational timeout defaults and observability for long tactical runs.
5. Integrate BLK-test validation adapters if doctrine is ready.
6. Add human-in-the-loop safety gates before live model execution.
7. Decide whether allowlist arrays should enforce tracked/new semantics separately or remain a combined explicit staging boundary.
8. Decide whether local extension exit codes `6`, `7`, and `9` should remain or be collapsed into strict V47 code families.

Codex/live engine integration should remain blocked until Sprint 002 behavior is accepted as the deterministic file-boundary, validation, revert, branch, signal, and adapter baseline.

---

## 12. Notes

- The Sprint 002 documentation task used subagent implementation and two-stage review gates.
- The first review caught real contract wording overclaims, and the implementation commit was amended before push.
- Python adapter tests create `python/__pycache__/`; it was removed after verification runs and before committing this closeout document.
- `origin/main` was aligned after the Task 11 documentation commit was pushed.
- This closeout document is the final sprint outcome artifact for Sprint 002.
