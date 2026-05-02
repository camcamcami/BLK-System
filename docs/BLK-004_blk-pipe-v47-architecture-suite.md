# BLK-004 — BLK-pipe V47 Architecture Suite

**Status:** Active Planning Doctrine
**Purpose:** Consolidate the BLK-pipe V47 master directive, bounded execution sequence, payload schema, CLI contract, Python adapter expectations, and operational edge-case constraints.

---

## Source Segment — blk_000_MASTER_DIRECTIVE_V47
## MASTER DIRECTIVE: BLK-pipe Infrastructure Build

## 1. Agent Persona & Prime Directive
You are an expert Go systems engineer. Your sole objective is to build `BLK-pipe`, a compiled, deterministic transport layer between a Python orchestrator and a tactical coding engine. It does not parse code, call LLM APIs, or make decisions.

**Compilation Target:** This binary is strictly for POSIX environments. You must include `//go:build linux || darwin` at the top of OS-dependent files. Do not write cross-platform Windows fallbacks.

## 2. Hard Bans & Concurrency Safeguards
You must strictly enforce these constraints to prevent system failure:
* **NO VOLUMETRIC FLOODING:** You MUST cap the engine's `stdout`/`stderr` combined output to 50MB. If exceeded, `SIGKILL` the engine, return `{"status": "FATAL_OUTPUT_FLOOD"}`, and exit with **code 5**.
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
8. **Subprocess Spawn:** 15-minute `engineCtx`. Spawn `SprintPayload.EngineArgs...` via pure helper (`Setpgid: true`).
9. **Volumetric Guillotine:** Stream `stdout`/`stderr` into memory limits. IF combined bytes > 50MB, `SIGKILL` the process tree. Set `Status = "FATAL_OUTPUT_FLOOD"`, print JSON, **`os.Exit(5)`**. Assign `Stdout` to `EngineLogs` if successful.

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
* **Struct Anatomy:** `Action`, `TargetHash`, `CebID`, `WorkDir`, `TargetBranch`, `Engine`, `EngineArgs`, `L2Packet`, `ValidationCommands`, `AllowedModifiedFiles`, `AllowedNewFiles`.

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
* Volumetric flood guard limits output to 50MB.
* Cleans env, scrubs `SSH_AUTH_SOCK`, handles SIGTERM/SIGKILL escalation on timeout or flood.

### Module 4: The Synchronous Reporter
* Prints the JSON `ExecutionResult` once.

---

## Source Segment — blk_003v47
## BLK_003v47: BLK-pipe Master Build Plan

### 1. The Data Contracts (JSON Schemas)

**Input: `SprintPayload`**
```go
type SprintPayload struct {
    Action               string   `json:"action"` // "execute" or "revert"
    TargetHash           string   `json:"target_hash,omitempty"`
    CebID                string   `json:"ceb_id"`
    WorkDir              string   `json:"work_dir"`
    TargetBranch         string   `json:"target_branch"`
    Engine               string   `json:"engine"`
    EngineArgs           []string `json:"engine_args"`
    L2Packet             string   `json:"l2_packet"`
    ValidationCommands   []string `json:"validation_commands"`
    AllowedModifiedFiles []string `json:"allowed_modified_files"`
    AllowedNewFiles      []string `json:"allowed_new_files,omitempty"`
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
            "ceb_id": "REVERT",
            "engine": "",
            "engine_args": [],
            "l2_packet": "",
            "validation_commands": [],
            "allowed_modified_files": []
        }
        return self._invoke_binary(payload)

    def execute_sprint(
        self,
        ceb_id: str,
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
            "ceb_id": ceb_id,
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
  "ceb_id": "CEB_010",
  "work_dir": "/home/dad/code/Kuronode-v1",
  "target_branch": "sprint/ceb-010",
  "engine": "codex",
  "engine_args": ["exec", "-", "-s", "danger-full-access"],
  "l2_packet": "## CEB 010...",
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
  "ceb_id": "CEB_011",
  "work_dir": "/tmp/kuronode-ephemeral-workspace",
  "target_branch": "sprint/ceb-011",
  "engine": "codex",
  "engine_args": ["exec", "-", "--json", "--isolated", "--yes", "--deny-read=**/.git/**"],
  "l2_packet": "## CEB 011...",
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
  "ceb_id": "REVERT",
  "work_dir": "/tmp/kuronode-ephemeral-workspace",
  "target_branch": "sprint/ceb-011",
  "engine": "",
  "engine_args": [],
  "l2_packet": "",
  "validation_commands": [],
  "allowed_modified_files": []
}
```
