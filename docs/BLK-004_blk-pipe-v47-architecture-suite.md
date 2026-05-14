# BLK-004 — BLK-pipe V47 Architecture Suite

**Status:** Active Planning Doctrine
**Purpose:** Consolidate the BLK-pipe V47 master directive, bounded execution sequence, payload schema, CLI contract, Python adapter expectations, and operational edge-case constraints.

---

## Current-State Overlay after BLK-PIPE-008

BLK-004 remains intentional V47/BLK-pipe authority. The source segments below are preserved as authority context, but current BLK-System operation applies these explicit overlays:

1. execute payloads require non-empty canonical `trace_artifacts`; `revert` and `--health` do not.
2. BLK-pipe validates trace metadata shape and presence only; it does not parse requirement/use-case bodies, generate RTMs, or verify hashes against BLK-req files.
3. `allowed_modified_files` and `allowed_new_files` are strict tracked/new authorization classes. Wrong-class paths fail closed before engine execution.
4. Execute payloads must provide either non-empty repository-owned `validation_profiles` or non-empty trusted-local `validation_commands`; no-validation execute payloads fail before engine side effects. Validation commands run only after the engine produces a candidate mutation.
5. Sprint 020/BLK-SYSTEM-112 validation profile boundary: BLK-pipe supports repository-owned named validation profiles through `validation_profiles`. Profile names resolve to deterministic structured argv/env specs owned by the repository; reports expose both human-readable exact resolved commands and exact `resolved_validation_argv` evidence for hostile audit. Repository-owned profiles must not execute through `sh -c` shell wrappers.
6. Free-form `validation_commands` are transitional trusted-local compatibility only and still execute through the legacy shell runner. Less-trusted/autonomous payload boundaries must use repository-owned structured-argv profiles or a later explicit human-reviewed doctrine exception; in short, less-trusted/autonomous payload boundaries must use profiles. Validation profiles do not authorize network, package-manager, secret-reading, protected BLK-req body reads, BLK-test production MCP, BEO publication, RTM generation, or arbitrary shell as BLK-test behavior.
7. BLK-SYSTEM-113 validation trust boundary: payloads may declare `payload_trust_boundary: "autonomous"`; that boundary rejects legacy shell `validation_commands` and requires repository-owned `validation_profiles`. Reports expose `validation_trust_boundary` and `validation_profile_capabilities` so operators can distinguish repository-profile validation from trusted-local legacy shell compatibility.
8. Python adapter support for `validation_profiles` is payload construction convenience only; Go remains the enforcement authority.
9. Sprint 021 Python adapter policy boundary: Python adapter policy checks are fail-fast convenience only. Go remains the final deterministic enforcement authority for payload validation, protected-path classification, validation profile resolution, execution, cleanup, and report evidence. Adapter preflight must preserve canonical trace_artifacts, validation profiles, exact allowlists, and raw report evidence; it may reject protected BLK-req path allowlists early but does not authorize BLK-req vault body reads. Adapter subprocess invocation scrubs high-risk SSH/askpass variables including `SSH_AUTH_SOCK`, `SSH_AGENT_PID`, and `SSH_ASKPASS`, but this is not a production sandbox, cgroup, VM, network, or host-secret isolation claim. This Sprint 021 boundary does not authorize production BLK-test MCP, live tactical LLM execution, authoritative BEO publication, RTM generation, or RTM drift rejection.
10. Current local health output is `{"status":"OK","component":"blk-pipe"}`. The older `{"status":"healthy"}` literal is not the current BLK-System local CLI contract.
11. `codex`/live examples in source segments are target-state examples only. Current live Codex, live BLK-test MCP, authoritative BEO publication, and RTM generation remain disabled unless later active doctrine explicitly authorizes them.
12. Local exit codes 6/7/9, stronger ignored-file cleanup, legacy migration fields, and additional report fields are accepted BLK-System local V47-compatible extensions.
13. Sprint 018 protected-vault routing treats protected BLK-req allowlist entries as `UNAUTHORIZED_FILE_MUTATION` / POSIX Exit 3; it does not authorize BLK-req vault body reads.
14. Sprint 018 emergency revert ordering: revert bypasses execute-mode clean preflight only after target hash validation. The revert path must still validate `target_hash`, optional target branch, full object identity, and ancestry from the current `HEAD` before reset/clean. Payload names that refer to the same recovery anchor, including historical `sprint_base_hash` language, are not relative anchors and must not become `HEAD~1` shortcuts.
15. Sprint 018 does not authorize live BLK-test MCP, does not authorize authoritative BEO publication, and does not authorize RTM generation.
16. Sprint 069 exact-target local mode: execute payloads may include `target_hash` to require the prepared local `HEAD` to exactly equal the approval-bound hash before engine execution. When both `target_branch` and `target_hash` are present, BLK-pipe checks out only an existing local branch and does not fetch, probe `ls-remote`, checkout remote-tracking branches, or create orphan branches. This mode does not replace external remote-alignment approval/preflight evidence and does not authorize source mutation without a fresh exact approval.
17. Timeout/output-cap semantics: `timeout_seconds` and `max_output_bytes` are caller-tunable finite execution caps. The V47 defaults are 900 seconds / 15 minutes and 52,428,800 bytes / 50MB combined `stdout`/`stderr`; payloads may explicitly select higher or lower values for a bounded run. The selected caps must be enforced by BLK-pipe and preserved in execution/report evidence. Tuning these caps is not an authority promotion and does not weaken file allowlists, protected BLK-req no-read boundaries, validation gates, publication/RTM boundaries, or source-mutation controls.
18. BLK-SYSTEM-114 report/evidence hardening: every local BLK-pipe report preserves selected caps, exact modified/new allowlists, target hash/branch identity, payload/validation trust evidence, failure class, denial route, and cleanup status as diagnostics. These report fields are evidence only and do not authorize runtime dispatch, target mutation, BLK-test runtime, BEO publication, RTM generation, drift rejection, protected-body reads, signer/storage/ledger behavior, or production isolation claims.

