L2_ID: L2-K2-021
BEB_ID: BEB-K2-021
BEO_ID: BEO-K2-021
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: c939a9667461a045f82902cb1c477b44fae922fd

# L2-K2-021 — Bounded Agent A isolated candidate generation

## Mission

Implement exactly the K2-021 bounded Agent A isolated candidate-generation seam described by `BEB-K2-021`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is that bounded Agent A output evidence can become an isolated candidate/staging record with reviewable non-secret provenance. Do not implement live provider/API/network calls, credentials, Agent A job orchestration, import/adoption/promotion, canonical source mutation, save/export/session persistence, parser/projection/renderer expansion, RTM, `blk-link`, or BEO publication.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/shared/candidate-staging.mjs`

You may create only:

- `src/shared/agent-a-candidate-generation.mjs`
- `tests/agent-a-candidate-generation.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, or traceability/roadmap/BEO docs during route execution.

## Required TDD sequence

1. Add `tests/agent-a-candidate-generation.test.mjs` first.
2. Run `node tests/agent-a-candidate-generation.test.mjs` and record RED because the current target lacks the K2-021 Agent A candidate-generation module/API.
3. Implement only the minimum shared pure-data module, validator/package metadata, foundation metadata, and any narrow candidate-staging helper changes required for GREEN.
4. Rerun `node tests/agent-a-candidate-generation.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- Create a new shared module such as `src/shared/agent-a-candidate-generation.mjs`. It must be pure data: no `fs`, `path`, `child_process`, `fetch`, `http`, `https`, `net`, provider SDK/client imports, Electron imports, parser/runtime imports, renderer imports, browser storage, package-manager/dependency behavior, or process spawning.
- The module should expose narrow functions such as `createAgentACandidateGenerationRecord(input, candidateOrder)` and optionally `createAgentACandidateGenerationRegistry()`.
- Reuse the K2-008 candidate staging authority posture. If you need a tiny helper from `src/shared/candidate-staging.mjs`, keep the change narrow and prove existing candidate-staging tests still pass.
- Public records must use exact keys and fixed vocabularies. Suggested fields: `agentCandidateId`, `candidateId`, `origin`, `state`, `candidateOrder`, `agentAStage`, `candidateKind`, `candidateStatus`, `provenance`, `authorityFlags`, and mirrored denied authority flags. Do not include arbitrary caller keys.
- Candidate provenance must be reviewable but non-secret. It may contain fixed fields such as `source`, `agentRole`, `providerStatus`, `outputClass`, `contentFingerprint`, `boundedEvidence`, and `sanitizedSummary`, but no raw prompt/source/body/provider payload/credential/path data.
- Missing/malformed/contradictory evidence must fail closed to a blocked or separated untrusted candidate descriptor. Do not throw from hostile caller objects unless unavoidable; prefer safe defaults.
- If a caller supplies approved/trusted/promotable/importable/savable/canonical metadata or authority flags, the output must keep candidate promotion, canonical mutation, import/adoption, save/export, AI authority metadata acceptance, raw content retention, and filesystem path retention false.
- Treat raw marker values and nested denied fields as hostile. Do not serialize them into public output. Do not call getters/callbacks/functions supplied by input.
- Deep-freeze public records, nested provenance, authority flags, registries/lists, and any exported catalog arrays.
- Update `package.json` test script to include `node tests/agent-a-candidate-generation.test.mjs` in a stable order near `candidate-staging`.
- Update `scripts/validate-foundation.mjs` so K2-021 files are required, governed marker coverage is enforced, authority field scans cover the new module, and the package test script remains exact.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-021 metadata only while preserving K2-001..K2-020 evidence.

## Required tests

Cover at least:

- current target RED for missing K2-021 module/API;
- deterministic accepted Agent A candidate record for bounded evidence;
- exact public key set and exact allowed vocabularies;
- reuse/preservation of K2-008 authority flags;
- raw prompt/source/body/sysml/content/path/filename/provider request/response/payload/credential/token/apiKey/stack/diagnostic/parser/RTM/blk-link/BEO-publication markers absent from public output;
- nested denied fields and contradictory approved/trusted/promotable/importable/savable/canonical metadata fail closed or are sanitized to non-authority;
- spoofed caller candidate ids/orders/states do not override deterministic ids/orders/state policy;
- hostile proxies/getters/callables/symbols/revoked proxies do not invoke caller code or leak fields;
- output and nested objects/lists are deeply frozen and expose no mutable function/prototype/DOM handles;
- static source scan for denied live behavior (`fetch`, provider SDK/client calls, network URL calls, credential/env reads, filesystem IO, parser process/runtime execution, renderer/IPC imports, layout engines, import/export/save/canonical mutation, telemetry, RTM, `blk-link`, BEO publication);
- package/foundation/validator metadata includes the focused K2-021 test and files.

## Verification commands

```bash
node tests/agent-a-candidate-generation.test.mjs
node tests/candidate-staging.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/candidate-staging.mjs src/shared/agent-a-candidate-generation.mjs tests/agent-a-candidate-generation.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution times out or fails due to environment/tooling, preserve the exact approved allowlist/target hash and report whether clean-worktree retargeting or supervised fallback was used.

