# BLK-109 — Protected Exact Root/Directory Hardening

**Status:** Active L1 local hardening boundary — not sprint/runtime authority
**Purpose:** Record BLK-SYSTEM-109 remediation of protected exact-root and directory allowlist/source-scope classification gaps from HR-007 and HR-008.
**Scope:** BLK-System Go `blk-pipe` allowlist classification and Python BLK-test helper source-scope guards only.

## Required Markers

```text
BLK_SYSTEM_109_PROTECTED_EXACT_ROOT_DIRECTORY_HARDENED
PROTECTED_DOCS_EXACT_ROOTS_REJECTED
GO_ALLOWLIST_REQUIRES_EXACT_FILES_BEFORE_ENGINE
PYTHON_BLK_TEST_SOURCE_SCOPE_REJECTS_PROTECTED_ROOTS
```

Persistent doctrine gate marker: BLK-SYSTEM-109 pins protected exact roots and directory allowlist/source-scope entries as pre-engine/pre-runtime denials.

## Authority Boundary

BLK-109 does not authorize target-repo BLK-pipe dispatch, BLK-test runtime execution, BEO publication, RTM generation, RTM drift rejection, protected BLK-req body reads, active-vault hash comparison, production `blk-link`, signer/storage/ledger/rollback behavior, package/network/model/browser/cyber tooling, production isolation claims, or source/Git mutation outside exact BLK-System sprint files.

## Remediation Summary

- `docs/active`, `docs/requirements`, and `docs/use_cases` exact roots are now treated as protected in Go payload validation, the same as descendants.
- Go `blk-pipe` preflight now requires `allowed_modified_files` to name an exact tracked file and rejects existing directories before engine execution.
- Go `blk-pipe` preflight now rejects existing directory entries in `allowed_new_files` before engine execution and checks exact tracked-file equality with `git ls-files -z`.
- Python BLK-test runtime helpers now share a no-read protected-path guard that rejects protected exact roots and descendants by path segments.
- The shared Python guard classifies path names only and does not read, copy, parse, hash, summarize, scan, or mutate protected BLK-req body bytes.

## Finding Disposition

- HR-007: CLOSED for exact protected root classification and tracked directory allowlist preflight.
- HR-008: CLOSED for exact protected source roots in the affected Python BLK-test runtime helpers.

## Residual Boundary

This sprint does not grant general BLK-test production MCP authority or reusable target-repo runtime authority. It only hardens denial paths that future separately approved runtime work must pass through.
