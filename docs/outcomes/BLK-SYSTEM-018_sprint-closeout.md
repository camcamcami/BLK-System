# BLK-SYSTEM-018 — Sprint Closeout

**Status:** Complete
**Date:** 2026-05-07T17:54:25+10:00
**Repository:** `/home/dad/BLK-System`
**Plan:** `docs/plans/blk-system-018_protected-vault-exit3-and-revert-hardening.md`
**Source review:** `docs/reviews/BLK-SYSTEM_current-implementation_BLK-001-through-BLK-006_hostile-alignment-review.md`
**Post-remediation review:** `docs/reviews/BLK-SYSTEM-018_post-remediation-hostile-review.md`

---

## 1. Executive Summary

BLK-SYSTEM-018 is complete. The sprint remediated the two immediate implementation blockers from the current BLK-001 through BLK-006 hostile alignment review:

1. protected BLK-req vault allowlist violations now route as `UNAUTHORIZED_FILE_MUTATION` / POSIX Exit 3;
2. verified `revert` now reaches the emergency reset/clean path before execute-mode clean preflight blocks dirty/broken residue.

The sprint did not address `BLOCKING-3`; doctrine contradiction cleanup around BLK-020 remains assigned to the next sprint seed, `BLK-SYSTEM-019 — Active doctrine authority overlay cleanup`.

---

## 2. Task Commit Table

| Task | Scope | Commit | Outcome |
| --- | --- | --- | --- |
| 0 | Commit sprint plan | `a8bee0a docs: plan blk-system sprint 018 hardening` | `docs/outcomes/BLK-SYSTEM-018_task-000-outcome.md` |
| 1 | RED protected-vault Exit 3 tests | `c47dba2 test: expose protected vault exit routing gap` | `docs/outcomes/BLK-SYSTEM-018_task-001-outcome.md` |
| 2 | Protected-vault Exit 3 routing fix | `21f37f4 fix: route protected vault allowlists as unauthorized mutations` | `docs/outcomes/BLK-SYSTEM-018_task-002-outcome.md` |
| 3 | RED revert reachability tests | `2edbd15 test: expose revert preflight reachability gap` | `docs/outcomes/BLK-SYSTEM-018_task-003-outcome.md` |
| 4 | Revert-before-execute-preflight fix | `a12fb7a fix: allow verified revert before execute preflight` | `docs/outcomes/BLK-SYSTEM-018_task-004-outcome.md` |
| 5 | Persistent doctrine gates | `ddd4203 docs: gate blk-system sprint 018 authority boundaries` | `docs/outcomes/BLK-SYSTEM-018_task-005-outcome.md` |
| 6 | Hostile self-review and sprint closeout | `c77736c docs: close out blk-system sprint 018` | `docs/outcomes/BLK-SYSTEM-018_sprint-closeout.md` |

Note: the closeout document was first committed as `c77736c`; this follow-up metadata patch records that landed closeout commit hash without attempting an impossible self-referential amend.

---

## 3. Before / After Summary

### 3.1 `BLOCKING-1` — protected vault allowlist hits routed as Exit 2

**Before:** protected BLK-req vault allowlist entries were rejected during payload validation and mapped to `INVALID_PAYLOAD` / Exit 2.

**After:** partially decoded payloads with protected allowlist entries are classified by path string and return:

```text
Status: UNAUTHORIZED_FILE_MUTATION
Exit:   3
```

Regression evidence:

```text
TestRunProtectedVaultAllowlistReturnsUnauthorizedMutation
```

### 3.2 `BLOCKING-2` — revert blocked by execute-mode clean preflight

**Before:** `run(...)` called `cleanPreflight(...)` before checking `payload.Action == "revert"`, making verified emergency recovery unreachable in dirty workspaces.

**After:** `run(...)` dispatches `Action == "revert"` to `runRevert(...)` immediately after payload parse/validation succeeds. `runRevert(...)` still validates target branch, full object identity, and ancestry before reset/clean.

