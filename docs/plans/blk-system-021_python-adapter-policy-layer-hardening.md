# BLK-SYSTEM-021 — Python Adapter Policy-Layer Hardening Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `test-driven-development`, and `requesting-code-review` when executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` first, then BLK-001 through BLK-006 as applicable. Execute task-by-task with strict RED/GREEN evidence, deterministic local tests, exact-path staging, per-task outcome docs, and push after each task. Do not use Hindsight unless explicitly requested. Do not run Codex, live tactical LLMs, network model services, cyber tooling, production BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication unless a separate execution approval explicitly grants it.

**Goal:** Harden the Python `blk-pipe` adapter as a fail-fast convenience layer that preserves BLK-native payload policy before invoking the Go blast shield, without making Python the source of authority.
**BLK-024 track:** Track E — Python adapter and orchestrator policy layer / maturity level L1 fixture-only implementation with L2-style local fail-closed preflight checks.
**Architecture:** The Go `blk-pipe` binary remains the final deterministic authority for payload validation, protected path rejection, validation profile resolution, Git routing, execution, cleanup, and reporting. This sprint adds Python-side mirror checks, typed payload construction helpers, and doctrine gates so operator/orchestrator mistakes are caught before the subprocess call while Go-side enforcement still catches malicious or broken payloads. Adapter checks must preserve `trace_artifacts`, `validation_profiles`, exact allowlists, revert anchors, and raw report evidence without broadening any authority.
**Tech Stack:** Python adapter/unit tests, Markdown doctrine gates, existing Go verification/profile tests, Git CLI.
**Authority boundary:** Fixture/local policy hardening only. This plan does not authorize production BLK-test MCP, live tactical execution, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

---

## 0. Current Known State

Planning preflight captured before drafting this plan:

```text
date -Iseconds              -> 2026-05-07T20:54:37+10:00
git status --short --branch -> ## main...origin/main
HEAD                        -> 6011cba docs: close blk-system sprint 020 validation profiles
```

Relevant existing sprint/document state:

```text
docs/BLK-024_blk-system-development-roadmap.md
docs/plans/blk-system-020_validation-command-profile-tightening.md
docs/outcomes/BLK-SYSTEM-020_sprint-closeout.md
docs/reviews/BLK-SYSTEM-020_post-remediation-hostile-review.md
```

Next-ID discovery:

```text
No existing docs/plans/blk-system-021* file was found.
No existing BLK-SYSTEM-021 outcome file was found.
BLK-SYSTEM-020 closeout recommends BLK-SYSTEM-021 — Python adapter policy-layer hardening.
Selected sprint ID: BLK-SYSTEM-021
Selected plan path: docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
```

BLK-024 Track E source:

- Track E says Python adapters are transport helpers unless explicitly upgraded.
- Track E calls for adapter-side preflight checks that mirror, but do not replace, Go authority checks.
- Track E requires adapter payload construction to preserve `trace_artifacts`, deny-read flags, validation profiles, and exact allowlists.
- Track E requires tests proving the adapter cannot silently drop required trace metadata or broaden authority fields.
- Track E exit marker says Python orchestration should reduce operator mistakes while fail-closed Go enforcement still catches malicious or broken payloads.

Current implementation surface observed during planning:

- `python/blk_pipe_adapter.py` constructs execute/revert payload dictionaries and invokes `blk-pipe --payload <temp.json>`.
- The adapter already routes known POSIX statuses, preserves raw report/stderr, forwards `trace_artifacts`, supports `validation_profiles`, and rejects mixed `validation_profiles` plus `validation_commands`.
- The adapter does not yet have a single explicit policy/preflight layer for canonical trace metadata shape, absolute work directories, empty critical fields, protected BLK-req allowlists, validation-profile hygiene, engine argument deny-read guardrails, or subprocess environment scrubbing.
- `python/blk_pipe_dry_run_orchestrator.py` has separate fixture-oriented trace and payload validation helpers; Sprint 021 may reuse patterns but should avoid turning dry-run fixtures into broad execution authority.

