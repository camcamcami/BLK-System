L2_ID: L2-K2-022
BEB_ID: BEB-K2-022
BEO_ID: BEO-K2-022
MODEL: gpt-5.5
REASONING_EFFORT: xhigh
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: b97bf72e5011b3c6841cb634115708cb5f75527d

# L2-K2-022 — Agent A pre-write candidate promotion-readiness disposition gate

## Mission

Implement exactly the K2-022 promotion-readiness/disposition gate described by `BEB-K2-022`. Keep the change small, test-driven, deterministic, and authority-bounded. The only product-facing delta is that existing Agent A pre-write candidate records can be classified as ready for later governed-promotion consideration or blocked with fixed reasons. Do not implement actual promotion, import/adoption, canonical source mutation, save/export/session persistence, provider calls, Agent A job lifecycle, parser/projection/renderer expansion, RTM, `blk-link`, or BEO publication.

## Allowed files

You may modify only:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/shared/agent-a-candidate-generation.mjs`

You may create only:

- `src/shared/agent-a-promotion-readiness.mjs`
- `tests/agent-a-promotion-readiness.test.mjs`

Do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, traceability/roadmap/BEO docs, save/export code, or canonical mutation code during route execution.

## Required TDD sequence

1. Add `tests/agent-a-promotion-readiness.test.mjs` first.
2. Run `node tests/agent-a-promotion-readiness.test.mjs` and record RED because the current target lacks the K2-022 promotion-readiness module/API.
3. Implement only the minimum shared pure-data module, validator/package metadata, foundation metadata, and any narrow Agent A candidate-generation export needed for GREEN.
4. Rerun `node tests/agent-a-promotion-readiness.test.mjs` to GREEN.
5. Run all verification commands below and capture exact outputs.

## Implementation constraints

- Create a new shared module such as `src/shared/agent-a-promotion-readiness.mjs`. It must be pure data: no `fs`, `path`, `child_process`, `fetch`, `http`, `https`, `net`, provider SDK/client imports, Electron imports, parser/runtime imports, renderer imports, browser storage, package-manager/dependency behavior, or process spawning.
- The module should expose narrow functions such as `createAgentAPromotionReadinessDisposition(input, readinessOrder)` and optionally `createAgentAPromotionReadinessRegistry()`.
- Consume K2-021 Agent A candidate-generation records as pure data. Do not call providers, do not create or retain raw generated content, and do not infer canonical authority.
- Public readiness records must use exact keys and fixed vocabularies. Suggested fields: `promotionReadinessId`, `candidateId`, `agentCandidateId`, `readinessOrder`, `readinessState`, `disposition`, `blockedReasons`, `provenanceStatus`, `nonCanonicalStatus`, `authorityFlags`, and mirrored denied authority flags. Do not include arbitrary caller keys.
- Ready disposition must require reviewable non-secret provenance and non-canonical authority posture. If provenance is missing/malformed/hostile, `providerStatus` is not `not-called`, authority flags are missing or permissive, or contradictory readiness/canonical/promotion metadata exists, block with fixed reasons.
- Treat raw marker values and nested denied fields as hostile. Do not serialize them into public output. Do not call getters/callbacks/functions supplied by input.
- Deep-freeze public records, nested blocked reasons, authority flags, registries/lists, and any exported catalog arrays.
- Update `package.json` test script to include `node tests/agent-a-promotion-readiness.test.mjs` after `agent-a-candidate-generation`.
- Update `scripts/validate-foundation.mjs` so K2-022 files are required, governed marker coverage is enforced, authority field scans cover the new module, and the package test script remains exact.
- Update `tests/foundation.test.mjs` and `src/shared/foundation.ts` for K2-022 metadata only while preserving K2-001..K2-021 evidence.

## Required tests

Cover at least:

- current target RED for missing K2-022 module/API;
- deterministic ready disposition for an accepted K2-021 Agent A candidate record;
- blocked dispositions for missing provenance, wrong provider status, missing/non-canonical authority flags, and contradictory ready/promotable/canonical/save/import metadata;
- exact public key set and exact allowed vocabularies;
- exact fixed blocked reason vocabulary and semantic consistency between status fields and reasons;
- raw prompt/source/body/sysml/content/path/filename/provider request/response/payload/credential/token/apiKey/stack/diagnostic/parser/RTM/blk-link/BEO-publication markers absent from public output;
- nested denied fields and contradictory approved/trusted/promotable/importable/savable/canonical metadata fail closed or are sanitized to non-authority;
- spoofed caller readiness ids/orders/states do not override deterministic ids/orders/state policy;
- hostile proxies/getters/callables/symbols/revoked proxies do not invoke caller code or leak fields;
- output and nested objects/lists are deeply frozen and expose no mutable function/prototype/DOM handles;
- static source scan for denied live behavior (`fetch`, provider SDK/client calls, network URL calls, credential/env reads, filesystem IO, parser process/runtime execution, renderer/IPC imports, layout engines, import/export/save/canonical mutation, telemetry, RTM, `blk-link`, BEO publication);
- package/foundation/validator metadata includes the focused K2-022 test and files.

## Verification commands

```bash
node tests/agent-a-promotion-readiness.test.mjs
node tests/agent-a-candidate-generation.test.mjs
node tests/candidate-staging.test.mjs
node scripts/validate-foundation.mjs
npm test
npm run build
npm run typecheck
git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/agent-a-candidate-generation.mjs src/shared/agent-a-promotion-readiness.mjs tests/agent-a-promotion-readiness.test.mjs
```

## Final response requirements to BLK-System

Report the RED command and expected failure excerpt, GREEN focused test output, full verification outputs, final changed file list, exact feature commit hash, denied-authority summary, hostile-review verdict or blockers, and residual blockers/watch items. If BLK-pipe route execution times out or fails due to environment/tooling, preserve the exact approved allowlist/target hash and report whether clean-worktree retargeting or supervised fallback was used.

## Adversarial readiness card

Slice: K2-022 — Agent A pre-write candidate promotion-readiness disposition gate.
Milestone: F — Governed promotion path, readiness gate only.
Compartment: Candidate / staging at the edge of Promotion / canonical mutation.
One authority boundary: isolated Agent A pre-write candidate records may be evaluated for promotion readiness, but no candidate may cross into canonical source and no write/save/undo behavior is implemented.
Direct requirements: `REQ-KN-128`, `REQ-KN-134`, `REQ-KN-135`.
Supporting-only requirements: `REQ-KN-030`, `REQ-KN-034`, `REQ-KN-072`, `REQ-KN-073`, `REQ-KN-076`, `REQ-KN-115`, `REQ-KN-121`.
Explicitly denied capabilities: live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source/body retention, Agent A job lifecycle/orchestration, project/source writes, source repair/adoption/import/promotion, canonical mutation/save/export/session persistence, parser process/runtime expansion, projection/layout trust, renderer/IPC/preload expansion, support export, telemetry, dependency changes, RTM generation, production `blk-link`, and BEO publication/signing/storage/ledger.
Malformed input behavior: missing/malformed/hostile Agent A candidate evidence must produce a blocked fail-closed disposition with fixed reason vocabulary, not throw, execute callbacks, read files, call providers, mutate source, or serialize hostile raw fields.
Contradictory input behavior: if a candidate says it is ready/promotable/canonical/savable while also missing provenance, carrying raw/leaky fields, containing authority metadata, or contradicting non-canonical K2-021 flags, K2-022 must choose the stricter blocked disposition.
Spoofing seams to forbid: caller candidate ids/orders/states, caller readiness statuses, authority flags, AI/provider approval metadata, provider readiness claims, trusted flags, source path/body fields, prompt/provider/credential/token fields, function/callback/DOM handles, mutable prototypes, parser/projection handles, import/export/save/session/canonical claims, BEO/RTM/`blk-link` claims.
Raw/leaky fields to forbid: `raw`, `content`, `body`, `sysml`, `sourceText`, `modelText`, `path`, `filename`, `dirname`, `prompt`, `providerPayload`, `providerRequest`, `providerResponse`, `credential`, `token`, `apiKey`, `errorBody`, `stack`, `diagnostic`, `parserInput`, `sourceCoordinates`, `layoutCoordinates`, `canvas`, `svg`, `save`, `export`, `rtm`, `blkLink`, `blk-link`, `beoPublication`, except fixed denied-authority labels that tests constrain.
Required hostile probes: focused K2-022 test must include ready-path disposition, missing provenance, wrong provider status, non-canonical/canonical contradiction, spoofed readiness/candidate ids, raw-marker non-leakage, nested denied-field rejection, proxies/getters/callables/symbols/revoked proxies, deep freeze checks, exact key/vocabulary checks, semantic-consistency checks, and static source scans for denied live behavior.
Closeout docs/mirrors to update after successful implementation: canonical `BEO-K2-022`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, and view-only Obsidian BEB/L2/BEO/BDOC/roadmap/traceability mirrors after final commit.

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

