# BLK-SYSTEM-113 — Validation Trust Boundary and Capability Policy Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Source finding:** HR-006 residual after BLK-SYSTEM-112
**Track:** Milestone 2 — BLK-pipe production hardening

## Purpose

Harden validation trust boundaries after structured profile argv exists. Repository-owned profiles need explicit capability labels; legacy shell `validation_commands` must remain trusted-local compatibility and must fail closed for payloads that declare an autonomous/less-trusted boundary.

## Scope

- Payload trust-boundary field validation in Go.
- Profile capability metadata in `internal/validationprofiles`.
- Report-visible validation trust evidence.
- Python adapter result parsing for new trust/capability evidence only.
- BLK-113 doctrine record, hostile review, and closeout.

## RED Tests First

1. Autonomous payloads using legacy `validation_commands` must fail before engine side effects.
2. Autonomous payloads using repository-owned profiles must remain valid.
3. Profile specs must carry allowed capability labels and reject dangerous capability strings.
4. Reports must expose validation trust boundary and profile capabilities.

## Explicit Non-Authority

This sprint does not authorize runtime dispatch, target-repo mutation, BLK-test runtime, BEO publication, RTM generation, drift rejection, protected-body reads, package/network/model/browser/cyber tooling, signer/storage/ledger behavior, or production isolation claims.