---

## 1. Scope and Non-Goals

### In scope

1. Add Python-side policy/preflight tests proving unsafe adapter inputs fail before invoking `blk-pipe`.
2. Implement small, reusable adapter policy helpers that mirror Go-side payload requirements without replacing Go enforcement.
3. Preserve canonical `trace_artifacts` and reject missing, empty, malformed, or uppercase/truncated hashes for execute payloads.
4. Refuse protected BLK-req vault paths in adapter allowlists before subprocess invocation while preserving Go Exit 3 as final authority.
5. Preserve Sprint 020 validation profile policy in Python: profiles are preferred for BLK-native requests, mixed source is refused, names are non-empty strings, and free-form commands remain trusted-local compatibility only.
6. Add adapter-side subprocess environment scrubbing for the same high-risk variables BLK-004 highlights (`SSH_AUTH_SOCK`, `SSH_AGENT_PID`, `SSH_ASKPASS`) and ensure `PWD`/working-directory behavior is explicit enough for audit.
7. Patch active doctrine and persistent review gates to say Python policy is a convenience/preflight layer; Go remains the authority.
8. Close with a hostile self-review against BLK-024 Track E and BLK-001 through BLK-006.

### Non-goals

This sprint must not implement or authorize:

- production BLK-test MCP or new live BLK-test smoke runs;
- live Codex, live tactical LLM execution, network model services, or cyber tooling;
- arbitrary shell as BLK-test behavior;
- source mutation by BLK-test;
- protected BLK-req vault body reads, copying, parsing, hashing, or mutation;
- authoritative BEO publication, public ledger mutation, signer/storage/rollback authority;
- RTM generation, runtime `rtm_id`, RTM coverage matrices, or RTM drift rejection;
- Python as final enforcement authority;
- a complete BEB generator migration;
- removal of trusted-local `validation_commands` compatibility;
- new validation profiles beyond those approved in Sprint 020 unless separately justified and reviewed.

---

## 2. BLK-001 through BLK-006 Alignment Matrix

| Governing doc | Required boundary | Sprint 021 treatment |
| --- | --- | --- |
| BLK-001 — Master Architecture | Preserve separation between BLK-req, Hermes planning, BLK-pipe mutation, BLK-test evidence, and blk-link trace closure. | Only Python preflight/payload construction is hardened. No BLK-test, BEO, RTM, or protected-vault authority is added. |
| BLK-002 — Artifact Lifecycle | Requirements/use-case staging, HITL approval, canonical hashes, and active vault isolation remain separate from tactical execution. | Adapter may validate trace metadata shape but must not fetch, read, hash, or compare active BLK-req bodies. |
| BLK-003 — Orchestration Protocol | BEB/L2 packets, exact trace artifacts, bounded payloads, POSIX routing, hostile audit, and failure ceilings remain explicit. | Adapter preflight preserves BEB IDs, L2 packet opacity, trace artifacts, profiles, exact allowlists, and POSIX status routing. |
| BLK-004 — BLK-pipe V47 Suite | BLK-pipe is deterministic compiled authority; validation, Git, cleanup, protected-path, and report evidence remain Go-owned. | Python mirrors obvious policy mistakes before subprocess invocation but Go remains final enforcement authority and report source of truth. |
| BLK-005 — BLK-Req Specification | Traceability remains atomic, hash-bound, and body-isolated. | Adapter accepts only canonical trace artifact metadata and does not inspect requirement/use-case bodies. |
| BLK-006 — BLK-Req Implementation Brief | Protected vault hard-deny and staged revisions remain BLK-req/backend concerns, not tactical/adapter authority. | Python refuses protected paths as early operator feedback, while doctrine states Go protected-path rejection remains authoritative. |

---

## 3. Controller Workflow for Each Task

For each task:

1. Preflight:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   git status --short --branch
   git log -1 --oneline
   ```
2. Read this task section and the governing docs named in it.
3. Use strict TDD where code changes are involved:
   - add/patch the failing focused test first;
   - run the focused test and capture RED;
   - implement only the scoped files;
   - rerun focused test and capture GREEN;
   - run shared verification.
4. Shared verification:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
5. Remove generated Python cache before status/staging:
   ```bash
   python3 - <<'PY'
   from pathlib import Path
   import shutil
   for p in [Path('python/__pycache__'), Path('python/.pytest_cache'), Path('.pytest_cache')]:
       if p.exists():
           shutil.rmtree(p)
   PY
   ```
6. Write a task outcome doc under `docs/outcomes/` recording RED/GREEN evidence, exact changed paths, verification commands, and the non-execution statement.
7. Stage exact paths only. Do not use `git add .`, `git add -u`, broad globs, stash, reset, checkout, or broad pathspecs to manage task files.
8. Verify staged paths:
   ```bash
   git diff --cached --name-only
   ```
9. Commit with the task-specific message.
10. Push to `origin/main` after each task commit.

---

## 4. Task 0 — Commit Sprint Plan

**Objective:** Preserve this sprint plan as an in-repo executable contract before implementation begins.

**Files:**

- Create: `docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md`
- Create: `docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md`

**Steps:**

1. Verify the plan exists and contains required authority markers:
   ```bash
   test -f docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
   grep -F "Track E — Python adapter and orchestrator policy layer" docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
   grep -F "Go remains the final deterministic authority" docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
   grep -F "does not authorize production BLK-test MCP" docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
   grep -F "does not authorize RTM generation" docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
   git diff --check -- docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md
   ```
2. Create `docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md` recording:
   - plan path;
   - BLK-024 Track E source;
   - current preflight status;
   - no implementation change;
   - non-execution statement.
3. Run shared verification or, if plan-only publication is intentionally kept light, at minimum run:
   ```bash
   git diff --check -- docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md
   python3 - <<'PY'
   from pathlib import Path
   for path in [Path('docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md'), Path('docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md')]:
       text = path.read_text()
       fence = chr(96) * 3
       assert text.count(fence) % 2 == 0, path
   PY
   ```
4. Stage exact files:
   ```bash
   git add docs/plans/blk-system-021_python-adapter-policy-layer-hardening.md \
           docs/outcomes/BLK-SYSTEM-021_task-000-outcome.md
   git diff --cached --name-only
   ```
5. Commit and push:
   ```bash
   git commit -m "docs: plan blk-system sprint 021 python adapter policy"
   git push origin main
   ```

---

## 5. Task 1 — Add RED Gates for Adapter Payload Policy Preflight

**Objective:** Prove the Python adapter currently lacks a centralized fail-fast policy layer for malformed execute payloads and protected allowlist mistakes.

**Files:**

- Modify: `python/test_blk_pipe_adapter.py`
- Create: `docs/outcomes/BLK-SYSTEM-021_task-001-outcome.md`

**Required RED tests:**

1. `execute_sprint` rejects missing or empty `trace_artifacts` for execute payloads before invoking the fake binary.
2. `execute_sprint` rejects malformed trace artifact entries:
   - non-object entries;
   - missing `kind`, `id`, or `version_hash`;
   - `version_hash` not matching `sha256:<64-lowercase-hex>`;
   - uppercase or truncated hash values.
3. `execute_sprint` rejects non-absolute `work_dir` values.
4. `execute_sprint` rejects empty `beb_id`, `target_branch`, `engine`, and `l2_packet` for execute payloads.
5. `execute_sprint` rejects protected BLK-req allowlist paths in both `allowed_modified_files` and `allowed_new_files`, including:
   - `docs/active/REQ-001.md`;
   - `docs/requirements/staging/REQ-001.md`;
   - `docs/use_cases/staging/UC-001.md`.
6. `execute_sprint` rejects empty, duplicate, or non-string `validation_profiles` before subprocess invocation.
7. `execute_sprint` rejects `validation_commands` entries that are non-strings or empty strings while preserving trusted-local compatibility for non-empty command strings.
8. The fake binary capture directory must prove rejected calls never invoke `blk-pipe`.

**Focused RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

**Expected RED:** tests fail because adapter policy helpers do not yet reject one or more unsafe payload shapes before subprocess invocation.

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-021_task-001-outcome.md` must record the RED output and confirm no production authority was granted.