Current deterministic local execute example:

```json
{
  "action": "execute",
  "beb_id": "BEB_011",
  "work_dir": "/absolute/path/to/clean/git/repo",
  "target_branch": "sprint/beb-011",
  "engine": "sh",
  "engine_args": ["-c", "printf after > README.md"],
  "l2_packet": "## bounded local packet",
  "trace_artifacts": [
    {
      "kind": "REQ",
      "id": "REQ-042",
      "version_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    }
  ],
  "validation_commands": ["go test ./..."],
  "allowed_modified_files": ["README.md"],
  "allowed_new_files": []
}
```

This current example authorizes only a deterministic local command supplied by the payload. It does not authorize live Codex, live tactical LLMs, network model services, live BLK-test MCP, authoritative BEO publication, RTM generation, cyber execution, or full sandbox/host-secret-isolation claims.

---

## Source Segment — blk_000_MASTER_DIRECTIVE_V47
## MASTER DIRECTIVE: BLK-pipe Infrastructure Build

## 1. Agent Persona & Prime Directive
You are an expert Go systems engineer. Your sole objective is to build `BLK-pipe`, a compiled, deterministic transport layer between a Python orchestrator and a tactical coding engine. It does not parse code, call LLM APIs, or make decisions.

**Compilation Target:** This binary is strictly for POSIX environments. You must include `//go:build linux || darwin` at the top of OS-dependent files. Do not write cross-platform Windows fallbacks.

