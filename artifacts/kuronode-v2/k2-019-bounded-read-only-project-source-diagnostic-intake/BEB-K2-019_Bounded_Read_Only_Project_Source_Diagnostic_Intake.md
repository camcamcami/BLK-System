---
beb_id: "BEB-K2-019"
beo_id: "BEO-K2-019"
l2_id: "L2-K2-019"
trace_artifacts:
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:aa9e636eb514850e7612fc8f179b7091deeeeb4362db25478b894ba96d21b5e5"
  - kind: "roadmap"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "process"
    id: "K2-ITERATION-DRIFT-PROTECTION"
    version_hash: "sha256:a2acedfa31dae7134298c39b0f7ec7ee9c47e79cd0d54179cd28a3f3fb76a393"
  - kind: "traceability"
    id: "K2-TRACEABILITY"
    version_hash: "sha256:35bd37c9b5888c793deadae0261ea2c0f3ad497fc26d41b9814a8c5fd8a8e853"
  - kind: "requirements-baseline"
    id: "KVRB-001-REQ-KN-008-015-016-084-104-129"
    version_hash: "sha256:736b0df3e082342377b5cd609b23f05599cca0f54b07edc27d106384268df824"
  - kind: "icd"
    id: "ICD-KVA-001"
    version_hash: "sha256:1074a27f2b1d44ccd9336c7257a8fe69f984ffadedb1e1fc8e871c67360612f3"
  - kind: "icd"
    id: "ICD-KVA-003"
    version_hash: "sha256:34ff70aaa1f9a00fdf4942b2b42f079f887b8fbac0872ca6c6d86d59230a13e2"
  - kind: "allocation"
    id: "KVA-013-REQ-ALLOCATION"
    version_hash: "sha256:7e2562c496a37c7ce7d35bb704a10abd0731922acf7f9aaa8d25b14280cc708d"
  - kind: "verification"
    id: "KVA-031-BEB-L2-PREFLIGHT"
    version_hash: "sha256:fd01ddb7ed1a54518e15efc8e238a29695a3c9342235eedcdb8fb6f9ccb512df"
  - kind: "verification"
    id: "KVA-032-EVIDENCE-LEDGER"
    version_hash: "sha256:d88483948373704534f7bf1b574d26f04dc15c2e5e1a3814cbe3e2e0c17abf6a"
---
# BEB-K2-019

## Executive intent / plain-English goal

K2-019 adds bounded, read-only source-body intake for the currently selected local project/package source and feeds that text into the existing K2-010 parser/model-health diagnostic path. The user-facing result remains sanitized model-health/status metadata only. This slice intentionally bridges K2-009 package shape inspection and K2-010 parser diagnostics without granting writes, import/adoption, provider behavior, source-coordinate truth, or projection/layout trust.

## Why this slice exists now

The K2 roadmap selected K2-019 after K2-018 closed the renderer-visible projection panel. The meaningful next delta is to connect real local package source to existing bounded diagnostics so the app can report model-health readiness from project source, rather than only from module-owned fixtures or caller-supplied in-memory strings. This strengthens the Milestone B/C/D bridge while preserving read-only discipline.

## Direct product requirement stance

Direct candidates for this slice are `REQ-KN-008`, `REQ-KN-015`, `REQ-KN-016`, `REQ-KN-084`, `REQ-KN-104`, and `REQ-KN-129`.

- `REQ-KN-008`: source access failures must be visible as sanitized readiness/diagnostic states.
- `REQ-KN-015`: parser/model-health result remains the authoritative model-health state for this bounded intake.
- `REQ-KN-016`: model-health user visibility is prepared through sanitized output fields and tests.
- `REQ-KN-084`: package-internal source selection is constrained to recognized local project-state package contents.
- `REQ-KN-104`: local package source/canonical source record handling is prepared as read-only evidence only.
- `REQ-KN-129`: V1 lessons require fail-closed source intake and no implicit trust in raw source/material.

Supporting context only: `REQ-KN-081`, `REQ-KN-082`, and `REQ-KN-083` remain projection-context support and do not authorize layout/projection-trust expansion in this slice.

## Lifecycle / enabling trace

This is product behavior at a narrow read/parser-status boundary. It also produces enabling evidence for later parser/projection/readiness loops by proving that package-internal source can be read only under exact safety gates and normalized to the existing parser diagnostic loop.

## Architecture/readiness guidance

Use the hash-bound trace artifacts in frontmatter as the authority context. The relevant architecture boundaries are:

- `ICD-KVA-001`: package layout / package-internal source boundaries.
- `ICD-KVA-003`: parser/model-health envelope and sanitized diagnostic boundaries.
- `KVA-013`: allocation matrix for direct requirement traces.
- `KVA-031` and `KVA-032`: BEB/L2 preflight and evidence-readiness constraints.

