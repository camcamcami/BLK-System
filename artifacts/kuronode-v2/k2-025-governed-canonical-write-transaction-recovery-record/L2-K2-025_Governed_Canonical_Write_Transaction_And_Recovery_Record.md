L2_ID: L2-K2-025
BEB_ID: BEB-K2-025
BEO_ID: BEO-K2-025
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: fef4065910cd6baba30e115443ba5972dd1d50cc

# L2-K2-025 — Governed Canonical Write Transaction and Recovery Record

## Mission

Implement exactly the K2-025 governed canonical write transaction and recovery record described by `BEB-K2-025`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is a shared pure-data transaction seam: an admitted K2-024 write-intent plus one controlled single-file fixture package record can produce a deterministic commit-or-fail transaction result plus recovery evidence.

Do not implement broad filesystem/source writes, source repair/import/adoption/promotion, live provider/API/network behavior, Agent A job lifecycle expansion, parser/runtime expansion, projection/layout expansion, renderer/preload/IPC expansion, general save/export/session persistence, RTM, production blk-link, BEO publication, signer/storage/ledger behavior, or reusable dispatch authority.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`

You may create only:

- `src/shared/governed-write-transaction.mjs`
- `tests/governed-write-transaction.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, traceability/roadmap/BEO docs, save/export/session code, Agent A candidate-generation/readiness/request/admission modules, or general canonical mutation/write code during route execution.

## Required TDD sequence

1. Add `tests/governed-write-transaction.test.mjs` first.
2. Run `node tests/governed-write-transaction.test.mjs` and record RED because the current target lacks the K2-025 governed-write transaction module/API.
3. Implement only the minimum shared pure-data module plus package/foundation/validator metadata needed for GREEN.
4. Rerun `node tests/governed-write-transaction.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- Create a new shared module `src/shared/governed-write-transaction.mjs`.
- The module must be pure data: no `fs`, `path`, `child_process`, `fetch`, `http`, `https`, `net`, provider SDK/client imports, Electron imports, parser/runtime imports, renderer imports, browser storage, package-manager/dependency behavior, project file IO, or process spawning.
- Consume K2-024 admission records, a controlled package record, and transaction request evidence as pure data. Do not call providers, do not create or retain raw generated content, do not infer broad canonical authority, and do not mutate submitted objects.
- Public transaction records must use exact keys and fixed vocabularies. Suggested fields: `transactionId`, `writeIntentId`, `promotionRequestId`, `targetPackagePath`, `targetVersionHash`, `candidateContentFingerprint`, `transactionState`, `commitStatus`, `recoveryStatus`, `failureReasons`, `beforeVersionHash`, `afterVersionHash`, `transactionEvidenceHash`, `recoveryRecord`, `readinessRefreshRequired`, and `authorityFlags`.
- Recompute `transactionEvidenceHash` and any recovery hash from submitted sanitized evidence with deterministic canonical JSON and SHA-256. Do not accept caller-supplied hashes as evidence.
- Committed status must require K2-024 admitted write-intent state, matching request/candidate fields, canonical candidate provenance `contentFingerprint`, a matching package current-version hash, exact controlled fixture path `fixtures/k2-025/single-file.sysml` or an equally narrow module-owned constant, and explicit fixture-only operator review confirmation.
- Treat raw marker values, nested denied fields, non-plain objects, non-finite numbers, hash aliases, path traversal, absolute paths, multi-file targets, and authority/writable/canonical/published/save/export/session claims as hostile. Do not serialize them into public output. Do not call getters/callbacks/functions supplied by input.
- Deep-freeze public records, nested failure reasons, recovery records, authority flags, registries/lists, and any exported catalog arrays. Registry methods may be frozen functions.
- Update `package.json` test script to include `node tests/governed-write-transaction.test.mjs` after `agent-a-write-admission`.
- Update `scripts/validate-foundation.mjs` so K2-025 files are required, governed marker coverage is enforced, authority field scans cover the new module, and the package test script remains exact.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-025 metadata only while preserving K2-001 through K2-024 evidence.

## Required tests

Cover at least:

- current target RED for missing K2-025 module/API;
- deterministic committed transaction record for an admitted K2-024 write-intent plus controlled single-file fixture package and matching request;
- blocked records for missing admission, blocked/non-admitted admission, missing package, missing request, stale target hash, malformed `contentFingerprint`, path traversal, absolute path, multi-file targets, unsupported package kind, permissive authority flags, and contradictory write/save/export/session/published/RTM/blk-link/BEO-publication metadata;
- exact public key set and exact allowed vocabularies;
- exact fixed blocked reason vocabulary and semantic consistency between transaction/commit/recovery status fields and reasons;
- recomputed transaction/recovery evidence hashes change when submitted evidence changes;
- raw prompt/source/body/sysml/content/provider request/response/payload/credential/token/apiKey/stack/diagnostic/parser/save/export/session/RTM/blk-link/BEO-publication markers absent from public output except fixed controlled fixture path and denied-authority labels;
- nested denied fields and contradictory approved/trusted/writable/committed/importable/savable/canonical metadata fail closed or are sanitized to non-authority;
- spoofed caller transaction ids/states/statuses/hashes/recovery records do not override deterministic policy;
- hostile proxies/getters/callables/symbols/revoked proxies do not invoke caller code or leak fields;
- non-finite numbers and hash-alias data do not produce committed records;
- output and nested objects/lists are deeply frozen and expose no mutable function/prototype/DOM handles;
- static source scan for denied live behavior (`fs`, `path`, `child_process`, `fetch`, provider SDK/client calls, network URL calls, credential/env reads, filesystem IO, parser process/runtime execution, renderer/IPC imports, layout engines, import/export/save/session persistence, telemetry, RTM, blk-link, BEO publication);
- package/foundation/validator metadata includes the focused K2-025 test and files.

## Verification commands

```bash
node tests/governed-write-transaction.test.mjs
node tests/agent-a-write-admission.test.mjs
node tests/agent-a-promotion-request.test.mjs
node tests/agent-a-promotion-readiness.test.mjs
node tests/agent-a-candidate-generation.test.mjs
node tests/candidate-staging.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/governed-write-transaction.mjs tests/governed-write-transaction.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution fails due to target mismatch, dirty worktree, timeout, missing route commit, zero engine logs, or absent final-message evidence, stop and report the blocker; retarget to a trusted sterile clean worktree only with a fresh approved manifest. Do not normalize supervised external Codex fallback without explicit one-off operator fallback authorization.

