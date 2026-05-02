# BLK-008 — BLK-Test MCP Test Execution Server

**Status:** Active Planning Doctrine
**Purpose:** Specify the local stdio-based MCP test execution server that acts as a deterministic physics oracle for Kuronode verification.

---

## Objective
Build a local, stdio‑based MCP server in TypeScript that acts as a rigid, deterministic “physics oracle” for an AI Auditor Agent. The server must safely execute native verification tests (Electron IPC, WASM memory profiling, SVG purity, architecture lint) against the Kuronode codebase, running on a bare‑metal Ubuntu machine with **16 GB RAM and a single SSD**.

It must:
- Never grant the agent arbitrary shell access.
- Prevent parallel test execution.
- Isolate all test workspaces ephemerally.
- Compress and triage output to avoid token overflow.
- Run without corrupting the primary repository.

---

## 1. Project Setup (Phase 1)
- Initialize a new Node.js/TypeScript project: `npm init -y`.
- Install dependencies:
  - `@modelcontextprotocol/sdk`
  - `zod`
  - `tree-kill`
  - `typescript`, `tsup` (or `esbuild`)
- **Set `"type": "module"` in `package.json`**. The MCP SDK is pure ESM; forcing CommonJS will cause import/export errors.
- `tsconfig.json`: target `ES2022`, module `NodeNext`, moduleResolution `NodeNext`.
- Transport: Use only `StdioServerTransport`. No HTTP or WebSockets.

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "kuronode-test-executor", version: "1.0.0" }, { capabilities: { tools: {} } });
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## 2. Environment Orchestrator (Phase 2)

### 2.1 OS-Level Atomic Mutex Lock (With Polling Backoff)
- Lockfile path: `/var/tmp/kuronode_mcp.lock`
- The server MUST acquire the lock using the kernel-level exclusive write flag (`wx`). To prevent collisions between concurrent operations, the acquisition must poll for up to 5 minutes before failing.

```typescript
import fs from "fs";

const LOCKFILE = "/var/tmp/kuronode_mcp.lock";

async function acquireLock(maxWaitMs = 300000): Promise<void> {
  const startTime = Date.now();

  while (true) {
    try {
      // The 'wx' flag delegates atomicity to the OS. Fails instantly if file exists.
      const fd = fs.openSync(LOCKFILE, "wx");
      fs.writeSync(fd, process.pid.toString());
      fs.closeSync(fd);
      return;
    } catch (e: any) {
      if (e.code === "EEXIST") {
        // Lock exists. Check if it's stale.
        const stalePid = parseInt(fs.readFileSync(LOCKFILE, "utf8"));
        try {
          if (!isNaN(stalePid)) process.kill(stalePid, 0); // Is it alive?
        } catch (killErr: any) {
          if (killErr.code === "ESRCH") {
            // Process is dead. Unlink and retry immediately.
            try { fs.unlinkSync(LOCKFILE); } catch (_) {}
            continue;
          }
        }

        // Still locked and process is alive. Check timeout.
        if (Date.now() - startTime > maxWaitMs) {
          throw new Error("SYSTEM_LOCKED_TIMEOUT");
        }

        // Wait 5 seconds before polling again
        await new Promise(resolve => setTimeout(resolve, 5000));
      } else {
        throw e;
      }
    }
  }
}
```

- If locked, return error JSON immediately.
- Release lock in `finally` block and on `SIGTERM`/`SIGINT`.

### 2.2 Ephemeral Workspace (Hardlink‑Only)
- Use **`/var/tmp`** (disk‑persistent), never `/tmp`.
- Clone repository via hardlinks:
  ```bash
  cp -al /path/to/kuronode/repo /var/tmp/kuronode_ephemeral_$(date +%s)
  ```
- Verify source and `/var/tmp` are on the same filesystem (`df ...`). If not, use a same‑fs mirror (e.g., under `/home/$USER/mcp-ephemeral-workspace`).

### 2.3 Guaranteed Teardown & Startup Purge