## Required adversarial readiness card

The implementation and tests must cover these probes before BEO closeout:

1. **K2-019-AR-001 malformed source** — malformed/unbalanced/invalid source body feeds existing diagnostics and returns fail-closed `malformed`/unsafe metadata, not raw text.
2. **K2-019-AR-002 unreadable source** — stat/read/access failures become sanitized source-access/model-health states without raw OS errors, paths, stack traces, or thrown exceptions.
3. **K2-019-AR-003 path spoofing** — path traversal, unsupported extensions, non-regular selections, and directory marker spoofing cannot select arbitrary files or leak body text.
4. **K2-019-AR-004 hostile source-like metadata** — caller-supplied metadata fields such as `sourceText`, `content`, `path`, `diagnostics`, `providerPayload`, or authority booleans cannot override the actual read/parsing outcome.
5. **K2-019-AR-005 oversized source** — source bodies above the bounded intake limit fail closed with sanitized metadata and no partial raw body leakage.
6. **K2-019-AR-006 unsupported extension** — non-SysML/KerML files remain unsupported and are not read as source bodies.
7. **K2-019-AR-007 stale or conflicting package markers** — marker conflict/recovery-required package states do not authorize source-body intake.
8. **K2-019-AR-008 parser runtime unavailable** — runtime-unavailable remains fail-closed and does not read/write/adopt/repair source.
9. **K2-019-AR-009 source-body leakage prevention** — public objects, capability descriptors, errors, diagnostics, JSON output, and tests must prove raw source markers do not serialize back out.
10. **K2-019-AR-010 authority confinement** — source write/repair/adoption/import/export/provider/projection/layout/support/telemetry/RTM/blk-link/BEO-publication flags remain explicitly false.

## L2 creation guidance

Codex must implement with strict TDD: add failing assertions first in the allowed test files, run them to RED, then implement the smallest source changes. Prefer extending the existing modules rather than introducing a new broad service. The implementation may add narrow exported helpers/capability methods, but their public fields must be fixed and frozen. The source-body intake helper may use Node `fs`/`path` only in `src/main/project-package-inspection.mjs`; `src/main/parser-diagnostic-loop.mjs` must remain free of filesystem, process, network, provider, Electron, and package-manager access.

The expected product shape is a bounded read-only intake function that selects a single package-internal `.sysml` or `.kerml` source candidate from a ready single-file or ready directory-package shape, reads only that bounded source body, feeds it to the existing parser diagnostic loop, and returns sanitized metadata that combines source-access/intake status with parser/model-health output. The output must not include raw source body, raw path, filenames, directory listing, OS errors, stack traces, provider/prompt/credential data, source coordinates, parser handles, or mutation authority.

## Exact allowed files

Allowed modified files only:

- `src/main/project-package-inspection.mjs`
- `src/main/parser-diagnostic-loop.mjs`
- `tests/project-package-inspection.test.mjs`
- `tests/parser-diagnostic-loop.test.mjs`

No new files are authorized by this package. Do not modify `package.json`, renderer files, preload/Electron IPC files, roadmaps, traceability, docs, generated assets, dependency manifests, lockfiles, or hidden package artifacts during route execution.

## Verification commands and acceptance criteria

Codex should run and preserve evidence for:

- `node tests/project-package-inspection.test.mjs`
- `node tests/parser-diagnostic-loop.test.mjs`
- `node scripts/validate-foundation.mjs`
- `npm test` when feasible after the focused tests pass

Acceptance requires fixed/frozen public output keys, no source/body/path/filename leakage, fail-closed malformed/unreadable/oversized/unsupported/conflict cases, explicit denied-authority booleans, and source code scans proving the parser diagnostic module still has no filesystem/process/network/provider/Electron/package-manager access.

## blk-link / RTM stance

This package produces bounded product evidence only. It does not run RTM generation, production `blk-link`, protected-body read/scan/hash, BEO publication/signing/storage/ledger, drift rejection, or coverage truth. Later trace closure may consume the final BEO metadata after closeout, but not this pending BEB package alone.

## Denied adjacent behaviors

No project writes, canonical SysML/KerML mutation, source repair, source adoption, external-edit import/promotion, save/export/session persistence, provider/Agent A behavior, live provider payload retention, multi-file SysML resolution, broad parser/projection correctness claims, source-coordinate truth claims, layout trust, canvas/SVG rendering, support-bundle export, telemetry, package/dependency installation, network calls, Electron IPC/preload/renderer filesystem expansion, RTM generation, production `blk-link`, or BEO publication/signing/storage/ledger.
