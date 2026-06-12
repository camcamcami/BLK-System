# K2-023 Hostile Review Remediation 001 Blockers

Independent hostile code review verdict: BLOCKED.

## Blocker 1 — readiness array getters execute during evidence hashing

`createAgentAPromotionRequestEnvelope` always computes `readinessEvidenceHash` from the submitted readiness value. The canonical snapshotter uses `Array.prototype.map` for arrays, which can invoke caller-controlled array/index/inherited getters and throw before returning a blocked envelope. Malformed/hostile readiness evidence must fail closed, not execute getter code or throw.

Required remediation:
- Add RED tests for top-level readiness array getters and nested readiness array getters.
- Change canonical snapshotting so arrays are traversed by descriptors/own keys without `.map` or ordinary property access.
- Ensure hostile readiness still returns a frozen blocked request envelope with fixed reasons and no raw leakage.

## Blocker 2 — exact `blk-link` denied field is not blocked

The deny-list constructs `blkLink` and `blklink`, but not the explicit hyphenated `blk-link` token. A candidate with nested `{ "blk-link": "caller supplied denied field" }` can remain reviewable.

Required remediation:
- Add RED tests for exact nested `blk-link` denied field names with non-marker values.
- Add explicit detection for hyphenated `blk-link` without weakening existing `blkLink`/`blklink` checks.
- Preserve all existing K2-023 public vocabularies and authority-denial behavior.

## Scope boundary

Modify only:
- `src/shared/agent-a-promotion-request.mjs`
- `tests/agent-a-promotion-request.test.mjs`

No provider/network/filesystem/project IO, parser/projection/renderer/IPC, canonical mutation, import/adoption/promotion execution, save/export/session persistence, approval capture, RTM, `blk-link`, or BEO publication behavior is authorized.
