# BLK-pipe Sprint 001 — Task 10 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Add BLK-004-compatible payload file CLI invocation
**Implementation Commit:** `b965a54 feat: add blk-pipe payload CLI`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 10 added the physical payload-file invocation shape needed by the BLK-004 Python adapter direction:

```bash
blk-pipe --payload /absolute/path/to/payload.json
```

The goal was intentionally narrow. Sprint 001 still keeps the existing minimal payload/report contracts and does not expand to the full BLK-004/V47 schema. This task only adds the CLI transport bridge so external callers can hand BLK-pipe a payload file path instead of piping JSON through stdin.

The task also required preserving existing explicit entrypoints:

```bash
blk-pipe --health
blk-pipe --payload-stdin
```

Unsupported invocations remain nonblocking invalid payload cases.

---

## 2. Files Changed

### `cmd/blk-pipe/main.go`

Added support for:

```bash
blk-pipe --payload /absolute/path/to/payload.json
```

The new branch:

1. requires exactly one argument after `--payload`,
2. rejects relative paths before file access,
3. reads the payload bytes with `os.ReadFile`,
4. returns `pipe.ExitInvalidPayload` for missing/unreadable files,
5. passes file bytes directly to:

```go
pipe.Run(context.Background(), payloadJSON, stdout)
```

Existing `--health` and `--payload-stdin` behavior remains intact. Zero-argument and unknown invocations still return invalid payload instead of blocking on stdin.

### `cmd/blk-pipe/main_test.go`

Added hermetic CLI tests for payload-file mode:

- `TestPayloadFileInvalidJSONEmitsPipeReport`
- `TestPayloadFileInvalidPayloadEmitsPipeReport`
- `TestPayloadFileRequiresAbsolutePath`
- `TestPayloadFileMissingPathIsInvalidPayload`
- `TestPayloadFlagRequiresPath`

The tests use temporary directories/files and call the `run(args, stdin, stdout, stderr)` helper directly so program exit codes can be asserted without `go run` wrapping nonzero exits.

---

## 3. Behavior Implemented

### 3.1 Supported invocations

```bash
blk-pipe --health
blk-pipe --payload-stdin
blk-pipe --payload /absolute/path/to/payload.json
```

`--payload` file mode reads the file and delegates to the same `pipe.Run` execution path used by `--payload-stdin`.

### 3.2 Rejected invocations

These remain invalid payload invocations:

```bash
blk-pipe
blk-pipe --payload
blk-pipe --payload relative/path.json
blk-pipe --payload /absolute/path/that/does/not/exist.json
blk-pipe --unknown
```

Relative payload paths are rejected with:

```text
payload path must be absolute
```

Missing/unreadable files return `pipe.ExitInvalidPayload` with stderr beginning:

```text
read payload file:
```

### 3.3 BLK-004 compatibility note

This task satisfies the BLK-004 physical adapter invocation shape:

```bash
blk-pipe --payload <temp_payload_path>
```

It does not implement full V47 payload fields, validation commands, revert flow, Python adapter code, or shared V47 exit-code reconciliation. Those remain deferred beyond Sprint 001 as planned.

---

## 4. TDD Evidence

### 4.1 RED

The implementation subagent first added payload-file CLI tests. Before production changes, those tests failed because `--payload` was still an unsupported invocation path and produced no pipe report for the file-mode scenarios.

### 4.2 GREEN

After adding the minimal file-mode branch, focused and package tests passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./cmd/blk-pipe -run 'TestPayloadFile|TestPayloadFlag' -v
go test ./cmd/blk-pipe -v
go test ./...
```

Controller-side final verification also passed before push.

---

## 5. Review Results

Two independent review gates were run against local commit `b965a54` before pushing.

### 5.1 Spec compliance review

**Result:** PASS

Evidence confirmed:

- commit message matched `feat: add blk-pipe payload CLI`,
- only `cmd/blk-pipe/main.go` and `cmd/blk-pipe/main_test.go` changed,
- `--payload /absolute/path/to/payload.json` is implemented,
- absolute path validation occurs before file read,
- file bytes are passed to `pipe.Run(context.Background(), payloadJSON, stdout)`,
- `--health` and `--payload-stdin` remain preserved,
- zero args, missing path, relative path, missing file, and unknown flags remain invalid payload paths,
- no V47 schema expansion or unrelated pipe changes were introduced.

### 5.2 Code quality and safety review

**Result:** APPROVED

Evidence confirmed:

- payload-file mode uses `os.ReadFile` directly and does not invoke a shell,
- file-read failures return `pipe.ExitInvalidPayload`,
- stderr for read failures uses deterministic prefix `read payload file:`,
- tests are hermetic and use temporary files,
- there is no broad Git staging, pipe mutation, contract expansion, or unrelated scope creep.

The reviewer noted one non-blocking observation: there is no separate test proving file mode ignores stdin, but the implementation branch does not reference stdin and existing coverage was sufficient for Task 10.

---

## 6. Final Verification

The controller ran final verification before pushing:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go
go test ./cmd/blk-pipe -run 'TestPayloadFile|TestPayloadFlag' -v
go test ./cmd/blk-pipe -v
go test ./...
git diff --check HEAD^ HEAD
go run ./cmd/blk-pipe --health
git push origin main
```

Results:

- `gofmt -l` produced no output,
- focused payload-file tests passed,
- full CLI package tests passed,
- full Go suite passed,
- `git diff --check HEAD^ HEAD` passed,
- health smoke output remained:

```json
{"status":"OK","component":"blk-pipe"}
```

Full suite packages passing:

```text
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/testutil
```

---

## 7. GitHub State

Implementation commit pushed:

```text
b965a54 feat: add blk-pipe payload CLI
```

After push, local `main` and `origin/main` were aligned at `b965a54`.

---

## 8. Deviations / Notes

- No production code outside `cmd/blk-pipe` changed.
- No payload/report contract expansion was made.
- No BLK-004/V47 revert behavior, validation command execution, Python adapter, or full V47 report schema was added.
- `go run` can wrap nonzero program exits and return shell exit code `1` while printing `exit status 2`; unit tests call `run(...)` directly and assert BLK-pipe's intended `pipe.ExitInvalidPayload` code.

---

## 9. Next Task

Task 11 remains: document Sprint 001 CLI usage and safety guarantees.

Expected Task 11 outputs include:

- creating `docs/BLK-009_blk-pipe-sprint-001-cli.md`,
- updating `README.md`,
- documenting supported CLI entrypoints,
- documenting Sprint 001 payload and report fields,
- documenting safety guarantees,
- explicitly listing BLK-004/V47 deferrals,
- documenting that Sprint 001 does not execute Codex directly.
