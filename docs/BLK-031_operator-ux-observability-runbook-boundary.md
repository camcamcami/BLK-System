# BLK-031 — Operator UX / observability runbook boundary

**Status:** Active fixture/runbook boundary contract — not execution authority
**Purpose:** Define the BLK-SYSTEM-028 operator observability and escalation runbook boundary so humans can distinguish policy blocks, broken code, missing approvals, disabled future authority, and dirty/revert states without granting new runtime power.
**Scope:** BLK-024 Track I — Operator UX, observability, and escalation. L1 deterministic local fixtures plus L0 runbook doctrine only.

---

## 0. Non-Execution and Non-Authority Boundary

BLK-031 does not run live health checks, does not execute commands, does not inspect files, does not fetch logs, does not contact Discord/GitHub APIs, does not contact network/model services, does not inspect Git state, does not mutate source, does not capture approvals, does not read protected BLK-req vault bodies, does not authorize production BLK-test MCP, does not authorize new live BLK-test smoke runs, does not authorize authoritative BEO publication, does not authorize runtime `PUBLISHED` BEO output, does not access signer/storage/ledger/rollback authority, does not authorize RTM generation, does not generate RTM IDs or ledgers, does not create runtime coverage matrices, and does not authorize RTM drift rejection.

The only current runtime shape owned by this boundary is deterministic normalization of already-supplied evidence dictionaries into local fixtures:

- `OPERATOR_OBSERVABILITY_FIXTURE_ONLY`
- `OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY`
- `OBSERVABILITY_ONLY_NOT_EXECUTION`

---

## 1. Governing Architecture

- **BLK-001:** Observability does not merge the V-model domains. It reports whether BLK-req, Hermes planning, BLK-pipe, BLK-test, BEO, blk-link/RTM, or human gates are blocked.
- **BLK-002 / BLK-005 / BLK-006:** Protected BLK-req bodies remain outside this helper. Status may reference caller-supplied artifact IDs and `version_hash` values only.
- **BLK-003:** Escalation packages explain failure ceilings, revert state, dirty state, and needed human decisions but do not dispatch retries or approve work.
- **BLK-004:** BLK-pipe remains the deterministic enforcement authority. Python observability is advisory and non-executing.

---

## 2. Required Runbook Vocabulary

BLK-SYSTEM-028 pins these operator-facing phrases:

| Failure class | Status phrase | Owning domain |
| --- | --- | --- |
| `INVALID_PAYLOAD` | `Blocked before execution: invalid payload (Exit 8)` | BLK-pipe |
| `UNAUTHORIZED_MUTATION` | `Blocked and reverted: unauthorized mutation` | BLK-pipe |
| `VALIDATION_FAILED` | `Blocked after mutation: validation failed` | BLK-pipe |
| `OUTPUT_FLOOD` | `Blocked: output limit exceeded` | BLK-pipe |
| `INVALID_REVERT_ANCHOR` | `Blocked: revert anchor mismatch` | BLK-pipe |
| `DIRTY_WORKSPACE` | `Blocked: workspace is dirty` | BLK-pipe |
| `MISSING_APPROVAL` | `Blocked: missing approval` | Human gate |
| `STALE_OR_REPLAYED_APPROVAL` | `Blocked: approval stale or replayed` | Human gate |
| `PROTECTED_VAULT_REQUEST` | `Blocked: protected BLK-req vault access denied` | BLK-req |
| `DISABLED_BLK_TEST` | `Blocked: BLK-test transport disabled` | BLK-test |
| `DRAFT_ONLY_BEO` | `Advisory only: BEO remains draft-only` | BEO |
| `RTM_NOT_GENERATED` | `Advisory only: RTM not generated` | blk-link |
| `OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY` | `Fixture RTM ledger generated: BLK-033 fixture-only evidence` | blk-link |
| `FORBIDDEN_RUNTIME_RTM_GENERATION` | `Blocked: runtime RTM generation is not authorized` | blk-link |
| `DRIFT_REVIEW_REQUIRED_NOT_REJECTED` | `Drift review required: human review only, not drift rejection` | blk-link / human gate |
| `UNKNOWN_OR_MALFORMED_REPORT` | `Blocked: report is unknown or malformed` | Observability |

These phrases intentionally separate policy blocks from broken code, missing approval, disabled future authority, and advisory-only evidence. A status phrase never implies permission to retry, publish, generate RTM, reject drift, or mutate source.

---

## 3. Status Fixture Contract

A valid `OPERATOR_OBSERVABILITY_FIXTURE_ONLY` record must include:

- `authority: "OBSERVABILITY_ONLY_NOT_EXECUTION"`;
- failure class and owning domain;
- concise status phrase;
- source report ID and `beb_id`;
- caller-supplied trace artifact identities and `version_hash` values;
- caller-supplied raw evidence reference and hash;
- bounded evidence excerpt only;
- explicit `retry_count`, `failure_ceiling`, `failure_ceiling_remaining`, `reverted`, and `dirty` indicators;
- `human_decision_required: true`;
- a non-authorizing `next_operator_action` phrase;
- no-side-effect booleans proving no command execution, file reading, network calls, source mutation, approval capture, BEO publication, RTM generation, drift decision, protected-body read, or active-vault scan occurred inside the helper.

