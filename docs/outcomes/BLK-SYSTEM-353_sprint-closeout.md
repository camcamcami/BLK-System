# BLK-SYSTEM-353 — Codex xhigh Route Contract Sprint Closeout

**Status:** Complete
**Date:** 2026-06-07
**Commit:** this commit (`fix: set BLK Codex route to xhigh`)

## 1. Objective

Change the BLK-System-owned Kuronode BEB-L2/Codex route contract so future routed Codex runs use `gpt-5.5` with `xhigh` reasoning by default, while preserving the closed route boundary: drop manifests still cannot provide `engine_args`, model choice, reasoning effort, validation commands, or L2 packet text.

This sprint also updates the private-bwrap smoke/rebuild documentation so operator-facing setup evidence matches the new route expectation.

## 2. Files Changed

- `python/beb_l2_blk_pipe_route.py`
- `python/test_beb_l2_blk_pipe_route.py`
- `python/codex_private_bwrap_setup.py`
- `python/test_codex_private_bwrap_setup_229.py`
- `python/test_lean_documentation_policy.py`
- `docs/runbooks/codex-private-bwrap-apparmor.md`
- `docs/BLK-121_codex-configuration-and-containment-contract.md`
- `docs/outcomes/BLK-SYSTEM-353_sprint-closeout.md`

## 3. Implementation Summary

- `build_kuronode_codex_engine_args(...)` now defaults to `model="gpt-5.5"` and `reasoning_effort="xhigh"`.
- The route rejects alternate model/reasoning requests, including the previous `high` value, so caller manifests cannot downgrade or override the BLK-System-owned tactical engine contract.
- The injected Codex argv now includes `-c model_reasoning_effort="xhigh"` as a direct argv element, preserving TOML string semantics without shell-dependent quoting.
- The BLK-SYSTEM-229 private-bwrap setup summary and runbook smoke command now use `model_reasoning_effort='"xhigh"'` with `--sandbox workspace-write`.
- The active Codex configuration contract in `docs/BLK-121_codex-configuration-and-containment-contract.md` records the xhigh update without converting configuration doctrine into runtime approval.
- Lean-documentation gates now include sprint 353 closeout coverage.

## 4. Verification

TDD RED evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_codex_args_are_not_caller_controlled
# FAILED: expected model_reasoning_effort="xhigh" but observed model_reasoning_effort=high

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_codex_private_bwrap_setup_229.CodexPrivateBwrapSetup229Test.test_setup_summary_documents_rebuild_without_hostwide_sysctl_relaxation \
  python.test_codex_private_bwrap_setup_229.CodexPrivateBwrapSetup229Test.test_runbook_and_script_document_recreate_setup
# FAILED: setup summary/runbook still documented model_reasoning_effort='"high"'

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_lean_documentation_policy.LeanDocumentationPolicyTest.test_new_sprints_use_one_outcome_only
# FAILED: BLK-SYSTEM-353 closeout missing
```

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_beb_l2_blk_pipe_route.BebL2BlkPipeRouteTest.test_codex_args_are_not_caller_controlled \
  python.test_codex_private_bwrap_setup_229.CodexPrivateBwrapSetup229Test.test_setup_summary_documents_rebuild_without_hostwide_sysctl_relaxation \
  python.test_codex_private_bwrap_setup_229.CodexPrivateBwrapSetup229Test.test_runbook_and_script_document_recreate_setup
# Ran 3 tests in 0.001s — OK

PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  python.test_beb_l2_blk_pipe_route \
  python.test_codex_private_bwrap_setup_229 \
  python.test_product_codex_config_containment_216
# Ran 52 tests in 0.584s — OK
```

Final closeout verification evidence:

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_lean_documentation_policy.LeanDocumentationPolicyTest.test_new_sprints_use_one_outcome_only python.test_lean_documentation_policy.LeanDocumentationPolicyTest.test_current_closeouts_do_not_keep_pending_verification_or_review_placeholders
# Ran 2 tests in 0.181s — OK

go test ./...
# ok for 10 Go packages, including internal/pipe and internal/execguard

python3 /var/tmp/blk-system-chunked-unittest.py
# 166 modules enumerated. Chunks 1-8 passed (160 modules). Chunk 9 timed out as a group; split results passed 5/6 modules and timed out on the known long side-effect trace module after emitting progress.
# modules_passed=165 before the long-module rerun.

TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_verified_loop_beo_publication_side_effect_trace_closure_330_333
# Ran 6 tests in 284.107s — OK

git diff --check -- python/beb_l2_blk_pipe_route.py python/test_beb_l2_blk_pipe_route.py python/codex_private_bwrap_setup.py python/test_codex_private_bwrap_setup_229.py python/test_lean_documentation_policy.py docs/runbooks/codex-private-bwrap-apparmor.md docs/BLK-121_codex-configuration-and-containment-contract.md docs/outcomes/BLK-SYSTEM-353_sprint-closeout.md
# OK
```

## 5. Hostile Review / Risk Check

Independent hostile-review verdict: PASS.

Evidence from hostile review:

- The live route still forbids caller manifest fields including `engine`, `engine_args`, `engine_command`, `validation_commands`, `l2_packet`, and `trace_artifacts`.
- `python/beb_l2_blk_pipe_route.py` defaults to `gpt-5.5` + `xhigh`, rejects alternate model/reasoning, and injects `--sandbox workspace-write` plus `model_reasoning_effort="xhigh"`.
- Live dispatch hard-codes `engine="codex"` and calls `build_kuronode_codex_engine_args(...)`; no caller model/reasoning is threaded into dispatch.
- Tests assert `model_reasoning_effort="xhigh"`, reject `high`/`low`, reject `gpt-5.4`, require `workspace-write`, and forbid `danger-full-access` / bypass flags in the live route.
- Private-bwrap setup docs use `gpt-5.5`, `model_reasoning_effort='"xhigh"'`, and `--sandbox workspace-write`; host-wide AppArmor relaxation remains forbidden.
- `docs/BLK-121` continues to deny reusable Codex dispatch, BLK-pipe dispatch authority, BEO/RTM/`blk-link` authority, protected-body authority, package/network/model/browser/cyber tooling, and production-isolation claims.

Nonblocking observations:

- Historical fixtures from older external-containment sprints still record `high`/`danger-full-access` as historical evidence. They are not the live BEB-L2 BLK-pipe route.
- `docs/BLK-121` still contains an external-containment `danger-full-access` shape for the older fallback doctrine. This sprint does not broaden that fallback and the live route remains `workspace-write`.

Blockers: none.

## 6. Authority Boundary

This sprint authorizes only a BLK-System repository development change to the deterministic Codex invocation contract.

It does not grant:

- caller-controlled Codex model, reasoning effort, engine args, validation commands, L2 body, or trace artifacts;
- broad or reusable BLK-pipe/Codex dispatch authority;
- `danger-full-access` in the live BEB-L2/BLK-pipe route;
- package-manager, network, browser, model-service, cyber tooling, or production-isolation claims;
- BEO publication or closeout execution;
- RTM generation or production `blk-link`;
- protected-body reads/copying/parsing/hashing/scanning;
- target/source/Git mutation outside exact approved route allowlists.

## 7. Documentation Burden Check

No new root `docs/BLK-###` sprint document was created. The only new sprint outcome is this single closeout. The existing durable Codex configuration contract and private-bwrap runbook were updated because they are the normative operator-facing references for Codex invocation shape and sandbox setup.
