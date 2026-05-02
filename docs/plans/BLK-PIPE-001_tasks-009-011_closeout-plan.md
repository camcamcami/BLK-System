# BLK-pipe Sprint 001 — Tasks 9-11 Closeout Plan

> **For Hermes:** Use `blk-system-sprint-execution`, `test-driven-development`, `subagent-driven-development`, and two-stage review before each implementation push. Do not let implementation subagents push.

**Status:** Planned
**Date:** 2026-05-03
**Repository:** `/home/dad/BLK-System`
**Branch:** `main`
**Primary Sprint Plan:** `docs/plans/BLK-PIPE-001_deterministic-execution-kernel.md`
**Primary Doctrine:** `docs/BLK-004_blk-pipe-v47-architecture-suite.md`

---

## 1. Purpose

This plan preserves execution context for the remaining BLK-pipe Sprint 001 tasks:

- Task 9: protected BLK-req artifact mutation deny tests,
- Task 10: CLI payload-file support,
- Task 11: Sprint 001 CLI documentation and README update.

Sprint 001 is intentionally a deterministic local safety kernel. It is compatible with BLK-004/V47 direction but does not attempt the full V47 schema, Python adapter, validation gate, revert gate, branch orchestration, or Codex execution.

---

## 2. Current Known State Before Task 9

At the time this plan was written:

```text
HEAD: b1d94a9 docs: record BLK-pipe task 8 outcome
Implementation HEAD before outcome doc: 0a05ba3 feat: orchestrate bounded blk-pipe execution
Branch: main
Remote: origin/main
Repo status: clean and aligned with origin/main
Full test suite: go test ./... PASS
```

Go is installed locally. Always run Go commands with:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Current CLI supports:

```bash
go run ./cmd/blk-pipe --health
go run ./cmd/blk-pipe --payload-stdin
```

Current CLI does **not** yet support:

```bash
go run ./cmd/blk-pipe --payload /absolute/path/to/payload.json
```

Current Sprint 001 payload contract is minimal and uses:

```json
{
  "action": "execute",
  "workdir": "/absolute/repo",
  "engine_command": ["sh", "-c", "..."],
  "allowed_modified_files": ["src/file.txt"],
  "allowed_new_files": ["src/new.txt"],
  "timeout_seconds": 5,
  "max_output_bytes": 4096
}
```

BLK-004/V47 later expects fields such as `work_dir`, `target_branch`, `engine`, `engine_args`, `ceb_id`, `l2_packet`, and `validation_commands`. Do not broaden Sprint 001 into V47 unless a later plan explicitly says so.

---

## 3. Non-Negotiable Safety Invariants To Preserve

These were proven during Tasks 1-8 and must not regress:

1. No live Codex/LLM invocation in Sprint 001.
2. No broad Git staging:
   - never `git add .`,
   - never `git add -u`,
   - never directory allowlist staging.
3. Stage only explicit allowlisted files using:

   ```bash
   git add -- <file>
   ```

4. Reject pathspec/glob/traversal allowlist entries before Git sees them:
   - `.`,
   - `..`,
   - absolute paths,
   - `*`, `?`, `[`,
   - leading `:` such as `:(glob)**`.
5. Clean repo preflight must reject modified, untracked, and ignored files before engine execution.
6. Engine output must remain bounded.
7. Process groups must be killed on timeout/flood and after direct process exit to avoid inherited pipe-writer hangs.
8. `.git` mutations are unauthorized:
   - `.git/info/exclude` mutation cannot hide files,
   - `.git/hooks/*` mutation is unauthorized,
   - `rm -rf .git` is detected/restored,
   - BLK-pipe commits with hooks disabled.
9. Unauthorized cleanup uses `git clean -ffdx` after allowlisted files are staged, so nested Git repositories and ignored engine-created files are destroyed.
10. Pre-existing ignored/untracked files must fail preflight before cleanup can delete anything.
11. Zero-arg CLI remains unsupported and nonblocking.
12. Outcome docs should be committed and pushed separately after each task; attach Markdown outcome files in Discord instead of pasting long summaries.