**Commit message:**

```text
test: add python adapter policy preflight gates
```

---

## 6. Task 2 — Implement Adapter Policy Helpers and Execute Payload Preflight

**Objective:** Add minimal Python policy helpers so common operator/orchestrator mistakes fail before `blk-pipe` is invoked, while preserving Go authority as the final source of truth.

**Files:**

- Modify: `python/blk_pipe_adapter.py`
- Modify: `python/test_blk_pipe_adapter.py`
- Create: `docs/outcomes/BLK-SYSTEM-021_task-002-outcome.md`

**Implementation requirements:**

1. Add helper functions with clear names, for example:
   - `_validate_execute_payload_policy(payload: dict[str, Any]) -> None`
   - `_validate_trace_artifacts(trace_artifacts: Any) -> list[dict[str, str]]`
   - `_validate_allowlist_paths(paths: Any, field_name: str) -> list[str]`
   - `_validate_validation_profiles(profiles: Any) -> list[str]`
   - `_validate_validation_commands(commands: Any) -> list[str]`
2. Execute payload validation must happen before `_invoke_binary(payload)` and before any temp payload file is created.
3. Execute payloads must require non-empty canonical `trace_artifacts`.
4. Trace validation must accept only dictionaries containing non-empty string `kind`, `id`, and lowercase canonical SHA-256 `version_hash` values.
5. `work_dir` must be absolute; `beb_id`, `target_branch`, `engine`, and `l2_packet` must be non-empty strings.
6. Allowed path lists must contain only non-empty relative path strings. Reject absolute paths, `..` traversal, and protected BLK-req path prefixes:
   - `docs/active/`
   - `docs/requirements/`
   - `docs/use_cases/`
7. Revert payloads must keep their separate shape and must not require `trace_artifacts`, validation profiles, engine, or L2 content.
8. Error messages should include the field name that failed (`trace_artifacts`, `allowed_modified_files`, etc.) so Discord/operator summaries are useful.
9. Do not import third-party dependencies.

**Focused GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

**Shared GREEN commands:**

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-021_task-002-outcome.md` must record Task 1 RED, Task 2 GREEN, exact changed paths, and a no-authority-expansion statement.

**Commit message:**

```text
feat: add python adapter payload policy preflight
```

---

## 7. Task 3 — Harden Subprocess Invocation Environment and Report Preservation

**Objective:** Ensure Python subprocess invocation reduces operator risk and preserves Go report evidence without hiding or upgrading statuses.

**Files:**

- Modify: `python/blk_pipe_adapter.py`
- Modify: `python/test_blk_pipe_adapter.py`
- Create: `docs/outcomes/BLK-SYSTEM-021_task-003-outcome.md`

**Required behavior:**

1. Build a scrubbed subprocess environment helper, for example `_build_subprocess_env(work_dir: str | None = None) -> dict[str, str]`.
2. Remove at minimum:
   - `SSH_AUTH_SOCK`
   - `SSH_AGENT_PID`
   - `SSH_ASKPASS`
3. Preserve necessary baseline environment variables unless explicitly high risk; do not invent a full sandbox claim.
4. Set or preserve `PWD` consistently for audit when a payload `work_dir` is known.
5. Keep subprocess invocation shell-free: `[self.binary_path, "--payload", temp_payload_path]` only.
6. Add tests proving high-risk variables are not present in the environment passed to `subprocess.run`.
7. Add tests proving `raw_report`, `stderr`, `trace_artifacts`, `validation_profiles`, `resolved_validation_commands`, `staged_files`, and `destroyed_files` are preserved for both success and non-success where present.
8. Do not reinterpret unknown future report fields; keep `raw_report` as the full Go output.
9. Do not treat nonzero unknown return codes as success.

**Focused RED/GREEN command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_pipe_adapter -v
```

