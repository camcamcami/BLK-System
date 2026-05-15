# BLK-SYSTEM-157 — Metadata-Bound RTM Generation Decision Request

## Goal

Consume the BLK-SYSTEM-156 post-reconciliation review package and emit a request-only package asking for a future exact operator decision on metadata-bound RTM generation.

## Scope

- Bind to exact BLK-SYSTEM-156 review package and reconciliation evidence hashes.
- Name the future approval decision scope for metadata-bound RTM generation.
- Preserve no approval capture, no run-ID reservation/consumption, no RTM generation, no production `blk-link`, no drift rejection, no coverage truth, no protected-body access, no runtime/tooling, no source/Git mutation, and no signer/storage/ledger reuse.
- Update only active roadmap/current-state surfaces needed to reflect the request-ready state.

## Validation

- RED first: missing request module/current-state markers fail.
- GREEN: exact upstream hash binding, closed schema, exact denied-authority/proof sets, nested laundering/protected-body rejection, request hash binding, no live tooling/file access, lean-doc closeout gate.

## Closeout

One outcome only: `docs/outcomes/BLK-SYSTEM-157_sprint-closeout.md`.
