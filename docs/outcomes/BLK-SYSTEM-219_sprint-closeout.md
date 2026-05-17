# BLK-SYSTEM-219 — Native Codex Sandbox Mitigation Sprint Closeout

**Status:** Complete
**Date:** 2026-05-18
**Commit:** this commit (`test: record native Codex sandbox mitigation`)

## 1. Objective

Plan and execute native Codex sandbox mitigation for BLK-System after the BLK-SYSTEM-216/218 evidence showed Codex CLI 0.130.0 native Linux sandboxing failed on this host with bubblewrap errors.

The sprint objective was bounded: reproduce and diagnose the native sandbox failure, record deterministic fail-closed mitigation evidence, keep external containment as the active Codex mode, and update active current-state guidance without mutating host configuration or granting live/reusable Codex dispatch.

## 2. Files Changed

- `python/product_codex_native_sandbox_mitigation_219.py`
- `python/test_product_codex_native_sandbox_mitigation_219.py`
- `python/blk_current_state_authority_index.py`
- `python/test_blk_current_state_authority_index.py`
- `python/test_product_codex_config_containment_216.py`
- `python/test_lean_documentation_policy.py`
- `python/test_blk_pipe_bounded_enforcement_204_206.py`
- `python/test_blk_req_production_gateway_195_199.py`
- `python/test_kuronode_blk_req_mapping_201_203.py`
- `python/test_kuronode_blk_req_vault_bootstrap_200.py`
- `python/test_metadata_rtm_post_generation_ladder_159_162.py`
- `python/test_post_metadata_rtm_blk_link_reconciliation_review.py`
- `python/test_production_blk_link_rtm_trace_closure_authority_request_165.py`
- `docs/BLK-077_blk-system-post-078-roadmap.md`
- `docs/BLK-079_post-078-current-state-authority-index.md`
- `docs/outcomes/BLK-SYSTEM-219_sprint-closeout.md`

## 3. Implementation Summary

BLK-SYSTEM-219 reproduced the native sandbox failure and recorded the root-cause/mitigation package as deterministic local evidence:

- Codex CLI: `codex-cli 0.130.0`
- bubblewrap: `bubblewrap 0.9.0`
- kernel/userns sysctls: `kernel.unprivileged_userns_clone = 1`, `user.max_user_namespaces = 63858`, `user.max_net_namespaces = 63858`
- AppArmor restriction marker: `kernel.apparmor_restrict_unprivileged_userns = 1`
- `unshare -Ur true`: `write failed /proc/self/uid_map: Operation not permitted`
- direct bwrap user namespace: `bwrap: setting up uid map: Permission denied`
- direct bwrap network namespace and Codex sandbox smoke: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`

The resulting mitigation decision is fail-closed:

```text
BLK_SYSTEM_219_NATIVE_CODEX_SANDBOX_MITIGATION_RECORDED
EXTERNAL_CONTAINMENT_REQUIRED
NO_NATIVE_WORKSPACE_WRITE_UNTIL_UNSHARE_BWRAP_CODEX_SMOKE_PASS
NO_HOST_CONFIGURATION_MUTATION_BY_THIS_SPRINT
NO_PRODUCTION_ISOLATION_CLAIM
```

BLK-SYSTEM-219 package hash:

```text
blk219_native_codex_sandbox_mitigation_hash=sha256:710dd82eabda1f2d792dfc8cce2af88612603ea0b1683e5ad644bc1453312404
```

The active next frontier is now:

```text
NEXT_FRONTIER_OPERATOR_SELECTED_BOUNDED_KURONODE_FEATURE_WITH_EXTERNAL_CONTAINMENT_OR_HOST_ADMIN_SANDBOX_REPAIR_NOT_GRANTED
```

## 4. Verification

Host reproduction / diagnosis commands:

```bash
codex --version
bwrap --version
sysctl kernel.unprivileged_userns_clone user.max_user_namespaces user.max_net_namespaces
sysctl kernel.apparmor_restrict_unprivileged_userns kernel.apparmor_restrict_unprivileged_unconfined
unshare -Ur true
unshare -Urn true
bwrap --unshare-user --ro-bind / / true
bwrap --unshare-net --ro-bind / / true
CODEX_HOME=<temp-config> codex sandbox linux --permissions-profile blk-smoke -C /home/dad/BLK-System true
```

Observed host evidence:

```text
codex-cli 0.130.0
bubblewrap 0.9.0
kernel.unprivileged_userns_clone = 1
user.max_user_namespaces = 63858
user.max_net_namespaces = 63858
kernel.apparmor_restrict_unprivileged_userns = 1
unshare: write failed /proc/self/uid_map: Operation not permitted
bwrap: setting up uid map: Permission denied
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
codex sandbox rc=1 with bwrap loopback RTM_NEWADDR failure
```

RED evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_codex_native_sandbox_mitigation_219
ModuleNotFoundError: No module named 'product_codex_native_sandbox_mitigation_219'
FAILED (errors=1)
```

