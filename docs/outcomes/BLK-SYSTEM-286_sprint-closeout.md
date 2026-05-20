# BLK-SYSTEM-286 — Speculative Quarantine Approval Contract Sprint Closeout

**Status:** Complete
**Date:** 2026-05-20
**Commit:** this commit (`feat: add speculative quarantine HITL gate package`)

## 1. Objective

Create the durable timing contract for Discord-first HITL approval, speculative quarantine compute, explicit policy bypass evidence, and promotion-only-after-decision gates.

## 2. Files Changed

- `docs/BLK-123_speculative-quarantine-approval-contract.md`
- `python/blk_speculative_quarantine_approval_286_289.py`
- `python/test_blk_speculative_quarantine_approval_286_289.py`
- Active roadmap/current-state gates updated in BLK-077, BLK-079, and current-state tests.

## 3. Implementation Summary

BLK-SYSTEM-286 added `build_approval_timing_contract_286(...)` and `validate_approval_timing_contract_286(...)`. The contract binds canonical BLK-SYSTEM-283 identity, BLK-SYSTEM-284 relay, and BLK-SYSTEM-285 loop evidence hashes. It names exactly three timing modes: `pre_approval_blocked`, `speculative_quarantine`, and `config_policy_bypass`. It makes Discord component UX primary and keeps long exact-text copy-paste out of the default path.

## 4. Verification

Focused verification completed:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_speculative_quarantine_approval_286_289 -v
Ran 13 tests in 0.250s
OK
```

Full verification completed with `TMPDIR=/var/tmp/blk-system-tests`: `Ran 1485 tests in 19.029s — OK (skipped=35)`. Whitespace verification is recorded in the commit verification output.

## 5. Hostile Review / Risk Check

- Canonical upstream hashes are pinned and revalidated, not accepted as self-reported fields.
- The contract rejects unsupported timing modes such as vague fast paths.
- Fallback approval uses short `Approve` only when bound to request hash, time window, and single-use evidence.
- No live transport, runtime, source mutation, protected-body access, BEO/RTM/`blk-link`, package manager, network, model-service, browser, cyber tooling, or production-isolation claim is introduced.

## 6. Authority Boundary

This sprint creates local contract evidence only. It does not start BLK-pipe, Codex, relay transport, Discord transport, BLK-test MCP, or any target/source/Git mutation. Durable promotion remains blocked until later exact promotion logic validates both the quarantined result hash and target hash.

## 7. Documentation Burden Check

A new BLK doc was intentionally created because BLK-123 is a durable future contract, not a per-sprint status document. Exactly one outcome closeout was produced for BLK-SYSTEM-286 and no per-task outcome docs were created.
