# BLK-SYSTEM-118 Hostile Review — Staging Intake Draft Writer

**Status:** PASS
**Date:** 2026-05-14
**Reviewed scope:** `python/lint_artifacts.py`, `python/test_blk_req_legislative_gateway.py`, `docs/BLK-118_staging-intake-draft-writer.md`

## Required Markers

```text
BLK_SYSTEM_118_STAGING_DRAFT_WRITER
DRAFT_WRITER_OUTPUTS_ONLY_TO_STAGING_DIRECTORIES
NEW_DRAFT_METADATA_ID_TBD_VERSION_HASH_PENDING
INVALID_DRAFTS_RETURN_DIAGNOSTICS_WITHOUT_WRITING
MAX_SELF_REMEDIATION_ATTEMPTS_THREE_DOCUMENTED
NO_HITL_APPROVAL_CAPTURE_OR_ACTIVE_PROMOTION_BY_118
```

## Hostile Checks

| Probe | Result |
| --- | --- |
| Requirement writer emits outside `docs/requirements/staging/` | BLOCKED by exact path assertion in writer tests. |
| Use-case writer emits outside `docs/use_cases/staging/` | BLOCKED by exact path assertion in writer tests. |
| New draft metadata invents permanent ID or future hash | BLOCKED by strict metadata assertions and linter. |
| Invalid requirement body creates a file anyway | BLOCKED by `test_writer_rejects_invalid_draft_without_creating_file`. |
| Path traversal through filename slug | BLOCKED by slug validation and `ValueError`. |
| Existing staging draft silently overwritten | BLOCKED by `STAGING_DRAFT_EXISTS`. |
| Active-vault path write attempted | BLOCKED by patched `Path.write_text` guard in tests. |
| Staging filename is a symlink to an active-vault target | BLOCKED after delegated hostile re-review by `_staging_symlink_diagnostic()` and `test_writer_rejects_symlinked_staging_filename_before_active_target_write`. |
| Writer launders HITL approval capture, baseline promotion, or retrieval | NOT PRESENT; return package keeps those side-effect flags false. |

## Post-Review Remediation

A delegated final hostile review found the original active-write probe did not cover symlinked staging filenames. The writer now rejects existing symlink components before write and rechecks after creating the parent directory. This preserves `DRAFT_WRITER_OUTPUTS_ONLY_TO_STAGING_DIRECTORIES` against symlink-to-active-vault bypasses.

## Review Result

PASS for BLK-SYSTEM-118 scope after symlink remediation. The writer is staging-only, linter-gated, and diagnostic on rejection. It does not promote, approve, revise, retrieve, or assign canonical hashes.