**Startup Purge (MANDATORY):** Before `server.connect(transport)`, perform a global cleanup of orphaned directories from previous crashes. Scan `/var/tmp/` and `/tmp/` for directories matching:
- `/var/tmp/kuronode_ephemeral_*`
- `/tmp/ts_cache_*`
- `/tmp/kuronode_cache_*`

Use `fs.rmSync` directly; no shell. Also, delete any stale lockfile whose PID is not alive (belt-and-suspenders). The environment must be sterile.

**Teardown (per test):** In a `finally` block (after each tool execution), delete the ephemeral workspace clone, the per‑execution caches (`/tmp/ts_cache_${executionId}`, `/tmp/kuronode_cache_${executionId}`), and the lockfile using `fs.rmSync`.

```typescript
function cleanUp(workspacePath: string, executionId: string) {
  fs.rmSync(workspacePath, { recursive: true, force: true });
  fs.rmSync(`/tmp/ts_cache_${executionId}`, { recursive: true, force: true });
  fs.rmSync(`/tmp/kuronode_cache_${executionId}`, { recursive: true, force: true });
  fs.rmSync("/var/tmp/kuronode_mcp.lock", { force: true });
}
```

---

## 3. Rigid Tool Definitions (Phase 3)

All tools use `zod` for strict input validation. **No dynamic command execution tool**.

- `run_ast_validation` – spawns `tsc --noEmit` with memory cap and per‑execution cache.
- `run_ipc_race_test` – Playwright test with `--disable-dev-shm-usage`, snapshots disabled, browsers path resolved dynamically.
- `run_svg_export_purity_test` – Playwright check for `foreignObject` count.
- `run_architecture_lint` – deterministic static analysis, no auto‑fix.

### 3.5 Critical: Enforced Filesystem Protections
- **Path Traversal Protection:** resolv the agent‑supplied path relative to ephemeral root, reject if it escapes.
- **Strict Cache Jailing:** every child process receives environment variables with per‑execution IDs (see below). All caches go to `/tmp`. No tool writes into the hardlinked workspace.

```typescript
import os from "os";
import path from "path";

const executionId = crypto.randomUUID();
const safeEnv = {
  ...process.env,
  XDG_CACHE_HOME: `/tmp/kuronode_cache_${executionId}`,
  NODE_OPTIONS: "--max-old-space-size=4096",
  TS_CACHEDIR: `/tmp/ts_cache_${executionId}`,
  CI: "true",
  PLAYWRIGHT_UPDATE_SNAPSHOTS: "false",
  PLAYWRIGHT_BROWSERS_PATH: path.join(os.homedir(), ".cache/ms-playwright"),
  // additional linter flags if needed
};
```

---

## 4. The Physics Guillotine: Timeout, Process Killing, & Volumetric Flood Guard (DRY)

Every test must be wrapped in a `Promise.race()` against a hard timeout **and** a hard output byte limit. Both triggers must synchronously await the process tree death before releasing resources, and the kill logic must be **shared** to avoid code duplication.

**Constants:**
- `MAX_TIMEOUT_MS`: 45 s (AST), 90 s (IPC), 60 s (others)
- `MAX_OUTPUT_BYTES = 50 * 1024 * 1024` (50 MB)

**Implementation:**

