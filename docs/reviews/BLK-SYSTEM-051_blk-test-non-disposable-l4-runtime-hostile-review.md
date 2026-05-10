# BLK-SYSTEM-051 — Hostile Review: BLK-test Non-Disposable L4 Runtime Pilot

**Status:** PASS after remediation
**Date:** 2026-05-10T10:48:26+10:00
**Scope:** BLK-SYSTEM-051 runtime wrapper, synthetic regression tests, BLK-054 boundary, runtime evidence, and sprint outcomes.

---

## 1. Review Focus

This hostile review checked whether the BLK-SYSTEM-051 non-disposable L4 runtime pilot accidentally expanded from one exact evidence-only `run_ast_validation` slice into reusable runtime authority or adjacent BEO/RTM/source-mutation authority.

Review probes focused on:

- exact approved target path, source subtree, workspace, tool, and HEAD enforcement;
- path spelling aliases such as `/.`, `/../`, or workspace aliases resolving to the approved target;
- durable replay protection across process restarts and process-local replay protection if the ledger is deleted mid-session;
- source and `.git` content/metadata parity, including root directories, symlinks, directory metadata, mode changes, and transient create/delete mutations;
- source-scope exclusions for Git metadata, protected BLK requirement descendants, symlink escapes, and secret-like descendants;
- evidence byte bounding and accurate `evidence_json_bytes` reporting;
- denied authority for production/generic BLK-test MCP, reusable service startup, live Codex, arbitrary shell/caller commands, package/network/model/browser/cyber tooling, BEO publication, RTM generation, drift rejection, source/Git mutation, and production isolation claims.

The real approved runtime envelope remained stale during review:

```text
approved_head: 75e44c4066f7cbad38ed15afdc93a8eafd703340
current_head: faf303bc244b49bb2ce6219d09cfdb7e6c2b93af
approval_id: APPROVAL-BLK-SYSTEM-051-001
run_id: RUN-BLK-SYSTEM-051-001
```

No second real pilot run was attempted. All remediation verification was synthetic.

---

## 2. Hostile Findings and Remediation

Initial hostile review rounds returned **BLOCKED**. All blocker classes were remediated with regression tests.

Remediated blocker classes:

1. **Caller-controlled target and HEAD bypass:** runtime now enforces the approved target/source/workspace constants and exact approved `EXPECTED_HEAD`.
2. **Replay bypass:** replay protection now uses caller-owned sets, a durable ledger at `/tmp/blk-system-051-non-disposable-l4-runtime-replay-ledger.json`, and process-local consumed ID sets.
3. **Existing workspace deletion:** the wrapper now rejects an existing workspace before ownership is established instead of deleting caller-owned paths.
4. **Incomplete source mutation detection:** snapshots now cover all source entries, not only `.py` files.
5. **Directory and symlink mutation bypasses:** snapshots now include directories, source root metadata, symlink lstat metadata, raw symlink payloads, and resolved symlink targets.
6. **Git metadata parity bypasses:** `.git` snapshots now include the `.git` root directory plus file/directory mode, uid, gid, size, mtime, ctime, and content hashes.
7. **Replay ledger temp symlink overwrite:** ledger writes use exclusive creation and reject pre-existing/symlink temp paths.
8. **Path spelling laundering:** exact spelling is checked before path resolution so approved targets cannot be reached through alias spellings.
9. **Output byte limit bypass:** minimum output cap is now 1024 bytes, compact evidence recomputes `evidence_json_bytes` to a fixed point, and overflow tests assert actual serialized JSON size stays within the reported cap.
10. **Secret-like descendant bypass:** source-scope rejection now covers `.env.local`, credentials/secrets/token variants, SSH key names, private-key names, `.pem` files, and secret-like directories.

---

## 3. Final Hostile Review Verdict

Final hostile review returned **PASS** after the output-bound and secret-descendant remediations.

The final review confirmed:

- exact target/source/workspace spelling and resolved target enforcement;
- exact approved tool and HEAD enforcement;
- durable plus in-process replay protection;
- expanded secret/protected source-scope rejection;
- source and `.git` metadata/content snapshots, including root directories and symlinks;
- evidence bounding with accurate byte accounting;
- no remaining BEO/RTM/source/Git mutation authority or shell/network/package/model/browser/cyber authority in the reviewed runtime path.

---

## 4. Final Regression Evidence

Focused runtime suite:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_non_disposable_l4_runtime_pilot -q
----------------------------------------------------------------------
Ran 16 tests in 0.151s

OK
```

Doctrine gate:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint051_non_disposable_l4_runtime_pilot_is_exact_one_run_evidence_only -q
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Full verification:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python -p 'test_*.py'
Ran 650 tests in 8.975s — OK

go test ./...
PASS

go vet ./...
PASS

git diff --check
PASS
```

---

## 5. Final Authority Boundary

BLK-SYSTEM-051 remains a one-run, exact-target, evidence-only L4 runtime pilot wrapper. The only real runtime attempt for the approved envelope safely returned `BLOCKED` before fixed-tool execution because the target HEAD had drifted.

BLK-SYSTEM-051 does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, arbitrary repositories, arbitrary shell, caller-supplied commands, dynamic tool expansion, source/Git mutation by BLK-test, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, package-manager/network/model/browser/cyber tooling, live Codex execution, or production sandbox/cgroup/VM/namespace/seccomp/AppArmor/SELinux/firewall/host-secret-isolation claims.
