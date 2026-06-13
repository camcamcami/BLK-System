---
beb_id: "BEB-K2-025"
beo_id: "BEO-K2-025"
l2_id: "L2-K2-025"
trace_artifacts:
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:a1458fc73ad0c230ca54d0619d2fe16ef00d7d309557ee34287b22dc64592285"
  - kind: "process_guard"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability_index"
    id: "K2-TRACEABILITY-MANIFEST"
    version_hash: "sha256:18d37cc30637e8bd2f53b457afb920b2b2c7d35ce5f0535763e85dc9ddb40bce"
  - kind: "prior_outcome"
    id: "K2-024-SPRINT-CLOSEOUT"
    version_hash: "sha256:36e14e8e5abee9d13992716b88bc68c8ec3a10d35697750c4ea387db06fcabaa"
  - kind: "prior_outcome"
    id: "BEO-K2-024"
    version_hash: "sha256:6ff0947cb7526aa2c1c2daae65525743475bc8477ddfa6d2f2ee6fbaee41fdd1"
  - kind: "requirement"
    id: "REQ-KN-072"
    version_hash: "sha256:b26e55993345b2b07bb1d31d62fa0f33280b684cfc764603d0cbec4c7447bd20"
  - kind: "requirement"
    id: "REQ-KN-073"
    version_hash: "sha256:6e43197e174704f0c2ec5d401fbf2c0e83743dfc0727e0f3ef5194a80a09b19c"
  - kind: "requirement_supporting"
    id: "REQ-KN-075"
    version_hash: "sha256:bdf3c6bb9bc5d2fb3b1562126647b4d2d9f8d58086215b003dcb6a3a429c2931"
  - kind: "requirement_supporting"
    id: "REQ-KN-076"
    version_hash: "sha256:00922100541a76a834128dec91cb0d99637e3d0368dbf26e3b508ca6543d6273"
  - kind: "requirement_supporting"
    id: "REQ-KN-085"
    version_hash: "sha256:c8b80d8422c7913fe8f4129872d3c405f0c9de22b92e623711327fab1d00202d"
  - kind: "requirement_supporting"
    id: "REQ-KN-128"
    version_hash: "sha256:cec62edb7fcd10c310c65712843922eb40b94e0a22456e3b55dedbdb1cba3dc5"
  - kind: "requirement_supporting"
    id: "REQ-KN-134"
    version_hash: "sha256:8778997655ffb3c2650a27a2814f97cf386a0a3b679c09b2b6bf43d39c5f8a67"
  - kind: "requirement_supporting"
    id: "REQ-KN-135"
    version_hash: "sha256:2d026cd78ba7681c47fe18a81deeb0f51511fb416ef578acc1e771611ac68f84"
---
# BEB-K2-025 — Governed Canonical Write Transaction and Recovery Record

## Executive intent / plain-English goal

K2-025 advances Milestone F by adding the first bounded governed-write transaction seam after K2-024 admission. Given a K2-024 admitted write-intent record and a controlled single-file fixture package target, Kuronode shall produce one deterministic transaction result: committed to the fixture package record, or failed closed with no package update. Either outcome must include verifiable recovery evidence.

This is intentionally a controlled single-file/fixture package path, not broad filesystem or Git mutation. The slice proves transaction semantics, target/path binding, before/after hashes, commit-or-fail status, and undo/recovery record shape before any general SysML/KerML write, import, save/export, or multi-file mutation exists.

## Why this slice exists now

K2-021 isolated Agent A candidate material. K2-022 classified candidate readiness. K2-023 produced a reviewable pre-write promotion request. K2-024 admitted a request into governed write-command review without mutating anything.

The next meaningful product delta is not another status-only gate. K2-025 adds the narrow transaction boundary that consumes K2-024 admission and proves how a future governed canonical write can be represented as auditable commit-or-fail evidence with undo/recovery support. The implementation must stay small enough that hostile review can reason about every input, output, path, and denied adjacent authority.