```typescript
import { spawn } from "child_process";
import treeKill from "tree-kill";

function runWithTimeout(
  command: string,
  args: string[],
  timeoutMs: number,
  env: Record<string, string>
): Promise<Buffer> {
  const MAX_OUTPUT_BYTES = 50 * 1024 * 1024;
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { env });
    const stdoutChunks: Buffer[] = [];
    const stderrChunks: Buffer[] = [];
    let totalBytes = 0;
    let timedOut = false;

    // DRY killer: call this to end the test immediately (flood or timeout)
    const triggerKill = async (reason: string) => {
      if (timedOut) return;
      timedOut = true;
      clearTimeout(timer);
      await new Promise<void>((killResolve) => {
        treeKill(child.pid!, "SIGKILL", (err) => {
          if (err) console.error(`tree-kill error (${reason}):`, err);
          killResolve();
        });
      });
      reject(new Error(reason));
    };

    const handleData = (chunk: Buffer) => {
      if (timedOut) return;
      totalBytes += chunk.length;
      if (totalBytes > MAX_OUTPUT_BYTES) {
        triggerKill("FATAL_OUTPUT_FLOOD");
        return;
      }
      stdoutChunks.push(chunk);
    };

    const handleStderr = (chunk: Buffer) => {
      if (timedOut) return;
      totalBytes += chunk.length;
      if (totalBytes > MAX_OUTPUT_BYTES) {
        triggerKill("FATAL_OUTPUT_FLOOD");
        return;
      }
      stderrChunks.push(chunk);
    };

    child.stdout.on("data", handleData);
    child.stderr.on("data", handleStderr);

    const timer = setTimeout(() => {
      triggerKill("FATAL_TIMEOUT");
    }, timeoutMs);

    child.on("close", (code) => {
      clearTimeout(timer);
      if (!timedOut) {
        if (code === 0) resolve(Buffer.concat(stdoutChunks));
        else reject(new Error(`Exit code ${code}\n${Buffer.concat(stderrChunks).toString()}`));
      }
    });
  });
}
```

**Why this matters:** The single `triggerKill` function ensures that the lockfile is never released before the OS reclaims RAM, and it avoids copy‑pasting the same fifteen lines. Both flood and timeout terminate identically, preserving the server’s health.

**Error payload on flood/timeout:**
```json
{
  "status": "FATAL_OUTPUT_FLOOD", // or FATAL_TIMEOUT
  "deduplicated_errors": [
    { "message": "Test output exceeded 50 MB. Probable infinite logging loop." }
  ]
}
```

---

## 5. Context Compressor (Phase 5)

- Strip ANSI codes, filter npm warnings, deduplicate errors (first‑three‑line hash or message+file hash).
- **Payload Triage:** sort errors by descending `count`, take top 7, add `truncated` flag and advice if more exist.
- No internal LLM. Deterministic hints only.

---

## 6. Build & Deployment (Phase 6)

- Bundle with `tsup` (or `esbuild`) to a single ESM file (`format: "esm"`, target `node18`/`node20`).
- Launch via `node dist/index.js`; Hermes connects via stdio.

---

## 7. Non‑Negotiable Constraints (Final Recap)

- No dynamic command execution.
- Ephemeral workspace in `/var/tmp` (or same‑fs), never `/tmp`.
- PID lockfile with OS-level `wx` flag creation and 5-minute async polling backoff for absolute atomic state.
- **Startup purge** of stale ephemeral/cache directories.
- Hard timeouts **and** volumetric output cap (50 MB); kill logic is DRY, awaited before lock release.
- Output compression, deduplication, payload triage (max 7 errors).
- No internal LLM.
- Stateless, idempotent teardown via Node’s `fs.rmSync`.
- Path traversal protection.
- All caches jailed to `/tmp` with per‑execution IDs.
- Playwright browser path resolved dynamically via `os.homedir()`.

---

## Appendix: Hermes Auditor Agent Prompt Template

Inject this into the Auditor phase system prompt:

```markdown
## TEST EVALUATION PROTOCOL

When you receive a JSON response from the Test Execution MCP Server where `"status": "FAIL"`, you are **STRICTLY FORBIDDEN** from immediately writing code or proposing a fix.

You must output a `[DIAGNOSTIC_REPORT]` block before taking any other action. If you attempt to use a file‑editing tool without generating this report, your execution will be terminated.

### Required Format:
[DIAGNOSTIC_REPORT]
1. **Total Distinct Errors:** <Number of objects in the deduplicated_errors array>
2. **Primary Failure:** <Copy the exact "message" string of the error with the highest "count">
3. **Affected Files:** <List the file paths cited in the error>
4. **Root Cause Hypothesis:** <A strictly deterministic, 1‑sentence hypothesis based ONLY on the physics of the error payload>
[/DIAGNOSTIC_REPORT]

Once the diagnostic report is complete, you may generate a Codex Execution Brief (CEB) and dispatch the tactical fix via BLK‑pipe.
```
