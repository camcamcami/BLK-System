# BLK-058 — Kuronode TypeScript Power-of-Ten Tactical Standard

**Status:** Active tactical coding-standard doctrine — not sprint authority
**Date:** 2026-05-10T14:58:24+10:00
**Purpose:** Formalize a Kuronode-specific adaptation of NASA JPL's "Power of Ten" safety-critical coding rules for TypeScript output produced by Codex or any tactical worker through BLK-System.
**Scope:** Kuronode TypeScript, React, Electron, Zustand, parser, worker, layout, and rendering code created or modified under BLK-System execution briefs. This document constrains tactical output quality; it does not grant runtime execution, source mutation, BLK-test production MCP, BEO publication, RTM generation, or protected BLK-req body-read authority.

---

## 0. Non-Execution and Non-Authority Boundary

BLK-058 is a coding-standard doctrine document. It does not authorize:

- live Codex execution;
- reusable tactical LLM dispatch;
- new `blk-pipe` execution runs;
- source mutation outside exact approved allowlists;
- production or generic BLK-test MCP;
- arbitrary shell as BLK-test behavior;
- protected BLK-req vault body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
- authoritative BEO publication;
- runtime `PUBLISHED` BEO output;
- runtime RTM generation;
- RTM drift rejection;
- signer, storage, ledger, rollback, revocation, supersession, or release authority;
- package-manager, network, browser, model-service, or cyber tooling authority;
- production sandbox, cgroup, namespace, VM, seccomp, AppArmor, SELinux, firewall, or host-secret-isolation claims.

A future sprint may implement mechanical gates for this standard, but those gates require their own plan, allowlists, tests, hostile review, and approval envelope.

---

## 1. Relationship to BLK-001

BLK-001 defines BLK-System as an autonomous V-model that separates architectural intent, tactical execution, deterministic enforcement, physical verification, BEO publication, and trace closure.

BLK-058 defines the default safety envelope for the tactical TypeScript that BLK-System forges for Kuronode.

In BLK-001 terms:

- Hermes remains Architect and Hostile Auditor.
- Codex or any tactical worker remains an implementation agent, not an authority source.
- `blk-pipe` remains the mutation blast shield and exact-path enforcement layer.
- BLK-test remains evidence only and must not mutate source, publish BEOs, or generate RTMs.
- The canonical `version_hash` and exact trace artifacts remain the trace baton.
- Kuronode TypeScript must be written so deterministic tools can inspect, typecheck, lint, bound, and hostile-review it.

This standard exists because BLK-System is built to safely modify Kuronode, and Kuronode is a TypeScript/Electron product. BLK-058 therefore targets Kuronode tactical TypeScript output, not the internal Go/Python implementation language of BLK-System.

---

## 2. Applicability

BLK-058 applies when a BEB, sprint plan, or Layer 2 tactical packet asks a worker to create or modify Kuronode source in any of these surfaces:

1. Electron main-process TypeScript.
2. Electron preload and IPC bridge TypeScript.
3. React renderer TypeScript and TSX.
4. Zustand stores, selectors, and state-transition helpers.
5. `GraphAdapter.ts` and any JointJS boundary module.
6. ELK.js layout adapters and layout workers.
7. tree-sitter SysML parser integration and any Wasm-facing parser worker.
8. SQLite persistence adapters.
9. test harnesses, fixtures, and validation helpers that exercise Kuronode TypeScript behavior.
10. future Kuronode TypeScript services introduced under BLK-System governance.

BLK-058 does not supersede product-specific Kuronode architecture documents. It complements them by converting tactical code-quality expectations into explicit, hostile-reviewable constraints.

---

## 3. The Ten Tactical Constraints

### Rule 1 — Control Flow Simplicity

Kuronode tactical TypeScript must use simple, reviewable control flow.

Requirements:

- Do not use recursion unless an execution brief explicitly grants a narrow exception and states the maximum depth plus proof of termination.
- Prefer bounded iterative traversal for ASTs, graph structures, layout queues, and dependency walks.
- Do not use complex nested `try`/`catch` blocks as control-flow routing.
- Do not hide state-machine transitions in callback chains or implicit event cascades.
- Make state transitions explicit and named when code spans Electron IPC, Zustand, workers, parser output, or renderer updates.

