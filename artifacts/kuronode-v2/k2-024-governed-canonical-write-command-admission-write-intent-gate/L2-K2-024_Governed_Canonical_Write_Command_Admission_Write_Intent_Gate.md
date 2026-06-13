L2_ID: L2-K2-024
BEB_ID: BEB-K2-024
BEO_ID: BEO-K2-024
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: 56fc8cd3e16aa9d73150104e35d1476f6851335d

# L2-K2-024 — Governed Canonical Write-Command Admission / Write-Intent Gate

## Mission

Implement exactly the K2-024 write-command admission/write-intent gate described by `BEB-K2-024`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is that an existing K2-023 reviewable Agent A promotion-request/preflight envelope plus explicit non-mutating governed-write invocation evidence can produce a deterministic admission/write-intent status record.

Do not implement approval capture, actual promotion/import/adoption, canonical source mutation, source repair, project/source writes, save/export/session persistence, undo/recovery execution, provider calls, Agent A job lifecycle, parser/projection/renderer/preload/IPC expansion, RTM, production `blk-link`, or BEO publication.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`

You may create only:

- `src/shared/agent-a-write-admission.mjs`
- `tests/agent-a-write-admission.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, traceability/roadmap/BEO docs, save/export/session code, Agent A candidate-generation/readiness/request modules, or canonical mutation/write code during route execution.

## Required TDD sequence

1. Add `tests/agent-a-write-admission.test.mjs` first.
2. Run `node tests/agent-a-write-admission.test.mjs` and record RED because the current target lacks the K2-024 write-admission module/API.
3. Implement only the minimum shared pure-data module plus package/foundation/validator metadata needed for GREEN.
4. Rerun `node tests/agent-a-write-admission.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- Create a new shared module `src/shared/agent-a-write-admission.mjs`.
- The module must be pure data: no `fs`, `path`, `child_process`, `fetch`, `http`, `https`, `net`, provider SDK/client imports, Electron imports, parser/runtime imports, renderer imports, browser storage, package-manager/dependency behavior, project file IO, or process spawning.
- Consume K2-023 request/preflight envelopes and explicit invocation evidence as pure data. Do not call providers, do not create or retain raw generated content, do not infer canonical authority, and do not mutate submitted objects.
- Public admission records must use exact keys and fixed vocabularies. Suggested fields: `writeIntentId`, `promotionRequestId`, `promotionReadinessId`, `candidateId`, `agentCandidateId`, `admissionOrder`, `admissionState`, `writeIntentStatus`, `reviewStatus`, `admissionBlockedReasons`, `governedFlowKind`, `requestEvidenceHash`, `invocationEvidenceHash`, `candidateContentFingerprint`, `provenanceStatus`, `nonCanonicalStatus`, `authorityFlags`, and mirrored denied authority booleans.
- Recompute `requestEvidenceHash` and `invocationEvidenceHash` from submitted evidence with deterministic canonical JSON and SHA-256. Do not accept caller-supplied hashes as evidence.
- Admitted status must require K2-023 reviewable request/preflight status, matching request/candidate fields, canonical candidate provenance `contentFingerprint`, reviewable non-secret provenance, non-canonical authority posture, and explicit non-mutating governed-write invocation evidence.
- Treat raw marker values, nested denied fields, non-plain objects, non-finite numbers, hash aliases, and authority/writable/canonical/approval claims as hostile. Do not serialize them into public output. Do not call getters/callbacks/functions supplied by input.
- Deep-freeze public records, nested blocked reasons, authority flags, registries/lists, and any exported catalog arrays. Registry methods may be frozen functions.
- Update `package.json` test script to include `node tests/agent-a-write-admission.test.mjs` after `agent-a-promotion-request`.
- Update `scripts/validate-foundation.mjs` so K2-024 files are required, governed marker coverage is enforced, authority field scans cover the new module, and the package test script remains exact.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-024 metadata only while preserving K2-001..K2-023 evidence.

## Required tests

Cover at least:

- current target RED for missing K2-024 module/API;
- deterministic admitted write-intent record for an accepted K2-023 request plus explicit non-mutating governed-write invocation evidence;
- blocked records for missing request, missing invocation evidence, blocked K2-023 request, unknown flow kind, wrong request states/statuses, permissive authority flags, missing/non-canonical authority flags, malformed `contentFingerprint`, and contradictory write/save/commit/canonical/import/promotion/approval metadata;
- exact public key set and exact allowed vocabularies;
- exact fixed blocked reason vocabulary and semantic consistency between admission/write-intent/review status fields and reasons;
- recomputed request/invocation evidence hashes change when submitted evidence changes;
- raw prompt/source/body/sysml/content/path/filename/provider request/response/payload/credential/token/apiKey/stack/diagnostic/parser/save/export/undo/RTM/blk-link/BEO-publication markers absent from public output;
- nested denied fields and contradictory approved/trusted/writable/committed/importable/savable/canonical metadata fail closed or are sanitized to non-authority;
- spoofed caller write-intent ids/orders/states/statuses/hashes do not override deterministic ids/orders/state policy;
- hostile proxies/getters/callables/symbols/revoked proxies do not invoke caller code or leak fields;
- non-finite numbers and hash-alias data do not produce admitted records;
- output and nested objects/lists are deeply frozen and expose no mutable function/prototype/DOM handles;
- static source scan for denied live behavior (`fs`, `path`, `child_process`, `fetch`, provider SDK/client calls, network URL calls, credential/env reads, filesystem IO, parser process/runtime execution, renderer/IPC imports, layout engines, import/export/save/canonical mutation, telemetry, RTM, `blk-link`, BEO publication);
- package/foundation/validator metadata includes the focused K2-024 test and files.

## Verification commands

```bash
node tests/agent-a-write-admission.test.mjs
node tests/agent-a-promotion-request.test.mjs
node tests/agent-a-promotion-readiness.test.mjs
node tests/agent-a-candidate-generation.test.mjs
node tests/candidate-staging.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/agent-a-write-admission.mjs tests/agent-a-write-admission.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution times out or fails due to environment/tooling, preserve the exact approved allowlist/target hash and report whether clean-worktree retargeting or supervised fallback was used.

