# BLK-SYSTEM-217 — Codex Exact Undo Exercise Sprint Closeout

**Status:** Complete
**Date:** 2026-05-17
**Commit:** this commit (`test: record Codex exact undo exercise`)

## 1. Objective

Plan and execute BLK-SYSTEM-217 as the exact undo/revert branch of the BLK-077/079 frontier: prove the BLK-SYSTEM-215 Codex-assisted Kuronode feature patch can be reversed exactly, while preserving BLK-121 Codex containment rules and denying reusable execution authority.

## 2. Files Changed

- `python/product_feature_loop_217.py`
- `python/test_product_feature_loop_217.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-217_sprint-closeout.md`

## 3. Implementation Summary

- Executed an external Codex exact-undo exercise in disposable Kuronode worktree `/tmp/kuronode-blk217-undo` at commit `35605698633d41c7fc5f0f84548a7b56e3782530`.
- Bound the BLK-SYSTEM-215 feature patch from parent `40f908b2a5d94991c2502018167d3a1c57031b2d` to merge commit `35605698633d41c7fc5f0f84548a7b56e3782530` across the exact BLK-215 file allowlist.
- Verified the patch was non-empty, matched SHA256 `sha256:088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e`, and passed `git apply --reverse --check`.
- Recorded Codex invocation evidence as external/advisory only: `gpt-5.5`, reasoning `high`, `danger-full-access` inside disposable external worktree, `-a never`, `--ephemeral`, `--ignore-user-config`, `--ignore-rules`, disabled hooks/plugins/goals, JSONL telemetry, and final-message capture.
- Added a deterministic BLK-SYSTEM-217 evidence package with authority-laundering guards, exact hash binding, and false side-effect flags.
- Advanced BLK-077/079 and the executable current-state index to the next frontier: third bounded Kuronode feature loop available after undo evidence, not granted.

BLK-SYSTEM-217 package hash:

```text
blk217_codex_exact_undo_package_hash=sha256:b730e69e4126377c4f726e3bfd9648e3c6478ac6bd21aa9ddc26d221ffa7c506
```

## 4. Verification

RED evidence was observed before implementation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_feature_loop_217
ModuleNotFoundError: No module named 'product_feature_loop_217'
FAILED (errors=1)
```

Codex exact-undo exercise evidence:

```text
codex-cli 0.130.0
Logged in using ChatGPT

codex --model gpt-5.5 -c model_reasoning_effort='"high"' -s danger-full-access -a never exec --ephemeral --ignore-user-config --ignore-rules --disable hooks --disable plugins --disable goals --json --output-last-message /tmp/blk217-codex-artifacts/final-message.md -C /tmp/kuronode-blk217-undo - < /tmp/blk217-codex-undo-prompt.md

sha256sum /tmp/blk217-codex-artifacts/events.jsonl /tmp/blk217-codex-artifacts/final-message.md /tmp/kuronode-blk217-undo-blk215.patch
9a768b0941f2a3ba699ad72ab2a5a1528e991ce89fdaa4d8ddabef7c77654e5a  /tmp/blk217-codex-artifacts/events.jsonl
8a850ea863c9b49f89f79d3fcff8804b96bd031d2795336911c98ed8cd7c7599  /tmp/blk217-codex-artifacts/final-message.md
088a62b1d73e0dec3f621ff2f44b62a3a94fa4f5998f2ef03a8915782a7a8b5e  /tmp/kuronode-blk217-undo-blk215.patch

git -C /tmp/kuronode-blk217-undo status --short --branch
## HEAD (no branch)
```

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_feature_loop_217 python.test_blk_current_state_authority_index
Ran 25 tests in 0.081s
OK
```

Post-closeout verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_feature_loop_217 python.test_blk_current_state_authority_index python.test_lean_documentation_policy
Ran 30 tests in 0.121s
OK
```

Full repository verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
Ran 1354 tests in 14.478s
OK (skipped=35)

go test ./...
ok  github.com/camcamcami/BLK-System/cmd/blk-pipe
ok  github.com/camcamcami/BLK-System/internal/contracts
ok  github.com/camcamcami/BLK-System/internal/engine
ok  github.com/camcamcami/BLK-System/internal/execguard
ok  github.com/camcamcami/BLK-System/internal/gitguard
ok  github.com/camcamcami/BLK-System/internal/pipe
ok  github.com/camcamcami/BLK-System/internal/runtimeguard
ok  github.com/camcamcami/BLK-System/internal/testutil
ok  github.com/camcamcami/BLK-System/internal/validation
ok  github.com/camcamcami/BLK-System/internal/validationprofiles

git diff --check -- <exact changed paths>
PASS
```

## 5. Hostile Review / Risk Check

Independent hostile review initially returned **BLOCKER** because this closeout did not yet exist while the lean documentation gate had been advanced to include BLK-SYSTEM-217. Remediation: created this single closeout and reran verification.

Hostile review findings after remediation:

- Authority laundering: denied authorities and false side-effect flags remain explicit; caller-controlled package fields reject Codex approval, BEO/RTM/publication, protected-body, package/network/tooling, and blanket source-mutation wording.
- Scope creep: the sprint records an exact undo exercise and current-state/frontier update only; it does not mutate Kuronode source or create a new BLK root document.
- Exact undo binding: full 40-character parent/merge commits, exact allowlist, non-empty patch, patch SHA256, reverse-apply check, advisory telemetry hashes, and clean final worktree status are recorded.
- Codex containment: Codex execution is recorded as external supervised evidence only. Native sandbox remains unavailable on this host; no production-isolation claim is made.
- Protected-body access: no protected BLK-req body read/copy/parse/hash/scan/migration authority is introduced.
- Source/Git mutation: no Kuronode commit was made, no tracked Kuronode mutation remained, and BLK-System source changes are limited to the sprint evidence/tests/docs listed above.

## 6. Authority Boundary

BLK-SYSTEM-217 does not grant live Codex dispatch, reusable Codex dispatch, tactical LLM dispatch, BLK-pipe dispatch/runtime, production BLK-test MCP, BEB dispatch, BEO closeout execution, BEO publication/signing/storage/ledger authority, RTM generation, production `blk-link`, drift rejection, coverage truth, active-vault comparison, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, package-manager/network/model/browser/cyber tooling, production-isolation claims, or blanket target/source/Git mutation.

The exact undo result is evidence that the BLK-SYSTEM-215 patch is reversible by the recorded patch; it is not reusable undo authority, not future Kuronode mutation authority, and not approval to execute the next feature loop.

## 7. Documentation Burden Check

No new BLK-### root document was created. BLK-SYSTEM-217 produced exactly one sprint outcome document: this closeout.
