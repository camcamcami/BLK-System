# BLK-SYSTEM-114 — BLK-pipe Report/Evidence Hardening Plan

**Status:** Planned / executing
**Date:** 2026-05-14
**Track:** Milestone 2 — BLK-pipe production hardening

## Purpose

Harden BLK-pipe report evidence so operator diagnostics and future automation can distinguish target identity, selected runtime caps, exact allowlists, validation evidence, cleanup/destruction evidence, and denial/status routes without inferring authority from prose.

## RED Tests First

1. Report JSON must include stable target/cap/allowlist/route evidence fields.
2. Successful V47 execution reports selected caps and exact allowlists.
3. Invalid payload reports a distinct invalid-payload failure class and payload-validation denial route.
4. Profile reports continue to include trust, capability, command, and argv evidence.

## Explicit Non-Authority

Report evidence is diagnostics only. This sprint does not authorize runtime dispatch, target-repo mutation, BLK-test runtime, BEO publication, RTM generation, drift rejection, protected-body reads, package/network/model/browser/cyber tooling, signer/storage/ledger behavior, or production isolation claims.
