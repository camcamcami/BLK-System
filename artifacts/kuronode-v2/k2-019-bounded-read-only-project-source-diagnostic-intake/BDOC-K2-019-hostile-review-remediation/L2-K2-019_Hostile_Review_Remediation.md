L2_ID: L2-K2-019
BEB_ID: BEB-K2-019
MODEL: gpt-5.5
ROUTE: BEB-L2 -> BLK-pipe -> Codex workspace-write
TARGET_HASH: 61c5d72dc01f15013c3a8a88f5691b9058e48181

Implement the BEB-K2-019 hostile-review remediation in the allowed files only.

Use strict TDD / regression-first remediation:

1. Add failing tests first in `tests/project-package-inspection.test.mjs` and/or `tests/parser-diagnostic-loop.test.mjs` for:
   - selected directory symlink package denial before source body read;
   - dynamic `process.getBuiltinModule` monkeypatch not accessed / unable to forge source bytes;
   - exported frozen K2-019 source-intake states/reasons exact arrays;
   - `runProjectSourceDiagnosticIntake` top-level and nested parser summary deny mutation-looking flags including `safeMutationAllowed: false`;
   - invalid selection and NUL path seam denial if not already covered.
2. Patch `src/main/project-package-inspection.mjs` minimally:
   - Replace dynamic `sourceAccessModule()` / `process.getBuiltinModule` with static `node:fs` imports (`lstatSync`, `openSync`, `fstatSync`, `readSync`, `closeSync` as needed).
   - Add a selected-path lstat/non-symlink guard for source-intake before accepting file or directory package reads.
   - Preserve direct symlink/non-regular denial and bounded read limit.
   - Add exported frozen K2-019 source-intake state/reason vocabularies and use the reason vocabulary fail-closed.
   - Sanitize parser summaries returned inside project source intake so no nested source-intake public envelope carries mutation/provider/runtime/publication authority; specifically `safeMutationAllowed` must be false in the returned source-intake parser summary.
   - Update stale top comments to say bounded read-only source-body intake is authorized only for K2-019 diagnostics, while parser runtime/process/provider/mutation remains denied.
3. Patch validation gates in `scripts/validate-foundation.mjs` (and only if needed, `scripts/validation/config/denied-authority-patterns.mjs`) so K2-019 is contract-pinned:
   - K2-019 section/listing exists.
   - Required exported states/reasons/method tokens are checked exactly.
   - Stale K2-001..K2-018 wording is advanced to include K2-019.
   - `process.getBuiltinModule` is forbidden for this source intake seam; static bounded fs operations are either explicitly expected or not falsely denied.
4. Run and keep green:
   - `node tests/project-package-inspection.test.mjs`
   - `node tests/parser-diagnostic-loop.test.mjs`
   - `node scripts/validate-foundation.mjs`
   - `npm test`
   - `npm run build`
5. Final status must modify only the allowed files listed in the manifest. Do not commit; BLK-pipe will stage/commit.