## 2. Hard Bans & Concurrency Safeguards
You must strictly enforce these constraints to prevent system failure:
* **NO VOLUMETRIC FLOODING:** You MUST cap the engine's `stdout`/`stderr` combined output to the selected finite output cap. The default cap is 50MB; callers may explicitly select a different finite `max_output_bytes` value. If the selected cap is exceeded, `SIGKILL` the engine, return `{"status": "FATAL_OUTPUT_FLOOD"}`, and exit with **code 5**.
* **NO ORPHAN AMNESIA:** If `git checkout --orphan` is used, you MUST execute `git commit --allow-empty -m "Initialize"` before capturing `HEAD` to prevent fatal Git errors.
* **NO ANCESTRY BLINDNESS (THE REVERT GATE):** If `payload.Action == "revert"`, execute `git merge-base --is-ancestor <TargetHash> HEAD`. If non-zero, abort and exit with **code 4**.
* **NO BLIND STAGING (THE FILE LOCK-DOWN):** You MUST NEVER execute `git add -u` or `git add .`. Iterate strictly through `AllowedModifiedFiles` and `AllowedNewFiles`.
* **NO UNAUTHORIZED MUTATIONS:** Immediately after staging allowed files, execute `git checkout -- .` and `git clean -fd` to physically destroy hallucinated edits before committing.
* **NO SILENT STAGING FAILURES:** If `git diff --cached --quiet` exits 0 (nothing staged), abort, return `{"status": "UNAUTHORIZED_FILE_MUTATION"}`, and exit with **code 3**.
* **NO BROKEN COMMITS:** If `hasValidationError == true`, execute `git reset --hard <PreEngineHash>`, return `{"status": "SYNTAX_GATE_FAILED"}`, and exit with **code 2**.
* **NO RELATIVE REVERT ANCHORS:** Never use `HEAD~1`. Only use a verified `<TargetHash>`.
* **NO STASH BLOAT:** Never execute `git stash`. Rely entirely on `git clean -fd` and `git reset --hard HEAD`.
* **NO TRIPLE-DOT DIFF BLINDNESS:** ALWAYS use `git diff <Hash> HEAD --`.
* **NO VALIDATION SHORT-CIRCUITS (SEQUENTIAL AGGREGATION):** Linters share caches. Run sequentially. Aggregate logs, evaluate after completion.
* **NO TOKEN-HEAVY BLINDNESS:** Generate `DiffSummary` using `git diff <PreEngineHash> HEAD --numstat --`.
* **NO OS SIGNAL ORPHANS:** In `main()`, trap `SIGINT`/`SIGTERM`, reap `activePGID`, and exit with **code 1**.
* **NO ENVIRONMENT BASELINE DROPS:** Clone `os.Environ()`, scrub `GIT_`, explicitly scrub `SSH_AUTH_SOCK`, `SSH_AGENT_PID`, and `SSH_ASKPASS`. Append `PWD=<payload.WorkDir>`.
* **NO UNBOUNDED GIT ESCAPES:** ALL git commands MUST flow through `runBoundedCommand`.
* **NO HEADLESS SSH HANGS:** Inject `GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes"` into `ls-remote`.

## 3. The Context Map (Conflict Resolution)
* **Authority 1 (Execution Flow):** `blk_001v47` and `blk_003v47` govern the state machine.
* **Authority 2 (Edge Cases):** `blk_006v47` govern safety, timeouts, and process groups.
* **Authority 3 (Interfaces):** `blk_005v47` governs the CLI entry point.

---

## Source Segment — blk_001v47
## BLK_001v47: The Bounded Execution Sequence

### The Bounded Execution Sequence

**Phase 1: Ingestion & Bounding**
1. **Boot & Parse:** Parses `--payload`. If `--health` is passed, execute Health Check, print `{"status": "healthy"}`, and `os.Exit(0)`.
2. **OS Signal Trapping & Panic Recovery:** Setup `os/signal` channels. Ensure `activePGID` is reaped. Instantiate sterile `ExecutionResult` on failure, `os.Exit(1)`.
3. **Action Routing (ESCAPE HATCH):** Evaluate `SprintPayload.Action`.
   * IF `Action == "revert"`:
     * Execute `git merge-base --is-ancestor <payload.TargetHash> HEAD`. IF Exit != 0: **`os.Exit(4)`**.
     * Execute `git reset --hard <payload.TargetHash>` and `git clean -fd`. Print JSON, `os.Exit(0)`.

**Phase 2: The Git Fortress (Pre-Execution)**
4. **The Fetch:** `git fetch origin`.
5. **Branch Isolation:** `git checkout <branch>`. Fallbacks: `-t origin/<branch>` -> `ls-remote --symref` -> `--orphan`.
   * **Crucial:** IF the fallback triggered `--orphan`, execute `git commit --allow-empty -m "Initialize branch"` to establish a valid `HEAD`.
6. **Workspace Sterilization:** `git reset --hard HEAD` and `git clean -fd`.
7. **Pre-Engine Snapshot:** `git rev-parse HEAD`. Trim whitespace, store as `PreEngineHash` and map to `result.PreEngineHash`.

**Phase 3: The Tactical Engine (Execution)**
8. **Subprocess Spawn:** Selected finite `engineCtx` from `timeout_seconds`; default 900 seconds / 15 minutes. Spawn `SprintPayload.EngineArgs...` via pure helper (`Setpgid: true`).
9. **Volumetric Guillotine:** Stream `stdout`/`stderr` into memory limits. If combined bytes exceed the selected `max_output_bytes` cap (default 52,428,800 bytes / 50MB), `SIGKILL` the process tree. Set `Status = "FATAL_OUTPUT_FLOOD"`, print JSON, **`os.Exit(5)`**. Assign `Stdout` to `EngineLogs` if successful.