## Direct product requirement stance

Direct requirements for this slice:

- `REQ-KN-072`: K2-025 implements a bounded governed write transaction record over one controlled fixture package path. The transaction may commit only when a K2-024 admission record is coherent and the submitted package target/version hashes match.
- `REQ-KN-073`: K2-025 emits undo/recovery evidence for every committed transaction and fail-closed recovery/no-op evidence for blocked transactions.

Supporting constraints:

- `REQ-KN-075`: post-change readiness remains supporting. K2-025 records readiness-refresh-required evidence but must not claim full project readiness refresh execution.
- `REQ-KN-076` and `REQ-KN-085`: failure paths must be honest, visible, and non-mutating.
- `REQ-KN-128`, `REQ-KN-134`, and `REQ-KN-135`: Agent A/provider output authority remains non-authority; pre-write provenance and hash binding remain visible; no raw prompt/source/body/provider/credential content may leak.

## Lifecycle / enabling trace

K2-025 is product-facing support behavior in the Promotion / canonical mutation compartment. It consumes K2-024 write-admission evidence and produces deterministic transaction evidence. It does not perform broad filesystem writes, source repair, external-edit import/adoption/promotion, general save/export/session persistence, RTM, production blk-link, or BEO publication.

## Architecture/readiness guidance

Use the hash-bound trace artifacts in frontmatter as authority context. Relevant boundaries:

- Product convergence map: governed canonical mutation is high authority and must advance through small auditable seams.
- K2 roadmap: K2-025 is selected but pending dispatch; selection alone did not authorize implementation.
- K2-024 closeout: admission records are write-intent evidence only and do not themselves mutate canonical source.
- K2-025 must prove a transaction boundary over a controlled fixture package path while keeping live source/Git/project mutation outside exact route allowlists denied.

## Exact implementation scope

Allowed modified files:

- `package.json`
- `scripts/validate-foundation.mjs`
- `tests/foundation.test.mjs`
- `src/shared/foundation.ts`

Allowed new files:

- `src/shared/governed-write-transaction.mjs`
- `tests/governed-write-transaction.test.mjs`

No other files may be modified or created by the implementation commit. In particular, do not modify docs, lockfiles, generated outputs, dependencies, parser/runtime modules, project/package inspection modules, renderer/main/preload files, provider clients, Electron IPC, projection/layout modules, existing K2 artifacts, traceability/roadmap/BEO docs, save/export/session code, Agent A candidate/readiness/request/admission modules, or general canonical mutation/write code during route execution.

## Required TDD evidence

1. Add `tests/governed-write-transaction.test.mjs` first.
2. Run `node tests/governed-write-transaction.test.mjs` and record RED because the current target lacks the K2-025 governed-write transaction module/API.
3. Implement only the minimum shared pure-data module plus package/foundation/validator metadata needed for GREEN.
4. Rerun `node tests/governed-write-transaction.test.mjs` to GREEN.
5. Run the full verification plan in L2 and capture exact outputs.

## Required API / behavior shape

Implement a narrow shared pure-data module such as `src/shared/governed-write-transaction.mjs` exposing:

- `createGovernedCanonicalWriteTransaction(admissionRecord, packageRecord, transactionRequest)`; and optionally
- `createGovernedWriteTransactionRegistry()`.

The public output must be exact-shape, deeply frozen, deterministic, and vocabulary-bound. Suggested public fields:

- `transactionId`
- `writeIntentId`
- `promotionRequestId`
- `targetPackagePath`
- `targetVersionHash`
- `candidateContentFingerprint`
- `transactionState`
- `commitStatus`
- `recoveryStatus`
- `failureReasons`
- `beforeVersionHash`
- `afterVersionHash`
- `transactionEvidenceHash`
- `recoveryRecord`
- `readinessRefreshRequired`
- `authorityFlags`

