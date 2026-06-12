L2_ID: L2-K2-019
BEB_ID: BEB-K2-019
BEO_ID: BEO-K2-019
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write

## Tactical route objective

Implement `BEB-K2-019` exactly: bounded read-only project source diagnostic intake that bridges the existing project/package inspection surface to the existing parser diagnostic/model-health loop. Keep the implementation inside the four allowed files and preserve the K2 authority boundary.

## Strict TDD route

1. In `tests/project-package-inspection.test.mjs` and/or `tests/parser-diagnostic-loop.test.mjs`, first add RED assertions for the K2-019 readiness probes below. Run focused tests and observe RED because the new intake helpers/fields are missing.
2. Implement the smallest changes in `src/main/project-package-inspection.mjs` and `src/main/parser-diagnostic-loop.mjs` to satisfy the tests.
3. Re-run focused tests to GREEN, then run `node scripts/validate-foundation.mjs`; run `npm test` if feasible.
4. Do not stage, commit, or modify files outside the route allowlist. BLK-pipe owns staging/commit.

## Required implementation constraints

- Add only bounded read-only source-body intake for a single `.sysml` or `.kerml` source selected from either a ready single-file selection or a ready directory package with exactly one active source candidate.
- If a directory package contains zero source candidates, multiple source candidates, conflicting package markers, malformed markers, unsupported extensions, unreadable source, non-regular selections, or path-spoof/traversal seams, fail closed with sanitized metadata.
- Feed the accepted bounded source text into the existing parser diagnostic loop without exposing the source text in the returned/public object.
- Add explicit false denied-authority flags for source write/repair/adoption/import/export/provider/projection/layout/support/telemetry/RTM/blk-link/BEO-publication surfaces where the public result needs them.
- Keep output objects and nested diagnostic objects deeply frozen.
- Keep `src/main/parser-diagnostic-loop.mjs` free of filesystem/path/process/network/Electron/provider/package-manager imports or calls; all filesystem reads must remain in `src/main/project-package-inspection.mjs` and only for the bounded source body.
- Use deterministic bounds; oversized source must produce a sanitized fail-closed result rather than truncating and passing partial source as healthy.
- Do not add dependencies, package scripts, renderer/preload/Electron IPC, provider clients, layout/canvas/SVG code, support-bundle export, telemetry, or persistence.

## Required adversarial tests

Cover every probe in the BEB readiness card:

- `K2-019-AR-001`: malformed/unbalanced/invalid source body becomes fail-closed parser/model-health metadata.
- `K2-019-AR-002`: unreadable source produces sanitized source-access failure with no raw OS error/path/stack.
- `K2-019-AR-003`: traversal/spoofing/non-regular/unsupported selections cannot read arbitrary files or leak body.
- `K2-019-AR-004`: hostile caller metadata and authority booleans cannot override result state.
- `K2-019-AR-005`: oversized source fails closed without partial body leakage.
- `K2-019-AR-006`: unsupported extension is not read.
- `K2-019-AR-007`: stale/conflicting/malformed package markers deny intake.
- `K2-019-AR-008`: parser runtime unavailable remains fail-closed.
- `K2-019-AR-009`: marker strings embedded in source body never serialize back out.
- `K2-019-AR-010`: denied adjacent authority flags remain false.

## Public vocabulary expectations

Prefer exact, bounded names such as `project-source-diagnostic-intake`, `runProjectSourceDiagnosticIntake`, `sourceIntakeState`, `sourceIntakeReason`, `sourceDiagnosticScope`, `sourceBodyReadAuthorized`, `rawSourceBodyRetained`, and `sourceBodyBytesRead`. Do not expose raw `path`, `filename`, `directoryListing`, `sourceText`, `content`, `rawContent`, `diagnostics` with raw messages, parser handles, source coordinates, provider payloads, prompts, credentials, OS error bodies, or stack traces.

## Verification commands

Run these from `/home/dad/code/Kuronode-v2` and preserve output in Codex final message:

```bash
node tests/project-package-inspection.test.mjs
node tests/parser-diagnostic-loop.test.mjs
node scripts/validate-foundation.mjs
npm test
```

If `npm test` is too slow or fails after focused GREEN for unrelated pre-existing reasons, report the exact blocker and keep the focused/foundation outputs. Do not fabricate successful output.

## Denied route authority

This L2 does not authorize project writes, canonical mutation, import/adoption/promotion, source repair, provider calls, Agent A behavior, dependency installation, package/network/browser/cyber tooling, renderer/preload/Electron IPC expansion, projection/layout trust, support export, telemetry, RTM generation, production `blk-link`, BEO publication/signing/storage/ledger, or future reusable BLK-pipe/Codex authority.
