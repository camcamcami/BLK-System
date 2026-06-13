# BLK-SYSTEM-364 — Route Retarget / Fallback Record / Remediation Wording Gates Plan

**Status:** planned-for-execution
**Created:** 2026-06-13
**Repository HEAD:** `7890ee9 feat: gate K2 route closeout fallback exceptions`

## 1. Goal

Strengthen the mechanical coverage left open after BLK-SYSTEM-363 for the operator's items 1 and 3–6:

1. source-worktree residue should default to a trusted sterile clean-worktree retarget package, not fallback;
3. fallback authorization should be a persisted exact record shape, not only prose/an in-memory dict;
4. remediation ceilings should apply to route/remediation policy, not only fallback authorization;
5. hostile-review remediation attempts should be classified as BLK-pipe-routed or blocked;
6. fallback/timeout/dirty wording in BEO/closeout prose should be toxic unless backed by successful later BLK-pipe route evidence or an explicit fallback authorization record.

This sprint remains deterministic/local: it adds validators and scanners only. It does not create worktrees, run live BLK-pipe, dispatch Codex, mutate Kuronode, publish BEOs, generate RTM, or authorize fallback.

## 2. Scope

Modify `python/beb_l2_blk_pipe_route.py` and `python/test_beb_l2_blk_pipe_route.py`.

### Item 1 — stronger clean-worktree default coverage

Add a default retarget planning helper that consumes a blocked source preflight and automatically builds the clean-worktree manifest candidate using the deterministic default clean-worktree path, while preserving:

- source cleanup unauthorized;
- worktree creation unauthorized;
- dispatch unauthorized;
- manifest approval required;
- no fallback classification.

### Item 3 — persisted fallback authorization record shape

Add an exact fallback authorization record materialization/loading path and require the fallback authorization object to carry persisted record identity fields:

- `fallback_auth_id` such as `FALLBACK-AUTH-K2-024`;
- `authorized_at`;
- `route_summary_path` and `route_summary_sha256`;
- `authorization_record_path` and `authorization_record_sha256`;
- `fallback_worktree`;
- exact allowed files, denied authorities, model, reason, status, target hash, remediation ceiling, and evidence artifacts.

### Items 4–5 — remediation policy gate

Add a local remediation route policy evaluator:

- remediation attempts must be routed through BLK-pipe;
- each remediation attempt must carry successful route summary evidence;
- 2 rounds emits warning evidence;
- 3 rounds requires a root-cause/scope review before closeout can continue;
- more than 3 rounds is blocked;
- Hermes-direct/external-Codex remediation attempts are blocked unless separately classified via the fallback exception path.

Wire this into the K2 final closeout scanner as optional evidence so closeout can fail mechanically when remediation routing is not governed.

### Item 6 — toxic fallback wording scanner

Add a closeout wording scan for BEO and optional closeout files. If text contains fallback/timeout/dirty/no-route-commit markers, require either:

- successful later BLK-pipe route gate PASS; or
- exact one-off fallback authorization record.

## 3. Files to Touch

- Modify: `python/beb_l2_blk_pipe_route.py`
- Modify: `python/test_beb_l2_blk_pipe_route.py`
- Modify: `python/test_lean_documentation_policy.py`
- Create: `docs/outcomes/BLK-SYSTEM-364_sprint-closeout.md`
- Create: this plan file

No new root `docs/BLK-###` doctrine document is planned.

## 4. TDD Tasks

1. RED: default clean-worktree retarget helper is missing and source residue does not yield a manifest candidate automatically.
2. RED: fallback authorization without persisted record fields still passes the gate.
3. RED: materialized fallback authorization records cannot be loaded/hash-bound.
4. RED: remediation attempts can be modeled as direct external Codex/Hermes-direct without a BLK-pipe route policy blocker.
5. RED: three/four remediation rounds lack root-cause/ceiling gate evidence.
6. RED: toxic fallback wording in BEO/closeout text is not detected by the closeout scanner.
7. GREEN: implement minimal deterministic helpers and scanner integration.
8. Verification: focused route tests, lean policy gates, diff/static/cache checks, hostile review, and broad/chunked suite as needed.

## 5. Authority Boundary

This sprint does **not** authorize:

- external Codex fallback;
- live BLK-pipe dispatch;
- BEO publication or BEO closeout execution;
- RTM generation or production `blk-link`;
- protected-body access;
- Kuronode source/Git mutation;
- source cleanup;
- worktree creation;
- package/network/model/browser/cyber tooling;
- reusable fallback policy.

It only adds local deterministic validation and record-shape gates.

## 6. Stop Conditions

Stop before commit if:

- tests do not go RED before implementation;
- fallback authorization can pass without persisted record identity fields;
- remediation attempts can pass as non-BLK-pipe route evidence;
- toxic fallback wording can pass with blocked route evidence and no fallback record;
- lean closeout policy fails for sprint 364;
- hostile review finds authority laundering or fail-open classification.
