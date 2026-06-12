---
beb_id: "BEB-K2-023"
beo_id: "BEO-K2-023"
l2_id: "L2-K2-023"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:d9b02a5c82bb592edd469deae76340335ce09060cdb680b9adc9a07c844e334b"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:6c4b42dbec7807f1cc7dd90ee8c9b3d6eb138fed247f3e6d253e3b4dd7bf3b81"
  - kind: "requirement"
    id: "REQ-KN-072"
    version_hash: "sha256:b26e55993345b2b07bb1d31d62fa0f33280b684cfc764603d0cbec4c7447bd20"
  - kind: "requirement"
    id: "REQ-KN-134"
    version_hash: "sha256:8778997655ffb3c2650a27a2814f97cf386a0a3b679c09b2b6bf43d39c5f8a67"
  - kind: "requirement"
    id: "REQ-KN-135"
    version_hash: "sha256:2d026cd78ba7681c47fe18a81deeb0f51511fb416ef578acc1e771611ac68f84"
  - kind: "requirement_supporting"
    id: "REQ-KN-073"
    version_hash: "sha256:6e43197e174704f0c2ec5d401fbf2c0e83743dfc0727e0f3ef5194a80a09b19c"
  - kind: "requirement_supporting"
    id: "REQ-KN-128"
    version_hash: "sha256:cec62edb7fcd10c310c65712843922eb40b94e0a22456e3b55dedbdb1cba3dc5"
  - kind: "prior_outcome"
    id: "BEO-K2-022"
    version_hash: "sha256:aaf9621afe50f71db9cd822989443ca5bf416c5671ed0574a3625d1b08de2365"
---
# BEB-K2-023 — Governed Agent A Candidate Promotion Request / Preflight Envelope

## Executive intent / plain-English goal

K2-023 advances Milestone F without crossing the canonical-write boundary. Kuronode shall be able to take an existing K2-022 `ready` Agent A promotion-readiness disposition plus the matching isolated K2-021 candidate record and emit a deterministic, reviewable promotion request/preflight envelope.

The product delta is a pure-data request object that says, in effect: “this isolated Agent A candidate and this readiness disposition are coherent enough to request later governed-promotion review.” It binds candidate identity, candidate content fingerprint, K2-022 readiness evidence hash, sanitized provenance state, denied-authority flags, and a fixed preflight/review status vocabulary.

K2-023 is not promotion, import, adoption, canonical mutation, save, undo, or source write execution. It must not create a canonical patch, edit SysML/KerML, write project files, call providers, expand Agent A job lifecycle behavior, or implement user approval capture. Actual governed write/undo behavior remains a later high-authority slice.

## Why this slice exists now

K2-021 created isolated non-canonical Agent A candidate records. K2-022 classified those records as ready or blocked for future governed-promotion review. The next safe movement toward Milestone F is a promotion-request/preflight envelope that binds the candidate and readiness evidence before any canonical write path exists.

Without K2-023, a future mutation slice would have to invent request/evidence binding at the same time as writing source. K2-023 keeps the boundary explicit and testable: request readiness first, mutation later.

## Direct product requirement stance

Direct requirements for this slice:

- `REQ-KN-072`: governed canonical write behavior is represented at the request/preflight boundary only; K2-023 prepares a governed-promotion request record but does not execute the write.
- `REQ-KN-134`: AI-generated or Agent A-produced model content before governed canonical write commit remains non-canonical pre-write material.
- `REQ-KN-135`: AI-generated or Agent A-produced pre-write model content requires sanitized, reviewable provenance metadata; K2-023 must bind provenance and evidence hashes without retaining raw payload/body/source text.

## Supporting / continuity requirement stance

Supporting context only:

- `REQ-KN-073`: undo/recovery remains supporting until actual canonical write/undo behavior exists.
- `REQ-KN-128`: AI output authority metadata remains non-authority. Any candidate/readiness/request metadata claiming approval, promotion execution, canonical mutation, import, save, RTM, `blk-link`, or BEO publication must be rejected or normalized to non-authority.
- K2-008, K2-021, and K2-022 evidence remains continuity context for candidate separation, Agent A candidate generation, and readiness disposition.