Kuronode-specific rationale:

Recursive graph, AST, or render traversals are a high-risk path for layout hangs, renderer lockups, memory growth, and context-runaway bugs.

### Rule 2 — Bounded Iterations

Every non-trivial loop must have a visible upper bound or operate over a pre-bounded collection with a known cap.

Requirements:

- Do not write `while (true)` in Kuronode tactical code.
- Do not write unbounded retry, polling, queue-drain, graph-walk, AST-walk, layout-pass, or event-processing loops.
- Preserve the Kuronode projected-node circuit breaker: layout/render paths must reject projected payloads above 500 nodes unless a later Kuronode doctrine explicitly revises the limit.
- Layout workers must bound node count, edge count, layout passes, retry attempts, and log volume where applicable.
- IPC request/response loops must have timeout, cancellation, or single-shot semantics.

Acceptable pattern:

```ts
const MAX_LAYOUT_PASSES = 3;
for (let pass = 0; pass < MAX_LAYOUT_PASSES; pass += 1) {
  // bounded layout recovery attempt
}
```

Forbidden pattern:

```ts
while (true) {
  // wait for layout convergence
}
```

### Rule 3 — Memory and Runtime State Stability

Kuronode tactical TypeScript must not create unbounded runtime state or rely on garbage collection for explicit lifecycle boundaries.

Requirements:

- Do not introduce unbounded arrays, maps, caches, subscription registries, pending IPC maps, log buffers, worker queues, or graph-cell registries.
- Bound any cache by item count, byte size, or lifecycle scope.
- Avoid module-level mutable state. If state must be module-scoped, document its authority, maximum size, initialization point, and cleanup path.
- Explicitly dispose Wasm/tree-sitter resources such as `Tree` and parser-owned objects where the API provides `delete()` or equivalent lifecycle calls.
- Explicitly clean up JointJS cells, papers, listeners, React effects, IPC handlers, workers, and timers.
- Never rely on renderer reloads, garbage collection, or process exit as the normal cleanup mechanism.

Kuronode-specific lifecycle rule:

Any code that creates a `Tree`, parser, worker, IPC listener, JointJS `cell`, JointJS `paper`, subscription, interval, timeout, or observer must define the matching teardown path in the same module or directly referenced lifecycle helper.

### Rule 4 — Function Length and Local Comprehensibility

Authority-sensitive Kuronode TypeScript functions must remain small enough for single-screen hostile review.

Requirements:

- A tactical function should not exceed 60 physical lines excluding blank lines and comments.
- A function over 60 lines requires decomposition or an explicit justification in the BEB/BEO outcome.
- Split mixed-responsibility functions into validation, transformation, side-effect, and reporting helpers.
- Do not combine parser traversal, layout mutation, renderer state update, IPC response handling, and persistence writes in one function.

Preferred decomposition:

1. validate input;
2. normalize or transform data;
3. perform exactly one side-effect class;
4. validate output/postcondition;
5. return a typed result.

### Rule 5 — High Assertion Density Through Preconditions and Postconditions

BLK-058 does not require fake assertion counts. It requires meaningful boundary checks.

Requirements:

- Every exported function must validate externally supplied parameters before use.
- Every IPC handler must validate channel payloads structurally before acting.
- Every parser, layout, graph, persistence, or worker boundary must reject malformed, missing, stale, or over-limit inputs.
- Functions returning nullable, optional, or error-shaped results must force callers to check the result before use.
- Critical transforms must check postconditions such as node-count preservation, unique IDs, non-negative coordinates, edge endpoint validity, and byte-offset ordering.

Kuronode-specific examples:

- AST nodes must preserve valid `startIndex <= endIndex` byte offsets.
- ELK-derived coordinates must be finite numbers before being applied to JointJS.
- Graph edges must reference known node IDs before rendering.
- IPC payloads must be discriminated and validated before they cross from main to renderer or renderer to main.

### Rule 6 — Minimal Data Scope and Controlled Mutation

