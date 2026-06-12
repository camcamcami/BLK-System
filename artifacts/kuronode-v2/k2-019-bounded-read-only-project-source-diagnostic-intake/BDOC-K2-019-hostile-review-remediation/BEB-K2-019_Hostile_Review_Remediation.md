---
beb_id: "BEB-K2-019"
l2_id: "L2-K2-019"
artifact_stage: "BDOC-K2-019-hostile-review-remediation"
target_hash: "61c5d72dc01f15013c3a8a88f5691b9058e48181"
status: "approved_for_remediation_route"
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
  - kind: "route-evidence"
    id: "K2-019-initial-route-patch"
    version_hash: "sha256:8d4041212c03c8da3d9adf6a9e11d672318da986c47ae5200f879885c2a4112d"
  - kind: "route-evidence"
    id: "K2-019-initial-codex-final-message"
    version_hash: "sha256:61655bc820f991c1bd019943bd8e08281b692fc4f753ce5abbe6d6047ac7503c"
---
# BEB-K2-019 — Hostile Review Remediation

Remediate K2-019 bounded read-only project source diagnostic intake after hostile review of the initial governed route commit.

## Objective

Close the hostile-review blockers without expanding product authority:

1. Deny symlinked selected directories / symlinked selected packages before any source-body read.
2. Remove the dynamic `process.getBuiltinModule("node:fs")` source-read seam; use static `node:fs` imports only.
3. Ensure K2-019 public source-intake state/reason vocabulary is exported, frozen, exact-pinned by tests, and exact-pinned by `scripts/validate-foundation.mjs`.
4. Ensure `runProjectSourceDiagnosticIntake()` never returns nested mutation-authority-looking `safeMutationAllowed: true`; source-intake parser summaries must be read-only/non-mutating even when the diagnostic health is healthy.
5. Update stale comments/validator wording so the bounded source-body read is explicit and no parser runtime/process/provider/network/mutation authority is implied.

## Direct constraints

- Allowed product behavior remains bounded read-only local `.sysml` / `.kerml` source-body intake for diagnostic summary only.
- Forbidden: project/source mutation, parser process/runtime spawning, provider/network calls, shell/process execution, renderer filesystem authority, import/promotion, save/export, session persistence, RTM, `blk-link`, BEO publication/storage/signing/ledger, raw source-body return/retention.
- Do not add new product files.
- Keep one canonical visible `BEO-K2-019`; this remediation BEB/L2 is support evidence under `BDOC-K2-019`, not a second BEO.

## Required adversarial probes

- Selected directory symlink to a package containing `.kuronode-project` + `.sysml` must return denied/non-regular and must not read source bytes.
- Direct source symlink must remain denied.
- NUL and `..` path seams must deny before source read.
- Monkey-patching `process.getBuiltinModule` must not influence source intake and must not be called.
- Accepted healthy source intake must not leak raw source text and must have top-level and nested mutation/provider/runtime/publication authority flags false, including nested `safeMutationAllowed: false`.
- K2-019 exported public source-intake states/reasons must be exact frozen arrays and validation-gated.
