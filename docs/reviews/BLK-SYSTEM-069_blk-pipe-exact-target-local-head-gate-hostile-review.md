# BLK-SYSTEM-069 Hostile Review — BLK-pipe Exact-Target Local Head Gate

**Status:** APPROVED after one remediation
**Date:** 2026-05-11T10:08:00+10:00
**Implementation commit reviewed:** `2e6dc85 feat: gate exact target blk-pipe execution by local head`

---

## 1. Review Scope

Reviewed the BLK-SYSTEM-069 implementation for authority laundering, target retargeting, private-repo credential shortcuts, and exact-target source-mutation safety.

Changed surfaces reviewed:

```text
docs/BLK-004_blk-pipe-v47-architecture-suite.md
internal/contracts/payload.go
internal/contracts/payload_test.go
internal/gitguard/branch.go
internal/gitguard/branch_test.go
internal/pipe/run.go
internal/pipe/run_test.go
python/blk_pipe_adapter.py
python/kuronode_power_of_ten_ceb009_fresh_target_patch_execution.py
python/test_blk_pipe_adapter.py
python/test_kuronode_power_of_ten_ceb009_fresh_target_patch_execution.py
```

---

## 2. Findings

### HR-001 — Python adapter initially collapsed `TARGET_HEAD_MISMATCH`

**Initial disposition:** REQUEST_CHANGES

The Go runner introduced `TARGET_HEAD_MISMATCH` with exit code 3, but `python/blk_pipe_adapter.py` initially allowed only `UNAUTHORIZED_FILE_MUTATION` for exit code 3. Adapter callers would have seen the wrong primary status even though raw report evidence retained the Go value.

**Remediation:** Added `TARGET_HEAD_MISMATCH` to `_ALLOWED_STATUSES_BY_CODE[3]` and added `test_execution_result_preserves_target_head_mismatch_status`.

**Final disposition:** APPROVED.

---

## 3. Hostile Checks

- **Target-hash retargeting:** PASS. `target_hash` is only compared against local `HEAD`; it is not used to checkout arbitrary refs or reset to another commit.
- **Fetch bypass scope:** PASS. Exact-target branch mode avoids fetch only when `target_hash` is present and requires an existing local branch. Unpinned legacy target-branch behavior remains fetch-capable.
- **Remote fallback/orphan bypass:** PASS. Exact-target branch mode rejects missing local branches instead of falling back to remote tracking or orphan creation.
- **Engine-before-head-check:** PASS. Head mismatch tests prove the tactical engine does not run and source files remain unmutated.
- **Adapter evidence preservation:** PASS after remediation. `TARGET_HEAD_MISMATCH` survives the Python adapter interface.
- **CEB_009 payload boundary:** PASS. The builder adds only `target_hash`; all patch side-effect flags remain false until future execution authority.
- **Credential injection:** PASS. No credential helper, token, global Git config restoration, SSH agent restoration, or askpass path was added.
- **Adjacent authority laundering:** PASS. No Codex, BLK-test MCP, Electron/smoke runtime, TypeScript/package-manager tooling, BEO/CEO publication, RTM generation, protected body read, or Kuronode remote push path was introduced.

---

## 4. Verification Evidence

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover python 'test_*.py'
Ran 731 tests in 9.356s
OK

go test ./...
OK

git diff --check
OK
```

---

## 5. Final Review Verdict

`APPROVED`

BLK-SYSTEM-069 resolves the immediate BLK-pipe internal fetch-auth blocker for future exact-target local attempts without credential injection or a hidden Kuronode patch attempt. A future CEB_009 patch still requires fresh explicit approval and should use a payload containing `target_hash`.
