# BLK-SYSTEM-335 — BEB/L2 Authorship Boundary Remediation Closeout

## Scope

Remediate stale BEB/L2 role-boundary wording found during hostile review after the dedicated `blkhermes` setup work. The correction keeps architect/system-engineer ownership of both BEB and L2 authorship and limits BLK-System to validation, hash-binding, manifest/SprintPayload route construction, and route enforcement.

## Changes

- Updated `docs/BLK-003_blk-pipe-blk-test-orchestration.md` so the architect/system-engineer agent owns BEB and L2 authorship.
- Updated `docs/BLK-077_blk-system-post-078-roadmap.md` so the Kuronode feature-drop lane no longer describes BLK-System as the L2 intent owner.
- Updated `docs/BLK-079_post-078-current-state-authority-index.md` so the active authority index states architect-authored BEB and L2 inputs.
- Updated `docs/outcomes/BLK-SYSTEM-334_sprint-closeout.md` to remove stale L2 ownership wording.
- Added regression coverage in `python/test_lean_documentation_policy.py` and updated `python/test_active_doctrine_review_gates.py` so stale L2 ownership wording fails closed.

## Boundary preserved

This remediation grants no BEB dispatch, no L2 authorship to BLK-System, no reusable Codex dispatch, no broad BLK-pipe dispatch, no production BLK-test MCP, no BEO publication, no RTM generation, no production or reusable `blk-link`, no protected-body access, no runtime/tooling authority, and no target/source/Git mutation authority outside BLK-System repository development.

## Hostile review

Independent hostile review of the first uncommitted diff found a blocker: active doctrine tests and BLK-077 / BLK-SYSTEM-334 still encoded the old L2 ownership model. This closeout records the remediation: stale wording was removed from active docs and the prior closeout, and regression gates now reject the old ownership phrases.

## Verification performed

- RED: `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python python3 -m unittest python.test_lean_documentation_policy.LeanDocumentationPolicyTest.test_beb_and_l2_authorship_boundary_stays_with_architect` failed on stale/missing BEB+L2 architect ownership wording.
- GREEN focused: same focused lean-policy test — OK.
- Active doctrine + lean/current-state focused suite: `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python python3 -m unittest python.test_active_doctrine_review_gates python.test_lean_documentation_policy python.test_blk_current_state_authority_index` — 168 tests OK, 34 skipped.
- Stale L2 ownership scan across Markdown docs: no matches for the old ownership phrases.
- Full Python module verification by chunks after monolithic discovery exceeded the 600s wrapper limit: all 163 `python/test_*.py` modules executed successfully, 1572 tests OK, 35 skipped.
- `git diff --check` — OK.
