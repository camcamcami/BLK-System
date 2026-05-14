# BLK-113 — Validation Trust Boundary and Capability Policy

**Status:** Active BLK-pipe validation trust-boundary hardening record — not runtime dispatch authority
**Date:** 2026-05-14
**Sprint:** BLK-SYSTEM-113
**Source finding:** HR-006 residual from `docs/reviews/BLK-SYSTEM_post-103_all-codebase-hostile-review-and-completion-roadmap.md`

## Purpose

BLK-SYSTEM-113 hardens the validation trust boundary after BLK-SYSTEM-112 structured profile argv. Repository-owned validation profiles now carry explicit local/fixture capability labels, and autonomous payload boundaries cannot use legacy shell `validation_commands`.

## Required Markers

```text
BLK_SYSTEM_113_VALIDATION_TRUST_BOUNDARY_CAPABILITY_POLICY
AUTONOMOUS_PAYLOADS_REQUIRE_REPOSITORY_OWNED_VALIDATION_PROFILES
LEGACY_VALIDATION_COMMANDS_TRUSTED_LOCAL_ONLY
VALIDATION_PROFILE_CAPABILITIES_REPORTED_FOR_HOSTILE_AUDIT
VALIDATION_TRUST_BOUNDARY_REPORTED_FOR_OPERATOR_DIAGNOSTICS
```

## Enforced Behavior

1. Payloads may declare `payload_trust_boundary: "autonomous"`.
2. Autonomous payloads with `validation_commands` fail closed before engine side effects.
3. Autonomous payloads with repository-owned `validation_profiles` remain accepted.
4. Profile specs expose explicit capability labels such as `local-go-test`, `local-go-vet`, `local-python-unittest`, `local-doctrine-gate`, and `fixture-only-python-unittest`.
5. Reports expose `validation_trust_boundary` and `validation_profile_capabilities`.

## Explicit Non-Authority

This record does not authorize BLK-pipe runtime dispatch against Kuronode or any target repository, BLK-test runtime, production MCP, BEO publication, RTM generation, RTM drift rejection, active-vault hash comparison, protected BLK-req body reads, package/network/model/browser/cyber tooling, signer/storage/ledger/rollback behavior, production sandbox/isolation claims, or source/Git mutation outside this BLK-System sprint commit.

## Finding Disposition

- HR-006 autonomous/less-trusted validation-shell boundary: CLOSED for declared `payload_trust_boundary: "autonomous"`.
- Legacy shell `validation_commands`: retained only as `trusted-local-legacy` compatibility and reported as such.
