# BLK-010 — BLK-pipe Sprint 002 V47 Hardening CLI Contract

**Status:** Active Sprint 002 V47-compatible developer contract
**Scope:** `blk-pipe` deterministic transport and safety layer
**Date:** 2026-05-03

---

## 1. Scope and Status

BLK-pipe is a deterministic transport and safety layer. It is not a code parser, tactical LLM caller, autonomous decision maker, or operating-system sandbox. Sprint 002 hardens the Sprint 001 local execution kernel toward the BLK-004/V47 contract by adding compatible payload/report fields, bounded Git operations, fatal-system handling, validation gates, revert behavior, target-branch preparation, and a thin Python adapter. Sprint 002.2 further hardens process cleanup, validation authority, validation safety classification, and `l2_packet` stdin transport.

Sprint 002 does not run Codex. Sprint 002.2 does not run Codex. It does not call OpenAI, local LLMs, live tactical engines, Discord HITL loops, MCP servers, or network model services. Engine execution remains whatever bounded local command the payload explicitly supplies.

The Sprint 002 contract is V47-compatible where implemented, but it is still a local hardening layer rather than the full BLK-004 autonomous orchestration system. For operator-facing cyber readiness and usability guardrails, see [`BLK-011 — BLK-pipe Cyber Readiness and Usability Guardrails`](BLK-011_blk-pipe-cyber-readiness-and-usability.md).

---

## 2. Supported Commands

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

Current health output is:

```json
{"status":"OK","component":"blk-pipe"}
```

Run BLK-pipe with a prepared physical payload file:

```bash
export PATH="$HOME/.local/bin:$PATH"
go run ./cmd/blk-pipe --payload /tmp/payload.json
```

The path passed to `--payload` must be absolute. The `/tmp/payload.json` path above is illustrative; create that payload file first or replace it with another prepared absolute payload path.

Optional/internal stdin payload entrypoint:

```bash
export PATH="$HOME/.local/bin:$PATH"
go run ./cmd/blk-pipe --payload-stdin
```

`--payload-stdin` is retained for tests and harnesses. It is intentionally explicit so zero-argument invocation does not block waiting for stdin.

---

## 3. V47-Compatible Payload Fields

Sprint 002 accepts `action` values `execute` and `revert`.

For V47-compatible execute payloads, accepted fields are:

| Field | Sprint 002 behavior |
|---|---|
| `action` | Required; `execute` or `revert`. |
| `target_hash` | Required for `revert`; must be a full 40- or 64-character hexadecimal commit object ID. |
| `ceb_id` | Accepted and reported for traceability. |
| `work_dir` | V47 work directory field; normalized internally to `workdir`; must be absolute. |
| `target_branch` | Optional execute branch target; validated with a conservative Git branch-name policy before Git receives it. |
| `engine` | V47 command executable; normalized with `engine_args` to the bounded local engine command. |
| `engine_args` | V47 command arguments appended after `engine`. |
| `l2_packet` | Accepted for contract compatibility and traceability; Sprint 002.2 delivers it to engine stdin, bounds its size, does not parse or decide from it, and does not log the packet body by default. |
| `validation_commands` | Sequential validation commands run after engine success and before staging/commit. |
| `allowed_modified_files` | Explicit relative path allowlist for permitted modifications; together with `allowed_new_files`, this forms the combined staging boundary. Sprint 002 keeps the intent names but does not separately enforce tracked-vs-new file semantics. |
| `allowed_new_files` | Explicit relative new-file allowlist for permitted new files. |

Legacy migration fields remain accepted:

| Field | Sprint 002 behavior |
|---|---|
| `workdir` | Legacy absolute work directory; accepted when it does not conflict with `work_dir`. |
| `engine_command` | Legacy command array; accepted when it does not conflict with `engine`/`engine_args`. |
| `timeout_seconds` | Positive execution timeout; V47-shaped payloads default to 900 seconds when omitted. |
| `max_output_bytes` | Positive combined output cap; V47-shaped payloads default to 52,428,800 bytes when omitted. |

Allowlist entries must be explicit clean relative file paths. They must not be absolute, empty, `.`, contain `..`, include Git pathspec metacharacters, or target protected BLK-req artifact paths under `docs/requirements/` or `docs/use_cases/`.

Example execute payload:

```json
{
  "action": "execute",
  "ceb_id": "CEB_011",
  "work_dir": "/absolute/path/to/clean/git/repo",
  "target_branch": "sprint/ceb-011",
  "engine": "sh",
  "engine_args": ["-c", "printf after > README.md"],
  "l2_packet": "## bounded local packet",
  "validation_commands": ["go test ./..."],
  "allowed_modified_files": ["README.md"],
  "allowed_new_files": []
}
```

Example revert payload:

```json
{
  "action": "revert",
  "work_dir": "/absolute/path/to/clean/git/repo",
  "target_hash": "0123456789abcdef0123456789abcdef01234567"
}
```

---

## 4. Stable V47-Compatible Report Fields

Sprint 002 emits one JSON report for payload execution. Stable V47-compatible report fields include:

| Field | Meaning |
|---|---|
| `status` | Final status string. |
| `exit_code` | BLK-pipe process/router exit code. |
| `action` | Payload action after decode. |
| `workdir` | Normalized internal work directory. |
| `work_dir` | V47 work directory field when present in the decoded payload. |
| `target_branch` | Payload target branch when present. |
| `ceb_id` | Payload CEB ID when present. |
| `commit_hash` | Success commit hash for execute payloads; empty on failures and revert success. |
| `pre_engine_hash` | HEAD before engine execution for execute payloads. |
| `git_diff` | Diff from `pre_engine_hash` to success commit. |
| `engine_logs` | Bounded combined engine stdout/stderr. |
| `validation_logs` | Map of deterministic sequential validation keys such as `validation_001`, `validation_002` to bounded command output. |
| `diff_summary` | Optional changed-file/insertions/deletions summary on execute success. |
| `untracked_files` | Stable list field for untracked-file reporting. |
| `staged_files` | Files staged for the success commit. |
| `destroyed_files` | Unauthorized mutation paths detected/cleaned on failure paths. |
| `engine_exit_code` | Local engine process exit code when observed. |
| `engine_output_bytes` | Bounded engine output byte count. |
| `error` | Human-readable error detail on non-success paths. |

Successful execute runs commit with message `blk-pipe: apply bounded engine changes`.

---

## 5. Strict V47 Router Exit Codes and Local Extensions

Sprint 002 aligns the strict V47 router exit-code meanings where implemented and retains local defensive extensions. The table lists status strings emitted by the completed Sprint 002 implementation and calls out strict V47 family names where they differ:

| Code | Status strings | Meaning |
|---:|---|---|
| 0 | `SUCCESS` | Execution or revert completed successfully. |
| 1 | `FATAL_SYSTEM_PANIC`, `FATAL_ENGINE_FAILED` | Fatal signal/panic or non-zero engine failure routed through the strict V47 fatal family. Strict V47 also names `INTERNAL_ERROR` in this family, but the current Sprint 002 implementation emits `INTERNAL_ERROR` through local extension code `9`. |
| 2 | `SYNTAX_GATE_FAILED`, `INVALID_PAYLOAD` | Invalid payload or validation/syntax gate failure family. Validation command failures currently emit `SYNTAX_GATE_FAILED`; payload validation failures emit `INVALID_PAYLOAD`. |
| 3 | `UNAUTHORIZED_FILE_MUTATION` | Engine or validation changed files outside the allowlist or produced no staged allowlisted diff. |
| 4 | `INVALID_REVERT_ANCHOR` | Revert target is invalid, not a full object ID, not a commit, or not an ancestor of `HEAD`. |
| 5 | `FATAL_OUTPUT_FLOOD` | Engine output exceeded `max_output_bytes`. |
| 6 | `ENGINE_TIMEOUT` | Local extension: bounded engine timeout. |
| 7 | `GIT_DIRTY` | Local extension: dirty target repository/branch workspace. |
| 9 | `INTERNAL_ERROR` | Local extension retained defensively for current infrastructure/reporting failures. |

When using `go run`, Go can wrap non-zero program exits and return shell exit code `1` while printing `exit status <code>`. Tests assert BLK-pipe's own internal exit-code values directly.

---

## 6. Signal/Panic Fatal Behavior

On POSIX builds (`linux` and `darwin` build tags), Sprint 002 wraps payload execution in a fatal-system guard. SIGINT, SIGTERM, and recovered panics produce one sterile JSON fatal report with status `FATAL_SYSTEM_PANIC`, exit code `1`, and an error such as `fatal signal received` or `fatal system panic`.

The report gate buffers normal output until no fatal condition wins. If a fatal signal or panic occurs, buffered normal output is discarded, active process groups are reaped through the execution guard where possible, and BLK-pipe returns the fatal code instead of mixing partial reports with fatal output.

---

## 7. Validation Gate Behavior

For execute payloads, BLK-pipe runs the bounded local engine first. If the engine succeeds and does not flood or time out, BLK-pipe runs `validation_commands` sequentially in the target work directory using the same timeout and output-bound discipline. Empty or whitespace-only validation commands are rejected during payload validation.