Regression evidence:

```text
TestRunRevertBypassesCleanPreflightForDirtyTrackedWorkspace
TestRunRevertBypassesCleanPreflightForUntrackedAndIgnoredResidue
TestRunRevertBypassesCleanPreflightForEmptyUntrackedDirectory
TestRunRevertCleansPreExistingNestedGitRepositoryAfterValidAnchor
TestRunRevertInvalidAnchorDoesNotReset
TestRunRevertWithTargetBranchRejectsWrongCurrentBranch
TestRunRevertSHA256RejectsAbbreviatedFortyHexTarget
```

---

## 4. Active Doctrine / Gate Closure

Task 005 added `test_sprint018_exit3_and_revert_boundaries_are_active_doctrine` to `python/test_active_doctrine_review_gates.py` and patched active doctrine:

```text
docs/BLK-006_blk-req-implementation-brief.md
docs/BLK-004_blk-pipe-v47-architecture-suite.md
```

The gate keeps the following markers persistent:

```text
protected BLK-req vault allowlist violations return POSIX Exit 3
UNAUTHORIZED_FILE_MUTATION
revert bypasses execute-mode clean preflight only after target hash validation
target_hash
sprint_base_hash
does not authorize BLK-req vault body reads
does not authorize live BLK-test MCP
does not authorize authoritative BEO publication
does not authorize RTM generation
```

---

## 5. Final Verification Evidence

Final verification was run from `/home/dad/BLK-System` after writing the hostile review and closeout documents.

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 311 tests in 6.385s
OK

go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.104s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)

go vet ./...
exit 0, no output

git diff --check
exit 0, no output
```

---

## 6. Acceptance Criteria Status

| Criterion | Status |
| --- | --- |
| Protected allowlist entries under `docs/active/`, `docs/requirements/`, and `docs/use_cases/` route to Exit 3 | PASS |
| Protected allowlist reports use `UNAUTHORIZED_FILE_MUTATION` | PASS |
| Protected allowlist reports do not require or perform protected body reads | PASS |
| Engine execution is skipped for protected allowlist payloads | PASS |
| Ordinary malformed payloads still route to Exit 2 | PASS |
| Valid revert executes from dirty tracked workspaces | PASS |
| Valid revert executes from untracked/ignored residue workspaces | PASS |
| Nested `.git` revert behavior is remediated | PASS |
| Invalid target hash/branch/ancestry still prevents revert reset | PASS |
| Execute-mode clean preflight remains enforced for non-revert execution | PASS |
| Active doctrine records the Exit 3 and emergency-revert boundaries | PASS |
| Python unittest discovery passes | PASS |
| `go test ./...` passes | PASS |
| `go vet ./...` passes | PASS |
| `git diff --check` passes | PASS |
| Task outcomes exist for every task | PASS |
| Sprint closeout and hostile self-review exist | PASS |
| All task commits are pushed to `origin/main` | PASS |
| No live BLK-test MCP, RTM generation, RTM authority, or authoritative BEO publication was introduced | PASS |
| Follow-up `BLK-SYSTEM-019` remains explicitly scoped to doctrine cleanup | PASS |

---

## 7. Non-Execution Statement

BLK-SYSTEM-018 did not invoke Codex or live tactical LLMs, did not call network model services, did not run cyber tooling, did not start production BLK-test MCP, did not read or mutate protected BLK-req vault bodies, did not generate RTM, did not assert RTM drift rejection authority, and did not publish authoritative BEOs.

---

## 8. Next Sprint Seed

`BLK-SYSTEM-019 — Active doctrine authority overlay cleanup`

Seed scope: remediate `BLOCKING-3` from the source hostile review by clarifying active doctrine around the accepted BLK-020 first live fixed-tool smoke exception while preserving that it grants no production BLK-test MCP authority, no source mutation authority, no protected-vault body read authority, no authoritative BEO publication, and no RTM generation or RTM drift authority.
