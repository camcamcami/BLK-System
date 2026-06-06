# BLK-SYSTEM-215 — Supervised Codex Kuronode Feature Loop Sprint Closeout

**Status:** Complete
**Date:** 2026-05-17
**Commit:** this commit (`feat: record supervised Codex feature loop`)

## 1. Objective

Plan and execute the next bounded Kuronode feature sprint using Codex as an external Hermes-supervised tactical worker, then record exact BLK-System evidence without granting reusable internal Codex dispatch, BLK-pipe runtime, protected-body access, BEB/BEO execution authority, or blanket Kuronode source/Git mutation.

## 2. Files Changed

Kuronode target repo `/home/dad/code/Kuronode-v1`:

- `docs/execution briefs/BEB_215_Codex_Projection_Summary_Badges.md`
- `docs/execution briefs/BEO_215_Codex_Projection_Summary_Badges_Outcome.md`
- `packages/kuronode-graph/src/components/CanonicalDataGrid.tsx`
- `packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx`

BLK-System evidence repo `/home/dad/BLK-System`:

- `python/product_feature_loop_215.py`
- `python/test_product_feature_loop_215.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-215_sprint-closeout.md`

## 3. Implementation Summary

Kuronode commit `35605698633d41c7fc5f0f84548a7b56e3782530` merges Codex worker commit `148d74b57febe828be359511488b3379622d132c` onto parent `40f908b2a5d94991c2502018167d3a1c57031b2d`.

The feature:

- uses `GraphProjectionEngine.projectToTreeWithSummary(requirements, true)` in `CanonicalDataGrid`;
- keeps table rows sourced from `projection.rows`;
- keeps `{requirements.length} loaded` as backend DTO count;
- adds projected row count and max-depth badges;
- reports shared-trace and hierarchy-warning counts from full projected-tree summary output;
- adds component tests for nested multi-parent clone summary display and nested warning summary display;
- includes BEB/BEO artifacts in Kuronode for the supervised Codex sprint.

BLK-System records the feature loop as hash-bound package evidence:

- BLK-SYSTEM-215 package hash: `sha256:4e2d6bd3c7d7d452452fa5a018a8e649e7cf614a9d33158b2232ee40c68f83a4`;
- Kuronode parent commit: `40f908b2a5d94991c2502018167d3a1c57031b2d`;
- Kuronode Codex worker commit: `148d74b57febe828be359511488b3379622d132c`;
- Kuronode feature merge commit: `35605698633d41c7fc5f0f84548a7b56e3782530`;
- Kuronode feature patch hash: `sha256:088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e`;
- next frontier: `NEXT_FRONTIER_THIRD_BOUNDED_KURONODE_FEATURE_LOOP_OR_OPERATOR_SELECTED_UNDO_NOT_GRANTED`.

## 4. Verification

Kuronode verification:

```bash
npm run test -w @kuronode/kuronode-graph -- src/components/CanonicalDataGrid.test.tsx
# 1 file passed, 2 tests passed

npm run test -w @kuronode/kuronode-graph -- tests/GraphProjectionEngine.test.ts src/components/CanonicalDataGrid.test.tsx
# 2 files passed, 10 tests passed

npm run test -w @kuronode/kuronode-graph
# 16 files passed, 53 tests passed

npm run build -w @kuronode/kuronode-graph
# built successfully; existing non-blocking Vite chunk warnings only
```

Undo/reverse-patch verification:

```bash
git diff --binary 40f908b2a5d94991c2502018167d3a1c57031b2d 35605698633d41c7fc5f0f84548a7b56e3782530 -- 'packages/kuronode-graph/src/components/CanonicalDataGrid.tsx' 'packages/kuronode-graph/src/components/CanonicalDataGrid.test.tsx' 'docs/execution briefs/BEB_215_Codex_Projection_Summary_Badges.md' 'docs/execution briefs/BEO_215_Codex_Projection_Summary_Badges_Outcome.md' > /tmp/kuronode-blk215.patch
test -s /tmp/kuronode-blk215.patch
printf '088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e  /tmp/kuronode-blk215.patch\n' | sha256sum --check --strict -
git apply --reverse --check /tmp/kuronode-blk215.patch
```

Patch digest check returned `/tmp/kuronode-blk215.patch: OK`; reverse-apply check passed without undoing committed work.

Kuronode MCP closeout review was run through the repo MCP stdio server in strict mode and returned `PASS` for existing requirements `R-UIX-040`, `R-PRJ-048` and existing use case `UC-REQ-004`. No new requirement or use case was introduced.

BLK-System focused package/current-state verification:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_feature_loop_215 python.test_blk_current_state_authority_index python.test_lean_documentation_policy
# Ran 29 tests — OK
```

Repository-wide verification was run after closeout creation:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
# Ran 1339 tests in 14.471s — OK (skipped=35)

go test ./...
# all Go packages OK

git diff --check
# clean
```

## 5. Hostile Review / Risk Check

Kuronode hostile review found no blockers. One nonblocking test-strength suggestion was remediated before commit by asserting `CanonicalDataGrid` calls `projectToTreeWithSummary(requirements, true)` and does not call legacy `projectToTree` for the summary badge path.

BLK-System hostile checks covered:

- full 40-character Kuronode parent, Codex-worker, and merge commit binding;
- exact allowed-file scope;
- non-empty exact-file reverse patch hash binding;
- executable SHA256 check plus reverse-apply verification;
- explicit separation between one external supervised Codex run and reusable BLK-System live Codex dispatch authority;
- caller-controlled notes/evidence refs recursively scanned for live-Codex, BLK-test PASS-as-approval, protected path/body, package-manager/tooling, BEO/RTM, and blanket source mutation laundering;
- all inherited denied-authority false flags remained explicit false.

## 6. BEB/BEO Evidence Boundary

Kuronode contains BEB/BEO artifacts for this feature sprint. BLK-System records them as sprint evidence only. This is not BLK-System BEB dispatch, BEO closeout execution, BEO publication/signing/storage/ledger authority, RTM generation, production `blk-link`, or protected BLK-req body access.

## 7. Authority Boundary

BLK-SYSTEM-215 records one external Hermes-supervised Codex worker run and the exact resulting Kuronode feature merge commit. It does not grant reusable BLK-System live Codex dispatch, tactical LLM dispatch, BLK-pipe runtime/dispatch, production BLK-test MCP, BEO closeout execution/publication, RTM generation, drift/coverage truth, active-vault comparison, protected BLK-req body read/copy/parse/hash/scan, blanket future Kuronode source/Git mutation, package/network/model/browser/cyber tooling, or production-isolation claims.

## 8. Documentation Burden Check

No new `docs/BLK-###` document was created. This is the single BLK-SYSTEM-215 sprint outcome. Active roadmap/index updates were kept lean and moved only the current feature-loop frontier.