The fixture must reject unsupported top-level fields and nested authority-laundering fields, including runtime RTM, publication, signer, ledger, drift, approval-capture, command/shell, protected path, body/content/text/markdown, and secret-bearing keys.

---

## 4. Escalation Package Contract

A valid `OPERATOR_ESCALATION_PACKAGE_FIXTURE_ONLY` record may aggregate one or more status fixtures. It must preserve:

- status fixture IDs;
- failure classes;
- owning domains;
- concise statuses;
- human-decision requirement;
- next operator actions;
- raw evidence references and hashes;
- bounded excerpts only;
- `raw_evidence_embedded: false`;
- no-side-effect booleans.

It must not embed unbounded raw logs in Discord/Hermes context. Raw evidence remains wherever the caller says it lives; this boundary does not fetch it.

Additional hard gates from the BLK-SYSTEM-028 hostile review:

- derivative/suffix authority fields fail closed, not only exact forbidden keys;
- escalation packages have package-level count/size bounds;
- retry wording never implies approval and `retry_approved_by_fixture` remains false;
- dirty/reverted indicators must be class-consistent;
- caller-supplied references/IDs are bounded;
- nested side-effect or authority fields under trace metadata are rejected rather than silently dropped.

---

## 5. Common Runbooks

### 5.1 Invalid payload

When the status says invalid payload, the operator should fix the payload or brief before redispatch. The system must not start tactical execution, BLK-test, BEO projection, or RTM generation from a rejected payload.

### 5.2 Unauthorized mutation

When the status says unauthorized mutation, inspect revert and dirty indicators. A successful revert is not accepted source change. A dirty state requires human workspace inspection before retry.

### 5.3 Validation failed

When validation failed, inspect the bounded validation excerpt and raw evidence reference. Do not publish BEO success or run BLK-test as if validation passed.

### 5.4 Output limit exceeded

When output limit exceeded, do not paste unbounded raw logs into Discord/Hermes context. Use the raw evidence reference/hash and narrow the task or inspect out of band.

### 5.5 Revert anchor mismatch

When revert anchor mismatch appears, do not perform blind broad resets. Human inspection owns the next step.

### 5.6 Workspace is dirty

When workspace is dirty, inspect exact dirty paths in the source report. Observability does not stage, commit, clean, reset, or checkout.

### 5.7 Missing approval / approval stale or replayed

A missing, stale, or replayed approval requires fresh source-bound human approval for the exact authority. Codex/execution approval is not BLK-test approval; BLK-test approval is not BEO publication approval; publication approval is not RTM generation approval; RTM generation approval is not RTM drift rejection authority.

### 5.8 Protected BLK-req vault access denied

Protected BLK-req vault access denial should be resolved through approved metadata/context channels. Observability must not read, copy, parse, or hash protected bodies.

### 5.9 BLK-test transport disabled

Disabled BLK-test transport is a current authority boundary, not a transient outage. Production BLK-test MCP and new live smoke runs require separate future approval.

### 5.10 BEO remains draft-only

Draft-only BEO evidence is advisory. It does not authorize authoritative BEO publication, runtime `PUBLISHED` output, signer key material, storage writes, public ledger mutation, rollback, revocation, or supersession.

### 5.11 RTM not generated

RTM not generated remains the expected state outside BLK-033 fixture-only generation. It does not authorize RTM IDs, ledgers, coverage matrices, active-vault comparison, protected-body reads, or drift rejection.

### 5.12 Fixture RTM ledger generated

`OFFLINE_RTM_LEDGER_GENERATED_FIXTURE_ONLY` means BLK-033 fixture-only evidence exists from already-supplied dictionaries. This fixture RTM does not authorize live vault comparison, fixture RTM does not authorize production RTM generation, and fixture RTM does not authorize drift rejection. It also does not authorize protected-body reads, active-vault filesystem scanning, authoritative BEO publication, signer/storage/public-ledger side effects, BLK-test startup, or source mutation.

### 5.13 Forbidden runtime RTM generation

`FORBIDDEN_RUNTIME_RTM_GENERATION` means an input or report attempted to treat fixture evidence as live/runtime RTM authority. The operator must block the path and require a separate human-approved sprint before any production RTM generation, active-vault file comparison, protected-body access, or runtime coverage matrix generation.

### 5.14 Drift review required, not rejected

`DRIFT_REVIEW_REQUIRED_NOT_REJECTED` means supplied trace/hash metadata indicates human review is needed. It is not RTM drift rejection, not automatic failure authority, not source rollback authority, and not BEO revocation/supersession authority.

### 5.15 Unknown or malformed

Unknown or malformed reports must be blocked for human/developer inspection. The helper must not guess PASS/FAIL or execute fallback commands.

---

## 6. Future Health-Check Split

Future Track I health checks for local binaries, Python tools, schemas, fixtures, and disabled transport stubs require a separate sprint because they would execute commands or inspect host state. That future sprint must define exact allowed commands, output bounds, network denial, path boundaries, redaction, and advisory-vs-blocking semantics before any implementation.