Validation output is aggregated in `validation_logs`. If any validation command fails, BLK-pipe reports `SYNTAX_GATE_FAILED` with exit code `2`, cleans/restores the run where possible, and does not create a success commit. If validation mutates files outside the allowlist, mutates the engine-produced candidate state, or mutates `.git`, BLK-pipe reports `UNAUTHORIZED_FILE_MUTATION`, records paths in `destroyed_files`, cleans/restores the run, and does not create a success commit.

Validation commands are local shell commands supplied by the payload. They are not interpreted as autonomous decisions. Sprint 002.2 treats validation commands as read-only gates over the post-engine candidate; use check-only modes and external caches/temp dirs rather than write modes in the production worktree.

---

## 8. Revert Route Behavior

Sprint 002 implements the `revert` action. A revert payload must provide an absolute work directory and full hexadecimal `target_hash`. BLK-pipe verifies that the target hash resolves exactly to a commit object in the repository and is an ancestor of `HEAD`. Relative anchors, abbreviations, non-commit objects, and non-ancestor commits are rejected as `INVALID_REVERT_ANCHOR` with exit code `4`.

On a valid revert, BLK-pipe performs a hard reset to `target_hash`, cleans untracked and ignored files with bounded Git helpers, verifies the workspace is clean, emits `SUCCESS`, and does not create a new commit.

---

## 9. Branch/Fetch/Orphan Behavior

For execute payloads with `target_branch`, Sprint 002 validates the branch name before invoking Git. The validator rejects option-like names, whitespace/control characters, path traversal, reserved refs/revisions, reflog syntax, hidden or lock ref components, shell metacharacters, pathspec metacharacters, and revision-range syntax.

BLK-pipe then requires a clean repository, detects whether `origin` exists, fetches `origin` when present, checks out an existing local branch when available, checks out an existing remote-tracking branch when available, and can use hardened headless SSH settings for `ls-remote` branch discovery. If no local or remote branch is available, BLK-pipe creates an orphan branch and initializes it with an empty commit whose message is `Initialize branch`.

After branch preparation, BLK-pipe performs hard reset and double-force clean sterilization before engine execution. Broad staging remains banned: production staging uses explicit allowlist path arguments and does not use `git add .` or `git add -u`.

---

## 10. Python Adapter Path

Task 10 added the thin Python adapter at `python/blk_pipe_adapter.py` with tests in `python/test_blk_pipe_adapter.py`. The adapter writes a temporary JSON payload file and invokes the binary with `--payload <temp_payload_path>`. It exposes `run_health_check`, `execute_sprint`, and `abort_sprint_and_revert` helpers and maps BLK-pipe return codes into adapter result statuses.

The adapter intentionally contains no tactical-engine or LLM integration. It is only a local subprocess bridge to the CLI contract.

Run adapter tests with:

```bash
python3 -m unittest discover -s python -p 'test_*.py'
```

---

## 11. Safety invariants retained from BLK-004

Sprint 002 preserves or advances these BLK-004 safety constraints:

- no volumetric flooding: engine output is byte-capped and reports `FATAL_OUTPUT_FLOOD` on overflow,
- no orphan amnesia: target branches are prepared deterministically and orphan fallback creates an initial commit,
- no ancestry blindness: revert target hashes must be commit ancestors of `HEAD`,
- no broad staging: production code does not use `git add .` or `git add -u`,
- no unauthorized mutations: only explicit allowlisted file paths can be staged,
- no silent staging failures: staging/reporting errors return failure reports,
- no broken commits after validation failure: validation failures clean/restore and do not create success commits,
- no relative revert anchors: revert requires a full object ID,
- no `git stash`,
- no triple-dot diffs for implemented report diffs,
- sequential validation aggregation,
- bounded Git escapes through the git guard command wrapper,
- headless SSH hardening for `ls-remote`.

---

## 12. Remaining Deferrals and Recommended Sprint 003 Scope

Remaining deferrals and recommended Sprint 003 scope:

1. Integrate BLK-pipe with the larger BLK-004 orchestration path only after this deterministic transport layer remains green under closeout verification.
2. Decide whether local extensions `ENGINE_TIMEOUT`, `GIT_DIRTY`, and defensive code `9` should remain stable V47 extension points or be folded into stricter upstream router families.
3. Expand report semantics only where tests prove the implementation first; avoid overclaiming unimplemented BLK-004 fields or autonomous decision behavior.
4. Add higher-level adapter/orchestrator tests around real binary discovery and packaged invocation without introducing live LLM calls.
5. Continue hardening Git branch/fetch behavior under more remote topologies while preserving no-stash, no-triple-dot, no-broad-staging constraints.
6. Keep Codex, local LLMs, live tactical engines, network model services, and Discord HITL loops deferred until a later sprint explicitly authorizes and tests those integrations.

Sprint 003 should focus on measured integration readiness, closeout traceability, and packaging around the proven local CLI contract, not on enabling live autonomous engine behavior by default.
