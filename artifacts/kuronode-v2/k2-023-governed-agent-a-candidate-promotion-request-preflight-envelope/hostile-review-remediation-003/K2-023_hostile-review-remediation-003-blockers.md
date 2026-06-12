# K2-023 Hostile Review Remediation 003 Blockers

Independent final hostile code review verdict after remediation 002: BLOCKED.

## Blocker 1 — `readiness.blockedReasons` Proxy array trap executes during validation

`validateReadinessShape` computes readiness shape using `Array.isArray(blockedReasons)` followed by `blockedReasons.length > 0`. A Proxy wrapping an array passes `Array.isArray(proxy)` and then invokes the caller-controlled `get` trap for `length` before later nested safety scanning can mark the object hostile.

Required remediation:
- Add RED tests proving a Proxy array used as `readiness.blockedReasons` does not execute caller traps and returns a frozen blocked envelope.
- Avoid direct property access such as `.length` on caller-owned arrays/objects unless safety/descriptors have already proved the value is non-hostile and descriptor-owned.
- Prefer descriptor-based length/value inspection or fail-closed for Proxy arrays.

## Blocker 2 — provider-called non-string `contentFingerprint` coerces and leaks caller object

When `providerStatus !== "not-called"`, `validateCandidateProvenance` calls `RegExp.test(contentFingerprint)`. If `contentFingerprint` is an object with `toString`, this invokes caller code. If coercion returns a sha-looking string, the function returns the original object as `candidateContentFingerprint`, leaking caller object into the request envelope.

Required remediation:
- Add RED tests proving non-string `contentFingerprint` objects do not execute `toString`/coercion and do not appear in output, including the provider-called branch.
- Require `typeof contentFingerprint === "string"` before regex checks in every branch.
- Keep malformed/non-string fingerprints fail-closed and sanitized as `unavailable`.

## Regression preservation

The following prior blockers must stay fixed:
- readiness array getters remain inert during hashing;
- exact nested `blk-link` remains blocked;
- own enumerable `__proto__` is represented as evidence data and cannot hash-alias clean readiness.

## Scope boundary

Modify only:
- `src/shared/agent-a-promotion-request.mjs`
- `tests/agent-a-promotion-request.test.mjs`

No provider/network/filesystem/project IO, parser/projection/renderer/IPC, canonical mutation, import/adoption/promotion execution, save/export/session persistence, approval capture, RTM, `blk-link`, or BEO publication behavior is authorized.