## Adversarial readiness card

Slice: K2-024 — Governed canonical write-command admission / write-intent gate.
Milestone: F — Governed promotion path, admission/write-intent side only.
Compartment: Promotion / canonical mutation boundary before canonical mutation exists.
One authority boundary: a reviewable K2-023 promotion request plus explicit non-mutating governed-write invocation evidence may produce a write-intent/admission record, but no candidate may cross into canonical source and no write/save/undo/promotion behavior is implemented.
Direct requirements: `REQ-KN-072`, `REQ-KN-128`, `REQ-KN-134`, `REQ-KN-135`.
Supporting-only requirements: `REQ-KN-073`, `REQ-KN-075`, `REQ-KN-076`, `REQ-KN-085`.
Explicitly denied capabilities: approval capture, live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source/body retention, Agent A job lifecycle/orchestration, project/source writes, source repair/adoption/import/promotion execution, canonical mutation/write/save/export/session persistence, undo/recovery execution, parser process/runtime expansion, projection/layout trust, renderer/IPC/preload expansion, support export, telemetry, dependency changes, RTM generation, production `blk-link`, BEO publication/signing/storage/ledger, run-ID reservation/consumption, and reusable dispatch authority.
Malformed input behavior: missing/malformed/hostile request or invocation evidence must produce a blocked fail-closed admission with fixed reason vocabulary, not throw, execute callbacks, read files, call providers, mutate source, or serialize hostile raw fields.
Contradictory input behavior: if request/invocation evidence says it is approved/writable/canonical/savable/committed while also missing provenance, carrying raw/leaky fields, containing authority metadata, contradicting K2-023 non-canonical flags, or requesting canonical mutation execution, K2-024 must choose the stricter blocked admission.
Spoofing seams to forbid: caller write intent ids/orders/states/statuses/hashes, caller request hashes, authority flags, AI/provider approval metadata, provider readiness claims, trusted flags, source path/body fields, prompt/provider/credential/token fields, function/callback/DOM handles, mutable prototypes, parser/projection handles, import/export/save/session/canonical claims, undo claims, BEO/RTM/`blk-link` claims.
Raw/leaky fields to forbid: `raw`, `content`, `body`, `sysml`, `sourceText`, `modelText`, `path`, `filename`, `dirname`, `prompt`, `providerPayload`, `providerRequest`, `providerResponse`, `credential`, `token`, `apiKey`, `errorBody`, `stack`, `diagnostic`, `parserInput`, `sourceCoordinates`, `layoutCoordinates`, `canvas`, `svg`, `save`, `export`, `undo`, `commit`, `rtm`, `blkLink`, `blk-link`, `beoPublication`, except fixed denied-authority labels that tests constrain.
Required hostile probes: focused K2-024 test must include admitted path, blocked request path, invocation mismatch/missing, malformed fingerprint, spoofed ids/hashes/states, raw-marker non-leakage, nested denied-field rejection, proxies/getters/callables/symbols/revoked proxies, non-finite hash-alias attempts, deep freeze checks, exact key/vocabulary checks, semantic-consistency checks, and static source scans for denied live behavior.
Closeout docs/mirrors to update after successful implementation: canonical `BEO-K2-024`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, `docs/outcomes/K2-024_sprint-closeout.md`, and view-only Obsidian BEB/L2/BEO/BDOC/roadmap/traceability/outcome mirrors after final commit.

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
