# BLK-SYSTEM-078 Task 001 Outcome — RED Deterministic Seed Reproduction

**Status:** Complete
**Date:** 2026-05-11

## RED Gate

At Kuronode HEAD `80e75e3b4f26c4654f00a703a83c00c8cb76e4cd`, a static deterministic-seed gate was run before implementation.

```text
FAIL: ipc handler exposes userData path
FAIL: preload exposes getUserDataPath
FAIL: smoke calls getUserDataPath
FAIL: smoke writes runtime model.sysml
PASS: smoke uses string eval for KuronodeAPI
RED_DETERMINISTIC_SEED_GAP: ipc handler exposes userData path, preload exposes getUserDataPath, smoke calls getUserDataPath, smoke writes runtime model.sysml
```

## Interpretation

The BLK-SYSTEM-077 smoke path is functional, but the smoke harness does not yet create `<userData>/model.sysml` deterministically before triggering the projection pipeline. A pass can therefore depend on persistent Electron userData from a previous run.

## Authority Boundary

This task produced RED evidence only. It did not mutate Kuronode source, run production BLK-test MCP, publish BEOs, generate RTM, or read protected BLK-req bodies.