Kuronode tactical TypeScript must minimize mutable state and keep data scoped to the smallest practical block.

Requirements:

- Use `const` by default.
- Use `let` only when mechanical mutation is required and local to a short block.
- Do not use `var`.
- Do not add ambient mutable singletons to bridge architectural gaps.
- Do not mutate Zustand state outside approved store actions.
- Do not mutate JointJS state outside `GraphAdapter.ts` or an explicitly approved adapter boundary.
- Do not leak worker-local or parser-local state into renderer-global state.

This rule reinforces the BLK-001 separation between architectural intent, tactical implementation, and deterministic verification by preventing hidden ambient authority inside the target TypeScript code.

### Rule 7 — Explicit Return and Caller Validation

Callers must check outputs before using them, especially across process, parser, layout, persistence, and worker boundaries.

Requirements:

- Do not ignore promises. Await or intentionally detach with a documented error path.
- Do not ignore return values from validation, parsing, layout, save, load, IPC, cleanup, or worker calls.
- Do not use non-null assertions (`!`) to bypass uncertainty at architectural boundaries.
- Do not use unchecked optional chaining as a substitute for validation when missing data changes authority, geometry, persistence, or rendering behavior.
- Use discriminated unions or result objects for recoverable errors.

Forbidden pattern:

```ts
void saveModel(model);
const x = graph.nodes[id]!.position.x;
```

Preferred pattern:

```ts
const saveResult = await saveModel(model);
if (!saveResult.ok) {
  return { ok: false, reason: saveResult.reason };
}

const node = graph.nodes[id];
if (!node) {
  return { ok: false, reason: "missing-node" };
}
```

### Rule 8 — Metaprogramming and Dynamic Execution Limits

Kuronode tactical TypeScript must remain statically analyzable.

Requirements:

- Do not use `eval()`.
- Do not use `new Function()`.
- Do not construct dynamic import paths from untrusted input.
- Do not use reflection-like dispatch to bypass explicit schema handling.
- Do not introduce deeply nested conditional types or type-level gymnastics that obscure runtime contracts.
- Do not generate executable JavaScript/TypeScript strings at runtime.
- Do not route IPC channel names through unvalidated dynamic strings.

Future exceptions require a separate approved design boundary and hostile review.

### Rule 9 — Flat, Validated Data Access

Kuronode tactical TypeScript should avoid fragile deep object chains and must validate nested structures before use.

Requirements:

- Avoid long chains such as `a.b.c.d.e` in authority-sensitive code.
- Normalize external payloads into flat, typed internal records before business logic.
- Validate parser JSON, IPC payloads, persisted SQLite records, and worker messages at the boundary.
- Prefer named selectors and accessors over repeated ad hoc deep property access.
- Keep nested structures schema-closed, depth-bounded, and hostile-reviewable.

This rule does not ban structured AST or graph objects. It bans trusting them without validation.

### Rule 10 — Zero Warning Tolerance

Kuronode tactical TypeScript must treat static diagnostics as blocking evidence unless the execution brief explicitly scopes an exception.

Requirements:

- TypeScript must pass the project-owned strict typecheck profile.
- ESLint warnings must be treated as failures when a project-owned lint profile exists.
- Unused variables, implicit `any`, unsafe assignment, unsafe member access, floating promises, unreachable branches, and missing cleanup warnings are sprint-blocking by default.
- Validation profiles must be repository-owned; less-trusted or autonomous payloads must not supply arbitrary shell validation commands.
- If package-manager, network, or tool-install commands are needed, they require a separate approval boundary.

Expected future validation profile examples:

```text
kuronode-typecheck-strict
kuronode-eslint-zero-warning
kuronode-power-of-ten-static
kuronode-renderer-lifecycle-tests
kuronode-ipc-boundary-tests
```

These names are future profile candidates only. BLK-058 does not create the profiles or authorize running them.

---

## 4. Kuronode-Specific Mandatory Overlays

The ten rules above are interpreted through current Kuronode architecture invariants.

### 4.1 Electron Process Boundary

Renderer-owned Zustand state must not be read directly by the Electron main process.

Allowed patterns:

- Main to renderer push: main process uses `webContents.send(...)`; renderer handles with `ipcRenderer.on(...)`.
- Main to renderer pull: renderer exposes an `ipcMain.handle(...)` / `ipcRenderer.invoke(...)` path where the state owner returns the requested typed payload.

Forbidden wording and code shape:

- "Main process queries Zustand."
- "Main process reads renderer store state."
- main-process imports of renderer Zustand stores.

### 4.2 ELK Geometry Authority

ELK.js is the authority for graph layout geometry.

Requirements:

- Do not hand-author persistent JointJS coordinates outside the approved ELK-to-JointJS adapter path.
- Force ELK bend points into JointJS link vertices when rendering routed edges.
- Reject non-finite, missing, or malformed layout coordinates before applying them to JointJS.
- Preserve the projected-node circuit breaker at 500 nodes.

### 4.3 GraphAdapter Quarantine

JointJS imperative operations must remain quarantined in `GraphAdapter.ts` or an explicitly approved adapter boundary.

Requirements:

- React/Zustand state should remain declarative.
- JointJS cells, papers, listeners, and view mutations should not leak into feature components.
- All graph synchronization mutexes must use `try`/`finally` so exceptions cannot leave the canvas deadlocked.
- Removed graph elements must call appropriate JointJS cleanup APIs such as `cell.remove()` where applicable.

### 4.4 Parser and Wasm Lifecycle

Parser and tree-sitter resources must be explicitly managed.

Requirements:

- Parser workers should be stateless between jobs unless a later approved design defines bounded state.
- Tree-sitter `Tree` objects must be deleted after use where supported.
- Parser output must preserve byte offsets required by the surgical splice editor path.
- Full-file generation and surgical editing paths must remain distinct when the governing Kuronode document requires that separation.

### 4.5 React and IPC Cleanup

Kuronode TypeScript must clean up side-effect subscriptions.

Requirements:

- React effects that subscribe must return cleanup functions.
- IPC listeners must be removed when their owning lifecycle ends.
- Worker handlers, timers, intervals, observers, and event listeners must be explicitly disposed.
- Cleanup failures must not be silently swallowed when they could leave stale renderer state, duplicate handlers, or resource leaks.

---

## 5. BEB / BEO Incorporation Rule

When a Kuronode execution brief modifies TypeScript in an applicable surface, Hermes should include a concise BLK-058 tactical standard section in the Layer 2 packet.

Minimum packet language:

```text
BLK-058 applies: produce Kuronode TypeScript with no recursion unless approved, bounded loops, no unbounded caches/state, small reviewable functions, validated inputs/outputs, const-first local scope, checked nullable/error results, no eval/dynamic execution, validated nested data access, and zero TypeScript/ESLint warnings under project-owned validation profiles. Preserve Electron process boundaries, ELK geometry authority, GraphAdapter quarantine, parser/Wasm cleanup, React/IPC cleanup, and the 500 projected-node circuit breaker.
```

If the task is intentionally outside one of these rules, the brief must name the exception, bound it, and state the validation evidence required.

---

## 6. Future Mechanical Enforcement Ladder

BLK-058 is immediately available as doctrine for planning and hostile review. Mechanical enforcement should be introduced through later bounded sprints.

Recommended ladder:

1. **L0 doctrine only:** BLK-058 exists as a tactical standard and can be cited in BEBs.
2. **L1 static-fixture gates:** add repository-local static checks over sample Kuronode TypeScript snippets for recursion, unbounded loops, dynamic execution, long functions, and missing cleanup markers.
3. **L2 validation profiles:** add project-owned Kuronode validation profiles for strict typecheck, lint zero-warning, and lifecycle/power-of-ten scans.
4. **L3 synthetic smoke:** run the checks on synthetic Kuronode fixtures under an explicit one-run approval envelope.
5. **L4 real-repo pilot:** run the checks against one bounded Kuronode branch/workspace under exact target approval.
6. **L5 production authority:** only after monitoring, rollback, false-positive handling, operator controls, and hostile review are proven.

No rung inherits authority from the previous rung without explicit sprint approval.