---

## 4. BLK-004 Alignment Notes For Tasks 9-11

Tasks 9-11 are closeout work for Sprint 001, not full BLK-004/V47 implementation.

Strong alignment already present:

- deterministic Go transport layer,
- output flood and timeout controls,
- explicit allowlist staging,
- unauthorized mutation destruction,
- dirty workspace preflight,
- protected BLK-req path validation,
- JSON report emission,
- no Codex/LLM decision-making inside BLK-pipe.

Known BLK-004/V47 gaps intentionally deferred after Sprint 001:

- full V47 payload schema,
- Python adapter,
- revert action and `target_hash`,
- validation command sequencing/log aggregation,
- final exit-code registry reconciliation,
- full V47 report fields such as `pre_engine_hash`, `git_diff`, `engine_logs`, `validation_logs`, `diff_summary`, and `untracked_files`,
- branch/fetch/orphan flow,
- full environment scrub including SSH variables,
- generalized bounded Git command wrapper.

Task 10 should bridge one important BLK-004 interface point by adding:

```bash
blk-pipe --payload /tmp/payload.json
```

but it should still feed the current Sprint 001 payload into `pipe.Run`.

---

## 5. Standard Controller Workflow For Each Task

For each task:

1. Preflight:

   ```bash
   cd /home/dad/BLK-System
   git status --short --branch
   git fetch origin main
   git status --short --branch
   export PATH="$HOME/.local/bin:$PATH"
   go version
   go test ./...
   ```

2. Read the exact task section in `docs/plans/BLK-PIPE-001_deterministic-execution-kernel.md`.
3. Dispatch implementation subagent with strict TDD instructions.
4. Inspect the diff manually.
5. Run focused tests and full tests.
6. Run two review subagents:
   - spec compliance review,
   - code quality/safety review.
7. If either reviewer requests changes, amend the local unpushed task commit and rerun both reviews.
8. Only the controller pushes:

   ```bash
   git push origin main
   ```

9. Create and push a matching outcome doc:

   ```text
   docs/outcomes/BLK-PIPE-001_task-00N-outcome.md
   ```

---

## 6. Task 9 Plan — Hard-Deny BLK-req Artifact Mutations

### Objective

Enforce and lock down the BLK-006 hard-deny boundary for these protected allowlist prefixes:

```regexp
^docs/(requirements|use_cases)/.*
```

The deny must apply to both:

- `allowed_modified_files`,
- `allowed_new_files`.

The pipe must reject protected paths during payload validation before running the engine.

### Files

Modify:

- `internal/contracts/payload.go`
- `internal/contracts/payload_test.go`
- `internal/pipe/run_test.go`

Expected implementation commit:

```bash
git commit -m "feat: hard-deny blk-req artifact mutations"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-001_task-009-outcome.md
```

Expected outcome commit:

```bash
git commit -m "docs: record BLK-pipe task 9 outcome"
```

### Current Pre-Implementation Observation

`internal/contracts/payload.go` already rejects:

```go
strings.HasPrefix(entry, "docs/requirements/")
strings.HasPrefix(entry, "docs/use_cases/")
```

`internal/contracts/payload_test.go` already contains basic protected path cases, but Task 9 still needs stronger explicit Sprint 001 coverage:

- `docs/requirements/active/REQ-001.md` in `allowed_modified_files`,
- `docs/use_cases/staging/UC-001.md` in `allowed_new_files`,
- `pipe.Run` proving engine is not invoked when protected validation fails.

If existing validation already passes new contract tests, Task 9 may be primarily a regression-test lock plus a small refactor to make the protected regex/predicate explicit. Do not weaken validation.

### TDD Steps

#### Step 1: Add contract tests

In `internal/contracts/payload_test.go`, add explicit table cases for:

```go
{
    name: "protected requirements active path in modified allowlist",
    edit: func(p *Payload) {
        p.AllowedModifiedFiles = []string{"docs/requirements/active/REQ-001.md"}
    },
    want: "docs/requirements",
},
{
    name: "protected use case staging path in new allowlist",
    edit: func(p *Payload) {
        p.AllowedNewFiles = []string{"docs/use_cases/staging/UC-001.md"}
    },
    want: "docs/use_cases",
},
```

Also preserve the existing use-case test if it remains useful.

Run focused test:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/contracts -run 'TestPayloadValidateRejectsInvalidPayloads' -v
```

Expected RED if a gap exists; otherwise expected GREEN proving current validation already covers it.

#### Step 2: Add pipe-level engine-not-invoked regression

In `internal/pipe/run_test.go`, add a test proving protected allowlist validation aborts before engine execution.

Suggested shape:

```go
func TestRunProtectedDocsAllowlistRejectsBeforeEngine(t *testing.T) {
    repo := testutil.NewGitRepo(t)
    marker := filepath.Join(repo, "engine-ran.txt")

    payload := payloadJSON(t, contracts.Payload{
        Action:               "execute",
        Workdir:              repo,
        EngineCommand:        []string{"sh", "-c", "printf ran > engine-ran.txt"},
        AllowedModifiedFiles: []string{"docs/requirements/active/REQ-001.md"},
        TimeoutSeconds:       5,
        MaxOutputBytes:       4096,
    })

    var stdout bytes.Buffer
    exitCode := Run(context.Background(), payload, &stdout)
    report := decodeReport(t, stdout.Bytes())

    if exitCode != ExitInvalidPayload {
        t.Fatalf("exit code = %d, want %d; report=%+v", exitCode, ExitInvalidPayload, report)
    }
    if report.Status != "INVALID_PAYLOAD" {
        t.Fatalf("report status = %q, want INVALID_PAYLOAD", report.Status)
    }
    if _, err := os.Stat(marker); !os.IsNotExist(err) {
        t.Fatalf("engine marker exists or stat failed with non-ENOENT: %v", err)
    }
    assertClean(t, repo)
}
```

Add a second variant or table row for:

```text
docs/use_cases/staging/UC-001.md
```

Run focused test:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./internal/pipe -run 'TestRunProtectedDocsAllowlistRejectsBeforeEngine' -v
```

Expected RED if pipe does not abort early; otherwise GREEN if existing `Payload.Validate()` already catches it.

#### Step 3: Implement or make validation explicit

If validation needs adjustment, update `internal/contracts/payload.go` so the protected predicate is equivalent to:

```regexp
^docs/(requirements|use_cases)/.*
```

A regex is not required if prefix logic is clearer, but the behavior must exactly match the Sprint plan.

Accept:

```text
docs/requirements_extra/file.md
```

Reject:

```text
docs/requirements/file.md
docs/requirements/active/REQ-001.md
docs/use_cases/file.md
docs/use_cases/staging/UC-001.md
```

Do not accidentally reject unrelated docs paths.

