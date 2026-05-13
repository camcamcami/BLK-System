# BLK-SYSTEM-097 Hostile Review — Bounded BLK-test Evidence Refresh

**Sprint:** BLK-SYSTEM-097 — Bounded BLK-test Evidence Refresh Request / Exact-Target Frontier
**Review status:** PASS after remediation
**Review scope:** `python/blk_test_kuronode_workspace_bounded_evidence_refresh.py`, focused tests, BLK-097 doctrine, BLK-077/BLK-079 current-state updates, runtime evidence, and outcome hygiene.

## Initial Hostile Review Findings

A delegated hostile review identified five blockers:

1. **Path-alias laundering via `Path` objects**
   - Risk: `Path("/approved/.")` normalized before exact raw spelling comparison.
   - Impact: alias inputs could pass and evidence would record canonical paths.
2. **Secret-like descendant gap**
   - Risk: `.envrc.local`, `.npmrc.local`, `api_key.txt`, `access_token.json`, and `private-key` were not rejected.
   - Impact: secret-like descendants could be copied into the wrapper-owned workspace.
3. **Replay consumption after documented pre-runtime stop conditions**
   - Risk: path alias, source-scope, output-cap, and similar checks raised before caller/process/durable replay retirement.
   - Impact: contradicted the one-run/consumed-ID doctrine for exact-ID attempts.
4. **Authority-laundering scanner under-scope**
   - Risk: percent/compact/camel forms such as `docs%2Factive`, `protected%20body%20read`, `BEO%20is%20published`, and `activeVaultHashComparison` were not covered.
   - Impact: PASS-as-approval/publication/RTM/coverage/protected-path wording could be smuggled into valid free-text fields.
5. **Stale post-096 current-frontier wording**
   - Risk: active docs still presented the post-096 bounded BLK-test refresh as current after BLK-SYSTEM-097 consumed the exact run, and BLK-097 status still said active one-run.
   - Impact: future operators could mistake consumed evidence for reusable refresh authority.

## Remediations Applied

### 1. Path spelling hardening

- `_require_exact_spelling()` now rejects non-`str` runtime path arguments so `Path` objects cannot erase caller spelling before comparison.
- Pre-runtime path spelling failures now retire the exact IDs and return BLOCKED evidence rather than allowing a silent retry.
- Tests now cover string aliases and `Path(.../.)` aliases for target, source, and workspace.

### 2. Secret-like descendant hardening

- `_is_secret_name()` now rejects `.envrc.*`, `.npmrc.*`, API/access token names, private-key variants, service-account/credential tokens, and compact key forms.
- Tests now cover `.env.local`, `.envrc.local`, `.npmrc.local`, `api_key.txt`, `access_token.json`, and `private-key`.

### 3. Replay ordering hardening

- Exact approval/run/tool/default-entrypoint checks still fail before replay when the request is not the approved run or the production IDs are already committed as retired.
- After exact runtime authorization validation, caller-owned, process-local, and durable replay state is consumed before documented pre-runtime stop-condition checks.
- Tests assert path aliases, secret descendants, low output caps, and pre-owned workspaces consume IDs.

### 4. Authority text scanner hardening

- Free-text scanning now checks percent-decoded variants and compact casefolded forms.
- Added compact tokens for protected paths, BEO publication, RTM generation, coverage truth, drift decision/rejection, active-vault comparison, production/generic BLK-test MCP, package/network/model/browser/cyber tooling, host-secret isolation, source/Git mutation, and related runtime surfaces.
- Tests cover `docs%2Factive%2FREQ-001.md`, `protected%20body%20read`, `BEO%20is%20published`, `activeVaultHashComparison`, `hostSecretIsolationClaimed`, and package/network/model/browser/cyber compact wording.

### 5. Current-state wording remediation

- BLK-097 status changed to `Completed consumed one-run BLK-test evidence-refresh boundary`.
- BLK-077 and BLK-079 now qualify post-096 bounded-refresh candidate text as historical/as-of-BLK-SYSTEM-096 and state BLK-SYSTEM-097 consumed the exact refresh.
- Added an active-doctrine regression blocking unqualified post-096 current-frontier wording after BLK-SYSTEM-097.

### 6. Closeout hash remediation

A re-review found one closeout blocker: Task 002 recorded pre-remediation wrapper/doc hashes. Recomputed hashes were patched into `docs/outcomes/BLK-SYSTEM-097_task-002-outcome.md`:

```text
9e486b62dd121321e93a4507982cd606c89e11ded176a55a7f90e4ac8a2c3ca5  python/blk_test_kuronode_workspace_bounded_evidence_refresh.py
d84fd126ec0f54e5310cf673fb55536542074d1301f27a0b6ac90fb0762ebb46  docs/BLK-097_bounded-blk-test-evidence-refresh-exact-target-frontier.md
```

The runtime evidence hash stayed unchanged:

```text
e5532f096edde0f99c729d6f0750d3d07f2347c0a76d9b7a57a69016f2e915c9  docs/outcomes/BLK-SYSTEM-097_runtime-evidence.json
```

## Re-Review Result

Second hostile review verified the five authority-boundary blockers were remediated. After the stale Task 002 hashes were patched, focused verification and `git diff --check` remained green:

```bash
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/blk-system-pycache python -m unittest python.test_blk_test_kuronode_workspace_bounded_evidence_refresh python.test_active_doctrine_review_gates python.test_blk_current_state_authority_index -q
```

```text
----------------------------------------------------------------------
Ran 147 tests in 15.264s

OK
```

```bash
git diff --check
```

```text
OK (no output)
```

## Final Boundary Statement

BLK-SYSTEM-097 remains exactly one consumed evidence-only BLK-test refresh. The PASS evidence does not grant production BLK-test MCP, generic BLK-test MCP, reusable service startup, arbitrary shell, dynamic tools, Kuronode source/Git mutation, BLK-pipe/Codex/MCP runtime, BEO publication, RTM generation, RTM drift rejection, coverage truth, drift truth, protected-body reads, public ledger mutation, package/network/model/browser/cyber tooling, signer/storage/rollback side effects, or production sandbox/host-secret-isolation claims.
