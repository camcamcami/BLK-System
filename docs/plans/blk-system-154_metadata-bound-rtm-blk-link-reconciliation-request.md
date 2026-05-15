# BLK-SYSTEM-154 — Metadata-Bound RTM / blk-link Reconciliation Request

## Goal

Consume the BLK-SYSTEM-153 review-only preflight and emit a request-only package for the exact metadata-bound RTM / `blk-link` reconciliation path.

## Scope

- Bind to exact BLK-SYSTEM-153 preflight hash.
- Name the future reconciliation scope with metadata-only IDs and hashes.
- Preserve no approval capture, no run ID, no RTM generation, no production `blk-link` execution, no drift rejection, no coverage truth, no protected-body access, no source/Git mutation, and no signer/storage/ledger reuse.

## Validation

- RED test first: missing module fails.
- GREEN tests verify exact upstream hash binding, closed schema, exact denied-authority sets, nested laundering rejection, request hash binding, and no live tooling/file access.

## Closeout

One outcome only: `docs/outcomes/BLK-SYSTEM-154_sprint-closeout.md`.