#### Step 4: Verify

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -l internal/contracts/payload.go internal/contracts/payload_test.go internal/pipe/run_test.go
go test ./internal/contracts ./internal/pipe -v
go test ./...
git diff --check
```

#### Step 5: Review gate

Spec reviewer must check:

- both protected prefixes are denied in both allowlists,
- pipe-level regression proves engine is not invoked,
- no broadening to full V47 schema.

Code-quality reviewer must check:

- tests are deterministic,
- no shell injection risk beyond controlled test fixtures,
- validation does not reject unrelated docs paths,
- no production broad staging commands were introduced.

#### Step 6: Push and outcome

After reviews pass:

```bash
git push origin main
```

Create `docs/outcomes/BLK-PIPE-001_task-009-outcome.md`, validate with `git diff --check`, commit, push, and attach to Discord.

---

## 7. Task 10 Plan — Add CLI Payload File Support

### Objective

Add the BLK-004-compatible physical payload-file invocation while preserving existing Sprint 001 behavior:

```bash
blk-pipe --payload /absolute/path/to/payload.json
```

This should read the JSON file and pass bytes to:

```go
pipe.Run(context.Background(), payloadJSON, stdout)
```

Do not replace or remove `--payload-stdin`; it remains useful for tests and internal invocation unless the user explicitly asks to remove it.

### Files

Modify:

- `cmd/blk-pipe/main.go`
- `cmd/blk-pipe/main_test.go`

Optional smoke-only temp files during tests; do not commit temp payloads.

Expected implementation commit:

```bash
git commit -m "feat: add blk-pipe payload CLI"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-001_task-010-outcome.md
```

Expected outcome commit:

```bash
git commit -m "docs: record BLK-pipe task 10 outcome"
```

### CLI Contract

Supported invocations after Task 10:

```bash
blk-pipe --health
blk-pipe --payload /absolute/path/to/payload.json
blk-pipe --payload-stdin
```

Unsupported invocations remain nonblocking and return invalid payload:

```bash
blk-pipe
blk-pipe --payload
blk-pipe --payload relative.json
blk-pipe --payload /missing/file.json
blk-pipe --unknown
```

### TDD Steps

#### Step 1: Add failing CLI tests

In `cmd/blk-pipe/main_test.go`, add tests around the testable `run(args, stdin, stdout, stderr)` helper.

Add a test for invalid JSON from a payload file:

```go
func TestPayloadFileInvalidJSONEmitsReport(t *testing.T) {
    payloadPath := filepath.Join(t.TempDir(), "payload.json")
    if err := os.WriteFile(payloadPath, []byte("{"), 0o600); err != nil {
        t.Fatalf("write payload: %v", err)
    }

    var stdout, stderr bytes.Buffer
    code := run([]string{"--payload", payloadPath}, strings.NewReader(""), &stdout, &stderr)

    if code != pipe.ExitInvalidPayload {
        t.Fatalf("exit code = %d, want %d; stdout=%s stderr=%s", code, pipe.ExitInvalidPayload, stdout.String(), stderr.String())
    }
    if !strings.Contains(stdout.String(), `"status":"INVALID_PAYLOAD"`) {
        t.Fatalf("stdout = %q, want INVALID_PAYLOAD report", stdout.String())
    }
}
```

Add a test for invalid but well-formed payload:

```go
func TestPayloadFileInvalidPayloadEmitsReport(t *testing.T) {
    payloadPath := filepath.Join(t.TempDir(), "payload.json")
    if err := os.WriteFile(payloadPath, []byte(`{"action":"execute"}`), 0o600); err != nil {
        t.Fatalf("write payload: %v", err)
    }

    var stdout, stderr bytes.Buffer
    code := run([]string{"--payload", payloadPath}, strings.NewReader(""), &stdout, &stderr)

    if code != pipe.ExitInvalidPayload {
        t.Fatalf("exit code = %d, want %d; stdout=%s stderr=%s", code, pipe.ExitInvalidPayload, stdout.String(), stderr.String())
    }
    if !strings.Contains(stdout.String(), `"status":"INVALID_PAYLOAD"`) {
        t.Fatalf("stdout = %q, want INVALID_PAYLOAD report", stdout.String())
    }
}
```

Add argument validation tests:

```go
func TestPayloadFileRequiresAbsolutePath(t *testing.T) { ... }
func TestPayloadFileMissingPathIsInvalidPayload(t *testing.T) { ... }
func TestPayloadFlagRequiresPath(t *testing.T) { ... }
```

Run focused tests before implementation:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./cmd/blk-pipe -run 'TestPayloadFile|TestPayloadFlag' -v
```

Expected: RED before implementation.

#### Step 2: Implement file reading

In `cmd/blk-pipe/main.go`:

- import `path/filepath` if needed,
- add branch before unsupported invocation:

```go
if len(args) == 2 && args[0] == "--payload" {
    if !filepath.IsAbs(args[1]) {
        fmt.Fprintln(stderr, "payload path must be absolute")
        return pipe.ExitInvalidPayload
    }
    payloadJSON, err := os.ReadFile(args[1])
    if err != nil {
        fmt.Fprintf(stderr, "read payload file: %v\n", err)
        return pipe.ExitInvalidPayload
    }
    return pipe.Run(context.Background(), payloadJSON, stdout)
}
```

