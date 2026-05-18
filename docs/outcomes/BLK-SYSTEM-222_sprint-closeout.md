# BLK-SYSTEM-222 — BEB-L2 to BLK-pipe/Codex Route Closeout

**Status:** Complete
**Date:** 2026-05-18T09:36:20+10:00
**Commit:** this commit (feat: route BEB-L2 drops through Codex)

## 1. Objective
Make the BEB-L2 → BLK-pipe/Codex route real, testable, and difficult to bypass accidentally after BLK-SYSTEM-221 exposed a process failure: a Kuronode feature landed without Codex participation.

## 2. Files Changed
- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `python/blk_pipe_adapter.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-222_sprint-closeout.md`

## 3. Implementation Summary
- Added a closed-schema drop route that accepts only exact BEB/L2 manifest fields for Kuronode work.
- The route requires trusted configuration for approved manifest hashes, allowed Kuronode work directories, and trusted BEB/L2/drop roots; drop manifests cannot self-authorize arbitrary repos or retarget themselves after approval.
- The approved manifest binds the BEB path/hash, L2 path/hash, target branch/hash, validation profiles, and allowlists as one exact tuple.
- BLK-System injects `engine="codex"` and exact `codex exec -` arguments itself, including `--model gpt-5.5`, `model_reasoning_effort=high`, `--ephemeral`, `--ignore-user-config`, and `--ignore-rules`; alternate model/reasoning kwargs are rejected.
- Drop manifests cannot supply `engine`, `engine_args`, `engine_command`, `validation_commands`, `l2_packet`, or `trace_artifacts`; route-level validation also rejects unknown validation profiles and broad/glob/protected allowlist entries before BLK-pipe dispatch.
- Added a deterministic one-shot inbox dispatcher: successful drops move to a processed directory; rejected drops move to failed with an error diagnostic.
- Updated active roadmap/current-state docs to make BLK-SYSTEM-222 the current route and preserve the next frontier as exact-payload-only, not blanket authority.

## 4. Verification
Focused RED/GREEN evidence:
- RED: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route -v` failed before implementation with `ModuleNotFoundError: No module named 'beb_l2_blk_pipe_route'`.
- GREEN: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route -v` → `Ran 9 tests ... OK`.
- Focused route/current-state/lean suite: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_beb_l2_blk_pipe_route python.test_blk_current_state_authority_index python.test_lean_documentation_policy -v` → `Ran 32 tests ... OK`.
- Full Python suite: `PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'` → `Ran 1387 tests in 14.590s; OK (skipped=35)`.
- Go suite: `go test ./...` → OK for all Go packages.
- Whitespace gate: `git diff --check -- <exact changed paths>` → no output.

Package hash:
- `blk222_beb_l2_blk_pipe_codex_route_hash=sha256:52b85fd75fb2542ed9aa05ec790986bbf40e21ea178d5c6c6f07a245e10b55fa`

## 5. Hostile Review / Risk Check
- Workdir/target bypass: blocked by trusted configuration for approved manifest hashes and allowed Kuronode work directories plus mandatory pinned `target_hash`; branch-only execution is rejected before BLK-pipe.
- Engine bypass: blocked by rejecting manifest-supplied `engine`, `engine_args`, and `engine_command` before adapter invocation.
- Hermes-direct bypass: the official BEB-L2 drop path has no field that can name Hermes or a shell engine; Codex is injected by BLK-System code.
- Validation-command injection: blocked by rejecting `validation_commands` and unknown validation profiles; route passes only repository-owned validation profile names.
- Broad allowlists: route rejects absolute paths, traversal, glob/pathspec-like entries, directory-wide `.` entries, and protected BLK-req doc paths before BLK-pipe dispatch.
- L2 substitution: blocked by requiring manifest BEB/L2 IDs, BEB frontmatter IDs, L2 packet text markers, and pinned BEB/L2 content hashes to agree before dispatch.
- Trace spoofing by manifest: blocked by rejecting manifest-supplied `trace_artifacts`; trace entries are derived only after BEB hash verification.
- Authority laundering: docs preserve exact-payload-only language and deny broad BLK-pipe dispatch, reusable live Codex authority, protected-body access, RTM/BEO authority, runtime/tooling authority, and production-isolation claims.

## 6. Authority Boundary
BLK-SYSTEM-222 creates a runnable/testable route, not blanket runtime authority. It does not grant broad BEB dispatch, BEO closeout execution, reusable live Codex dispatch, reusable BLK-pipe runtime, broad target/source/Git mutation, protected-body reads/copying/parsing/hashing/scanning/mutation, RTM generation, production `blk-link`, production BLK-test MCP, package/network/model/browser/cyber tooling, persistent host policy, or production-isolation authority.

Each Kuronode feature still needs an exact BEB/L2 drop payload with approved manifest hash, pinned BEB hash, L2 hash, target hash, trusted root, and trusted workdir configuration plus the current Codex containment decision: native workspace-write only after an active-session recheck, otherwise external containment.

## 7. Documentation Burden Check
No new BLK-### root document was created. BLK-001..006 were not touched. This sprint produced one outcome document only: `docs/outcomes/BLK-SYSTEM-222_sprint-closeout.md`.