## Lifecycle / enabling trace

K2-023 is product-facing support behavior in the Promotion / canonical mutation compartment, request/preflight side only. It consumes prior Candidate / staging evidence and creates a deterministic request envelope suitable for later human/system review. It remains pure-data and non-mutating.

## Architecture/readiness guidance

Use the hash-bound trace artifacts in frontmatter as authority context. Relevant boundaries:

- Product convergence map: promotion/canonical mutation is a high-authority compartment and must not be bundled into status/readiness slices.
- K2 roadmap: `K2-023` is selected as request/preflight only; roadmap selection did not authorize implementation or dispatch by itself.
- K2-021 closeout: Agent A candidates are isolated, non-canonical, and carry non-secret provenance including a `contentFingerprint` but not raw content.
- K2-022 closeout: readiness dispositions are pure-data and may be `ready`; they do not authorize promotion.
- Requirements `REQ-KN-134` and `REQ-KN-135`: pre-write non-authority/provenance is direct product scope.
- BLK-System caller-object readiness profile: this is a caller-object/control-plane boundary, so tests must prove denied nested fields, raw marker values, proxies/getters/callables/symbols, duplicate/spoofed identifiers, and authority/status laundering fail closed.

## Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`

Allowed new files:

- `src/shared/agent-a-promotion-request.mjs`
- `tests/agent-a-promotion-request.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, traceability/roadmap/BEO docs, save/export code, or canonical mutation code during route execution.

## Required TDD evidence

1. Add `tests/agent-a-promotion-request.test.mjs` first.
2. Run `node tests/agent-a-promotion-request.test.mjs` and record RED because the current target lacks the K2-023 promotion-request module/API.
3. Implement only the minimum shared pure-data module plus validator/package/foundation metadata needed for GREEN.
4. Rerun the focused test to GREEN, then run the full verification plan in L2.

## Required API / behavior shape

Implement a narrow shared pure-data module such as `src/shared/agent-a-promotion-request.mjs` exposing:

- `createAgentAPromotionRequestPreflight(input, requestOrder)`; and optionally
- `createAgentAPromotionRequestRegistry()`.

The input should be a closed record that contains the existing isolated K2-021 candidate record and the K2-022 readiness disposition, for example `{ candidate, readinessDisposition }`. Do not accept raw candidate content, source paths, prompt text, provider payloads, credentials, callbacks, or approval text.

A ready request/preflight envelope must include deterministic/fixed public fields such as:

- `promotionRequestId`
- `promotionReadinessId`
- `candidateId`
- `agentCandidateId`
- `requestOrder`
- `requestState`
- `preflightStatus`
- `reviewStatus`
- `requestBlockedReasons`
- `candidateContentFingerprint`
- `readinessEvidenceHash`
- `provenanceStatus`
- `nonCanonicalStatus`
- `authorityFlags`
- mirrored denied-authority booleans from K2-008/K2-021/K2-022

Exact names may be refined by tests, but public output must be exact-shape, deeply frozen, deterministic, and vocabulary-bound. Suggested request states: `ready-for-governed-promotion-request-review` and `blocked`. Suggested review status values: `request-review-required` and `request-blocked`. Suggested preflight status values: `request-preflight-ready` and `request-preflight-blocked`.

## Acceptance criteria

- A ready request is emitted only when:
  - the candidate has valid K2-021 identity, staged/non-canonical state, `providerStatus: "not-called"`, sanitized bounded provenance, and a canonical `sha256:<64 hex>` `contentFingerprint`;
  - the readiness disposition has `disposition: "ready"`, `readinessState: "ready-for-governed-promotion-review"`, no blocked reasons, `provenanceStatus: "reviewable-non-secret"`, `nonCanonicalStatus: "non-canonical"`, matching candidate identity, and K2 authority flags still deny promotion/canonical mutation/import/save/export/raw/path retention;
  - the request envelope recomputes a deterministic `readinessEvidenceHash` from the submitted readiness disposition rather than trusting any caller-supplied hash.
- Missing/malformed/blocked readiness, mismatched candidate/readiness identity, non-hex or missing candidate content fingerprint, wrong provider status, permissive authority flags, raw/leaky fields, contradictory approval/promote/canonical/save/import metadata, hostile object/proxy/getter/callable/symbol/revoked-proxy input, or caller-supplied request IDs/states must fail closed to a blocked request with fixed reasons.
- Public request output must not contain raw prompt/source/body/SysML/content/path/filename/provider request/response/payload/credential/token/apiKey/stack/diagnostic/parser/RTM/`blk-link`/BEO-publication markers.
- Request output must not authorize promotion. It may only say review is required for a future governed-promotion decision.
- Existing K2-021 and K2-022 behavior must remain compatible; no modifications to those modules are allowed in this route.
- No live provider/API/network behavior, credential handling, parser execution, projection/layout behavior, renderer behavior, Electron IPC/preload behavior, save/export/session persistence, support export, package-manager/dependency change, RTM generation, production `blk-link`, or BEO publication/storage/ledger is introduced.

## Required hostile probes

Before closeout, verify:

1. exact K2-023 request/preflight public keys and exact allowed vocabularies;
2. semantic consistency between `requestState`, `preflightStatus`, `reviewStatus`, `requestBlockedReasons`, readiness state, provenance status, authority flags, and candidate identity;
3. fixed blocked reason vocabulary, not arbitrary caller text;
4. caller-supplied `promotionRequestId`, request order, request state, review status, trusted/approved/promotable/importable/savable/canonical flags, or readiness hashes do not override deterministic policy;
5. readiness evidence hash is recomputed from the submitted readiness disposition and changes when readiness evidence changes;
6. candidate/readiness identity mismatch blocks;
7. blocked K2-022 readiness disposition blocks;
8. missing/malformed candidate content fingerprint blocks;
9. hostile objects, nested proxies, getters, symbols, callable values, revoked proxies, and descriptor traps fail closed without invoking caller code;
10. raw marker values for `content`, `body`, `sysml`, `sourceText`, `path`, `filename`, `prompt`, `providerPayload`, `providerRequest`, `providerResponse`, `credential`, `token`, `apiKey`, `stack`, `diagnostic`, `parserInput`, `rtm`, `blkLink`, and `beoPublication` do not serialize into public output;
11. generated request records and registries are deeply frozen and expose no mutable function/prototype/DOM handles except registry methods themselves;
12. changed source text does not introduce `fetch`, provider SDK/client calls, network URLs, credentials/env reads, filesystem IO, parser process/runtime execution, renderer/IPC code, layout engines, import/export/save/canonical mutation, telemetry, RTM, `blk-link`, or BEO publication behavior;
13. package and validator gates include the focused K2-023 test and governed file metadata.

## Adversarial readiness card

Slice: K2-023 — Governed Agent A candidate promotion request / preflight envelope.
Milestone: F — Governed promotion path, request/preflight side only.
Compartment: Promotion / canonical mutation boundary before canonical mutation exists.
One authority boundary: a ready K2-022 disposition plus matching isolated K2-021 candidate may produce a reviewable promotion-request/preflight record, but no candidate may cross into canonical source and no write/save/undo/promotion behavior is implemented.
Direct requirements: `REQ-KN-072`, `REQ-KN-134`, `REQ-KN-135`.
Supporting-only requirements: `REQ-KN-073`, `REQ-KN-128`.
Explicitly denied capabilities: live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source/body retention, Agent A job lifecycle/orchestration, project/source writes, source repair/adoption/import/promotion execution, canonical mutation/save/export/session persistence, parser process/runtime expansion, projection/layout trust, renderer/IPC/preload expansion, support export, telemetry, dependency changes, RTM generation, production `blk-link`, BEO publication/signing/storage/ledger, approval capture, run-ID reservation/consumption, and reusable dispatch authority.
Malformed input behavior: missing/malformed/hostile candidate or readiness evidence must produce a blocked fail-closed request with fixed reason vocabulary, not throw, execute callbacks, read files, call providers, mutate source, or serialize hostile raw fields.
Contradictory input behavior: if candidate/readiness/request evidence says it is approved/promotable/canonical/savable while also missing provenance, carrying raw/leaky fields, containing authority metadata, contradicting K2-021/K2-022 non-canonical flags, or mismatching identity/hash evidence, K2-023 must choose the stricter blocked request.
Spoofing seams to forbid: caller request ids/orders/states/statuses, caller readiness hashes, caller candidate ids/orders/states, authority flags, AI/provider approval metadata, provider readiness claims, trusted flags, source path/body fields, prompt/provider/credential/token fields, function/callback/DOM handles, mutable prototypes, parser/projection handles, import/export/save/session/canonical claims, BEO/RTM/`blk-link` claims.
Raw/leaky fields to forbid: `raw`, `content`, `body`, `sysml`, `sourceText`, `modelText`, `path`, `filename`, `dirname`, `prompt`, `providerPayload`, `providerRequest`, `providerResponse`, `credential`, `token`, `apiKey`, `errorBody`, `stack`, `diagnostic`, `parserInput`, `sourceCoordinates`, `layoutCoordinates`, `canvas`, `svg`, `save`, `export`, `rtm`, `blkLink`, `blk-link`, `beoPublication`, except fixed denied-authority labels that tests constrain.
Required hostile probes: focused K2-023 test must include ready request path, blocked readiness path, identity mismatch, fingerprint mismatch/malformed, spoofed request/readiness ids, raw-marker non-leakage, nested denied-field rejection, proxies/getters/callables/symbols/revoked proxies, deep freeze checks, exact key/vocabulary checks, semantic-consistency checks, and static source scans for denied live behavior.
Closeout docs/mirrors to update after successful implementation: canonical `BEO-K2-023`, `docs/roadmaps/K2_implementation-roadmap.md`, `docs/traceability/K2_traceability.yaml`, `docs/outcomes/K2-023_sprint-closeout.md`, and view-only Obsidian BEB/L2/BEO/BDOC/roadmap/traceability/outcome mirrors after final commit.

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

## Verification commands and acceptance evidence

Codex should run and preserve evidence for:

- `node tests/agent-a-promotion-request.test.mjs`
- `node tests/agent-a-promotion-readiness.test.mjs`
- `node tests/agent-a-candidate-generation.test.mjs`
- `node tests/candidate-staging.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test`
- `npm run build`
- `npm run typecheck`
- `git diff --check -- package.json scripts/validate-foundation.mjs tests/foundation.test.mjs src/shared/foundation.ts src/shared/agent-a-promotion-request.mjs tests/agent-a-promotion-request.test.mjs`

Acceptance requires focused RED/GREEN evidence, full static validation, full test-suite pass, exact allowed-file diff, no raw/leaky fragments in public request records, no denied live behavior introduced in source text, and hostile-review PASS or a narrow remediation BEB/L2 before BEO closeout.

## blk-link / RTM stance

This package produces bounded product/request-preflight evidence only. It does not run RTM generation, production `blk-link`, protected-body read/copy/scan/hash, drift rejection, coverage truth, BEO publication/signing/storage/ledger, reusable BLK-pipe/Codex dispatch, live provider dispatch, or any runtime/filesystem/source mutation authority beyond the exact approved drop.

## Denied adjacent behaviors

K2-023 does not authorize live provider/API/network calls, credential reads/storage, raw provider request/response/prompt/source retention, Agent A job lifecycle/orchestration, source repair, source adoption/import/promotion execution, canonical mutation/save/export/session persistence, parser execution/process spawning/runtime expansion, projection/layout/canvas/SVG trust, renderer/IPC/preload expansion, filesystem path/content retention, support-bundle export, telemetry, dependency/package-manager changes, RTM generation, production `blk-link`, protected-body access, coverage/drift truth, approval capture, run-ID reservation/consumption, or BEO publication/signing/storage/ledger.
