L2_ID: L2-K2-025
BEB_ID: BEB-K2-025
BEO_ID: BEO-K2-025
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
TARGET_HASH: ee1a0071adfeef973e658dc0149914c459ff3dab

Objective: remediate only the hostile-review blockers in K2-025 after route commit ee1a0071adfeef973e658dc0149914c459ff3dab. Keep edits within the allowed files. Do not broaden product scope.

Critical route-control instruction: Do not run `git add`, `git commit`, `git reset`, `git checkout`, `git clean`, or any command that writes Git metadata. BLK-pipe owns staging, commit creation, cleanup, and route-summary evidence after you exit. After tests pass, write a concise final message with RED/GREEN/verification evidence and stop. Treat sandbox inability to write `.git` as expected; do not retry Git metadata writes.

Required RED tests first:
1. Import `createAgentAWriteAdmissionRecord` plus the existing K2-021/K2-023 helper producers needed to build a real admitted K2-024 record; assert `createGovernedCanonicalWriteTransaction(realK2024Admission, packageRecord(), transactionRequest())` commits.
2. Assert the old hand-rolled minimal admitted object blocks with a spoof/malformed reason.
3. Assert every authority/raw/provider/publication/RTM/blk-link alias listed in the BEB blocks at top level and nested under admission/package/request evidence.
4. Assert package/request multi-file path aliases listed in the BEB block, including `files` arrays and `targetPaths`/`packagePaths`/`targetPackagePathList`/`adjacentFilePath`/absolute/traversal strings.
5. Assert getter/proxy/callable/symbol/revoked proxy hostile input behavior for admission and package as well as request.

Implementation constraints:
- Prefer a small deny-alias classifier: normalize separators/case, then deny exact aliases and dangerous substrings for write/commit/canonical mutation/runtime dispatch/publication/RTM/blk-link/provider/raw prompt/source/body/path/credential/parser/import/export/save/undo/BEO publication.
- Permit real K2-024 evidence fields (`promotionReadinessId`, `candidateId`, `agentCandidateId`, `admissionOrder`, `governedFlowKind`, `requestEvidenceHash`, `invocationEvidenceHash`, `provenanceStatus`, `nonCanonicalStatus`) only with valid admitted-state semantics and canonical hash validation.
- Require admitted admission semantics: `admissionState=admitted`, `writeIntentStatus=intent-recorded`, `reviewStatus=pending-review`, empty `admissionBlockedReasons`, `governedFlowKind=agent-a-governed-canonical-write`, valid request/invocation evidence hashes, valid candidate content fingerprint, and false/true authority flags matching K2-024 noncanonical status. A minimal object lacking real evidence hashes must not commit.
- For package/request path fields, any recognized path/multi-file key must be exactly the controlled fixture path or a singleton list containing exactly that path only when explicitly supported; extra/absolute/traversal/sibling paths fail closed.
- Preserve no real file IO/network/provider/parser/runtime/RTM/blk-link/BEO publication behavior.

Verification commands to run before final message:
- `node tests/governed-write-transaction.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`
- `git diff --check -- src/shared/governed-write-transaction.mjs tests/governed-write-transaction.test.mjs scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts package.json`


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