---

## 7. Hostile Review Checklist

A hostile review of Kuronode TypeScript tactical output should ask:

1. Does any recursion exist, direct or indirect?
2. Does every non-trivial loop have a bounded collection or explicit maximum?
3. Can any cache, queue, map, array, listener registry, log, or worker state grow without bound?
4. Are functions small enough to review, or has complexity been hidden in a large mixed-responsibility function?
5. Are external inputs validated at parser, IPC, worker, persistence, and layout boundaries?
6. Are nullable/error returns checked before use?
7. Are promises awaited or intentionally detached with an error path?
8. Are `eval`, `new Function`, dynamic imports, dynamic IPC channels, or reflection-like dispatch present?
9. Are deep property chains trusted without validation?
10. Are TypeScript/ESLint warnings present or suppressed without approved justification?
11. Does main-process code attempt to read Zustand or renderer-owned state directly?
12. Does any code bypass ELK as the geometry authority?
13. Does JointJS imperative state escape the adapter boundary?
14. Are `Tree`, parser, worker, IPC, React effect, timer, observer, and JointJS lifecycles cleaned up?
15. Does any output imply BLK-test authority, BEO publication, RTM generation, protected BLK-req reads, or broader source mutation authority?

Findings should be remediated with tests or validation-profile gates where possible, not only prose.

---

## 8. BLK-001 Through BLK-006 Alignment

| Governing doc | BLK-058 alignment |
| --- | --- |
| BLK-001 — Master Architecture | Strengthens tactical execution quality while preserving separation between Hermes architecture, Codex implementation, deterministic enforcement, BLK-test evidence, BEO publication, and RTM trace closure. |
| BLK-002 — Artifact Lifecycle | Does not change BLK-req staging, linting, HITL approval, canonical hashing, active-vault immutability, or staged revision. |
| BLK-003 — Orchestration Protocol | Provides Layer 2 packet constraints for Kuronode TypeScript work while preserving human dispatch gates, failure ceilings, hostile audit, current BLK-test disablement, draft-only BEO boundaries, and disabled RTM authority. |
| BLK-004 — BLK-pipe V47 Suite | Complements exact allowlists, validation profiles, output caps, Git cleanup, and report evidence; does not replace `blk-pipe` enforcement or authorize arbitrary validation shell. |
| BLK-005 — BLK-Req Specification | Preserves canonical `version_hash`, trace binding, schema enforcement, staging isolation, and protected artifact boundaries. |
| BLK-006 — BLK-Req Implementation Brief | Preserves protected-vault hard-deny semantics and no protected body reads; BLK-058 applies to Kuronode tactical TypeScript, not BLK-req vault mutation. |

---

## 9. Stop Conditions

Pause and require human review if a proposed Kuronode tactical change attempts to use BLK-058 to justify:

1. live Codex execution without a separate approval envelope;
2. source mutation outside exact approved allowlists;
3. arbitrary shell validation instead of repository-owned validation profiles;
4. production or generic BLK-test MCP;
5. BLK-test source mutation;
6. protected BLK-req body reads, copying, parsing, hashing, summarizing, scanning, mutation, or drift comparison;
7. authoritative BEO publication;
8. RTM generation or drift rejection;
9. signer, storage, ledger, rollback, revocation, supersession, or release authority;
10. package-manager, network, model-service, browser, or cyber tooling authority;
11. production sandbox or host-secret-isolation claims;
12. weakening Kuronode's Electron process boundary, ELK geometry authority, GraphAdapter quarantine, projected-node circuit breaker, or parser/Wasm lifecycle rules.

---

## 10. Final Doctrine Statement

BLK-System exists to turn human and architectural intent into bounded, traceable Kuronode implementation changes without trusting an LLM's memory, restraint, or self-reported success.

BLK-058 makes the tactical TypeScript side of that contract explicit:

```text
Kuronode code forged through BLK-System must be bounded, typed, lifecycle-safe, statically analyzable, hostile-reviewable, and mechanically verifiable.
```

This standard improves the safety of future Kuronode work, but it is not itself an activation approval. It is a constraint that future approved execution must obey.
