---
status: active
last_verified: 2026-09-15
evidence: local process/module observations + corpus/hash inventory
---
# Process Tracing

Process tracing is used to connect AE actions to file I/O, module loading, thread activity, cache writes and process boundaries without assuming one module owns an entire feature.

Useful tools include ProcMon, ETW/WPR, module snapshots, process trees, wait-chain inspection and controlled stdout/stderr capture.

## What to correlate
For each action record: process ID, host version, module set, relevant file paths, thread IDs, timestamps, trace markers and output hashes.

This matters because `AfterFX.exe`, `AfterFX.com`, `aerender.exe` and helper/service processes can expose different plug-in planes and different warm-state behavior.

Headless experiments already showed that module presence and plug-in loading policy cannot be inferred solely from the interactive host.

## Causality rule
A file or DLL appearing during an action is correlation, not proof of semantic ownership. Stronger evidence combines timing with call stacks, feature toggles, repeated A/B experiments or a public contract.

## Reproducibility
Prefer disposable profiles and deterministic fixtures. Record fresh-host versus reused-host explicitly because cache/module state can change observations.

Process evidence should be linked to the exact binary corpus hash from the corpus coverage manifest.## Failure modes and observer effect
Process/file tracers can drop events under load, truncate stack collection, change scheduling and produce enormous I/O volumes that alter the workload. Always include a control event whose path is known, record tracer loss counters when available, and narrow filters before interpreting absence.

File opens also do not prove semantic consumption: scanners, antivirus, metadata probes and speculative preload can touch the same path. Repeated A/B timing plus stack/module attribution is stronger than path correlation alone.

## Unknown frontier
Process tracing reveals boundaries visible to the OS, not in-process object identity. It cannot directly equate a file write with a BEE Render GUID, a worker thread with an RG node or a loaded module with the owner of a semantic feature.

Use it to constrain hypotheses, then join with host traces, binary symbols and controlled output changes.

Cross-links: `module-inventory.md`, `logging.md`, `trace-database.md`, `../capability-recipes/headless-fresh-vs-reuse.md`, and `../memory-system/overview.md`.