## Adversarial readiness card

Slice: K2-021 — Bounded Agent A isolated candidate generation.
Milestone: E — Agent A can produce isolated candidates.
Compartment: Provider / Agent A and Candidate / staging.
One authority boundary: bounded Agent A output evidence becomes an isolated candidate/staging record with reviewable non-secret provenance.
Direct requirements: `REQ-KN-127`, `REQ-KN-128`.
Supporting-only requirements: `REQ-KN-110`, `REQ-KN-114`, `REQ-KN-008`, `REQ-KN-015`, `REQ-KN-016`.
Explicitly denied capabilities: live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source retention, Agent A job lifecycle/orchestration, project/source writes, source repair/adoption/import/promotion, canonical mutation/save/export/session persistence, parser process/runtime expansion, projection/layout trust, renderer/IPC/preload expansion, support export, telemetry, dependency changes, RTM generation, production `blk-link`, and BEO publication/signing/storage/ledger.
Malformed input behavior: missing/malformed/hostile Agent A output evidence must produce a blocked or separated fail-closed candidate descriptor, not throw, execute callbacks, read files, call providers, or serialize hostile raw fields.
Contradictory input behavior: if evidence claims approved/trusted/promotable/importable/savable/canonical while also containing untrusted/generated/provider output, raw/leaky fields, or denied authority metadata, K2-021 must choose the stricter non-authority blocked/untrusted state.
Spoofing seams to forbid: caller candidate ids/orders/states, authority flags, AI approval metadata, provider readiness claims, trusted flags, source path/body fields, prompt/provider/credential/token fields, function/callback/DOM handles, mutable prototypes, parser/projection handles, import/export/save/session/canonical claims, BEO/RTM/`blk-link` claims.
Raw/leaky fields to forbid: `raw`, `content`, `body`, `sysml`, `sourceText`, `modelText`, `path`, `filename`, `dirname`, `prompt`, `providerPayload`, `providerRequest`, `providerResponse`, `credential`, `token`, `apiKey`, `errorBody`, `stack`, `diagnostic`, `parserInput`, `sourceCoordinates`, `layoutCoordinates`, `canvas`, `svg`, `save`, `export`, `rtm`, `blkLink`, `blk-link`, `beoPublication`, except fixed denied-authority labels that tests constrain.
Required hostile probes: focused K2-021 test must include raw-marker non-leakage, nested denied-field rejection, contradictory authority metadata, spoofed candidate id/order/state, proxies/getters/callables/symbols/revoked proxies, deep freeze checks, exact key/vocabulary checks, and static source scans for denied live behavior.
Closeout docs/mirrors to update after successful implementation: canonical `BEO-K2-021`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, and view-only Obsidian BEB/L2/BEO/BDOC/roadmap/traceability mirrors after final commit.

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
