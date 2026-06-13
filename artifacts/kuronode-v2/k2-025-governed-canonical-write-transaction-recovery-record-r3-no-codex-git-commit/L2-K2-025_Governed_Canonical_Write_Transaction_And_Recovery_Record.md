L2_ID: L2-K2-025
BEB_ID: BEB-K2-025
BEO_ID: BEO-K2-025
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
TARGET_HASH: fef4065910cd6baba30e115443ba5972dd1d50cc

Implement K2-025 with strict TDD, but keep the route concise enough to finish.

Allowed paths only:
- Modify: package.json; scripts/validate-foundation.mjs; tests/foundation.test.mjs; src/shared/foundation.ts
- Create: src/shared/governed-write-transaction.mjs; tests/governed-write-transaction.test.mjs

TDD sequence:
1. Create tests/governed-write-transaction.test.mjs importing ../src/shared/governed-write-transaction.mjs and asserting the missing API. Run `node tests/governed-write-transaction.test.mjs` and capture RED.
2. Implement src/shared/governed-write-transaction.mjs as a pure-data module, then run the focused test GREEN.
3. Update package.json test script to append the new test, and update scripts/validate-foundation.mjs, tests/foundation.test.mjs, and src/shared/foundation.ts with K2-025 metadata.
4. Run: `node tests/governed-write-transaction.test.mjs`; `node scripts/validate-foundation.mjs`; `npm test`; `npm run build`; `npm run typecheck`; `git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/governed-write-transaction.mjs tests/governed-write-transaction.test.mjs`.

Required API:
- Export `GOVERNED_WRITE_TRANSACTION_CAPABILITIES`, `GOVERNED_WRITE_TRANSACTION_ALLOWED_VOCABULARY`, `CONTROLLED_FIXTURE_PACKAGE_PATH`, `createGovernedCanonicalWriteTransaction(admissionRecord, packageRecord, transactionRequest)`, and `createGovernedWriteTransactionRegistry()`.
- Public record exact keys: transactionId, writeIntentId, promotionRequestId, targetPackagePath, targetVersionHash, candidateContentFingerprint, transactionState, commitStatus, recoveryStatus, failureReasons, beforeVersionHash, afterVersionHash, transactionEvidenceHash, recoveryRecord, readinessRefreshRequired, authorityFlags.
- Committed state vocabulary: transactionState `transaction-committed`, commitStatus `fixture-package-record-updated`, recoveryStatus `recovery-recorded`, readinessRefreshRequired true.
- Blocked vocabulary: transactionState `transaction-blocked`, commitStatus `commit-failed`, recoveryStatus `recovery-noop-recorded`, afterVersionHash equals beforeVersionHash or empty when unavailable.
- Controlled fixture path: exactly `fixtures/k2-025/single-file.sysml`. No absolute path, traversal, aliases, or multi-file paths.
- Hash format: `sha256:<64 lowercase hex>`. Recompute transaction/recovery evidence hashes from sanitized fields with deterministic canonical JSON. Do not accept caller-supplied transaction/recovery hashes, ids, statuses, or records.

Commit criteria for createGovernedCanonicalWriteTransaction:
- admission is a plain finite object with K2-024 admitted write-intent status; use tolerant field names from existing K2-024 outputs where practical (`writeIntentId`, `promotionRequestId`, `admissionStatus`, `writeCommandAdmissionStatus`, `authorityFlags`, etc.).
- packageRecord is plain and single-file with targetPackagePath exactly CONTROLLED_FIXTURE_PACKAGE_PATH, currentVersionHash sha256, packageKind/targetKind indicating controlled fixture single-file.
- transactionRequest is plain, confirms fixture-only operator review, repeats targetPackagePath and expectedCurrentVersionHash, supplies candidateContentFingerprint sha256 and candidateReplacementHash sha256, and has false adjacent authority flags.
- any malformed/hostile/contradictory evidence returns a blocked record with fixed failure reason vocabulary; do not throw for caller input problems.

Tests must cover: committed happy path, blocked/non-admitted admission, stale hash, path traversal/absolute/multi-file, malformed hashes, spoofed ids/states/hashes/recovery ignored, raw-marker non-leakage, nested denied authority fields, getters/proxies/callables/symbols/revoked proxies not invoked/leaked, deep-freeze outputs, exact key/vocabulary sets, registry immutability, and static scan denying fs/path/child_process/fetch/http/https/net/provider/electron/parser/renderer/save/export/session/RTM/blk-link/BEO publication/live IO behavior.

Keep implementation minimal and deterministic. Do not modify existing Agent A modules.

## Readiness profile probe card

These probes are required pre-dispatch checklist evidence only. They do not authorize source/Git mutation, parser execution, provider/runtime dispatch, BEO publication, RTM generation, or reusable BLK-pipe/Codex authority beyond the exact approved drop.

### kuronode-caller-object-control-plane-v1

- [ ] KCP-001 direct accepted ready input
- [ ] KCP-002 wrapper accepted ready input
- [ ] KCP-003 top-level denied raw/authority/source/provider/parser/import/export/mutation fail closed
- [ ] KCP-004 nested denied raw/authority/source/provider/parser/import/export/mutation fail closed
- [ ] KCP-005 raw marker values fail closed and do not serialize back out
- [ ] KCP-006 duplicate filters or entries beyond cap fail closed
- [ ] KCP-007 proxy/getter/callable/symbol inputs fail closed without invoking caller code
- [ ] KCP-008 public capability/result objects deeply frozen and public getters have no mutable prototype
- [ ] KCP-009 helper vocabulary confined to owning module/tests
- [ ] KCP-010 downstream compatibility probe for the paired payload/capability surface
- [ ] KCP-011 deep hostile object graph hits a bounded circuit breaker without throwing
- [ ] KCP-012 caller authority/status/trust laundering fields force fail-closed false readiness

## Critical route-control instruction

Do not run `git add`, `git commit`, `git reset`, `git checkout`, `git clean`, or any command that writes Git metadata. BLK-pipe owns staging, commit creation, cleanup, and route-summary evidence after you exit. After the requested tests pass, write a concise final message with RED/GREEN/verification evidence and stop. Treat any sandbox inability to write `.git` as expected and do not retry it.