**Shared GREEN commands:**

```bash
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-021_task-003-outcome.md` must record RED/GREEN evidence, subprocess environment markers, report-preservation evidence, and no production BLK-test/BEO/RTM authority.

**Commit message:**

```text
feat: scrub python adapter subprocess environment
```

---

## 8. Task 4 — Patch Doctrine and Persistent Review Gates

**Objective:** Make active doctrine accurately describe the Python adapter policy boundary and prevent future readers from treating Python preflight as final authority.

**Files:**

- Modify: `docs/BLK-004_blk-pipe-v47-architecture-suite.md`
- Modify: `python/test_active_doctrine_review_gates.py`
- Create: `docs/outcomes/BLK-SYSTEM-021_task-004-outcome.md`

**Doctrine requirements:**

Patch BLK-004 current-state overlay or Python adapter section to state:

- Python adapter policy checks are fail-fast convenience only.
- Go remains the final deterministic enforcement authority.
- Adapter preflight must preserve canonical `trace_artifacts`, validation profiles, exact allowlists, and raw report evidence.
- Adapter preflight may reject protected BLK-req path allowlists early but does not authorize BLK-req vault body reads.
- Adapter subprocess invocation scrubs high-risk SSH/askpass variables but does not claim production sandbox, cgroup, VM, network, or host-secret isolation.
- The boundary does not authorize production BLK-test MCP, live tactical LLM execution, authoritative BEO publication, RTM generation, or RTM drift rejection.

**Persistent gate requirements:**

Add a focused Python doctrine gate, recommended name:

```text
test_sprint021_python_adapter_policy_boundary_preserves_go_authority
```

The gate should verify required markers in `docs/BLK-004_blk-pipe-v47-architecture-suite.md`, including:

```text
Python adapter policy checks are fail-fast convenience only
Go remains the final deterministic enforcement authority
canonical trace_artifacts
validation profiles
exact allowlists
raw report evidence
SSH_AUTH_SOCK
does not authorize production BLK-test MCP
```

**RED command:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
```

**Expected RED:** missing Sprint 021 Python adapter policy markers in BLK-004.

**GREEN/shared commands:**

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -v
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
go test ./...
go vet ./...
git diff --check
```

**Outcome doc:**

`docs/outcomes/BLK-SYSTEM-021_task-004-outcome.md` must record RED/GREEN doctrine-gate evidence and confirm no BLK-test/BEO/RTM/protected-vault authority expansion.

**Commit message:**

```text
docs: define python adapter policy boundary
```

---

## 9. Task 5 — Hostile Self-Review and Sprint Closeout

**Objective:** Verify the completed sprint against BLK-024 Track E, BLK-001 through BLK-006, and the authority boundaries in this plan.

**Files:**

- Create: `docs/reviews/BLK-SYSTEM-021_post-remediation-hostile-review.md`
- Create: `docs/outcomes/BLK-SYSTEM-021_sprint-closeout.md`
- Create: `docs/outcomes/BLK-SYSTEM-021_task-005-outcome.md`

**Hostile review checklist:**

