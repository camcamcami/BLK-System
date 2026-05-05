# BLK-pipe Sprint 009 — Task 002 Outcome

**Status:** Complete
**Date:** 2026-05-06 06:27:23 AEST
**Task:** Split BLK-006 draft and revision hash lifecycle examples

## Objective

Task 002 closed the Sprint 009 `MEDIUM-1` doctrine gap by aligning BLK-006 DRAFT schema examples with the BLK-002 hash lifecycle. New drafts now show no parent hash and a pending version hash; staged revisions now show a canonical parent hash while still leaving the draft `version_hash` pending until promotion.

## Files Changed

- `docs/BLK-006_blk-req-implementation-brief.md`
- `python/test_active_doctrine_review_gates.py`

## RED Evidence

Command:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Result before the BLK-006 patch:

```text
test_blk003_escalation_is_current_boundary_safe (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk003_escalation_is_current_boundary_safe) ... ok
test_blk003_strict_yaml_examples_do_not_use_truncated_trace_hashes (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk003_strict_yaml_examples_do_not_use_truncated_trace_hashes) ... ok
test_blk006_documents_new_draft_and_staged_revision_lifecycles (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk006_documents_new_draft_and_staged_revision_lifecycles) ... FAIL
test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders) ... FAIL

FAIL: test_blk006_documents_new_draft_and_staged_revision_lifecycles
AssertionError: Lists differ: ['parent_hash: ""', 'version_hash: "PENDING"', 'parent_hash: "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"', 'DRAFT documents must not invent future hashes'] != []

FAIL: test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders
AssertionError: Lists differ: ['sha256:...', 'sha256:...'] != []

FAILED (failures=2)
```

The RED gate proved BLK-006 still had a universal DRAFT schema with truncated `sha256:...` examples and lacked explicit split lifecycle markers.

## Implementation

Patched `docs/BLK-006_blk-req-implementation-brief.md`:

- Replaced the single universal DRAFT YAML schema with two explicit examples:
  - **New Draft Intake YAML Schema** using `parent_hash: ""` and `version_hash: "PENDING"`.
  - **Staged Revision Draft YAML Schema** using a synthetic canonical parent hash, `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`, and `version_hash: "PENDING"`.
- Added explicit lifecycle language: `Promotion/baseline mechanics assign the final canonical version_hash. DRAFT documents must not invent future hashes.`
- Updated baseline assignment language to say promotion computes the canonical `version_hash`.
- Updated §C staged-revision mechanism language so staged revision drafts keep `version_hash: "PENDING"` until promotion/baseline mechanics compute the final canonical hash.

Extended `python/test_active_doctrine_review_gates.py`:

- Added BLK-006 path constant.
- Hardened YAML fence matching so indented closing fences are scanned.
- Added a gate rejecting truncated BLK-006 YAML `sha256:...` placeholders.
- Added a gate requiring the new-draft and staged-revision lifecycle markers.

## GREEN Evidence

Focused gate:

```bash
python3 -m unittest discover -s python -p 'test_active_doctrine_review_gates.py' -v
```

Result:

```text
test_blk003_escalation_is_current_boundary_safe (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk003_escalation_is_current_boundary_safe) ... ok
test_blk003_strict_yaml_examples_do_not_use_truncated_trace_hashes (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk003_strict_yaml_examples_do_not_use_truncated_trace_hashes) ... ok
test_blk006_documents_new_draft_and_staged_revision_lifecycles (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk006_documents_new_draft_and_staged_revision_lifecycles) ... ok
test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders (test_active_doctrine_review_gates.ActiveDoctrineReviewGateTest.test_blk006_yaml_examples_do_not_use_truncated_sha256_placeholders) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

## Shared Verification Evidence

Command:

```bash
python3 -m unittest discover -s python -p 'test_*.py' && go test ./... && go vet ./... && git diff --check
```

Result:

```text
.............................................................................................................................
----------------------------------------------------------------------
Ran 125 tests in 0.649s

OK
ok  	github.com/camcamcami/BLK-System/cmd/blk-pipe	(cached)
ok  	github.com/camcamcami/BLK-System/internal/contracts	(cached)
ok  	github.com/camcamcami/BLK-System/internal/engine	(cached)
ok  	github.com/camcamcami/BLK-System/internal/execguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/gitguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/pipe	6.899s
ok  	github.com/camcamcami/BLK-System/internal/runtimeguard	(cached)
ok  	github.com/camcamcami/BLK-System/internal/testutil	(cached)
ok  	github.com/camcamcami/BLK-System/internal/validation	(cached)
```

`go vet ./...` and `git diff --check` produced no diagnostics and the combined command exited `0`.

## BLK-002 Lifecycle Alignment Rationale

BLK-002 separates draft identity from canonical baseline identity. A new draft cannot know its future canonical hash, so it must use `parent_hash: ""` and `version_hash: "PENDING"`. A staged revision must bind to the active artifact's current canonical hash through `parent_hash`, but it also cannot assign its own future canonical `version_hash` before promotion. The final `version_hash` belongs to the promotion/baseline mechanic.

## Non-Execution Statement

Task 002 was deterministic local documentation and gate hardening only. No Hindsight tools were used. No live Codex, live tactical LLM, network model service, cyber tooling, live BLK-test MCP, RTM generation, or authoritative BEO publication was invoked or authorized.
