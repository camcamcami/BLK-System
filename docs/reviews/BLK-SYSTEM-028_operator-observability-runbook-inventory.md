# BLK-SYSTEM-028 — Operator Observability Runbook Inventory

**Status:** Complete inventory — fixture/runbook planning evidence only
**Date:** 2026-05-08T11:07:00+10:00
**Plan:** `docs/plans/blk-system-028_operator-ux-observability-runbooks.md`
**BLK-024 track:** Track I — Operator UX, observability, and escalation
**Maturity:** L0 runbook inventory supporting L1 local fixtures

---

## 1. Inventory Boundary

This inventory maps common BLK-System operator-facing failure surfaces to concise status vocabulary and escalation needs. It is not a live health-check implementation, not a command runner, not an approval gate, and not a grant of new runtime authority.

The future helper for this sprint may normalize already-supplied evidence dictionaries only. It must not read raw files or logs, execute commands, inspect Git state, call Discord/GitHub APIs, contact model/network services, read protected BLK-req bodies, publish BEOs, generate RTM, or decide drift.

---

## 2. Failure Surface Table

| Failure class | Owning domain | Evidence inputs expected | Concise status phrase | Needed human decision | Forbidden authority inheritance |
| --- | --- | --- | --- | --- | --- |
| `INVALID_PAYLOAD` | BLK-pipe / contracts | POSIX route, validation error, payload ID, `beb_id`, trace artifact identities | `Blocked before execution: invalid payload` | Fix payload/brief and redispatch if still approved | Must not start tactical execution, BLK-test, BEO, or RTM from a rejected payload |
| `UNAUTHORIZED_MUTATION` | BLK-pipe / gitguard | unauthorized paths, revert status, dirty status, target hash, report ID | `Blocked and reverted: unauthorized mutation` | Decide whether to revise allowlist or reject tactical work | Must not treat reverted mutation as accepted source change |
| `VALIDATION_FAILED` | BLK-pipe / validation | validation profile/command, exit code, bounded output excerpt, report ID | `Blocked after mutation: validation failed` | Decide whether tactical retry is needed within failure ceiling | Must not publish BEO success or run BLK-test as if validation passed |
| `OUTPUT_FLOOD` | BLK-pipe / execguard | output cap, killed/truncated flag, report ID, bounded excerpt | `Blocked: output limit exceeded` | Decide whether to inspect raw evidence out of band or retry with narrower task | Must not embed unbounded logs in Discord/Hermes context or mark unknown output as PASS |
| `INVALID_REVERT_ANCHOR` | BLK-pipe / revert | target hash, sprint base hash, current hash, revert refusal reason | `Blocked: revert anchor mismatch` | Human must inspect workspace before further mutation | Must not perform blind reset, broad checkout, or accept dirty state silently |
| `DIRTY_WORKSPACE` | BLK-pipe / gitguard | dirty paths, allowed paths, revert status, report ID | `Blocked: workspace is dirty` | Human must clean/commit/inspect exact paths before retry | Must not stage broad paths or assume BLK-pipe cleaned unknown files |
| `MISSING_APPROVAL` | Human gate / blk-relay | approval ID, source channel, actor identity, requested action, timestamp | `Blocked: missing approval` | Obtain separate current human approval for the specific authority | Must not inherit Codex/execution/BLK-test/BEO/RTM approvals across stages |
| `STALE_OR_REPLAYED_APPROVAL` | Human gate / blk-relay | approval ID, expiry, used IDs, source evidence hash | `Blocked: approval stale or replayed` | Obtain a fresh source-bound approval | Must not run one-run tools or publication from stale approval |
| `PROTECTED_VAULT_REQUEST` | BLK-req / BLK-pipe | requested path/class, refusal route, report ID | `Blocked: protected BLK-req vault access denied` | Revise request to use approved metadata/context channel | Must not read/copy/parse/hash protected bodies through observability or tactical layers |
| `DISABLED_BLK_TEST` | BLK-test | disabled transport descriptor, requested tool/profile, approval state | `Blocked: BLK-test transport disabled` | Decide whether a separate future BLK-test approval/sprint is warranted | Must not start production BLK-test MCP, arbitrary shell, or new smoke from status summary |
| `DRAFT_ONLY_BEO` | BEO | BEO fixture status, `beo_publication`, evidence status, source report ID | `Advisory only: BEO remains draft-only` | Decide whether a separate publication-authority sprint is needed | Must not emit runtime `PUBLISHED` BEOs, signer actions, storage writes, or ledger mutation |
| `RTM_NOT_GENERATED` | blk-link / RTM | `rtm_status`, proposal status, missing approval reason, trace/hash metadata identities | `Advisory only: RTM not generated` | Decide whether to explicitly authorize a future runtime RTM sprint | Must not generate RTM IDs, ledgers, coverage matrices, or drift decisions |
| `UNKNOWN_OR_MALFORMED_REPORT` | Observability helper | report type, malformed fields, raw evidence hash/reference if supplied | `Blocked: report is unknown or malformed` | Human or developer must inspect source evidence and add a supported fixture path if needed | Must not guess PASS/FAIL, infer approvals, or execute fallback commands |

---

## 3. Standard Status Vocabulary

The sprint should pin concise status phrases to reduce operator ambiguity:

- `Blocked before execution` — no tactical/source mutation should have occurred.
- `Blocked and reverted` — mutation was attempted and BLK-pipe reports cleanup/revert evidence.
- `Blocked after mutation` — mutation may exist or have been reverted; dirty/revert indicators must be explicit.
- `Advisory only` — evidence is useful context but no new authority follows.
- `Needs human approval` — a specific, separate approval is missing; another stage's approval is not enough.
- `Needs human inspection` — workspace/raw evidence state cannot be safely summarized into an automatic next step.

---

## 4. Escalation Package Evidence Rules

A valid L1 escalation fixture should preserve:

1. `package_status: "OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY"`;
2. status fixture IDs and failure classes;
3. owning domains;
4. human decision required;
5. retry/revert/dirty indicators;
6. bounded excerpts only;
7. raw evidence hashes/references supplied by the caller;
8. explicit no-side-effect booleans.

It should not preserve unbounded raw logs inline. Token-heavy evidence belongs in a referenced artifact path, URL, or operator-controlled log system supplied by the caller, not in Discord/Hermes context.

---

## 5. Future Health-Check Boundary

BLK-024 Track I mentions health checks for local binaries, Python tools, schemas, test fixtures, and disabled transport stubs. This sprint intentionally does not implement live health checks because that would require executing commands and inspecting the host. A future health-check sprint must separately decide:

- which commands may run;
- whether network is forbidden;
- which paths may be inspected;
- how output is bounded/redacted;
- whether failures are advisory only or blocking;
- how protected-vault body reads remain impossible.

---

## 6. Acceptance Mapping for Task 2

Task 2 should prove via RED/GREEN tests that the observability fixture layer:

- classifies all failure classes in the table;
- rejects unsupported top-level and nested forbidden fields;
- rejects runtime authority laundering (`rtm`, publication, signer, ledger, drift, approval-capture, command execution, body/path/secret fields);
- bounds excerpts and packages;
- preserves raw evidence identity/hash/reference without fetching evidence;
- exposes dirty/revert/retry/human-decision flags explicitly;
- contains no live execution/network/file-scan surface in implementation source.
