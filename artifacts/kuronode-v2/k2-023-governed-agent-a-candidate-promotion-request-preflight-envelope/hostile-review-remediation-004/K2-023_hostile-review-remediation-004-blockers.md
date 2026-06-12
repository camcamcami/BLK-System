# K2-023 Hostile Review Remediation 004 Blockers

Independent final hostile code review after remediation 003: BLOCKED.

## Blocker 1 — non-plain containers hide denied entries while envelope remains reviewable

Nested containers such as `Map` can contain entries like `blk-link`, raw provider payload markers, or `canonicalMutationAllowed: true`, but descriptor-only scanning and snapshotting ignore Map entries. Candidate/readiness evidence with nested Maps remained `reviewable` and the denied content was not represented in `readinessEvidenceHash`.

Required remediation:
- Add RED tests for candidate and readiness nested `Map` entries containing denied keys/values.
- Restrict accepted caller evidence graph to JSON-like values: primitives with finite numbers, arrays, and plain/null-prototype records.
- Treat `Map`, `Set`, `Date`, `RegExp`, typed arrays, class instances, and other non-plain objects as hostile/malformed and block the envelope.
- Do not attempt to iterate caller Map/Set entries if doing so can invoke caller code; fail closed based on object type/prototype.

## Blocker 2 — non-finite numbers alias in readiness evidence hash

`createCanonicalSnapshot` returned numbers directly, and `JSON.stringify` serializes `NaN`, `Infinity`, and `-Infinity` as `null`. A readiness object with nested `NaN` produced the same `readinessEvidenceHash` as nested `null` while remaining reviewable.

Required remediation:
- Add RED tests proving `NaN`/`Infinity`/`-Infinity` cannot alias `null` in reviewable readiness evidence.
- Prefer fail-closed for non-finite numbers in candidate/readiness nested evidence; alternatively encode them as tagged values, but the envelope must not remain reviewable with a hash alias.
- Preserve deterministic hashes for safe finite-number evidence.

## Regression preservation

The following prior blockers must stay fixed:
- readiness array getters remain inert;
- exact nested `blk-link` remains blocked;
- own enumerable `__proto__` is represented as data, not omitted;
- Proxy `blockedReasons.length` trap remains inert;
- provider-called non-string `contentFingerprint` does not coerce or leak.

## Scope boundary

Modify only:
- `src/shared/agent-a-promotion-request.mjs`
- `tests/agent-a-promotion-request.test.mjs`

No provider/network/filesystem/project IO, parser/projection/renderer/IPC, canonical mutation, import/adoption/promotion execution, save/export/session persistence, approval capture, RTM, `blk-link`, or BEO publication behavior is authorized.
