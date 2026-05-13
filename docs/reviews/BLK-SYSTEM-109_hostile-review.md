# BLK-SYSTEM-109 Hostile Review — Protected Exact Root/Directory Hardening

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `internal/contracts/payload.go`, `internal/contracts/payload_test.go`, `internal/pipe/run.go`, `internal/pipe/run_test.go`, `python/blk_protected_path_guards.py`, affected BLK-test runtime helpers/tests, and `docs/BLK-109_protected-exact-root-directory-hardening.md`.

## Required Markers

```text
BLK_SYSTEM_109_PROTECTED_EXACT_ROOT_DIRECTORY_HARDENED
PROTECTED_DOCS_EXACT_ROOTS_REJECTED
GO_ALLOWLIST_REQUIRES_EXACT_FILES_BEFORE_ENGINE
PYTHON_BLK_TEST_SOURCE_SCOPE_REJECTS_PROTECTED_ROOTS
```

## Finding Disposition

- **HR-007:** CLOSED. Exact protected roots are protected, and tracked directories no longer satisfy `allowed_modified_files` preflight by producing descendant `git ls-files` output.
- **HR-008:** CLOSED. Affected Python BLK-test runtime source-scope helpers reject exact protected roots and descendants.

## Hostile Checks

| Probe | Result |
| --- | --- |
| `allowed_modified_files: ["docs/active"]` | BLOCKED as protected path by Go payload validation. |
| `allowed_new_files: ["docs/requirements"]` | BLOCKED as protected path by Go payload validation. |
| `allowed_modified_files: ["docs/use_cases"]` in V47 payload | BLOCKED as protected path by Go payload validation. |
| `allowed_modified_files: ["src"]` where `src/file.txt` is tracked | BLOCKED before engine execution as not an explicit file; external sentinel remains absent. |
| Python source subtree exactly `docs/active` | BLOCKED before runtime helper can proceed. |
| Python source subtree exactly `docs/requirements` | BLOCKED before runtime helper can proceed. |
| Python source subtree exactly `docs/use_cases` | BLOCKED before runtime helper can proceed. |
| Protected-body leakage from shared helper | NOT PRESENT; helper uses `Path.resolve().parts` and path segment classification only. |
| Authority laundering from denial hardening into BLK-test/RTM/BEO authority | NOT PRESENT; docs preserve explicit denials. |

## Review Result

PASS for BLK-SYSTEM-109 scope. The patch closes HR-007/HR-008 without granting new runtime authority or reading protected BLK-req bodies.
