# K2-023 Hostile Review Remediation 002 Blockers

Independent post-remediation hostile code review verdict: BLOCKED.

## Blocker — `__proto__` readiness evidence is omitted from evidence hash

A readiness object with an own enumerable `__proto__` field can remain `reviewable` while producing the same `readinessEvidenceHash` as the clean readiness object. The canonical snapshotter uses normal object containers plus assignment, so `snapshot["__proto__"] = ...` mutates prototype behavior rather than recording an own data property in canonical JSON.

Required remediation:
- Add RED tests proving own enumerable `__proto__` in readiness evidence changes the evidence hash or fails closed, and does not leave a reviewable envelope with the same hash.
- Add tests for array/object properties where `__proto__`, `constructor`, or `prototype` cannot be silently omitted from canonical evidence.
- Patch canonical snapshot containers to use null-prototype objects plus `Object.defineProperty`, or entry tuples, so special property names are represented as data and deterministic hashing remains safe.
- Preserve the previous remediation: array getters must remain inert, exact `blk-link` must remain blocked.

## Scope boundary

Modify only:
- `src/shared/agent-a-promotion-request.mjs`
- `tests/agent-a-promotion-request.test.mjs`

No provider/network/filesystem/project IO, parser/projection/renderer/IPC, canonical mutation, import/adoption/promotion execution, save/export/session persistence, approval capture, RTM, `blk-link`, or BEO publication behavior is authorized.