Use `pipe.ExitInvalidPayload` for CLI argument/file-read failures so the Python adapter can route failed invocation as non-success. Do not panic.

Do not require `stdin` for file mode.

#### Step 3: Preserve existing behavior

Existing tests must continue passing:

- `--health` prints current Sprint 001 health JSON,
- `--payload-stdin` still works,
- zero args remain unsupported/nonblocking.

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
gofmt -w cmd/blk-pipe/main.go cmd/blk-pipe/main_test.go
go test ./cmd/blk-pipe -v
go test ./...
git diff --check
```

#### Step 4: Manual smoke checks

Run:

```bash
export PATH="$HOME/.local/bin:$PATH"
go run ./cmd/blk-pipe --health
```

Expected stdout exactly:

```json
{"status":"OK","component":"blk-pipe"}
```

Optional smoke for invalid payload file:

```bash
tmp_payload=$(mktemp /tmp/blk-pipe-invalid-XXXXXX.json)
printf '{' > "$tmp_payload"
go run ./cmd/blk-pipe --payload "$tmp_payload"; code=$?
rm -f "$tmp_payload"
printf 'exit=%s\n' "$code"
```

Expected exit code: `2`.

#### Step 5: Review gate

Spec reviewer must check:

- `--payload /absolute/path` exists,
- file mode calls `pipe.Run`,
- `--health` remains intact,
- zero args remain unsupported/nonblocking,
- no premature V47 schema expansion.

Code-quality reviewer must check:

- absolute path handling is clear,
- file read failures are deterministic,
- tests do not rely on external shell state,
- no broad Git staging or unrelated pipe changes.

#### Step 6: Push and outcome

After reviews pass:

```bash
git push origin main
```

Create `docs/outcomes/BLK-PIPE-001_task-010-outcome.md`, validate with `git diff --check`, commit, push, and attach to Discord.

---

## 8. Task 11 Plan — Document Sprint 001 CLI

### Objective

Document the first usable local developer command contract for BLK-pipe Sprint 001 and explicitly state Sprint 001 non-goals/deviations from full BLK-004/V47.

### Files

Create:

- `docs/BLK-009_blk-pipe-sprint-001-cli.md`

Modify:

- `README.md`

Expected implementation/docs commit:

```bash
git commit -m "docs: describe blk-pipe sprint 001 CLI"
```

Expected outcome doc:

```text
docs/outcomes/BLK-PIPE-001_task-011-outcome.md
```

Expected outcome commit:

```bash
git commit -m "docs: record BLK-pipe task 11 outcome"
```

### Required Documentation Content

`docs/BLK-009_blk-pipe-sprint-001-cli.md` must include:

1. Scope and status:
   - Sprint 001 deterministic execution kernel,
   - local fake-engine safety kernel,
   - no Codex execution.
2. Commands:

   ```bash
   go test ./...
   go run ./cmd/blk-pipe --health
   go run ./cmd/blk-pipe --payload /tmp/payload.json
   ```

3. Optional/internal command retained from Task 8:

   ```bash
   go run ./cmd/blk-pipe --payload-stdin
   ```

4. Sprint 001 payload schema:

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

5. Report fields:
   - `status`,
   - `action`,
   - `workdir`,
   - `commit_hash`,
   - `staged_files`,
   - `destroyed_files`,
   - `engine_exit_code`,
   - `engine_output_bytes`,
   - `error`.
6. Exit codes currently implemented in Sprint 001:

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

7. Safety guarantees:
   - no broad Git staging,
   - clean repo preflight,
   - bounded engine output,
   - process group cleanup,
   - protected BLK-req path denial,
   - `.git` mutation hardening,
   - hook-disabled commits,
   - nested Git repo cleanup.
8. Non-goals/deferred V47 work:
   - no Codex invocation,
   - no Python adapter yet,
   - no revert route yet,
   - no full V47 payload schema yet,
   - no validation command gate yet,
   - exit-code registry must be reconciled before revert support because BLK-004 reserves code 4 for invalid revert anchor while Sprint 001 uses it for engine failure.
9. Short BLK-004 compatibility note:
   - Sprint 001 provides the mechanical safety kernel that BLK-004 needs before autonomous execution,
   - full V47 contract remains Sprint 002+.

### README Update

Add `docs/BLK-009_blk-pipe-sprint-001-cli.md` to the initial/core doctrine/document list or add a new short section such as:

```markdown
## BLK-pipe Sprint 001 CLI

