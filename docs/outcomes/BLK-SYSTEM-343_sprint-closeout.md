# BLK-SYSTEM-343 — Controlled Codex CLI Update and Smoke Evidence Sprint Closeout

**Status:** Blocked after successful CLI update; private-bwrap AppArmor profile evidence is not READY
**Date:** 2026-05-30 AEST
**Commit:** this commit (`feat: add codex cli capability probe evidence`)

## 1. Objective

Update the local Codex CLI from `0.130.0` to `0.135.0`, inventory the baseline non-interactive route flags, record advisory `codex doctor` diagnostics in redacted form, and run a no-op `workspace-write` smoke only if BLK-SYSTEM-229 private-bwrap/AppArmor setup is observable as READY.

## 2. Files Changed

- `python/codex_cli_capability_probe.py` — pure, non-executing capability report builder and diagnostics redactor for BLK-SYSTEM-343 evidence.
- `python/test_codex_cli_capability_probe.py` — focused RED/GREEN coverage for required flag inventory, doctor-as-advisory behavior, redaction, private-bwrap descriptor binding, and all-denied side-effect authority flags.
- `python/test_lean_documentation_policy.py` — extends the one-closeout lean-documentation gate through BLK-SYSTEM-343.
- `docs/outcomes/BLK-SYSTEM-343_sprint-closeout.md` — this single sprint closeout.

## 3. Implementation / Execution Summary

- Ran `CODEX_NON_INTERACTIVE=1 npm install -g @openai/codex@0.135.0`.
- Verified installed CLI: `codex-cli 0.135.0`.
- Verified npm latest: `0.135.0`.
- Verified `codex exec --help` still exposes required BLK route baseline flags:
  - `--sandbox`
  - `--ephemeral`
  - `--ignore-user-config`
  - `--ignore-rules`
  - `--disable`
  - `--json`
  - `--output-last-message`
- Recorded `codex doctor` as redacted advisory diagnostics only.
- Built local machine-readable evidence at `/var/tmp/blk-system-343-codex-cli-smoke-evidence.json`; this file is intentionally not staged or committed.
- Evaluated BLK-SYSTEM-229 private-bwrap descriptor:
  - `private_bwrap_path`: `/opt/blk-system/codex-bwrap/bwrap`
  - `required_sysctl`: `kernel.apparmor_restrict_unprivileged_userns=1`
  - `status`: `BLOCKED`
  - blocker: `APPARMOR_PROFILE_NOT_LOADED` for `blk-codex-bwrap`
- Per the package stop condition, no `workspace-write` no-op Codex smoke was attempted and no downgrade to `danger-full-access` was used.

## 4. Verification

- RED: after extending `test_new_sprints_use_one_outcome_only` through BLK-SYSTEM-343, the focused lean gate failed with `BLK-SYSTEM-343 closeout missing`.
- RED: `python.test_codex_cli_capability_probe` initially failed because `codex_cli_capability_probe` did not exist.
- RED after hostile review: focused probes failed because `workspace-write` mode was not enforced, contradictory `status: READY` plus blockers could report READY, malformed non-list blockers could report READY, and private-bwrap descriptor fields were not recursively redacted.
- GREEN: `TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_codex_cli_capability_probe python.test_lean_documentation_policy` → `Ran 15 tests ... OK`.

Final verification after the closeout file existed:

```text
TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest python.test_codex_cli_capability_probe python.test_lean_documentation_policy
...............
----------------------------------------------------------------------
Ran 15 tests in 0.121s

OK

TMPDIR=/var/tmp/blk-system-testtmp PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/blk-system-pycache python3 -m unittest discover -s python -p 'test_*.py'
[default discovery timed out after 600s before completion]

Earlier after the closeout existed and before the hostile-review remediation, equivalent chunked full-module verification completed with all chunks/modules green. The post-remediation change set is covered by the focused 15-test gate above.
- chunks 1..8: 1557 tests, all exit 0
- python.test_verified_loop_beo_publication_approval_request_306_309: Ran 8 tests in 89.460s — OK
- python.test_verified_loop_beo_publication_bounded_execution_kernel_329: Ran 4 tests in 137.695s — OK
- python.test_verified_loop_beo_publication_live_challenge_guard_313_315: Ran 4 tests in 157.700s — OK
- python.test_verified_loop_beo_publication_refresh_challenge_310_312: Ran 4 tests in 55.870s — OK
- python.test_verified_loop_beo_publication_review_302_305: Ran 8 tests in 101.152s — OK
- python.test_verified_loop_beo_publication_side_effect_trace_closure_330_333: Ran 6 tests in 270.000s — OK
Total earlier chunked full-module coverage: 1591 tests, all invoked modules exit 0.

git diff --check -- python/codex_cli_capability_probe.py python/test_codex_cli_capability_probe.py python/test_lean_documentation_policy.py docs/outcomes/BLK-SYSTEM-343_sprint-closeout.md
[exit 0]
```

## 5. Hostile Review / Risk Check

- The new probe is pure and non-executing. It does not import or call subprocess, network, package-manager, shell, or Codex execution APIs.
- `codex doctor` evidence is explicitly advisory-only and sanitized before being recorded in committed documentation.
- Missing required `codex exec` baseline flags block the report even if `codex doctor` says OK.
- Private-bwrap evidence is a required descriptor for a `workspace-write` smoke. A missing loaded AppArmor profile blocks the smoke rather than becoming permission to downgrade to `danger-full-access`.
- Hostile review remediation added fail-closed probes for non-list/nonconforming descriptor blockers, contradictory `status: READY` plus blockers, missing `workspace-write` mode evidence, and recursive descriptor redaction.
- Post-remediation one-off hostile probes produced:
  - malformed dict blockers → `BLOCKED ['PRIVATE_BWRAP_DESCRIPTOR_BLOCKERS_MALFORMED']`
  - malformed string blockers → `BLOCKED ['PRIVATE_BWRAP_DESCRIPTOR_BLOCKERS_MALFORMED']`
  - missing workspace-write mode → `BLOCKED ['--sandbox workspace-write']`
  - sanitized descriptor retained no raw `/home/dad` path and no raw synthetic token
  - all side-effect authority fields remained false.
- The closeout status remains blocked because live host evidence still reports `PRIVATE_BWRAP_DESCRIPTOR_NOT_READY`; the remediation only prevents false READY reports.
- All side-effect authority booleans in the BLK-SYSTEM-343 report remain false.

## 6. Authority Boundary

BLK-SYSTEM-343 authorizes only the explicit local Codex CLI package update and diagnostic/smoke evidence collection described in the sprint package. It does not authorize BEB/L2 authorship by BLK-System, live or reusable Codex dispatch, broad BLK-pipe dispatch, BEO publication or closeout execution, RTM generation, production `blk-link`, drift rejection, coverage truth, active-vault comparison, protected-body access, production BLK-test MCP, generic runtime/tooling expansion, Kuronode source/Git mutation, package/network/model/browser/cyber tooling beyond the explicit CLI update, or any production-isolation claim.

## 7. Documentation Burden Check

No new root `docs/BLK-###` document was created. BLK-SYSTEM-343 produced exactly one closeout document and no per-task outcome documents.
