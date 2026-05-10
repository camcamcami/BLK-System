# BLK-SYSTEM-062 — CEB_009 Patch Approval Envelope Integrity Hardening Plan

> **For Hermes:** Use `blk-system-plan-writing` while planning. Use `blk-system-sprint-execution`, `blk-system-authority-gated-sprints`, `test-driven-development`, and hostile review while executing. This plan is guided by `docs/BLK-024_blk-system-development-roadmap.md` for maturity vocabulary, by `docs/BLK-059_blk-system-post-058-roadmap.md` for current sequencing, and by BLK-001 through BLK-006 as applicable.

**Goal:** Harden the BLK-SYSTEM-061 CEB_009 patch approval-envelope fixture against forged upstream remediation packet hashes, weak status hashing, and normalized authority-laundering variants without approving or applying a Kuronode patch.
**BLK-024 / BLK-059 track:** Track A/J and Workstream B — authority-boundary hygiene and Kuronode TypeScript Power-of-Ten mechanical-gate safety; maturity L1 fixture-only hardening.
**Architecture:** BLK-SYSTEM-061 correctly created a review-only exact-target patch approval envelope, but the next safe step is to strengthen its trust boundary before any future approval decision. The envelope must recompute the submitted BLK-SYSTEM-060 remediation packet's canonical hash from the packet body rather than trusting a self-reported `packet_hash`, and it must reject nested/compact authority laundering in the upstream packet as well as in the request. This preserves the BLK-001 V-model separation between remediation evidence, approval envelopes, source mutation, runtime verification, BEO publication, and RTM closure.
**Tech Stack:** Python deterministic fixture module/tests; Python active doctrine gate; Markdown boundary, hostile review, and outcome docs.
**Authority boundary:** Fixture-only integrity hardening. No approval is granted by this sprint. No Kuronode source/Git mutation, no live Kuronode repository scan, no live source validation, no Electron launch, no smoke-test execution, no TypeScript tooling/typechecker/linter/formatter execution, no package-manager/network/model/browser/cyber tooling, no live Codex, no production/generic/reusable BLK-test MCP, no protected BLK-req body reads, no BEO publication, no RTM generation, and no production isolation claim.

---

## 1. Current Known State

Preflight:

```text
date: 2026-05-10T21:35:08+10:00
BLK-System git status --short --branch: ## main...origin/main
BLK-System git log -1 --oneline: 4b4a9be feat: add ceb009 patch approval envelope fixture
BLK-System git ls-remote origin refs/heads/main: 4b4a9be7193db5775f35de02633da50c8e8a9d65 refs/heads/main
```

ID discovery:

```text
BLK-SYSTEM-062 plan: not present before this sprint
BLK-067 document: not present before this sprint
BLK-SYSTEM-062 outcomes: not present before this sprint
```

Relevant completed state:

```text
BLK-SYSTEM-060 packet marker: KURONODE_POWER_OF_TEN_CEB009_REMEDIATION_PACKET_READY_NOT_PATCHED
BLK-SYSTEM-061 envelope marker: KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_READY_FOR_HUMAN_REVIEW_NOT_APPROVED_NOT_PATCHED
BLK-SYSTEM-061 target: github:camcamcami/Kuronode-v1 main cb09d965c0407612c9ce8fc9cc58c5e62c82e1b2 scripts/smoke_test.ts
```

---

## 2. Why This Is the Next Logical Sprint

BLK-SYSTEM-061 produced a patch approval envelope that is ready for human review, not approved, and not patched. The operator has not explicitly approved a Kuronode patch, live scan, smoke test, Codex run, BLK-test MCP run, BEO publication, or RTM generation. Therefore the next logical sprint must remain fixture-only.

The concrete blocker identified by authority-gated review practice is evidence identity trust: a downstream approval envelope must not trust a submitted upstream packet's self-reported hash. It must recompute that hash from the submitted upstream body, excluding the hash field, and reject forged or stale packet bodies even when the request's `remediation_packet_hash` matches the forged self-report.

