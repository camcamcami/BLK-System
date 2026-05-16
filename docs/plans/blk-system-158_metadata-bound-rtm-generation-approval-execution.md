# BLK-SYSTEM-158 — Metadata-Bound RTM Generation Approval + Bounded Execution

## Goal

Consume the BLK-SYSTEM-157 request-only package, capture the operator's exact BLK-SYSTEM-158 approval, assign/consume one run ID inside returned evidence, and emit one bounded metadata-only RTM generation record.

## Scope

- Bind to exact BLK-SYSTEM-157 request package hash.
- Capture only the exact operator approval for BLK-SYSTEM-158 metadata-bound RTM generation.
- Consume one exact run ID in the generated evidence package.
- Emit RTM record metadata only: trace identities and hashes already present upstream.
- Preserve no production `blk-link`, no drift rejection, no coverage truth, no protected-body reads/copy/parse/hash/scan, no active-vault filesystem scan, no signer/storage/ledger reuse, no BLK-pipe/BLK-test/Codex runtime, no target/source/Git mutation, and no production-isolation claim.

## Validation

- RED first: missing module/current-state markers fail.
- GREEN: exact upstream hash binding, exact approval text, run ID, request-window hash binding, RTM record hash binding, closed schema, hostile text/path rejection, and no live tooling/file access.

## Closeout

One outcome only: `docs/outcomes/BLK-SYSTEM-158_sprint-closeout.md`.
