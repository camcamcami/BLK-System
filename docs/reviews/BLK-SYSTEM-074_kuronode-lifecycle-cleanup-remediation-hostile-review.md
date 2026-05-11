# BLK-SYSTEM-074 Hostile Review — Kuronode Lifecycle Cleanup Remediation Packet

**Status:** Complete — blockers found and remediated with regression tests
**Date:** 2026-05-11
**Scope:** BLK-SYSTEM-074 plan, BLK-075 boundary, remediation packet builder/tests, active doctrine gate, and Task 000-002 outcomes.

---

## Review Summary

A hostile review found that the initial BLK-SYSTEM-074 implementation correctly stayed fixture-only, but was under-scoped for evidence trust and authority-laundering hardening. The review treated these as blockers because BLK-SYSTEM-074 converts one real BLK-test finding into future remediation guidance; forged evidence or permissive wording could launder patch, rerun, BEO, RTM, coverage, or production BLK-test authority.

The original BLK-SYSTEM-073 evidence remains evidence-only:

```text
status: FAIL
finding: smoke_test.ts:53 LIFECYCLE_CLEANUP_REQUIRED
approval_id: APPROVAL-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
run_id: RUN-BLK-SYSTEM-073-KURONODE-WORKSPACE-001
```

---

## Blockers and Remediation

### 1. Source evidence was not anchored to the committed artifact

**Finding:** The initial builder validated caller-supplied evidence against a caller-supplied hash, so a structurally valid forged evidence object could produce a ready packet.

**Remediation:** Added committed artifact constants:

```text
COMMITTED_SOURCE_EVIDENCE_HASH=sha256:4962ca31a932daf9905d5834b6daec28f1da449b4afeaf575cb16ee451df328f
COMMITTED_SOURCE_EVIDENCE_FILE_SHA256=sha256:e60cac20a9ea9dcae05e5a1844295ddd954e3d41e3fff898a258fbfe0ab5c062
```

`load_committed_blk_system_073_evidence` now verifies the file bytes hash, and `_validate_source_evidence` requires the committed canonical hash.

### 2. Source evidence integrity fields were under-validated

**Finding:** The initial validator accepted mutated integrity fields such as missing/altered tree hashes, mismatched counts, truncated findings, oversized evidence, or `fixed_tool_executed: false`.

**Remediation:** Added exact key-set validation and checks for:

- `fixed_tool_executed is True`;
- `files_checked == ["smoke_test.ts"]`;
- `findings_count == 1` and `findings_truncated is False`;
- `evidence_json_bytes <= output_byte_limit`;
- exact source tree and `.git` metadata hashes before/after.

### 3. Evidence/request laundering coverage was too narrow

**Finding:** Hostile probes found request strings that could pass, including retired runtime IDs in free text, BLK-pipe invocation wording, dynamic tool expansion, reusable BLK-test service startup, `BEO is PUBLISHED`, coverage truth, source writes, Git staging, `.env` secret reads, patch-authority wording, and pilot-rerun wording.

**Remediation:** Expanded laundering regexes and retired-ID free-text rejection. Added regressions for each hostile phrase class.

### 4. Denied-authority and false-flag surfaces were incomplete

**Finding:** `EXACT_EXCLUDED_AUTHORITIES` and packet false booleans collapsed several BLK-075 boundary items rather than representing them as machine-checkable denial surfaces.

**Remediation:** Added missing denied authorities including dynamic tool expansion, protected-body copy/parse/hash/summarize/scan/mutate/drift compare, Kuronode revert/stash/autofix/remote writes, release authority, active-vault hash comparison, and host-secret-isolation claims. Added `PACKET_FALSE_SIDE_EFFECT_FLAGS` and emitted every denied side-effect flag as explicit `False`.

### 5. Active doctrine gate was string-only

**Finding:** The BLK-075 gate checked text markers but did not also check code/doc drift in denied authority and false-flag surfaces.

**Remediation:** Extended the active doctrine gate to import BLK-SYSTEM-074 code constants and assert required denied-authority and false-flag markers exist.

---

## Regression Coverage Added

Focused packet tests now cover:

- committed source-evidence canonical hash and file hash;
- rejection of non-committed evidence even if caller recomputes a matching request hash;
- stale/rewritten source evidence integrity fields;
- retired runtime ID reuse in fields and free text;
- nested source-evidence/request authority laundering and protected-path strings;
- broad request laundering phrases for BLK-pipe, dynamic tool expansion, BEO publication, coverage/drift, source/Git mutation, `.env` secrets, patch authority, and pilot reruns;
- exact denied-authority boundary markers;
- complete packet no-side-effect false-flag emission.

---

## Verification

Focused packet tests after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_blk_test_kuronode_lifecycle_cleanup_remediation_packet -q
----------------------------------------------------------------------
Ran 11 tests in 0.018s

OK
```

Focused active doctrine gate after remediation:

```text
PYTHONPATH=python PYTHONDONTWRITEBYTECODE=1 python -m unittest python.test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_sprint074_kuronode_lifecycle_cleanup_remediation_packet_is_fixture_only -q
----------------------------------------------------------------------
Ran 1 test in 0.009s

OK
```

---

## Boundary Statement

No remediation reran the BLK-SYSTEM-073 pilot, reused retired IDs, allocated fresh runtime IDs, invoked BLK-pipe, invoked Codex, launched Electron, ran smoke/TypeScript/package-manager tooling, mutated Kuronode source or Git state, read protected BLK-req bodies, published BEOs, generated RTM, promoted coverage/drift authority, or claimed production BLK-test MCP/sandbox authority.