**Phase 4: Mechanical Output Validation & Abort Gate**
10. **Zero-Diff Gate:** `git status --porcelain`. Fail Exit 2 if empty.
11. **Bounded Validation (SEQUENTIAL):** Iterate `ValidationCommands`. Prepend index to `mapKey`. Assign logs. If any fail, flag `hasValidationError = true`.
12. **Validation Abort Gate:** IF `hasValidationError == true`:
    * Execute `git reset --hard <PreEngineHash>` via helper to restore state.
    * Execute `git clean -fd`.
    * Set `result.Status = "SYNTAX_GATE_FAILED"`. Print JSON. **`os.Exit(2)`**. DO NOT PROCEED.

**Phase 5: Strict Staging & Erasure**
13. **The Strict Staging Stage:** Iterate strictly through `AllowedModifiedFiles` and `AllowedNewFiles`. Execute `git add -- <file>` ONLY for explicit paths.
14. **The Unauthorized Erasure:** Execute `git checkout -- .` followed by `git clean -fd`. This physically destroys hallucinated edits.
15. **The Commit Gate:** Execute `git diff --cached --quiet`.
    * If exit 0 -> ABORT (Staging Failure). Set `result.Status = "UNAUTHORIZED_FILE_MUTATION"`, print JSON, and **`os.Exit(3)`**.
    * If exit 1 -> execute `git commit -m "..."`.

**Phase 6: Return & Terminate**
16. **Rogue File Audit:** `git ls-files -z --others --exclude-standard --directory`.
17. **Diff Summary Extraction:** `git diff <PreEngineHash> HEAD --numstat --`. Parse into `DiffSummary`.
18. **Bounded Diff Extraction:** `git diff <PreEngineHash> HEAD --`.
19. **Terminate:** Print JSON to `stdout`. Exit 0.

---

## Source Segment — blk_002v47
## BLK_002v47: Architectural Blueprint

### Module 1: The Input Unmarshaler
* **Struct Anatomy:** `Action`, `TargetHash`, `BebID`, `WorkDir`, `TargetBranch`, `Engine`, `EngineArgs`, `L2Packet`, `ValidationCommands`, `AllowedModifiedFiles`, `AllowedNewFiles`.

### Module 2: The Git State Controller
* **The Revert Escape Hatch:** Verifies ancestry, fast-paths to `git reset --hard TargetHash` and terminates.
* **The Forward Execution:**
  1. Fetch, checkout, reset, clean. Capture `PreEngineHash` (init orphan branch if necessary).
  2. If validation fails -> `git reset --hard <PreEngineHash>` and ABORT with exit code 2.
  3. `git add` strictly mapped files.
  4. `git checkout -- .` and `git clean -fd` to wipe unauthorized edits.
  5. `git diff --cached --quiet` -> ABORT with exit code 3 if empty.
  6. `git commit -m "..."`.
  7. Extract diffs.

### Module 3: The Engine Wrapper (The Pure Helper Abstraction)
* Abstracted reusable helper (`Setpgid: true`).
* Volumetric flood guard limits output to selected finite `max_output_bytes`; default 52,428,800 bytes / 50MB.
* Cleans env, scrubs `SSH_AUTH_SOCK`, handles SIGTERM/SIGKILL escalation on timeout or flood.

### Module 4: The Synchronous Reporter
* Prints the JSON `ExecutionResult` once.

---

## Source Segment — blk_003v47
## BLK_003v47: BLK-pipe Master Build Plan

### 1. The Data Contracts (JSON Schemas)

**Input: `SprintPayload`**
```go
type TraceArtifact struct {
    Kind        string `json:"kind"`
    ID          string `json:"id"`
    VersionHash string `json:"version_hash"`
}

type SprintPayload struct {
    Action               string          `json:"action"` // "execute" or "revert"
    TargetHash           string          `json:"target_hash,omitempty"`
    BebID                string          `json:"beb_id"`
    WorkDir              string          `json:"work_dir"`
    TargetBranch         string          `json:"target_branch"`
    Engine               string          `json:"engine"`
    EngineArgs           []string        `json:"engine_args"`
    L2Packet             string          `json:"l2_packet"`
    TraceArtifacts       []TraceArtifact `json:"trace_artifacts"`
    ValidationCommands   []string        `json:"validation_commands"`
    AllowedModifiedFiles []string        `json:"allowed_modified_files"`
    AllowedNewFiles      []string        `json:"allowed_new_files,omitempty"`
}
```