1. Does Python still remain a convenience/preflight layer rather than the final authority?
2. Does Go `blk-pipe` still own final payload validation, protected-path classification, profile resolution, execution, cleanup, and report evidence?
3. Does adapter preflight require canonical non-empty `trace_artifacts` for execute payloads without reading protected artifact bodies?
4. Does adapter preflight refuse protected BLK-req allowlist paths early while preserving Go Exit 3 as the authoritative protected-path outcome?
5. Are `validation_profiles` preserved and mixed with `validation_commands` rejected?
6. Does trusted-local `validation_commands` compatibility remain explicitly bounded and not future autonomous authority?
7. Are subprocess invocations shell-free and high-risk SSH/askpass environment variables scrubbed?
8. Are raw Go report fields preserved without hiding non-success statuses?
9. Did the sprint avoid production BLK-test MCP, new live smoke runs, arbitrary shell as BLK-test, protected-vault body reads, authoritative BEO publication, RTM generation, and drift authority?
10. Are follow-up candidates separated cleanly, especially BEB generator/profile migration and later removal or stricter gating of legacy free-form validation commands?

**Verification commands:**

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go vet ./...
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
git diff --check
git status --short --branch
```

**Closeout requirements:**

`docs/outcomes/BLK-SYSTEM-021_sprint-closeout.md` must include:

- final commit table for task commits;
- summary of adapter policy checks and subprocess environment hardening;
- final verification output;
- non-execution statement;
- no-authority-expansion statement;
- residual/next-sprint seeds.

Likely next-sprint seeds after closeout:

- BEB generator/profile migration if trusted-local payload producers still emit `validation_commands`;
- later explicit removal or stricter gating of legacy free-form validation commands after approved producers migrate;
- BLK-test pilot design review only after adapter/profile hardening is closed and hostile-reviewed.

**Staging and commit:**

```bash
git add docs/reviews/BLK-SYSTEM-021_post-remediation-hostile-review.md \
        docs/outcomes/BLK-SYSTEM-021_task-005-outcome.md \
        docs/outcomes/BLK-SYSTEM-021_sprint-closeout.md
git diff --cached --name-only
git commit -m "docs: close blk-system sprint 021 python adapter policy"
git push origin main
```

---

## 10. Acceptance Criteria

BLK-SYSTEM-021 is complete only if all criteria below pass:

1. Python adapter execute payloads require non-empty canonical `trace_artifacts` and reject malformed hashes before subprocess invocation.
2. Python adapter rejects empty critical execute fields and non-absolute `work_dir` before subprocess invocation.
3. Python adapter rejects protected BLK-req allowlist paths early without claiming protected-vault body access.
4. Python adapter preserves Sprint 020 validation profile policy: profile requests are preserved, duplicates/empty names fail, and mixed profile/free-form command requests fail.
5. Python adapter subprocess invocation remains shell-free and scrubs `SSH_AUTH_SOCK`, `SSH_AGENT_PID`, and `SSH_ASKPASS`.
6. Python adapter preserves raw Go report evidence, stderr, trace artifacts, validation profiles, resolved validation commands, staged files, destroyed files, and non-success statuses.
7. Revert payload behavior remains valid and is not forced to include execute-only trace/profile/L2 fields.
8. BLK-004 and persistent doctrine gates preserve the adapter policy boundary and Go final authority.
9. Full verification passes:
   ```bash
   go test ./...
   go vet ./...
   PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
   git diff --check
   ```
10. Every task has an outcome doc under `docs/outcomes/`.
11. Hostile self-review and sprint closeout are committed and pushed.

---

## 11. Non-Execution and No-Authority-Expansion Statement

This plan does not authorize Hindsight use, Codex use, live tactical LLM execution, network model services, cyber tooling, production BLK-test MCP, new live BLK-test smoke runs, arbitrary shell as BLK-test behavior, protected BLK-req vault body reads, copying, parsing, hashing, or mutation, authoritative BEO publication, RTM generation, RTM drift rejection authority, public ledger mutation, signer/storage/rollback authority, or source mutation outside exact approved allowlists.

The intended authority movement is only local operator-error reduction: Python adapter preflight should make malformed BLK-native payloads fail earlier and more readably, while the compiled Go `blk-pipe` remains the final enforcement authority and hostile-audit evidence source.
