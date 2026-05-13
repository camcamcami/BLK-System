# BLK-SYSTEM-106 Hostile Review — Go Protected-Body No-Read Remediation

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `internal/pipe/run.go`, `internal/pipe/run_test.go`, BLK-106 plan/boundary docs.

---

## Source Finding

Source report: `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`.

Relevant finding:

- HR-001: Go `blk-pipe` physical snapshots read protected BLK-req body files while constructing worktree snapshots.

---

## Hostile Probes

1. **Direct body-read regression:** added `TestSnapshotPhysicalWorktreeDoesNotReadProtectedBlkReqBody`.
   - RED: failed with `permission denied` when `snapshotPhysicalWorktree` attempted `os.ReadFile` on `docs/active/REQ-001.md`.
   - GREEN: passes after protected prefixes return metadata-only entries before `os.ReadFile`.

2. **Source inspection:** `physicalSnapshotEntry(entryPath, rel)` branches on `contracts.IsProtectedDocsPath(rel)` before the remaining `os.ReadFile(entryPath)` call. The remaining direct read path applies only to non-protected regular files. `.git` snapshot reads remain separate Git metadata preservation, not BLK-req body reads.

3. **Authority boundary probe:** the patch does not weaken protected allowlist validation. Protected BLK-req paths are still denied in `allowed_modified_files` and `allowed_new_files` by the contracts layer and mapped to `UNAUTHORIZED_FILE_MUTATION` in `blk-pipe`.

4. **Detection tradeoff probe:** protected body bytes are no longer read for byte-for-byte physical snapshot comparison. Metadata-only comparison preserves mode/kind/size/mtime checks; tracked protected content mutations remain governed by Git state and protected allowlist denial, but this sprint intentionally prioritizes `NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE` over direct body inspection.

---

## Verification

```text
go test ./internal/pipe -run TestSnapshotPhysicalWorktreeDoesNotReadProtectedBlkReqBody -count=1 -v
PASS
ok  	github.com/camcamcami/BLK-System/internal/pipe	0.019s

go test ./...
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	0.012s
ok  	github.com/camcamcami/BLK-System/internal/pipe	7.057s
(all packages OK)

go vet ./...
OK
```

---

## Finding Disposition

PASS. BLK-SYSTEM-106 remediates HR-001 for direct Go physical worktree snapshot body reads and preserves explicit non-authority boundaries: no BLK-pipe runtime dispatch, no BLK-test runtime, no BEO publication, no RTM generation/drift rejection, no protected-body read authority, and no production `blk-link`.
