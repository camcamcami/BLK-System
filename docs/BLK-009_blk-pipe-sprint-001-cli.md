# BLK-009 — BLK-pipe Sprint 001 CLI Contract

**Status:** Active Sprint 001 developer contract
**Scope:** `blk-pipe` deterministic execution kernel
**Date:** 2026-05-03

---

## 1. Scope and Status

BLK-pipe Sprint 001 establishes the first local, deterministic execution kernel for BLK-System. It is intentionally small: a local developer can provide a minimal JSON payload describing bounded engine execution, BLK-pipe can run a local fake or shell engine inside a clean Git repository, and BLK-pipe can stage and commit only explicitly allowlisted mutations.

Sprint 001 does not run Codex. It does not call live tactical LLMs, remote model APIs, Discord HITL loops, Python adapters, MCP servers, or full BLK-004/V47 orchestration. Those integrations remain deferred until the mechanical safety kernel is stable and well-tested.

The current Sprint 001 CLI contract is useful for local development and safety testing. It is not the final BLK-pipe V47 contract.

---

## 2. Supported Developer Commands

Run all Go tests from the repository root:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
```

Check CLI health:

```bash
export PATH="$HOME/.local/bin:$PATH"
go run ./cmd/blk-pipe --health
```

Expected output:

```json
{"status":"OK","component":"blk-pipe"}
```

Run BLK-pipe with a physical payload file:

```bash
export PATH="$HOME/.local/bin:$PATH"
go run ./cmd/blk-pipe --payload /tmp/payload.json
```

The path passed to `--payload` must be absolute. BLK-pipe reads the file bytes and sends them directly into the same pipe execution path used by stdin mode.

---

## 3. Optional Internal Command

Sprint 001 retains the explicit stdin entrypoint added during pipe orchestration work:

```bash
export PATH="$HOME/.local/bin:$PATH"
go run ./cmd/blk-pipe --payload-stdin
```

`--payload-stdin` is useful for tests and internal harnesses. It is intentionally explicit so zero-argument invocation does not block while waiting for stdin.

---

## 4. Unsupported Invocations

The following invocations are invalid payload cases in Sprint 001:

```bash
go run ./cmd/blk-pipe
go run ./cmd/blk-pipe --payload
go run ./cmd/blk-pipe --payload relative/payload.json
go run ./cmd/blk-pipe --payload /absolute/path/that/does/not/exist.json
go run ./cmd/blk-pipe --unknown
```

Current behavior:

- zero arguments return invalid payload and print `unsupported invocation`,
- unknown flags return invalid payload and print `unsupported invocation`,
- `--payload` without a path returns invalid payload and prints `unsupported invocation`,
- `--payload` with a relative path returns invalid payload and prints `payload path must be absolute`,
- `--payload` with a missing or unreadable file returns invalid payload and prints an error beginning with `read payload file:`.

When using `go run`, Go may wrap non-zero program exits and return shell exit code `1` while printing `exit status <code>`. Unit tests call the internal `run(...)` helper directly and assert BLK-pipe's own exit codes.

---

## 5. Sprint 001 Payload Schema

Sprint 001 accepts a deliberately minimal payload schema:

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

Field meanings:

| Field | Meaning |
|---|---|
| `action` | Must be `execute` in Sprint 001. |
| `workdir` | Absolute path to the target Git repository. |
| `engine_command` | Local command array executed by the bounded engine runner. Empty or whitespace-only elements are rejected. |
| `allowed_modified_files` | Explicit relative file paths allowlisted for staging. Sprint 001 keeps this name for intent but does not yet enforce tracked-file semantics separately from `allowed_new_files`. |
| `allowed_new_files` | Explicit relative file paths allowlisted for staging. Sprint 001 keeps this name for intent but treats the two allowlist arrays as a combined staging boundary. |
| `timeout_seconds` | Positive execution timeout in seconds. |
| `max_output_bytes` | Positive combined stdout/stderr output cap for the engine. |

Allowlist entries must be clean relative file paths. They must not be absolute paths, `..` traversal, `.`, Git pathspec/glob expressions, or protected BLK-req artifact paths under `docs/requirements/` or `docs/use_cases/`.

---

## 6. Example Payload File

Create a payload file with an absolute `workdir` pointing to a clean Git repository:

```bash
cat > /tmp/payload.json <<'JSON'
{
  "action": "execute",
  "workdir": "/absolute/path/to/clean/git/repo",
  "engine_command": ["sh", "-c", "printf '\nBLK-pipe touched this file\n' >> README.md"],
  "allowed_modified_files": ["README.md"],
  "allowed_new_files": [],
  "timeout_seconds": 5,
  "max_output_bytes": 4096
}
JSON
```

Then run:

```bash
go run ./cmd/blk-pipe --payload /tmp/payload.json
```

For a successful allowlisted mutation, BLK-pipe stages only the allowlisted file, commits with a deterministic message, and emits a JSON report. If unauthorized mutations are detected, BLK-pipe reports `UNAUTHORIZED_FILE_MUTATION`, cleans or restores the run where possible, and does not create a success commit.

---

## 7. Report Fields

Sprint 001 emits a JSON report with these fields:

| Field | Meaning |
|---|---|
| `status` | Final BLK-pipe status string. |
| `action` | Payload action, currently `execute` for valid Sprint 001 payloads. |
| `workdir` | Target repository path from the payload. |
| `commit_hash` | Commit hash created by BLK-pipe on success. Empty on failure. |
| `staged_files` | Files staged and committed by BLK-pipe. |
| `destroyed_files` | Unauthorized mutation paths reported during cleanup/restoration. For `.git` metadata failures, paths may be reported even when BLK-pipe restores metadata before exit. |
| `engine_exit_code` | Exit code returned by the local engine command, where available. |
| `engine_output_bytes` | Count of bounded engine output bytes observed. |
| `error` | Human-readable error detail for failure reports. |

---

## 8. Current Exit Codes

Sprint 002 reconciles the Sprint 001 `ENGINE_FAILED`/code `4` conflict with BLK-004/V47. Non-zero engine exits now use code `1` with `FATAL_ENGINE_FAILED`; code `4` is reserved for `INVALID_REVERT_ANCHOR` before revert support is implemented.

```text
0 SUCCESS
1 FATAL_ENGINE_FAILED
2 INVALID_PAYLOAD
3 UNAUTHORIZED_FILE_MUTATION
4 INVALID_REVERT_ANCHOR (reserved; revert route not implemented as of Sprint 002 Task 1)
5 FATAL_OUTPUT_FLOOD
6 ENGINE_TIMEOUT
7 GIT_DIRTY
9 INTERNAL_ERROR
```

Status strings currently used by the pipe include:

```text
SUCCESS
INVALID_PAYLOAD
UNAUTHORIZED_FILE_MUTATION
FATAL_ENGINE_FAILED
FATAL_OUTPUT_FLOOD
ENGINE_TIMEOUT
GIT_DIRTY
INTERNAL_ERROR
```

---

## 9. Safety Guarantees Implemented in Sprint 001

Sprint 001 includes the following mechanical safety guarantees:

1. **Explicit payload execution only** — health, stdin payload, and file payload entrypoints are explicit; zero-argument invocation does not block on stdin.
2. **Clean Git preflight** — BLK-pipe refuses to run when the target repository already has tracked changes, untracked files, or ignored files.
3. **Bounded engine execution** — engine commands are run with timeout and maximum output byte limits.
4. **Process group cleanup** — timeout/flood/error paths kill the engine process group so child processes and inherited pipe writers do not hang execution.
5. **No broad Git staging** — production staging uses explicit file path staging and avoids `git add .` and `git add -u`.
6. **Allowlist-only staging** — only validated `allowed_modified_files` and `allowed_new_files` can be staged.
7. **Protected BLK-req path denial** — `docs/requirements/` and `docs/use_cases/` paths are hard-denied in payload allowlists.
8. **Unauthorized mutation cleanup** — normal worktree cleanup removes non-allowlisted tracked, untracked, ignored, and nested Git repo mutations. Unauthorized outcomes fail instead of being committed.
9. **`.git` mutation hardening** — `.git` metadata changes are treated as unauthorized, including hidden-file tricks such as `.git/info/exclude` changes and hook installation; `.git` mutation failures are restored before exit where possible.
10. **Hook-disabled commits** — BLK-pipe commits with hooks disabled via `core.hooksPath=/dev/null`.
11. **Nested Git repo cleanup** — cleanup uses double-force Git clean semantics so unauthorized nested repositories are removed.
12. **Deterministic success commit message** — successful engine changes are committed with `blk-pipe: apply bounded engine changes`.

---

## 10. BLK-004 Compatibility Note

Sprint 001 provides the mechanical safety kernel that BLK-004 needs before autonomous execution. It now supports the BLK-004-compatible physical invocation shape:

```bash
blk-pipe --payload <temp_payload_path>
```

However, Sprint 001 does not implement the full BLK-004/V47 contract. It deliberately keeps the payload and report minimal while proving the core safety physics.

Full V47 contract work remains Sprint 002+.

---

## 11. Non-Goals and Deferred V47 Work

Sprint 001 intentionally does not implement:

- Codex invocation or any live tactical LLM execution,
- the Python adapter,
- the full V47 payload schema (`work_dir`, `target_branch`, `engine`, `engine_args`, `beb_id`, `l2_packet`, `validation_commands`, and related fields),
- validation command sequencing or validation log aggregation,
- revert route handling,
- revert ancestry gate or `target_hash` verification,
- full V47 report fields such as `pre_engine_hash`, full diff summaries, validation logs, and untracked-file summaries,
- most V47 hardening-layer work beyond the exit-code registry reconciliation.

Exit-code reconciliation was completed before adding revert support because BLK-004 reserves code `4` for invalid revert anchor; engine failures no longer use code `4`.

---

## 12. Sprint 001 Closeout Verification

Before treating Sprint 001 as complete, run:

```bash
export PATH="$HOME/.local/bin:$PATH"
git status --short
go test ./...
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
```

Expected:

- no uncommitted changes,
- all Go packages pass,
- the production-code broad-staging grep prints no matches.

Sprint 001 closeout should explicitly state that Codex integration remains deferred until later BLK-pipe hardening work.
