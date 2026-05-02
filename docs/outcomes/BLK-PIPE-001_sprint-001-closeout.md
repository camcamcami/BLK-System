# BLK-pipe Sprint 001 Closeout

**Status:** Complete
**Date:** 2026-05-03
**Sprint:** BLK-pipe Sprint 001 — deterministic execution kernel
**Task-line Final Commit Before Closeout Note:** `628b943 docs: record BLK-pipe task 11 outcome`
**Sprint Closeout Commit:** `b5f5456 docs: close out blk-pipe sprint 001`
**Remote:** `origin/main`

---

## 1. Closeout Summary

BLK-pipe Sprint 001 is complete.

Sprint 001 produced the first deterministic local execution kernel for BLK-System. The sprint established a small but strong mechanical safety base before any Codex/live LLM execution is connected:

- local Go CLI skeleton,
- explicit health and payload entrypoints,
- minimal Sprint 001 payload/report contracts,
- hermetic Git test utilities,
- clean Git preflight,
- bounded local engine runner,
- allowlist-only staging,
- unauthorized mutation cleanup,
- full pipe orchestration,
- protected BLK-req artifact path denial,
- BLK-004-compatible payload-file CLI invocation,
- Sprint 001 developer-facing CLI documentation.

Codex integration remains deferred. Sprint 001 intentionally uses local fake/shell engines and does not invoke live tactical LLMs.

---

## 2. Final Verification

Final closeout verification was run from `/home/dad/BLK-System` with the local Go toolchain on `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
git status --short --branch
go test ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
git diff --check
```

Observed results:

```text
## main...origin/main
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/testutil
```

The production-code broad-staging grep printed no matches, and `git diff --check` passed. The original broad text grep was narrowed to production Go argv patterns to avoid expected documentation/comment false positives while still checking the safety property: no production code invokes `git add .` or `git add -u`.

---

## 3. Implemented Exit Codes

Sprint 001 currently implements:

```text
0 SUCCESS
2 INVALID_PAYLOAD
3 UNAUTHORIZED_FILE_MUTATION
4 ENGINE_FAILED
5 FATAL_OUTPUT_FLOOD
6 ENGINE_TIMEOUT
7 GIT_DIRTY
9 INTERNAL_ERROR
```

Known note: BLK-004/V47 reserves code `4` for invalid revert anchor. Sprint 001 uses code `4` for `ENGINE_FAILED`, so Sprint 002 must reconcile the shared exit-code registry before adding revert behavior.

---

## 4. Implemented Tasks

### Task 1 — Initialize CLI and exit-code constants

Commit:

```text
7a681ce feat: initialize blk-pipe Go CLI
```

Outcome:

```text
5bb37da docs: record BLK-pipe task 1 outcome
```

Implemented a Go module, `blk-pipe --health`, and initial exit-code constants.

### Task 2 — Define payload/report contracts

Commit:

```text
95f01b8 feat: define blk-pipe payload contracts
```

Outcome:

```text
5cdfeb4 docs: record BLK-pipe task 2 outcome
```

Implemented Sprint 001 payload and report contracts with validation for action, absolute workdir, engine command, allowlist paths, timeout, output cap, Git pathspec/glob hazards, and protected BLK-req artifact paths.

### Task 3 — Add hermetic Git repository test utility

Commit:

```text
fc2bd98 test: add git repository test utility
```

Outcome:

```text
be8a322 docs: record BLK-pipe task 3 outcome
```

Added a hermetic Git test helper that filters inherited `GIT_*` environment state and disables global/system Git config.

### Task 4 — Enforce clean Git preflight

Commit:

```text
8fa61c6 feat: enforce clean git preflight
```

Outcome:

```text
eff481a docs: record BLK-pipe task 4 outcome
```

Added deterministic clean-repo preflight using Git porcelain status with untracked-file visibility.

### Task 5 — Add bounded engine runner

Commit:

```text
a86af82 feat: add bounded engine runner
```

Outcome:

```text
ec33df1 docs: record BLK-pipe task 5 outcome
```

Added bounded local engine execution with timeout, output cap, process-group kill behavior, and regression coverage for inherited pipe writers.

### Task 6 — Stage only allowlisted files

Commit:

```text
6250618 feat: stage only allowlisted files
```

Outcome:

```text
bfcd39d docs: record BLK-pipe task 6 outcome
```

Added explicit allowlist-only staging via `git add -- <path>` and rejected broad/directory/deletion/pathspec hazards.

### Task 7 — Destroy unauthorized mutations

Commit:

```text
cbe11b0 feat: destroy unauthorized mutations
```

Outcome:

```text
7ee6a9a docs: record BLK-pipe task 7 outcome
```

Added cleanup for unauthorized tracked/untracked mutations while preserving the staging safety sequence.

### Task 8 — Orchestrate bounded pipe execution

Commit:

```text
0a05ba3 feat: orchestrate bounded blk-pipe execution
```

Outcome:

```text
b1d94a9 docs: record BLK-pipe task 8 outcome
```

Implemented the main pipe execution sequence:

```text
validate payload → clean repo preflight → run engine → stage allowlist → cleanup unauthorized mutations → commit/report
```

Task 8 also hardened `.git` mutation detection/restoration, hook-disabled commits, ignored/untracked preflight, and nested Git repo cleanup.

### Task 9 — Hard-deny BLK-req artifact mutations

Commit:

```text
fbc3a6c feat: hard-deny blk-req artifact mutations
```

