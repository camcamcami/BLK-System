# BLK-121 — Codex Configuration and Containment Contract

**Status:** Active Codex configuration contract — not sprint authority and not runtime authority
**Date:** 2026-05-17
**Sprint:** BLK-SYSTEM-216; Codex reasoning-effort default updated by BLK-SYSTEM-353
**Purpose:** Pin the current Codex CLI configuration shape for bounded BLK-System/Kuronode tactical work after Codex CLI 0.130.0 moved deny-read behavior into permission profiles.
**Scope:** Configuration doctrine, permission-profile contract, host sandbox observation, external-containment fallback, and telemetry expectations. This document is not a BEB, not a BEO, not runtime approval, not reusable live Codex dispatch, and not production-isolation proof.

---

## 1. Contract Markers

```text
CODEX_CONFIGURATION_AND_CONTAINMENT_CONTRACT_ACTIVE
CODEX_CLI_0_130_0_CONFIGURATION_PINNED
SANDBOX_MODE_AND_APPROVAL_POLICY_ARE_SEPARATE_CONTROLS
PERMISSION_PROFILES_USE_NONE_FOR_DENY_READ
LEGACY_EXEC_DENY_READ_FLAGS_NOT_SUPPORTED
HOST_NATIVE_CODEX_SANDBOX_UNAVAILABLE_BWRAP_RTM_NEWADDR
DEVCONTAINER_OR_EXTERNAL_SANDBOX_FOR_DANGER_FULL_ACCESS
CODEX_JSONL_TELEMETRY_ADVISORY_ONLY
NO_LIVE_CODEX_DISPATCH_AUTHORITY
NO_REUSABLE_CODEX_DISPATCH_AUTHORITY
NO_BLK_PIPE_DISPATCH_AUTHORITY
NO_PRODUCTION_BLK_TEST_MCP_AUTHORITY
NO_BEB_DISPATCH_AUTHORITY
NO_BEO_CLOSEOUT_EXECUTION_AUTHORITY
NO_BEO_PUBLICATION_AUTHORITY
NO_RTM_GENERATION_AUTHORITY
NO_PRODUCTION_BLK_LINK_AUTHORITY
NO_PROTECTED_BODY_READ
NO_PACKAGE_NETWORK_MODEL_BROWSER_CYBER_TOOLING
NO_PRODUCTION_ISOLATION_CLAIM
```

---

## 2. Current Codex CLI Shape

BLK-SYSTEM-216 records `codex-cli 0.130.0`. For BLK-System/Kuronode tactical packets, the stable non-interactive invocation shape is:

```bash
codex --model gpt-5.5 \
  -c model_reasoning_effort="xhigh" \
  -s danger-full-access \
  -a never \
  exec \
  --ephemeral --ignore-user-config --ignore-rules --json \
  --disable hooks --disable plugins --disable goals \
  --output-last-message artifacts/codex/final-message.md \
  -C <externally-contained-worktree> \
  "<bounded tactical prompt>"
```

`danger-full-access` is allowed only as a current-host workaround inside a separately controlled external containment boundary. It is not a sandbox claim and not permission to run Codex directly on the host against broad source trees.

Do not use legacy `--deny-read`, `--isolated`, `--yes`, or `--dry-run` flags in new Codex exec payloads. In Codex CLI 0.130.0, deny-read behavior belongs in permission profiles, and `codex sandbox linux --permissions-profile <name>` is the direct enforcement path when the host sandbox works.

---

## 3. Permission Profile Contract

A bounded Kuronode Codex feature packet should define a permission profile with explicit allow/deny roots. Denied reads use `"none"`; writable exact files use `"write"`; the repository baseline may be `"read"`.

Illustrative profile shape:

