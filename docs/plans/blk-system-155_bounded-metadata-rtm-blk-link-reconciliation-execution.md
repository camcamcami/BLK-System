# BLK-SYSTEM-155 — Bounded Metadata RTM / blk-link Reconciliation Execution

## Goal

Consume BLK-SYSTEM-154 request evidence and the operator's exact instruction to execute BLK-SYSTEM-154 through BLK-SYSTEM-156, then emit one bounded metadata-only reconciliation execution record.

## Scope

- Capture exact approval only for this bounded metadata reconciliation package.
- Assign and consume one run ID in returned evidence.
- Reconcile only metadata IDs and hashes already present in upstream evidence.
- Preserve no protected-body reads, no drift rejection, no coverage truth, no reusable production `blk-link`, no signer/storage/ledger reuse, no BLK-pipe/BLK-test/Codex runtime, and no target/source/Git mutation beyond this repo patch.

## Validation

- RED test first: missing module fails.
- GREEN tests verify request-window hash binding, upstream rehash rejection, exact approval text, one run ID, record hash binding, false side-effect flags, and laundering/protected-body rejection.

## Closeout

One outcome only: `docs/outcomes/BLK-SYSTEM-155_sprint-closeout.md`.
