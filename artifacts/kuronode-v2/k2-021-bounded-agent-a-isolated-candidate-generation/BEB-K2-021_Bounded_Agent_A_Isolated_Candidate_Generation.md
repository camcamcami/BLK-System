---
beb_id: "BEB-K2-021"
beo_id: "BEO-K2-021"
l2_id: "L2-K2-021"
model: "gpt-5.5"
reasoning_effort: "xhigh"
route: "BEB-L2 -> BLK-pipe -> Codex workspace-write"
target_repo: "/home/dad/code/Kuronode-v2"
target_branch: "main"
target_hash: "c939a9667461a045f82902cb1c477b44fae922fd"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:3de91eb303a8e92f328f569f3551ce4c69465241defb3d247dd582b25bef65de"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:78221e81350d2c59a6df1e995b69317a7be0ada24b565b45f88c0b8799545085"
  - kind: "requirement"
    id: "REQ-KN-127"
    version_hash: "sha256:19c73bb4c32449bc79a92580a9b7a1bb7bc3a5c1a1cd3a74e5dd8b337856a299"
  - kind: "requirement"
    id: "REQ-KN-128"
    version_hash: "sha256:cec62edb7fcd10c310c65712843922eb40b94e0a22456e3b55dedbdb1cba3dc5"
  - kind: "requirement_supporting"
    id: "REQ-KN-110"
    version_hash: "sha256:fd19ce2f95f31d981fa28f1a3013b8ce4838dfa40534da9684ef9f52f3d72740"
  - kind: "requirement_supporting"
    id: "REQ-KN-114"
    version_hash: "sha256:cec8768ea1f6868e50d0c425bea6e989b3fdcfb210248c3baca04130c3eba053"
  - kind: "requirement_supporting"
    id: "REQ-KN-008"
    version_hash: "sha256:e7f8860fc625778a3c440d9b91ae195cd5025239f75f484bf25255ebeab2613c"
  - kind: "requirement_supporting"
    id: "REQ-KN-015"
    version_hash: "sha256:79c5d26a80f7f206a3898cad31f54a64273ede08b474c0dcb3cdbf05cb0e1af8"
  - kind: "requirement_supporting"
    id: "REQ-KN-016"
    version_hash: "sha256:406aedd68ab491fc83bb705df958766228d60efbcdfad9de5a363bb33534dc54"
  - kind: "prior_outcome"
    id: "BEO-K2-020"
    version_hash: "sha256:dca0e3c87687e06195c5b0b2d7f51517d8def75bd6dc99a140a8320764517667"
---
# BEB-K2-021 — Bounded Agent A Isolated Candidate Generation

## Executive intent / plain-English goal

K2-021 opens Milestone E with the smallest useful Agent A/candidate slice: Kuronode shall be able to convert **bounded Agent A output evidence** into an isolated candidate/staging record with reviewable provenance, while keeping every generated/AI-provided artifact separate from canonical source.

This is not live provider execution. The slice accepts a caller-supplied, bounded evidence object that represents an Agent A output outcome and normalizes it into a safe candidate descriptor. The product delta is the first Agent A-specific candidate-generation seam: AI/Agent A output can be represented as separated candidate material without becoming canonical source, without retaining raw prompt/provider/source content, without accepting AI authority metadata, and without enabling import/adoption/promotion/save.

K2-021 must not add provider/API/network calls, credentials, Agent A job orchestration, raw provider request/response persistence, source repair/import/adoption/promotion, canonical source mutation, projection/layout trust, save/export/session persistence, support export, RTM generation, production `blk-link`, or BEO publication/signing/storage/ledger.

## Why this slice exists now

K2-008 created generic candidate/staging separation and K2-002 created provider readiness/status. K2-009 through K2-020 then built the read-only project/parser/projection/renderer status foundation. With Milestone D closed at the bounded read-only level, the next selected milestone is E: Agent A can produce isolated candidates.

The safe first step is not a live provider call. It is a deterministic, testable boundary that turns bounded Agent A output evidence into a candidate/staging record and proves that hostile or contradictory Agent A metadata cannot launder authority into canonical source mutation, import, adoption, promotion, save/export, provider access, parser expansion, or RTM/`blk-link` claims.

## Direct product requirement stance

Direct requirements for this slice:

- `REQ-KN-127`: AI/external generated material must remain separated from canonical source until a later governed import/adoption/promotion path exists.
- `REQ-KN-128`: AI output authority metadata is not canonical authority. Any Agent A/provider metadata claiming approval, promotion, canonical mutation, import, save, RTM, `blk-link`, or BEO publication must be rejected or normalized to non-authority.

## Supporting / prepared requirement stance

Supporting context only:

- `REQ-KN-110`: provider/Agent A readiness context exists, but K2-021 does not perform live provider calls.
- `REQ-KN-114`: raw provider credentials and provider payload details must remain contained; K2-021 must not expose raw prompt, credential, token, provider request/response, or secret-like material.
- `REQ-KN-008`, `REQ-KN-015`, and `REQ-KN-016`: existing degraded/status discipline informs fail-closed Agent A candidate evidence handling, but K2-021 does not change project load, parser, or renderer status behavior.

## Lifecycle / enabling trace

K2-021 is product-facing support behavior in the Provider / Agent A and Candidate / staging compartments. It prepares Milestone E by creating a deterministic candidate-generation boundary that future live Agent A/provider orchestration can call after separate authorization. It remains pure-data and non-mutating.

## Architecture/readiness guidance

Use the hash-bound trace artifacts in frontmatter as authority context. Relevant boundaries:

- Product convergence map: Agent A output must land only in candidate/staging structures and candidate existence does not imply adoption, import, promotion, save, or canonical mutation.
- K2-008 candidate/staging contract: use the existing authority flags and separation posture rather than inventing a second promotion model.
- K2-020 closeout discipline: hostile caller objects/proxies/getters and raw provider/prompt/credential fragments must fail closed or be omitted from public records.
- BLK-System caller-object readiness profile: this slice is a caller-object/control-plane boundary, so tests must prove denied nested fields, raw marker values, proxies/getters/callables/symbols, duplicate/spoofed identifiers, and authority/status laundering fail closed.

## Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`
- `src/shared/candidate-staging.mjs`

Allowed new files:

- `src/shared/agent-a-candidate-generation.mjs`
- `tests/agent-a-candidate-generation.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, or traceability/roadmap/BEO docs during route execution.

## Required TDD evidence

1. Add `tests/agent-a-candidate-generation.test.mjs` first.
2. Run `node tests/agent-a-candidate-generation.test.mjs` and record RED because the current target lacks the K2-021 Agent A candidate-generation module/API.
3. Implement only the minimum shared pure-data module, validator/package metadata, foundation metadata, and any narrow candidate-staging helper changes required for GREEN.
4. Rerun the focused test to GREEN, then run the full verification plan in L2.

## Acceptance criteria

- A new shared pure-data module exposes a narrow API such as `createAgentACandidateGenerationRecord(...)` and/or `createAgentACandidateGenerationRegistry(...)` that converts bounded Agent A output evidence into isolated candidate/staging records.
- The output must include a deterministic candidate id/order, Agent A origin, separated/staged candidate state, reviewable non-secret provenance summary, bounded candidate kind/status labels, and the existing candidate-staging authority flags.
- The output must be deeply frozen and must not expose raw source text, raw generated SysML/KerML/body/content, raw prompt, provider request/response, credential/token/API-key values, filesystem paths, stack traces, parser handles, function/callback/DOM handles, mutable prototypes, arbitrary caller keys, or unbounded provider metadata.
- Malformed/missing/proxy/getter/callable/symbol/contradictory evidence must fail closed to a blocked or separated untrusted candidate record without invoking caller code or serializing hostile fields.
- Caller-supplied candidate ids/orders/states, promotion flags, canonical mutation flags, authority metadata, import/adoption/save/export claims, RTM/`blk-link` claims, BEO publication claims, provider-readiness claims, and trusted/approved wording must not be accepted as authority.
- Existing candidate staging authority remains intact: separated from canonical source is true; canonical/source mutation, promotion, external-edit adoption, AI authority metadata acceptance, raw candidate retention, and filesystem-path retention remain false; governed import remains required.
- No live provider/API/network behavior, credential handling, parser execution, projection/layout behavior, renderer behavior, Electron IPC/preload behavior, save/export/session persistence, support export, package-manager/dependency change, RTM generation, production `blk-link`, or BEO publication/storage/ledger is introduced.
- `scripts/validate-foundation.mjs`, `tests/foundation.test.mjs`, `src/shared/foundation.ts`, and `package.json` include K2-021 metadata and focused test coverage while preserving K2-001..K2-020 gates.

## Required hostile probes

Before closeout, verify:

1. exact Agent A candidate public keys and exact allowed vocabularies;
2. fixed denied-authority fields, not arbitrary object-key enumeration;
3. hostile objects, nested proxies, getters, symbols, callable values, revoked proxies, and descriptor traps fail closed without invoking caller code;
4. raw marker values for `content`, `body`, `sysml`, `sourceText`, `path`, `filename`, `prompt`, `providerPayload`, `providerRequest`, `providerResponse`, `credential`, `token`, `apiKey`, `stack`, `diagnostic`, `parserInput`, `rtm`, `blkLink`, and `beoPublication` do not serialize into public output;
5. contradictory evidence that says candidate is approved/trusted/promotable/importable/savable/canonical must force non-authority blocked/untrusted status or sanitized omission;
6. generated records and registries are deeply frozen and expose no mutable function/prototype/DOM handles;
7. changed source text does not introduce `fetch`, provider SDK/client calls, network URLs, credentials/env reads, filesystem IO, parser process/runtime execution, renderer/IPC code, layout engines, import/export/save/canonical mutation, telemetry, RTM, `blk-link`, or BEO publication behavior;
8. package and validator gates include the focused K2-021 test and governed file metadata.

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

## Verification commands and acceptance evidence

Codex should run and preserve evidence for:

- `node tests/agent-a-candidate-generation.test.mjs`
- `node tests/candidate-staging.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`
- `git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/candidate-staging.mjs src/shared/agent-a-candidate-generation.mjs tests/agent-a-candidate-generation.test.mjs`

Acceptance requires focused RED/GREEN evidence, full static validation, full test-suite pass, exact allowed-file diff, no raw/leaky fragments in public candidate records, no denied live behavior introduced in source text, and hostile-review PASS or a narrow remediation BEB/L2 before BEO closeout.

## blk-link / RTM stance

This package produces bounded product/candidate-staging evidence only. It does not run RTM generation, production `blk-link`, protected-body read/copy/scan/hash, drift rejection, coverage truth, BEO publication/signing/storage/ledger, reusable BLK-pipe/Codex dispatch, live provider dispatch, or any runtime/filesystem/source mutation authority beyond the exact approved drop.

## Denied adjacent behaviors

K2-021 does not authorize live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source retention, Agent A job lifecycle/orchestration, source repair, source adoption/import/promotion, canonical mutation/save/export/session persistence, parser execution/process spawning/runtime expansion, projection/layout/canvas/SVG trust, renderer/IPC/preload expansion, filesystem path/content retention, support-bundle export, telemetry, dependency/package-manager changes, RTM generation, production `blk-link`, protected-body access, coverage/drift truth, or BEO publication/signing/storage/ledger.

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
