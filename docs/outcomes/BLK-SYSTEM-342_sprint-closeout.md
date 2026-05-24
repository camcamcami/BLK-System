# BLK-SYSTEM-342 — Repo-Local Agent Instructions Sprint Closeout

**Status:** Complete
**Date:** 2026-05-24
**Commit:** this commit (`docs: add repo-local agent instructions`)

## 1. Objective

Add a repo-local agent instruction file so future Hermes, `blkhermes`, Codex-adjacent, or collaborator agents entering the repository have the BLK-System operating contract immediately available from the worktree.

The instruction file makes the V-Model / system-of-systems framing explicit, preserves the architect/executor role split, names the expected skills, and gives `blkhermes` a durable communication contract.

## 2. Files Changed

- `AGENTS.md`
- `README.md`
- `python/test_lean_documentation_policy.py`
- `docs/outcomes/BLK-SYSTEM-342_sprint-closeout.md`

## 3. Implementation Summary

Created `AGENTS.md` with these repo-local instructions:

- BLK-System is framed as a local-first control loop for AI-assisted development, aligned with the Systems Engineering V-Model.
- Agents must load `blk-system-sprint-execution` and `blk-system-authority-gated-sprints` for BLK-System work.
- `hermes-agent` is required when changing Hermes profile, gateway, tool, skill, or setup behavior.
- Architect/System Engineer Hermes owns requirements, BEB, L2, acceptance boundaries, and architecture intent.
- BLK-System validates, schema-checks, hash-binds, routes, and records evidence from architect-authored inputs.
- `blkhermes` is documented as the dedicated executor/status-relay profile.
- Product/runtime gates remain separate from BLK-System repository development authority.
- `blkhermes` progress relay should report only meaningful milestones and avoid scheduled status spam.
- Secrets and runtime profile state stay out of the repository.

Updated `README.md` so `AGENTS.md` appears in the repository layout and starter document list.

Extended the lean documentation policy range through BLK-SYSTEM-342 so this sprint has the same one-closeout and stale-placeholder coverage as recent sprints.

## 4. Verification

- Docs/link/secret/trailing-whitespace check: OK.
- Hostile review script for AGENTS/README authority claims: PASS.
- `python3 -m unittest python.test_lean_documentation_policy`: OK.
- `git diff --check -- AGENTS.md README.md python/test_lean_documentation_policy.py docs/outcomes/BLK-SYSTEM-342_sprint-closeout.md`: OK.

## 5. Hostile Review / Risk Check

The hostile review checked that the new instructions do not launder evidence into authority, do not treat PASS/green tests as approval, do not authorize BEO publication, RTM generation, production `blk-link`, protected-body access, or runtime/tooling expansion, and preserve the no-invention boundary for missing BEB/L2 intent.

The review also checked that README remains product-name agnostic and that the new instruction file includes the required denial markers, `blkhermes` profile guidance, and status-spam avoidance contract.

## 6. Authority Boundary

This sprint is documentation and policy-gate alignment only.

It grants no BEO publication, no BEO closeout execution, no RTM generation, no production `blk-link`, no run-ID reservation or consumption, no signer/storage/ledger action, no protected-body access, no BLK-test MCP/runtime/tooling expansion, no target/source/Git mutation outside ordinary BLK-System repository development, and no production-isolation claim.

## 7. Documentation Burden Check

No new root BLK doctrine document was created. The sprint used one repo-local instruction file and one lean outcome closeout.
