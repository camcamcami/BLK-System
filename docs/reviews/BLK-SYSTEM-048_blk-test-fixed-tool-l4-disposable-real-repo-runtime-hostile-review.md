# BLK-SYSTEM-048 — Hostile Review: BLK-test Fixed-Tool L4 Disposable Real-Repo Runtime

**Status:** PASS after remediation
**Date:** 2026-05-10T07:47:19+10:00
**Scope:** BLK-SYSTEM-048 runtime fixture, BLK-051 boundary, active doctrine gate, and outcomes.

---

## 1. Review Focus

This hostile review checked whether BLK-SYSTEM-048 improperly expanded BLK-test authority while adding the first L4 disposable real-repo runtime fixture.

Review probes focused on:

- replay/preflight consumption before source reads;
- fake `.git` acceptance and disposable target identity;
- broad `.git` byte reads or host-secret leakage;
- final evidence output cap enforcement;
- source/Git mutation detection;
- protected BLK-req path/body leakage;
- PASS-as-BEO/RTM/publication/coverage/drift laundering;
- production/generic BLK-test MCP authority laundering.

---

## 2. Initial Hostile Findings

The first hostile review returned **BLOCKED** with six blocker classes:

1. source files were read/hashed before preflight replay rejection;
2. ordinary fake `.git` directories could be accepted as real repositories, and Git mutation detection compared two after-the-fact snapshots;
3. alternate BEO/RTM laundering such as `PASS authorizes BEO and RTM` was accepted;
4. evidence output bounds were not enforced against returned JSON;
5. source snapshots read/hash all files instead of only the approved source files;
6. runtime extension validation was allowlist-only rather than exact/required.

All six were converted into regression tests before remediation.

---

## 3. Remediation Summary

Implemented remediations:

- moved BLK-050 preflight/replay consumption before source scope scans, source hashing, or AST reads;
- required a harness-owned repo marker and verified a real disposable Git identity before runtime;
- rejected fabricated Git identities by validating that the HEAD loose commit object and HEAD tree object match their Git SHA-1 object IDs;
- replaced broad `.git` byte hashing with bounded Git identity reads plus metadata-only mutation snapshots;
- narrowed source snapshots to approved `.py` files;
- enforced exact runtime extension keys and exact runtime notes;
- expanded authority-laundering rejection to tokenized BEO/RTM/publication/drift/coverage/trace/protected/signer/ledger/storage/rollback/production terms;
- returned bounded evidence summaries instead of full per-file snapshot maps;
- computed final returned JSON byte size after adding `output_byte_limit` and `evidence_json_bytes` fields.

---

## 4. Final Regression Evidence

Focused final test suite:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_l4_disposable_repo_runtime -q
----------------------------------------------------------------------
Ran 10 tests in 0.096s

OK
```

Related doctrine/runtime suite:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python3 -m unittest python.test_blk_test_fixed_tool_l4_disposable_repo_runtime python.test_blk_test_fixed_tool_pilot_l4_real_repo_approval_boundary python.test_active_doctrine_review_gates -q
----------------------------------------------------------------------
Ran 92 tests in 0.108s

OK
```

Regression coverage includes:

- replay blocks before any source hashing;
- missing `.git`, empty fake `.git`, and forged commit-like fake `.git` identities block;
- `.git` sentinel bytes are not broadly read/hashed by the runtime path;
- final returned evidence JSON respects `output_byte_limit`;
- alternate `PASS authorizes BEO and RTM` laundering is rejected;
- exact runtime extension key set is required;
- protected descendants, primary repo targets, and unknown tools block.

---

## 5. Final Verdict

PASS after remediation.

BLK-SYSTEM-048 remains limited to one harness-owned disposable exact-target real Git repository runtime using in-process `ast.parse` over approved `.py` files. The sprint does not authorize production BLK-test MCP, generic BLK-test MCP, arbitrary repositories, arbitrary shell, package-manager/network/model/browser/cyber tooling, source/Git mutation by BLK-test, protected BLK-req body reads, authoritative BEO publication, RTM generation, RTM drift rejection, public ledger mutation, signer/storage/rollback/revocation/supersession/release authority, or production isolation claims.
