# BLK-pipe Sprint 001 — Task 11 Outcome

**Status:** Complete
**Date:** 2026-05-03
**Task:** Add documentation for Sprint 001 CLI
**Implementation Commit:** `94a5e9b docs: describe blk-pipe sprint 001 CLI`
**Remote:** pushed to `origin/main`

---

## 1. Objective

Task 11 documented the first usable local developer command contract for BLK-pipe Sprint 001.

The required documentation work was to:

1. create `docs/BLK-009_blk-pipe-sprint-001-cli.md`,
2. update `README.md` so the new document is discoverable,
3. document current Sprint 001 CLI commands,
4. explicitly state that Sprint 001 does not run Codex,
5. document the Sprint 001 payload schema, report fields, exit codes, and safety guarantees,
6. state BLK-004/V47 non-goals and deferrals accurately.

This was a documentation-only task. No Go behavior changed.

---

## 2. Files Added / Changed

### Created

- `docs/BLK-009_blk-pipe-sprint-001-cli.md`

### Modified

- `README.md`

---

## 3. Documentation Added

### 3.1 BLK-009 CLI contract

The new `docs/BLK-009_blk-pipe-sprint-001-cli.md` records the Sprint 001 developer-facing command contract:

```bash
export PATH="$HOME/.local/bin:$PATH"
go test ./...
go run ./cmd/blk-pipe --health
go run ./cmd/blk-pipe --payload /tmp/payload.json
go run ./cmd/blk-pipe --payload-stdin
```

The document also explains unsupported invocation behavior for:

```bash
go run ./cmd/blk-pipe
go run ./cmd/blk-pipe --payload
go run ./cmd/blk-pipe --payload relative/payload.json
go run ./cmd/blk-pipe --payload /absolute/path/that/does/not/exist.json
go run ./cmd/blk-pipe --unknown
```

### 3.2 Payload schema

BLK-009 documents the Sprint 001 payload schema:

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

The documentation explicitly notes that Sprint 001 treats `allowed_modified_files` and `allowed_new_files` as the combined validated staging boundary and does not yet separately enforce tracked/new semantics.

### 3.3 Report fields

BLK-009 documents the current Sprint 001 report fields:

- `status`,
- `action`,
- `workdir`,
- `commit_hash`,
- `staged_files`,
- `destroyed_files`,
- `engine_exit_code`,
- `engine_output_bytes`,
- `error`.

The final reviewed wording clarifies that `destroyed_files` reports unauthorized mutation paths during cleanup/restoration and that `.git` metadata paths can be reported while BLK-pipe restores metadata before exit where possible.

### 3.4 Exit codes

BLK-009 records the Sprint 001 exit codes currently implemented:

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

### 3.5 Safety guarantees

BLK-009 documents the current safety guarantees:

- explicit payload execution only,
- clean Git preflight,
- bounded engine execution,
- process group cleanup,
- no broad Git staging,
- allowlist-only staging,
- protected BLK-req path denial,
- unauthorized mutation cleanup,
- `.git` mutation hardening,
- hook-disabled commits,
- nested Git repo cleanup,
- deterministic success commit message.

### 3.6 BLK-004/V47 deferrals

BLK-009 explicitly states that Sprint 001 does not implement:

- Codex invocation,
- live tactical LLM execution,
- Python adapter,
- full V47 payload schema,
- validation command sequencing,
- revert route,
- revert ancestry gate,
- full V47 report fields,
- shared exit-code registry reconciliation.

It also records the known exit-code reconciliation issue: BLK-004 reserves code `4` for invalid revert anchor, while Sprint 001 uses code `4` for `ENGINE_FAILED`.

---

## 4. README Update

`README.md` now links to the new BLK-009 document in the doctrine list and includes a short `BLK-pipe Sprint 001 CLI` section.

No existing doctrine links were removed.

---

## 5. Review Results

Task 11 went through two review passes.

### 5.1 Initial review

Spec compliance passed, but the code-quality/doc review requested changes for documentation accuracy:

1. The success-path example overclaimed that successful allowlisted mutations also destroy unauthorized mutations and commit.
2. The cleanup wording implied staged allowlisted files were preserved on all unauthorized outcomes.
3. The closeout broad-staging grep was not sufficiently precise/copy-pasteable.
4. The allowlist field descriptions over-implied tracked/new semantic enforcement that Sprint 001 does not yet enforce.
5. The opening scope wording implied payload bytes were bounded; the implementation bounds engine execution/output, not payload file size.

### 5.2 Fixes applied

The documentation was revised to state:

- successful runs commit allowlisted changes only,
- unauthorized mutations produce `UNAUTHORIZED_FILE_MUTATION` and do not create a success commit,
- cleanup/restoration behavior differs for normal worktree mutation and `.git` metadata mutation paths,
- `allowed_modified_files` and `allowed_new_files` are currently the combined staging boundary,
- only engine execution/output is bounded in Sprint 001,
- the production-code broad-staging grep is:

```bash
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
```

### 5.3 Final review

Final review results:

- **Spec compliance:** PASS
- **Documentation/code quality:** APPROVED

The final reviewers found no critical, important, or minor issues.

---

## 6. Final Verification

Controller-side final verification before push passed:

```bash
export PATH="$HOME/.local/bin:$PATH"
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
for i, line in enumerate(text.splitlines(), 1):
    assert line.rstrip() == line, f'trailing whitespace line {i}'
readme = Path('README.md').read_text()
assert 'docs/BLK-009_blk-pipe-sprint-001-cli.md' in readme
print('task 11 doc validation passed')
PY
go test ./...
git diff --check
! git grep -n -E '"add",[[:space:]]*"(\.|-u)"' -- '*.go' ':!*_test.go'
```

Observed results:

```text
task 11 doc validation passed
ok github.com/camcamcami/BLK-System/cmd/blk-pipe
ok github.com/camcamcami/BLK-System/internal/contracts
ok github.com/camcamcami/BLK-System/internal/engine
ok github.com/camcamcami/BLK-System/internal/gitguard
ok github.com/camcamcami/BLK-System/internal/pipe
ok github.com/camcamcami/BLK-System/internal/testutil
```

`git diff --check` passed, and the production-code broad-staging grep printed no matches.

---

## 7. Git / Remote State

Implementation documentation commit:

```text
94a5e9b docs: describe blk-pipe sprint 001 CLI
```

The commit was pushed to `origin/main`.

---

## 8. Deviations / Notes

- This task was documentation-only, so there was no RED/GREEN code cycle.
- The verification gate still ran the full Go suite to ensure documentation changes did not mask a broken repository state.
- The final BLK-009 doc intentionally avoids claiming Sprint 001 implements full BLK-004/V47.
- Codex integration remains deferred.

---

## 9. Next Step

Task 11 completes Tasks 9-11 in the closeout plan. The remaining closeout-plan step is final Sprint 001 closeout verification and a recommended Sprint 001 closeout document:

```text
docs/outcomes/BLK-PIPE-001_sprint-001-closeout.md
```