**Output: `ExecutionResult`**
```go
type DiffSummary struct {
    FilesChanged int      `json:"files_changed"`
    Insertions   int      `json:"insertions"`
    Deletions    int      `json:"deletions"`
    Files        []string `json:"files"`
}

type ExecutionResult struct {
    Status          string            `json:"status"`
    ExitCode        int               `json:"exit_code"`
    PreEngineHash   string            `json:"pre_engine_hash,omitempty"`
    GitDiff         string            `json:"git_diff"`
    EngineLogs      string            `json:"engine_logs"`
    ValidationLogs  map[string]string `json:"validation_logs"`
    DiffSummary     *DiffSummary      `json:"diff_summary,omitempty"`
    Error           string            `json:"error,omitempty"`
    UntrackedFiles  []string          `json:"untracked_files"`
    TraceArtifacts  []TraceArtifact   `json:"trace_artifacts"`
}
```

---

## Source Segment — blk_004v47
## BLK_004v47: Python Integration Adapter

```python
import os
import json
import subprocess
import tempfile
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

@dataclass
class ExecutionResult:
    status: str
    exit_code: int
    pre_engine_hash: str
    git_diff: str
    engine_logs: str
    validation_logs: Dict[str, str]
    diff_summary: Optional[Dict] = None
    error: Optional[str] = None
    untracked_files: Optional[List[str]] = None

class BlkPipeAdapter:
    def __init__(self, binary_path: str = "blk-pipe"):
        self.binary_path = binary_path

    def run_health_check(self) -> bool:
        result = subprocess.run([self.binary_path, "--health"], capture_output=True)
        return result.returncode == 0

    def abort_sprint_and_revert(self, work_dir: str, target_branch: str, pre_engine_hash: str) -> ExecutionResult:
        payload = {
            "action": "revert",
            "work_dir": work_dir,
            "target_branch": target_branch,
            "target_hash": pre_engine_hash,
            "beb_id": "REVERT",
            "engine": "",
            "engine_args": [],
            "l2_packet": "",
            "validation_commands": [],
            "allowed_modified_files": []
        }
        return self._invoke_binary(payload)

    def execute_sprint(
        self,
        beb_id: str,
        work_dir: str,
        target_branch: str,
        engine: str,
        engine_args: List[str],
        l2_packet: str,
        validation_cmds: List[str],
        allowed_modified_files: List[str],
        allowed_new_files: Optional[List[str]] = None
    ) -> ExecutionResult:

        payload = {
            "action": "execute",
            "beb_id": beb_id,
            "work_dir": work_dir,
            "target_branch": target_branch,
            "engine": engine,
            "engine_args": engine_args,
            "l2_packet": l2_packet,
            "validation_commands": validation_cmds,
            "allowed_modified_files": allowed_modified_files,
            "allowed_new_files": allowed_new_files or []
        }
        return self._invoke_binary(payload)

    def _invoke_binary(self, payload: Dict) -> ExecutionResult:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_payload:
            json.dump(payload, temp_payload)
            temp_payload_path = temp_payload.name

        run_env = os.environ.copy()

        try:
            result = subprocess.run(
                [self.binary_path, "--payload", temp_payload_path],
                env=run_env,
                capture_output=True,
                text=True,
                check=False,
                timeout=1800
            )

            try:
                parsed_output = json.loads(result.stdout)
            except json.JSONDecodeError:
                return ExecutionResult(
                    status="FATAL_CRASH",
                    exit_code=result.returncode,
                    pre_engine_hash="", git_diff="", engine_logs="", validation_logs={},
                    error=f"No JSON returned. Go Panic or OS Kill. Stderr: {result.stderr.strip()}"
                )

            # POSIX Exit Code Strict Routing
            if result.returncode == 1:
                final_status = "FATAL_SYSTEM_PANIC"
            elif result.returncode == 2:
                final_status = "SYNTAX_GATE_FAILED"
            elif result.returncode == 3:
                final_status = "UNAUTHORIZED_FILE_MUTATION"
            elif result.returncode == 4:
                final_status = "INVALID_REVERT_ANCHOR"
            elif result.returncode == 5:
                final_status = "FATAL_OUTPUT_FLOOD"
            elif result.returncode == 8:
                final_status = "INVALID_PAYLOAD"
            else:
                final_status = parsed_output.get("status", "SUCCESS")

            return ExecutionResult(
                status=final_status,
                exit_code=result.returncode,
                pre_engine_hash=parsed_output.get("pre_engine_hash", ""),
                git_diff=parsed_output.get("git_diff", ""),
                engine_logs=parsed_output.get("engine_logs", ""),
                validation_logs=parsed_output.get("validation_logs", {}),
                diff_summary=parsed_output.get("diff_summary"),
                error=parsed_output.get("error"),
                untracked_files=parsed_output.get("untracked_files", [])
            )

        except subprocess.TimeoutExpired as e:
            return ExecutionResult(
                status="FATAL_PYTHON_TIMEOUT", exit_code=1, pre_engine_hash="", git_diff="", engine_logs="", validation_logs={},
                error=f"Catastrophic Go deadlock. Python adapter killed process."
            )
        finally:
            Path(temp_payload_path).unlink(missing_ok=True)
```