Focused GREEN evidence:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_codex_native_sandbox_mitigation_219
Ran 5 tests
OK
```

Current-state / lean-doc verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_product_codex_native_sandbox_mitigation_219 python.test_blk_current_state_authority_index python.test_lean_documentation_policy python.test_product_codex_config_containment_216
Ran 36 tests in 0.125s
OK
```

Historical active-frontier compatibility verification after advancing BLK-077/079:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest \
python.test_blk_pipe_bounded_enforcement_204_206 \
python.test_blk_req_production_gateway_195_199 \
python.test_kuronode_blk_req_vault_bootstrap_200 \
python.test_kuronode_blk_req_mapping_201_203 \
python.test_metadata_rtm_post_generation_ladder_159_162 \
python.test_post_metadata_rtm_blk_link_reconciliation_review \
python.test_production_blk_link_rtm_trace_closure_authority_request_165 \
python.test_product_codex_native_sandbox_mitigation_219 \
python.test_blk_current_state_authority_index \
python.test_lean_documentation_policy
Ran 75 tests in 0.302s
OK
```

Repository-wide verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest discover python 'test_*.py'
Ran 1366 tests in 14.524s
OK (skipped=35)

go test ./...
all packages OK

git diff --check -- <exact changed paths>
PASS
```

## 5. Hostile Review / Risk Check

Hostile review result: PASS after fail-closed scoping and remediation of two documentation-accuracy nonblockers (complete changed-file list and BLK-079 section-2 current-state marker).

Checks performed:

- Root-cause discipline: the sprint reproduced the Codex/bwrap failure with Codex sandbox, direct bwrap, and unshare probes before implementing mitigation evidence.
- Scope: no host sysctl, AppArmor, package installation, setuid, capability, Docker, or system service mutation was performed.
- Authority laundering: caller-controlled notes/evidence refs reject native-sandbox-enforced, production-isolation, live-Codex, protected-body, package/network/tooling, BEO publication, and RTM wording.
- Sandbox overclaim: package validation rejects `native_sandbox_enforced=True`, `host_configuration_mutated=True`, and any native workspace-write READY state.
- Current-state docs: BLK-077/079 record `EXTERNAL_CONTAINMENT_REQUIRED` and a host-admin repair/recheck frontier, not native sandbox success.
- Adjacent surfaces: no BLK-pipe dispatch, production BLK-test MCP, BEB dispatch, BEO closeout/publication, RTM/blk-link, protected-body access, broad source/Git mutation, package/network/model/browser/cyber tooling, or production-isolation authority is granted.

## 6. Authority Boundary

BLK-SYSTEM-219 does not grant live Codex dispatch, reusable Codex dispatch, tactical LLM dispatch, native workspace-write authority, host configuration mutation, BLK-pipe dispatch/runtime, production BLK-test MCP, BEB dispatch, BEO closeout execution, BEO publication/signing/storage/ledger authority, RTM generation, production `blk-link`, drift rejection, coverage truth, protected BLK-req body reads/copying/parsing/hashing/scanning, broad target/source/Git mutation, package/network/model/browser/cyber tooling, or production-isolation claims.

Native Codex workspace-write remains blocked on this host until a separately approved host-admin repair is applied and the recorded unshare, bwrap, and Codex sandbox smoke tests pass.

## 7. Documentation Burden Check

No new `docs/BLK-###` root document was created. BLK-SYSTEM-219 produced exactly one sprint outcome document: this closeout. BLK-077/079 were updated only because the current active Codex operating mode and next frontier changed.
