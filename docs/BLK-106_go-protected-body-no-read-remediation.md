# BLK-106 — Go Protected-Body No-Read Remediation

**Status:** Active BLK-pipe implementation hardening record — not runtime dispatch authority
**Date:** 2026-05-14
**Purpose:** Record the BLK-SYSTEM-106 remediation of Go `blk-pipe` physical worktree snapshots so protected BLK-req body files remain opaque to direct Go reads.
**Scope:** Local BLK-System Go implementation and regression tests only.

---

## 0. Boundary Markers

```text
BLK_SYSTEM_106_GO_PROTECTED_BODY_NO_READ_REMEDIATED
GO_PHYSICAL_WORKTREE_PROTECTED_BODY_METADATA_ONLY
NO_PROTECTED_BODY_READS_FOR_TRACE_CLOSURE
```

---

## 1. Remediated Behavior

`internal/pipe/run.go` now treats protected BLK-req regular files under these prefixes as metadata-only entries during physical worktree snapshots:

```text
docs/active/
docs/requirements/
docs/use_cases/
```

For those paths, the physical worktree snapshot records only filesystem metadata needed for cleanup/change detection (`mode`, kind, size, modification timestamp) and does not call `os.ReadFile` on the protected body. Non-protected regular files retain byte-for-byte snapshot comparison.

`internal/pipe/run_test.go` adds `TestSnapshotPhysicalWorktreeDoesNotReadProtectedBlkReqBody`, which chmods a protected body to unreadable and proves the snapshot succeeds without reading that body.

---

## 2. Authority Boundary

BLK-SYSTEM-106 does not authorize BLK-pipe runtime dispatch against Kuronode or any target repository, BLK-test runtime, BEO publication, RTM generation, RTM drift rejection, protected BLK-req body reads, production/reusable `blk-link`, public ledger mutation, signer/storage/rollback authority, live Codex execution, or target/source/Git mutation outside the BLK-System sprint commit.

This sprint is implementation hardening only. Existing allowlist denials for protected BLK-req paths remain active and unchanged.
