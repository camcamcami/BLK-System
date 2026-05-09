# BLK-SYSTEM-039 — Codex Deterministic Dispatch Envelope Hostile Review

**Status:** PASS after remediation
**Date:** 2026-05-09T14:02:27+10:00
**Sprint:** BLK-SYSTEM-039 — Codex deterministic dispatch envelope

---

## 1. Review Scope

This hostile review examined the BLK-SYSTEM-039 doctrine boundary, dispatch-envelope fixture implementation, and tests:

```text
docs/BLK-041_codex-deterministic-dispatch-envelope-boundary.md
python/blk_codex_dispatch_envelope.py
python/test_blk_codex_dispatch_envelope.py
python/test_active_doctrine_review_gates.py
```

The review objective was to determine whether the sprint accidentally created live Codex execution authority, BLK-pipe dispatch authority, protected-vault access, BEO/RTM authority, telemetry-as-evidence laundering, or production sandbox claims.

---

## 2. Hostile Questions and Findings

### 2.1 Does the helper start subprocesses, call Codex, call Git, create worktrees, call BLK-pipe, or inspect protected vaults?

**Verdict:** PASS.

`python/blk_codex_dispatch_envelope.py` imports only:

```text
__future__.annotations
datetime.datetime
pathlib.PurePosixPath
typing.Any
blk_codex_invocation_profile.validate_codex_deterministic_invocation_profile
```

AST inspection found no forbidden imports or live-surface calls for subprocess, shell, socket, requests, urllib, http, ftplib, `system`, `popen`, `run`, `Popen`, `call`, `check_call`, `check_output`, `exec`, or `eval`.

### 2.2 Can missing, stale, expired, or replayed approval provenance pass?

**Verdict:** PASS.

The fixture requires all approval provenance fields, including approval ID, source system, operator identity, message/event ID, timestamp, expiry, exact approved scope, and explicit excluded authorities. Tests reject missing fields, incomplete explicit exclusions, expired approval, replayed approval IDs, replayed run IDs, and missing replay-state inputs.

### 2.3 Can broad pathspecs, protected paths, `.git` paths, parent traversal, or empty allowlists pass?

**Verdict:** PASS.

Tests reject broad pathspecs, globs, magic pathspecs, parent traversal, absolute paths, `.git`, protected BLK-req paths under `docs/active`, `docs/requirements`, and `docs/use_cases`, shell-like separators, and empty modified-file boundaries.

### 2.4 Can validation gates become free-form shell or package-manager/network/model/cyber/browser execution?

**Verdict:** PASS.

The implementation accepts only repository-owned allowlisted validation profile names. Tests reject free-form shell-like profiles such as `python -m unittest`, `npm install`, `curl https://example.test`, and `codex exec`.

### 2.5 Can telemetry artifacts become canonical mutation, validation, approval, BEO, RTM, or drift evidence?

**Verdict:** PASS.

The envelope records `CODEX_DISPATCH_TELEMETRY_ADVISORY_ONLY`. Telemetry paths must be bounded relative artifact paths under `artifacts/codex/`; escaping, absolute, `.git`, active-vault, non-artifact-root, and overlong paths fail closed.

### 2.6 Does the envelope launder `danger-full-access` or BLK-040 telemetry into production sandbox or execution authority?

**Verdict:** PASS.

The embedded BLK-040 profile is validated rather than trusted blindly. The dispatch envelope keeps all live execution, BLK-pipe dispatch, BLK-test, source mutation, Git mutation, protected body read/copy, active vault scan, BEO publication, RTM generation, drift rejection, network/model/cyber tooling, package-manager, and production sandbox flags false.

---

## 3. Blocker Found During Review

**Blocker:** The original authority-laundering heuristic was too narrow for generic authority-bearing metadata keys.

The Task 2 implementation rejected known authority keys such as `rtm_generation_authority`, but did not reject generic nested authority claims such as:

```text
metadata.runtime_execution_authority = APPROVED
metadata.generic_approval_claim = APPROVED_FOR_LIVE_EXECUTION
```

This was a blocker because a future caller could preserve a technically valid envelope while smuggling authority into unrelated metadata fields.

---

## 4. Remediation

Remediation added regression tests for generic nested authority-laundering attempts:

```text
metadata.runtime_execution_authority = APPROVED
metadata.generic_approval_claim = APPROVED_FOR_LIVE_EXECUTION
```

Remediation then tightened recursive authority scanning by adding:

```text
SUSPICIOUS_AUTHORITY_KEY_TERMS = authority, authorized, authorization, approval, approved, allowed, claim
ALLOWED_AUTHORITY_KEY_EXCEPTIONS = approval_provenance, approval_id, exact_approved_scope, explicit_excluded_authorities, telemetry_authority, sandbox_authority, jsonl_events_authority, final_message_artifact_authority, allowed_modified_files, allowed_new_files
```

The allowlist preserves legitimate fixture fields while failing closed on arbitrary authority-like metadata keys. Additional forbidden strings were added for live-execution approval wording.

---

## 5. Post-Remediation Verification

Focused and full verification passed after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_dispatch_envelope -q
Ran 11 tests in 0.019s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_codex_invocation_profile -q
Ran 12 tests in 0.005s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates -q
Ran 59 tests in 0.004s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 498 tests in 7.021s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 6. Final Verdict

**PASS after remediation.**

BLK-SYSTEM-039 creates a non-executing deterministic dispatch-envelope fixture only. It does not authorize live Codex execution, BLK-pipe dispatch, source mutation, protected-vault access, production BLK-test MCP, authoritative BEO publication, RTM generation, drift rejection, network/model/cyber/browser tooling, package-manager execution, or production sandbox/firewall/host-secret-isolation claims.

No protected BLK-req body reads occurred during the sprint or hostile review.