---

## Source Segment — blk_005v47
## BLK_005v47: CLI Parsing Constraints

### 1. The Health Check Invocation
`blk-pipe --health`

### 2. The Physical Input (The JSON File)
```json
{
  "action": "execute",
  "beb_id": "BEB_010",
  "work_dir": "/home/dad/code/Kuronode-v1",
  "target_branch": "sprint/beb-010",
  "engine": "codex",
  "engine_args": ["exec", "-", "-s", "danger-full-access"],
  "l2_packet": "## BEB 010...",
  "validation_commands": ["npm run lint", "npx tsc --noEmit"],
  "allowed_modified_files": ["packages/core/src/parser.ts"],
  "allowed_new_files": ["packages/core/src/new_feature.ts"]
}
```

### 3. The Execution Invocation
`blk-pipe --payload /tmp/tmp8675309.json`

---

## Source Segment — blk_006v47
## BLK_006v47: Concurrency & Edge Cases

* **The POSIX Router:** Python must route control flow strictly off Go exit codes (0 = Success, 1 = Fatal, 2 = Syntax/Validation Failed, 3 = Unauthorized File Mutation, 4 = Invalid Revert Anchor, 5 = Output Flood).
* **The Absolute Revert Anchor:** The revert escape hatch relies strictly on `git reset --hard <TargetHash>`. It MUST be verified via `git merge-base` before execution. Never use relative anchors like `HEAD~1`.
* **The Unauthorized Erasure:** The agent cannot be trusted. If it modifies a file outside `AllowedModifiedFiles`, `git checkout -- .` and `git clean -fd` will silently revert the hallucinated change. If no allowed files were modified, BLK-pipe explicitly hard-aborts with Exit Code 3.
* **The Environment Baseline:** Explicitly scrub **`SSH_AUTH_SOCK`, `SSH_AGENT_PID`, and `SSH_ASKPASS`**.
* **Orphan Branch Survival:** Committing an empty initialization block ensures the pipeline does not fail when targeting brand new sprint branches.

---

## Source Segment — blk_007v47
## BLK_007v47: The Orchestrator Payload Contract (Hermes)

### 1. Payload Construction Example (Execution)
```json
{
  "action": "execute",
  "beb_id": "BEB_011",
  "work_dir": "/tmp/kuronode-ephemeral-workspace",
  "target_branch": "sprint/beb-011",
  "engine": "codex",
  "engine_args": ["exec", "-", "--json", "--isolated", "--yes", "--deny-read=**/.git/**"],
  "l2_packet": "## BEB 011...",
  "validation_commands": ["npm run lint", "npm run test:ipc"],
  "allowed_modified_files": ["src/ipc_router.ts"],
  "allowed_new_files": []
}
```

### 2. Payload Construction Example (Revert/Escape Hatch)
```json
{
  "action": "revert",
  "target_hash": "a1b2c3d4e5f6...",
  "beb_id": "REVERT",
  "work_dir": "/tmp/kuronode-ephemeral-workspace",
  "target_branch": "sprint/beb-011",
  "engine": "",
  "engine_args": [],
  "l2_packet": "",
  "validation_commands": [],
  "allowed_modified_files": []
}
```


## BLK-SYSTEM-110 Exit-Code Taxonomy Overlay

```text
BLK_SYSTEM_110_EXIT_CODE_TAXONOMY_SPLIT
INVALID_PAYLOAD_EXIT_CODE_8
SYNTAX_VALIDATION_FAILURE_REMAINS_EXIT_CODE_2
PROTECTED_ALLOWLIST_VIOLATIONS_REMAIN_EXIT_CODE_3
```

Invalid payload and syntax/validation failure are separate failure classes. Current Go `blk-pipe` routes generic `INVALID_PAYLOAD` to POSIX Exit 8. `SYNTAX_GATE_FAILED` / validation failure remains Exit 2. Protected BLK-req allowlist violations and unauthorized mutation remain Exit 3.