Outcome:

```text
68f0089 docs: record BLK-pipe task 9 outcome
```

Added explicit regression coverage proving `docs/requirements/` and `docs/use_cases/` allowlist entries are rejected before engine execution.

### Task 10 — Add payload-file CLI support

Commit:

```text
b965a54 feat: add blk-pipe payload CLI
```

Outcome:

```text
df60523 docs: record BLK-pipe task 10 outcome
```

Added the BLK-004-compatible physical invocation shape:

```bash
blk-pipe --payload /absolute/path/to/payload.json
```

The CLI preserves `--health` and `--payload-stdin`, rejects relative payload paths, and treats missing/unreadable payload files as invalid payload invocations.

### Task 11 — Document Sprint 001 CLI

Commit:

```text
94a5e9b docs: describe blk-pipe sprint 001 CLI
```

Outcome:

```text
628b943 docs: record BLK-pipe task 11 outcome
```

Created `docs/BLK-009_blk-pipe-sprint-001-cli.md` and updated `README.md` so local developers can find the Sprint 001 CLI contract and safety guarantees.

---

## 5. Current CLI Contract

Supported Sprint 001 commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go run ./cmd/blk-pipe --health
go run ./cmd/blk-pipe --payload /tmp/payload.json
go run ./cmd/blk-pipe --payload-stdin
```

`--payload` requires an absolute payload-file path.

Zero-argument invocation remains unsupported/nonblocking and returns invalid payload.

---

## 6. Current Payload Contract

Sprint 001 payloads use this minimal schema:

```json
{
  "action": "execute",
  "workdir": "/absolute/path/to/repo",
  "engine_command": ["sh", "-c", "printf after > README.md"],
  "allowed_modified_files": ["README.md"],
  "allowed_new_files": [],
  "timeout_seconds": 5,
  "max_output_bytes": 4096
}
```

Sprint 001 validates allowlist paths as explicit relative file paths and rejects:

- absolute paths,
- `..` traversal,
- `.`,
- Git pathspec/glob metacharacters,
- protected `docs/requirements/` paths,
- protected `docs/use_cases/` paths.

---

## 7. Current Report Contract

Sprint 001 reports include:

- `status`,
- `action`,
- `workdir`,
- `commit_hash`,
- `staged_files`,
- `destroyed_files`,
- `engine_exit_code`,
- `engine_output_bytes`,
- `error`.

---

## 8. Safety Guarantees Achieved

Sprint 001 currently provides:

1. explicit CLI entrypoints for health, stdin payload, and file payload,
2. clean Git preflight before engine execution,
3. bounded engine timeout and output,
4. process-group cleanup for timeout/flood/error behavior,
5. allowlist-only staging,
6. no production broad Git staging commands,
7. protected BLK-req artifact path denial,
8. unauthorized mutation cleanup,
9. `.git` mutation hardening and restoration where possible,
10. hook-disabled commits,
11. ignored/untracked preflight,
12. nested Git repo cleanup,
13. deterministic success commit message.

---

## 9. BLK-004 / BLK-006 Deviations and Deferrals

Sprint 001 aligns with BLK-004 by establishing a deterministic compiled transport and the physical payload-file invocation:

```bash
blk-pipe --payload <temp_payload_path>
```

Sprint 001 intentionally does not implement full BLK-004/V47.

Deferred BLK-004/V47 work:

- full V47 payload schema,
- Python adapter,
- revert route,
- revert ancestry gate with `target_hash`,
- validation command sequencing and validation log aggregation,
- full V47 report fields,
- complete environment scrub including SSH-related variables,
- shared bounded Git command helper if required by final V47 doctrine,
- branch/fetch/orphan handling,
- exit-code registry reconciliation,
- Codex/live engine integration.

BLK-006 protected-path behavior is enforced for BLK-req artifact paths:

```text
docs/requirements/*
docs/use_cases/*
```

Those paths are hard-denied in payload allowlists and regression-tested at both contract and pipe layers.

---

## 10. Codex Integration Status

Codex integration remains deferred.

Sprint 001 intentionally does not run Codex, OpenAI models, local LLMs, or any live tactical AI engine. The safety kernel must remain deterministic and physically testable before autonomous engine integration is introduced.

---

## 11. Recommended Sprint 002 Scope

Recommended Sprint 002 seed scope:

1. Reconcile BLK-pipe exit-code registry with BLK-004/V47.
2. Introduce full V47 payload schema or a compatibility adapter.
3. Add validation command sequencing and validation log aggregation.
4. Add revert action with verified `target_hash` and no relative anchors.
5. Add Python adapter around `blk-pipe --payload <file>`.
6. Add full environment scrub:
   - `GIT_*`,
   - `SSH_AUTH_SOCK`,
   - `SSH_AGENT_PID`,
   - `SSH_ASKPASS`,
   - deterministic `PWD`.
7. Decide whether all Git calls must route through a generalized bounded Git helper.
8. Add branch/fetch/orphan handling.
9. Only then revisit Codex/live engine integration.

---

## 12. Final State

At closeout verification time:

```text
Branch: main
Remote: origin/main
Latest task-line commit: 628b943 docs: record BLK-pipe task 11 outcome
Working tree: clean
Go suite: passing
Production broad staging grep: no matches
Markdown diff check: passing
```

BLK-pipe Sprint 001 is complete and ready to serve as the deterministic safety foundation for Sprint 002 planning.
