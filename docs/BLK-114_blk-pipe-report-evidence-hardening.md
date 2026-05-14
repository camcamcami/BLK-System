# BLK-114 — BLK-pipe Report/Evidence Hardening

**Status:** Active BLK-pipe evidence-shape hardening record — not runtime dispatch authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-114
**Track:** Milestone 2 — BLK-pipe production hardening bridge

## Purpose

BLK-SYSTEM-114 hardens local `blk-pipe` report shape so hostile review and future automation can inspect execution-boundary evidence without inferring it from prose. Reports now preserve selected caps, exact allowlists, target identity, validation trust evidence, failure classification, denial route, and cleanup status.

## Required Markers

```text
BLK_SYSTEM_114_REPORT_EVIDENCE_HARDENING
REPORT_PRESERVES_SELECTED_TIMEOUT_AND_OUTPUT_CAPS
REPORT_PRESERVES_EXACT_FILE_ALLOWLIST_EVIDENCE
REPORT_PRESERVES_VALIDATION_TRUST_AND_PROFILE_EVIDENCE
REPORT_EXPOSES_FAILURE_CLASS_DENIAL_ROUTE_AND_CLEANUP_STATUS
REPORT_EVIDENCE_IS_DIAGNOSTIC_NOT_AUTHORITY
```

## Report Evidence Added / Pinned

- `timeout_seconds`
- `max_output_bytes`
- `allowed_modified_files`
- `allowed_new_files`
- `target_hash`
- `payload_trust_boundary`
- `validation_trust_boundary`
- `validation_profile_capabilities`
- `failure_class`
- `denial_route`
- `cleanup_status`

## Behavior

1. Successful execute reports include selected caps and exact file allowlists.
2. Invalid payload reports include `failure_class: invalid_payload`, `denial_route: payload_validation`, and `cleanup_status: not_started`.
3. Repository-profile validation reports include structured argv, trust-boundary evidence, and capability labels.
4. Python adapter parsing preserves the new fields and `raw_report` for operator diagnostics.

## Explicit Non-Authority

These fields are diagnostics only. BLK-SYSTEM-114 does not authorize BLK-pipe runtime dispatch against Kuronode or any target repository, BLK-test runtime, production MCP, BEO publication, RTM generation, RTM drift rejection, active-vault hash comparison, protected BLK-req body reads, package/network/model/browser/cyber tooling, signer/storage/ledger/rollback behavior, production sandbox/isolation claims, or source/Git mutation outside this BLK-System sprint commit.

## Functional Module Warning

`BLK-test` is a BLK-System functional module/oracle surface, not this repository's internal test suite. The Go and Python tests cited for this sprint are BLK-System repository verification, not BLK-test runtime authority.