Suggested admitted/committed vocabularies: `transaction-committed`, `fixture-package-record-updated`, `recovery-recorded`, and `post-change-readiness-refresh-required`. Suggested blocked vocabularies: `transaction-blocked`, `commit-failed`, `recovery-noop-recorded`, and `no-package-update`.

A committed transaction requires:

- a K2-024 admitted write-intent record with coherent IDs, fixed admitted status vocabulary, explicit review-required posture, `undoRecoveryRequired: true` or equivalent future-obligation metadata, canonical `sha256:<64 hex>` request/invocation hashes, and denied adjacent authority flags;
- a controlled package record for exactly one fixture package path, e.g. `fixtures/k2-025/single-file.sysml`, with canonical `sha256:<64 hex>` current version hash and explicit single-file target kind;
- a transaction request that names the same target path, same expected current version hash, same candidate content fingerprint, deterministic candidate replacement hash, explicit `operatorReviewConfirmed: true` for this fixture transaction only, and false adjacent authority flags;
- no raw source body, prompt, provider payload, credential, path traversal, absolute path, multi-file target, filesystem handle, function/callback/proxy/getter/symbol, approval/publication/RTM/blk-link claims, save/export/session-persistence claims, or source/Git mutation claims.

## Acceptance criteria

- Valid admitted inputs produce a committed transaction record that binds target path, before hash, after hash, write intent ID, candidate fingerprint, and recovery record.
- Invalid, blocked, contradictory, stale-hash, multi-file, path-traversal, absolute-path, raw-content, non-finite, hostile-object, or permissive-authority inputs produce a blocked fail-closed transaction with no package update and fixed failure reasons.
- Public output must recompute transaction/recovery evidence hashes from sanitized submitted evidence. Do not trust caller-supplied hashes.
- Public output must not contain raw prompt/source/body/SysML/content/path outside the fixed controlled fixture path, provider request/response/payload, credential/token/apiKey, stack/diagnostic/parser/save/export/session, RTM/blk-link/BEO-publication markers except fixed denied-authority labels constrained by tests.
- Existing K2-021 through K2-024 modules must remain compatible; no modifications to those modules are allowed in this route.
- No live provider/API/network behavior, credential handling, parser execution, projection/layout behavior, renderer behavior, Electron IPC/preload behavior, general save/export/session persistence, package-manager/dependency change, RTM generation, production blk-link, or BEO publication/storage/ledger is introduced.

## Required hostile probes

Before closeout, verify:

1. exact K2-025 transaction public keys and exact allowed vocabularies;
2. semantic consistency among `transactionState`, `commitStatus`, `recoveryStatus`, `failureReasons`, before/after hashes, admission state, package target, and request evidence;
3. fixed blocked reason vocabulary, not arbitrary caller text;
4. stale target version hash blocks;
5. blocked or non-admitted K2-024 admission blocks;
6. package path traversal, absolute paths, multi-file targets, path aliases, and unsupported package kinds block;
7. raw marker fields or values for source/body/sysml/content/prompt/provider/credential/diagnostic/parser/save/export/session/RTM/blk-link/BEO-publication do not serialize into public output;
8. caller-supplied transaction IDs/states/statuses/evidence hashes/recovery records cannot override deterministic policy;
9. hostile objects, nested proxies, getters, symbols, callable values, revoked proxies, non-plain containers, non-finite numbers, and hash aliases fail closed without invoking caller code;
10. generated transaction records and registries are deeply frozen and expose no mutable function/prototype/DOM handles except registry methods themselves;
11. changed source text does not introduce fs/path/child_process/fetch/http/https/net provider SDK/client calls, environment/credential reads, filesystem IO, parser process/runtime execution, renderer/IPC imports, layout engines, import/export/save/session persistence, telemetry, RTM, blk-link, BEO publication, or broad source/Git mutation behavior;
12. package and validator gates include the focused K2-025 test and governed file metadata.

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