- [`docs/BLK-009_blk-pipe-sprint-001-cli.md`](docs/BLK-009_blk-pipe-sprint-001-cli.md) — first local BLK-pipe Sprint 001 CLI contract and safety guarantees.
```

Do not remove existing doctrine links.

### TDD/Verification Steps

Task 11 is documentation-only, but still verify by command:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
git diff --check
```

Also run targeted text checks to catch missing required sections:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('docs/BLK-009_blk-pipe-sprint-001-cli.md')
text = p.read_text()
required = [
    'go run ./cmd/blk-pipe --health',
    'go run ./cmd/blk-pipe --payload /tmp/payload.json',
    'Sprint 001 does not run Codex',
    'UNAUTHORIZED_FILE_MUTATION',
    'FATAL_OUTPUT_FLOOD',
    'ENGINE_TIMEOUT',
    'GIT_DIRTY',
    'BLK-004',
]
missing = [s for s in required if s not in text]
assert not missing, missing
assert text.count(chr(96) * 3) % 2 == 0
PY
```

Use `chr(96) * 3` in validation snippets inside Markdown fences when checking fence counts.

### Review Gate

Spec reviewer must check:

- Task 11 required commands documented,
- non-goals include no Codex,
- README points to the new document,
- deviations from BLK-004/V47 are explicit.

Code-quality/doc reviewer must check:

- docs are accurate against current code,
- no claims that full V47/Python adapter/revert are implemented,
- no Markdown trailing whitespace,
- code fences are balanced,
- commands are copy-pasteable.

### Push and outcome

After reviews pass:

```bash
git push origin main
```

Create `docs/outcomes/BLK-PIPE-001_task-011-outcome.md`, validate with `git diff --check`, commit, push, and attach to Discord.

---

## 9. Final Sprint 001 Closeout After Task 11

After Task 11 outcome is pushed, perform Sprint 001 closeout verification:

```bash
cd /home/dad/BLK-System
export PATH="$HOME/.local/bin:$PATH"
git status --short --branch
go test ./...
git grep -n "git add \.\|git add -u" -- . ':!docs/plans/BLK-PIPE-001_deterministic-execution-kernel.md' ':!docs/plans/BLK-PIPE-001_tasks-009-011_closeout-plan.md'
git diff --check
```

Expected:

- clean and aligned branch,
- all tests pass,
- no production broad staging commands,
- no Markdown trailing whitespace.

Recommended final Sprint 001 closeout document:

```text
docs/outcomes/BLK-PIPE-001_sprint-001-closeout.md
```

The closeout note must include:

- final commit hash,
- implemented exit codes,
- test output summary,
- list of implemented tasks 1-11,
- deviations from BLK-004/BLK-006,
- explicit statement that Codex integration remains deferred,
- recommended Sprint 002 scope.

---

## 10. Recommended Sprint 002 Seed Scope

Do not implement this in Tasks 9-11 unless the user explicitly asks. Use it for next planning only:

1. Reconcile exit-code registry with BLK-004/V47.
2. Introduce full V47 payload schema or compatibility adapter.
3. Add validation command sequencing and log aggregation.
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

## 11. Quick Resume Prompt For Future Hermes

If context is lost, resume with:

```text
Open /home/dad/BLK-System/docs/plans/BLK-PIPE-001_tasks-009-011_closeout-plan.md. Execute Task 9 next using blk-system-sprint-execution, strict TDD, two-stage review, controller-only push, and a pushed/attached outcome doc.
```