```toml
default_permissions = "blk-kuronode-codex-feature"

[permissions.blk-kuronode-codex-feature.filesystem]
glob_scan_max_depth = 4

[permissions.blk-kuronode-codex-feature.filesystem.":project_roots"]
"." = "read"
"packages/kuronode-graph/src/utils/GraphProjectionEngine.ts" = "write"
"packages/kuronode-graph/tests/GraphProjectionEngine.test.ts" = "write"
"packages/kuronode-ui/src/components/CanonicalDataGrid.tsx" = "write"
"packages/kuronode-ui/src/components/CanonicalDataGrid.test.tsx" = "write"
"**/.git/**" = "none"
"**/.env*" = "none"
"**/.codex/**" = "none"
"**/.agents/**" = "none"
"**/node_modules/**" = "none"
"docs/requirements/**" = "none"
"docs/use_cases/**" = "none"
"../**" = "none"

[permissions.blk-kuronode-codex-feature.network]
enabled = false
```

This profile is a configuration contract unless the Codex native sandbox or an outer container/VM enforces it during the run. BLK-System canonical evidence remains Git diff scope, exact allowlists, test output, telemetry retention, and hostile audit.

---

## 4. Sandbox and Approval Are Separate Controls

Sandbox mode controls what the process can read/write/network. Approval policy controls when the agent must stop and ask. They are not interchangeable.

- `--sandbox workspace-write` with `--ask-for-approval on-request` is the preferred direction once native sandbox smoke tests pass.
- `--sandbox read-only --ask-for-approval never` is review-only/CI evidence, not mutation authority.
- `-s danger-full-access -a never` is acceptable only inside external containment with exact prompt scope, exact file allowlists, telemetry capture, tests, and hostile audit.
- A Codex approval, JSONL event, final message, or PASS-like text never grants runtime authority, BEB dispatch, BEO closeout execution, BEO publication, RTM generation, drift rejection, coverage truth, or future source/Git mutation authority.

---

## 5. Current Host Observation

Local host smoke evidence remains blocked:

```text
HOST_NATIVE_CODEX_SANDBOX_UNAVAILABLE_BWRAP_RTM_NEWADDR
observed_failure=bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

Until this changes, BLK-System must not claim Codex native sandbox, namespace, seccomp, AppArmor, SELinux, cgroup, VM, firewall, network-denial, or host-secret-isolation enforcement on this host. Use `DEVCONTAINER_OR_EXTERNAL_SANDBOX_FOR_DANGER_FULL_ACCESS` for feature-producing Codex work, then audit the physical diff and validation output outside Codex.

---

## 6. Required Evidence for Future Codex Feature Loops

A future Codex-assisted Kuronode feature loop must preserve:

1. exact model and reasoning effort;
2. exact worktree path and branch;
3. exact allowed modified/new file lists;
4. exact prompt/brief or compact tactical packet;
5. permission-profile name and profile text/hash;
6. JSONL telemetry path and final-message artifact path;
7. validation commands and output;
8. exact parent/feature/merge commits when mutation occurs;
9. exact patch hash for allowed files;
10. hostile audit verdict and any remediation.

Telemetry is advisory. The committed diff and external validation are canonical.

---

## 7. Explicit Non-Authorities

BLK-121 does not authorize live tactical LLM execution, live Codex execution, reusable Codex dispatch, BLK-pipe dispatch, production BLK-test MCP, arbitrary shell, package-manager execution, network/API/model/browser/cyber tooling, source mutation, Git mutation, protected BLK-req body reads/copying/parsing/hashing/scanning/mutation, active-vault path scans, BEO closeout execution, BEO publication/signing/storage/ledger authority, RTM generation, production `blk-link`, drift rejection, coverage truth, signer access, immutable storage writes, public ledger mutation, rollback/revocation/supersession, or final drift decisions.

BLK-121 does not claim production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall enforcement, network firewall enforcement, kernel containment, host-secret isolation, or comprehensive host side-effect observation.

---

## 8. Stop Conditions

Stop and treat proposed Codex work as outside this contract if it asks to read protected BLK-req bodies, scan active/protected requirement documents broadly, use network/package-manager/browser/cyber tooling, run without external containment while requiring `danger-full-access`, mutate files outside an exact allowlist, ignore user config/rules suppression, enable hooks/plugins/goals, skip telemetry, treat Codex self-report as canonical proof, or convert a sprint-specific feature run into reusable runtime authority.