## Adversarial readiness card

Slice: K2-025 — Governed canonical write transaction and recovery record.
Milestone: F — Governed promotion path.
Compartment: Promotion / canonical mutation boundary.
One authority boundary: a K2-024 admitted write-intent plus controlled single-file fixture package record may produce a deterministic commit-or-fail transaction result and recovery record for that fixture path only.
Direct requirements: `REQ-KN-072`, `REQ-KN-073`.
Supporting-only requirements: `REQ-KN-075`, `REQ-KN-076`, `REQ-KN-085`, `REQ-KN-128`, `REQ-KN-134`, `REQ-KN-135`.
Explicitly denied capabilities: broad filesystem/source writes, source repair/adoption/import/promotion execution, multi-file SysML support, live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source/body retention, Agent A job lifecycle/orchestration, general save/export/session persistence, parser process/runtime expansion, projection/layout trust, renderer/IPC/preload expansion, support export, telemetry, dependency changes, RTM generation, production blk-link, BEO publication/signing/storage/ledger, run-ID reservation/consumption, reusable dispatch authority, and future source/Git mutation outside a new exact BEB/L2/BEO route.
Malformed input behavior: missing/malformed/hostile admission, package, or transaction request evidence must produce a blocked fail-closed transaction with fixed reason vocabulary, not throw, execute callbacks, read files, call providers, mutate source, or serialize hostile raw fields.
Contradictory input behavior: if evidence says it is committed/saved/exported/published/canonical across a broad target while also missing recovery data, carrying raw/leaky fields, containing authority metadata, or mismatching target hashes, K2-025 must choose the stricter blocked no-update outcome.
Spoofing seams to forbid: caller transaction IDs/states/statuses/hashes/recovery records, caller admission hashes, authority flags, AI/provider approval metadata, provider readiness claims, trusted flags, source path/body fields, prompt/provider/credential/token fields, function/callback/DOM handles, mutable prototypes, parser/projection handles, import/export/save/session/canonical claims, undo claims outside recovery record evidence, BEO/RTM/blk-link claims.
Raw/leaky fields to forbid: raw, content, body, sysml, sourceText, modelText, prompt, providerPayload, providerRequest, providerResponse, credential, token, apiKey, errorBody, stack, diagnostic, parserInput, sourceCoordinates, layoutCoordinates, canvas, svg, save, export, session, commit metadata claims outside fixed transaction fields, rtm, blkLink, blk-link, beoPublication, except fixed denied-authority labels that tests constrain.
Required hostile probes: focused K2-025 test must include committed path, blocked admission path, stale hash, path traversal/absolute/multi-file block, malformed candidate fingerprint, spoofed ids/hashes/states, raw-marker non-leakage, nested denied-field rejection, proxies/getters/callables/symbols/revoked proxies, non-finite hash-alias attempts, deep freeze checks, exact key/vocabulary checks, semantic-consistency checks, and static source scans for denied live behavior.

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
