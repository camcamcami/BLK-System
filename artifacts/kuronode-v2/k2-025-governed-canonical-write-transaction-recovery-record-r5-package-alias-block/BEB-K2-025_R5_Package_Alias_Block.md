---
beb_id: "BEB-K2-025"
beo_id: "BEO-K2-025"
l2_id: "L2-K2-025"
trace_artifacts:
  - kind: "roadmap"
    id: "K2-IMPLEMENTATION-ROADMAP"
    version_hash: "sha256:a1458fc73ad0c230ca54d0619d2fe16ef00d7d309557ee34287b22dc64592285"
  - kind: "product_convergence_map"
    id: "K2-PRODUCT-CONVERGENCE-MAP"
    version_hash: "sha256:bc70f88549b0939395495861a3797d4d42fcf72b584926927712700c00c69cb9"
  - kind: "prior_outcome"
    id: "BEO-K2-024"
    version_hash: "sha256:6ff0947cb7526aa2c1c2daae65525743475bc8477ddfa6d2f2ee6fbaee41fdd1"
  - kind: "prior_outcome"
    id: "K2-024-SPRINT-CLOSEOUT"
    version_hash: "sha256:36e14e8e5abee9d13992716b88bc68c8ec3a10d35697750c4ea387db06fcabaa"
  - kind: "requirement"
    id: "REQ-KN-072"
    version_hash: "sha256:b26e55993345b2b07bb1d31d62fa0f33280b684cfc764603d0cbec4c7447bd20"
  - kind: "requirement"
    id: "REQ-KN-073"
    version_hash: "sha256:6e43197e174704f0c2ec5d401fbf2c0e83743dfc0727e0f3ef5194a80a09b19c"
  - kind: "requirement_supporting"
    id: "REQ-KN-134"
    version_hash: "sha256:8778997655ffb3c2650a27a2814f97cf386a0a3b679c09b2b6bf43d39c5f8a67"
  - kind: "requirement_supporting"
    id: "REQ-KN-135"
    version_hash: "sha256:2d026cd78ba7681c47fe18a81deeb0f51511fb416ef578acc1e771611ac68f84"
---
# BEB-K2-025 — R5 Package Path-Alias Blocker Remediation

This exact BLK-pipe remediation targets only the remaining R4 hostile-review blocker: package-side singleton path aliases (`targetPaths`, `packagePaths`, `targetPackagePaths`, `files`) still committed when they exactly matched the controlled fixture path. K2-025 must treat those package-side aliases as unsupported/ambiguous evidence and fail closed; the only accepted package path field is `targetPackagePath` equal to `fixtures/k2-025/single-file.sysml`.

Do not change the public K2-025 output vocabulary or broaden scope. Denied authorities remain unchanged: no real file IO, provider/network/runtime/parser execution, broad source/Git mutation, BEO publication, RTM generation, production blk-link, or fallback.

Allowed modified files: `src/shared/governed-write-transaction.mjs`, `tests/governed-write-transaction.test.mjs`, `scripts/validate-foundation.mjs`.
Allowed new files: none.

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