This sprint closes that gap and also hardens the upstream packet scan surface before any future human patch decision.

---

## 3. Governing Doctrine Alignment

- **BLK-001:** Preserves V-model separation. Evidence packet identity, approval request, tactical source mutation, verification, publication, and trace closure remain separate domains.
- **BLK-002 / BLK-005:** Reinforces canonical hash trust without introducing protected BLK-req active-vault reads or body parsing.
- **BLK-003:** Preserves human confirmation gates and does not invoke BLK-pipe, Codex, or BLK-test.
- **BLK-004:** Keeps `blk-pipe` as final mutation authority for future source changes; this sprint does not broaden validation command or source allowlist authority.
- **BLK-006:** Preserves protected-vault hard-deny/no-read semantics.
- **BLK-059:** Continues Kuronode tactical-quality work without silently crossing into runtime/source mutation authority.
- **BLK-066:** Remains the immediate authority boundary being hardened.

---

## 4. Non-Authority Boundary

This plan does not authorize production BLK-test MCP, generic BLK-test MCP, reusable BLK-test service startup, live Codex execution, arbitrary shell, caller-supplied commands, Electron launch, headless smoke-test execution, wall-clock timeout waits, TypeScript tooling/typechecker/linter/formatter execution, package-manager/network/model/browser/cyber tooling, live Kuronode repository scans, live Kuronode source validation, Kuronode source mutation, Kuronode Git mutation, source/Git mutation by BLK-test or by a Kuronode gate, protected BLK-req body reads/copying/parsing/hashing/summarizing/scanning/mutation/drift comparison, authoritative BEO publication, runtime `PUBLISHED` BEO output, live publication approval capture, signer key material access, cryptographic signing, immutable storage writes, public ledger append/mutation, rollback/revocation/supersession execution, runtime RTM generation, RTM drift rejection, active-vault hash comparison, coverage matrices, coverage claims, drift decisions, or production isolation claims.

Hermes sprint-closeout verification and exact-path Git commit/push are BLK-System repository maintenance. They are not capabilities granted to the CEB_009 patch approval envelope.

---

## 5. Implementation Intent

Patch `python/kuronode_power_of_ten_ceb009_patch_approval_envelope.py` so `_validate_remediation_packet`:

1. recomputes `packet_hash` from `{key: value for key, value in packet.items() if key != "packet_hash"}` using the canonical hash function;
2. rejects mismatched, stale, or forged self-reported packet hashes before the envelope can become review-ready;
3. returns the recomputed hash as the trusted upstream identity;
4. recursively scans allowed upstream string surfaces for compact/camel/allcaps authority-laundering and protected-path variants, while preserving required safe status/authority tokens through exact structural validation;
5. requires exact excluded-authority equality on the upstream remediation packet as well as on the envelope request;
6. exposes a hardening marker in the returned envelope without changing the review-only/not-approved/not-patched status:

```text
KURONODE_POWER_OF_TEN_CEB009_PATCH_APPROVAL_ENVELOPE_INTEGRITY_HARDENED_UPSTREAM_HASH_RECOMPUTED
```

The sprint must not create `CEO_009`, must not edit `/home/dad/code/Kuronode-v1/scripts/smoke_test.ts`, and must not run Kuronode validation commands.

---

## 6. Task Plan

### Task 000 — Plan and publish this sprint plan

Deliverables:

```text
docs/plans/blk-system-062_ceb009-patch-approval-envelope-integrity-hardening.md
docs/outcomes/BLK-SYSTEM-062_task-000-outcome.md
```

Actions:

1. Record preflight state, ID discovery, governing docs, and selected scope.
2. Publish the plan and Task 000 outcome.
3. Do not implement hardening behavior in Task 000.

### Task 001 — Upstream hash and laundering hardening via TDD

