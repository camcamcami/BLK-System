# BLK-SYSTEM-220 — Native Codex Sandbox Repair/Recheck Sprint Closeout

**Status:** Complete
**Date:** 2026-05-18
**Commit:** this commit (`test: record native Codex sandbox repair recheck`)

## 1. Objective

Execute the operator-approved host-admin Codex native sandbox repair/recheck path after BLK-SYSTEM-219 identified that native `workspace-write` was blocked by host policy.

The sprint goal was to determine the minimal host change set that makes unshare, bubblewrap, and a non-mutating Codex `workspace-write` smoke pass, while preserving BLK-System authority cutlines.

## 2. Files Changed

- `python/product_codex_native_sandbox_repair_recheck_220.py`
- `python/test_product_codex_native_sandbox_repair_recheck_220.py`
- `python/test_product_codex_native_sandbox_mitigation_219.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_lean_documentation_policy.py`
- `python/test_product_codex_config_containment_216.py`
- `python/test_blk_pipe_bounded_enforcement_204_206.py`
- `python/test_blk_req_production_gateway_195_199.py`
- `python/test_kuronode_blk_req_mapping_201_203.py`
- `python/test_kuronode_blk_req_vault_bootstrap_200.py`
- `python/test_metadata_rtm_post_generation_ladder_159_162.py`
- `python/test_post_metadata_rtm_blk_link_reconciliation_review.py`
- `python/test_production_blk_link_rtm_trace_closure_authority_request_165.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-220_sprint-closeout.md`

## 3. Implementation Summary

BLK-SYSTEM-220 records a deterministic evidence package with package hash:

```text
sha256:9d63c4b7d99615db812e3751718574ce96cf101fc755af6d50ccc50d7f10146e
```

Observed pre-repair state:

```text
newuidmap=missing
newgidmap=missing
kernel.apparmor_restrict_unprivileged_userns = 1
unshare --user --map-current-user true -> uid_map EPERM
bwrap full namespace smoke -> bwrap: loopback: Failed RTM_NEWADDR
codex sandbox linux -> bwrap: loopback: Failed RTM_NEWADDR
```

Operator-performed host-admin repair/recheck:

```text
uidmap installed: /usr/bin/newuidmap and /usr/bin/newgidmap mode 4755 root:root
runtime-only sysctl: kernel.apparmor_restrict_unprivileged_userns=0
```

Passing smoke evidence under that runtime host state:

```text
unshare_map_current_rc=0
unshare_map_root_rc=0
bwrap_user_rc=0
bwrap_net_rc=0
bwrap_full_rc=0
codex_exec_workspace_write_rc=0
codex_exec_last_message=CODEX_WORKSPACE_WRITE_SMOKE_OK
```

The runtime AppArmor userns relaxation was restored after the test:

```text
kernel.apparmor_restrict_unprivileged_userns = 1
unshare --user --map-current-user true -> uid_map EPERM
bwrap full namespace smoke -> bwrap: loopback: Failed RTM_NEWADDR
```

Therefore the engineering result is: native Codex `workspace-write` is validated under a specific host-admin runtime state, but it is not currently always-on and not a reusable BLK-System Codex dispatch authority. Before any future native `workspace-write` run, the active session must pass the uidmap/AppArmor/unshare/bwrap/Codex smoke; otherwise use external containment.

## 4. Verification

Focused RED/GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_codex_native_sandbox_repair_recheck_220
```

Initial result before implementation: module import failed as expected.

Focused post-implementation verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_codex_native_sandbox_repair_recheck_220 python.test_product_codex_native_sandbox_mitigation_219 python.test_blk_current_state_authority_index python.test_product_codex_config_containment_216
```

Result:

```text
Ran 36 tests in 0.108s
OK
```

Final verification after closeout/doc gate:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
Ran 1371 tests in 16.113s
OK (skipped=35)
```

```text
go test ./...
ok github.com/camcamcami/BLK-System/cmd/blk-pipe (cached)
ok github.com/camcamcami/BLK-System/internal/contracts (cached)
ok github.com/camcamcami/BLK-System/internal/engine (cached)
ok github.com/camcamcami/BLK-System/internal/execguard (cached)
ok github.com/camcamcami/BLK-System/internal/gitguard (cached)
ok github.com/camcamcami/BLK-System/internal/pipe (cached)
ok github.com/camcamcami/BLK-System/internal/runtimeguard (cached)
ok github.com/camcamcami/BLK-System/internal/testutil (cached)
ok github.com/camcamcami/BLK-System/internal/validation (cached)
ok github.com/camcamcami/BLK-System/internal/validationprofiles (cached)
```

```text
git diff --check -- <exact changed paths>
clean
```

## 5. Hostile Review / Risk Check

Local and independent hostile review conclusions:

- Independent hostile review initially returned FAIL on two closeout/documentation blockers: stale verification placeholder text and an extra read-only file in the changed-file list. Both were remediated before final verification; re-review returned PASS with no concrete blockers.
- Minor hardening from hostile review was applied: the BLK-SYSTEM-220 validator and tests now assert restored `bwrap_full_rc=1`, not only restored unshare failure.
- PASS evidence is scoped to the runtime host state where `kernel.apparmor_restrict_unprivileged_userns=0` and `uidmap` exists.
- The package records `persisted_sysctl_change=False` and `native_sandbox_currently_available=False` after the runtime-only recheck restored the AppArmor sysctl to `1`.
- Codex `workspace-write` smoke is not treated as reusable BLK-System live Codex dispatch, broad source/Git mutation authority, package/network/model/browser/cyber tooling authority, BLK-pipe authority, or production-isolation proof.
- Caller-controlled notes/evidence refs are scanned for sandbox, tooling, protected-body, BEO/RTM, and production authority laundering.
- Active docs move the next frontier to bounded Kuronode feature work with native workspace-write only after active-session recheck PASS, otherwise external containment.

## 6. Authority Boundary

This sprint does not grant:

- persistent host-policy change;
- reusable Codex dispatch;
- one-off or reusable BLK-System live Codex subprocess authority;
- broad source/Git mutation;
- package-manager, network, model-service, browser, or cyber tooling;
- production-isolation claim;
- BLK-pipe runtime outside separately approved exact payloads;
- production BLK-test MCP;
- BEB dispatch or BEO closeout execution;
- BEO publication/signing/storage/ledger reuse;
- RTM generation, drift rejection, coverage truth, protected-body access, or blanket production `blk-link`.

## 7. Documentation Burden Check

No new root `docs/BLK-###` document was created. The sprint produced exactly one outcome document: this closeout.
