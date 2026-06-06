# BLK-SYSTEM-352 — BLK-pipe Allowed-New Parent Directory Mode Normalization Sprint Closeout

**Status:** Complete
**Date:** 2026-06-06
**Commit:** this commit (`fix: normalize allowed-new parent directory modes`)

## 1. Objective

Fix the BLK-pipe fail-closed route limitation observed during the voided Kuronode K2-001 foundation attempt: clean-repo feature drops that create first-time parent directories under host `umask 0002` can create safe `0775` directories, causing BLK-pipe to return `UNAUTHORIZED_FILE_MUTATION` after Codex and validation succeeded.

The sprint scope was intentionally narrow:

- normalize safe `0775` newly-created parent directories to `0755` before staging/commit;
- tolerate safe directory entries in `allowed_new_files` as scaffold/path evidence without trying to stage directories;
- preserve fail-closed behavior for unsafe directory modes and unlisted descendants;
- preserve exact-file staging and no adjacent runtime/product authority.

## 2. Files Changed

- `internal/pipe/run.go`
  - skips directory entries when building the list of produced allowed-new files to stage;
  - normalizes safe allowed-new directory modes from `0775` to `0755`;
  - normalizes safe first-time parent directory modes from `0775` to `0755`;
  - rejects setuid, setgid, sticky, world-writable/exotic, and non-directory parent residues.
- `internal/pipe/run_test.go`
  - adds focused regressions for nested allowed-new files under `umask 0002`;
  - adds regressions for directory entries in `allowed_new_files`;
  - adds a regression that directory entries do not authorize unlisted descendants;
  - adds a setgid `2775` unsafe-parent rejection regression alongside the existing sticky `1777` rejection.

## 3. Implementation Summary

BLK-pipe previously normalized safe group-writable regular files (`0664` to `0644`) but required newly-created parent directories to be exactly `0755`. On this host, `umask 0002` makes first-time directories `0775`, so an otherwise bounded clean-repo drop failed closed after validation.

The fix adds `safeAllowedNewParentDirectoryMode`:

- accepts `0755` unchanged;
- accepts `0775` and normalizes it to `0755`;
- rejects setuid, setgid, sticky, and all other permission shapes.

Directory paths that appear in `allowed_new_files` are not staged; only regular produced files are staged. Directory allowlist entries also do not recursively authorize extra files.

## 4. Verification

### RED evidence

Focused regression initially failed before the implementation:

```text
--- FAIL: TestRunAllowedNewNestedFileWithGroupWritableUmaskNormalizesParentsAndCommits
exit code = 3, want 0
status=UNAUTHORIZED_FILE_MUTATION
destroyed_files=[src/ src/main/]
```

A second regression for directory entries in `allowed_new_files` also failed before the directory-staging adjustment:

```text
--- FAIL: TestRunAllowedNewDirectoryEntriesWithGroupWritableUmaskNormalizeAndCommitNestedFile
exit code = 9, want 0
status=INTERNAL_ERROR
error=stage path "src" ... must name a file, not a directory
```

### GREEN / focused tests

```text
go test ./internal/pipe -run 'TestRunAllowedNew(NestedFile|DirectoryEntries|DirectoryEntryDoesNotAuthorize).*|TestRunUnauthorizedAllowedNewParentDirectoryMode(1777|2775)FailsCleansAndDoesNotCommit' -count=1
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.257s
```

### Manual route reproduction after fix

A disposable repo payload with:

```text
umask 0002; mkdir -p src/main; printf 'ok\n' > src/main/main.ts
allowed_new_files = ["src", "src/main", "src/main/main.ts"]
```

returned:

```text
exit_code 0
status SUCCESS
denial_route none
destroyed_files []
staged_files ['src/main/main.ts']
diff_summary {'files_changed': 1, 'insertions': 1, 'deletions': 0, 'files': ['src/main/main.ts']}
src 755
src/main 755
git_status <clean>
```

### Full Go suite

```text
go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	9.780s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validationprofiles	(cached)
```

### Whitespace / diff check

```text
git diff --check -- internal/pipe/run.go internal/pipe/run_test.go
# no output
```

## 5. Hostile Review / Risk Check

Independent hostile review returned `PASS` with no blockers.

Nonblocker recommendations were remediated before closeout:

- added setgid `2775` unsafe-parent rejection coverage;
- added explicit coverage that a directory allowlist entry does not authorize unlisted descendants.

Risk conclusions:

- Directory entries in `allowed_new_files` are scaffold/path evidence only; they are not staged and do not recursively authorize file creation.
- Unsafe parent modes remain fail-closed and cleaned.
- Exact-file staging remains intact.
- The change does not grant reusable BLK-pipe dispatch, Codex dispatch, Kuronode mutation, BEO publication, RTM generation, production `blk-link`, protected-body access, runtime/tooling expansion, package-manager/network authority, or production-isolation claims.

## 6. Authority Boundary

This sprint only changes BLK-pipe local execute cleanup/staging behavior for safe newly-created directory modes in exact allowed-new file routes.

It does **not** authorize rerunning K2-001 by itself. A future K2 retry still needs a fresh exact BEB/L2/drop package, trusted approved manifest hash, target hash, validation profile, BLK-pipe dispatch boundary, and honest BEO evidence.

## 7. Documentation Burden Check

No new root `docs/BLK-###` doctrine document was created. The change is a narrow implementation hardening sprint with tests and exactly one sprint outcome closeout:

```text
docs/outcomes/BLK-SYSTEM-352_sprint-closeout.md
```