Deliverables:

```text
python/kuronode_power_of_ten_ceb009_patch_approval_envelope.py
python/test_kuronode_power_of_ten_ceb009_patch_approval_envelope.py
docs/outcomes/BLK-SYSTEM-062_task-001-outcome.md
```

Actions:

1. Add RED tests proving a forged packet body with a forged self-reported `packet_hash` is currently accepted if the request matches the forged hash.
2. Add RED tests proving stale packet hashes are rejected after packet body mutation.
3. Add RED tests for nested upstream authority laundering variants such as `authoritativeBEOpublication`, `RTMGenerated`, `ActiveVaultHashComparison`, `PRIVATEKEY`, `APPROVED_FOR_LIVE_EXECUTION`, `blkTestPassApproval`, and double-encoded protected paths.
4. Add RED tests requiring exact upstream excluded-authority set equality and list cardinality.
5. Implement the smallest GREEN change to recompute upstream packet hash, enforce exact upstream denied authorities, and recursively scan safe upstream fields.
6. Preserve existing BLK-SYSTEM-061 status and no-side-effect flags.

### Task 002 — BLK-067 boundary, active doctrine gate, and hostile review

Deliverables:

```text
docs/BLK-067_ceb009-patch-approval-envelope-integrity-hardening-boundary.md
python/test_active_doctrine_review_gates.py
docs/reviews/BLK-SYSTEM-062_ceb009-patch-approval-envelope-integrity-hardening-hostile-review.md
docs/outcomes/BLK-SYSTEM-062_task-002-outcome.md
```

Actions:

1. Add BLK-067 boundary markers for upstream remediation packet hash recomputation, exact upstream denied-authority equality, recursive upstream laundering rejection, and review-only/no-patch/no-runtime preservation.
2. Add a persistent active doctrine gate proving BLK-067 denies inherited approval, forged self-reported packet hashes, live Kuronode scans, source/Git mutation, Electron/smoke-test execution, TypeScript tooling, package managers, live Codex, BLK-test MCP, BEO publication, RTM generation, protected-body reads, coverage/drift claims, and production isolation claims.
3. Hostile-review forged packet hash acceptance, stale packet body acceptance, request hash matching a forged upstream hash, nested laundering in upstream packet surfaces, compact/camel/allcaps authority tokens, protected path encoding, exact denied-authority weakening, and status-marker drift.
4. Remediate blockers with tests or docs before closeout.

### Task 003 — Verification, closeout, commit, and push

Deliverables:

```text
docs/outcomes/BLK-SYSTEM-062_task-003-outcome.md
docs/outcomes/BLK-SYSTEM-062_sprint-closeout.md
```

Actions:

1. Run focused CEB_009 patch approval envelope tests.
2. Run focused BLK-067 active doctrine gate.
3. Run full Python discovery.
4. Run Go tests and Go vet.
5. Run `git diff --check` and markdown fence checks.
6. Record final verification output.
7. Stage exact paths only.
8. Commit and push to `origin/main`.
9. Report final commit hash.

---

## 7. Stop Conditions

Stop and report before closeout if any implementation:

1. treats this sprint as approval to patch Kuronode;
2. edits Kuronode source or Git;
3. runs `npm run test:smoke`, launches Electron, or waits for the 30-second timeout path;
4. scans the live Kuronode checkout beyond existing BLK-System-owned fixture material;
5. executes TypeScript tooling, package managers, network, browser, model-service, or cyber tooling;
6. starts BLK-test MCP or Codex;
7. reads protected BLK-req bodies or accepts protected paths as envelope targets;
8. claims production sandbox/host-secret isolation;
9. publishes BEOs, generates RTM, claims coverage, or performs drift rejection;
10. treats the approval envelope as granted approval, source fix, live validation, BEO/CEO publication, RTM, Codex, BLK-test MCP, source-mutation, or production authority;
11. fails hostile review or verification.
