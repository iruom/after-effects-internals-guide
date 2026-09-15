---
status: active
last_verified: 2026-09-15
---
# Recipe: Observe Internal Rendering Without Depending on Private ABI

## Goal
Understand BEE/TDB/RG/cache behavior deeply enough to debug or design a plug-in without binding production code to unsupported C++ objects.

## Preferred observation stack
1. public suite/selector behavior;
2. controlled project/render fixtures;
3. Debug/Trace Database categories;
4. crash/log symbols;
5. PE exports/imports/dependencies;
6. disposable standalone probes against exported diagnostic surfaces;
7. private invocation only if a separate ownership/lifetime experiment justifies it.

## Why this matters
Installed AE exposes rich internals such as `BEE_RenderOptions`, `TDB_Stream::GetRenderGuid`, `RG_CacheNodeBase`, `BEE_VectorArt` and MediaCore decode objects. Their visibility proves architecture, not supported lifetime, threading or mutation semantics.

## Safe example
`EXP-OBS-002` used exported dvacore trace functions in a disposable process to prove live threshold semantics. `EXP-RG-001` then uses the host's own trace providers around a normal render instead of calling RG node methods.

## ABI warning
Even diagnostic functions drift: `Get/SetTraceVolume(std::string_view)` changed from const-reference in AE 25.6 to by-value in 26.3. Private semantic continuity is weaker than ABI continuity.

## Production rule
If a private symbol is only needed to answer "what is AE doing?", keep it in tooling/observability, not in the shipped plug-in. Promote it into product code only when a stable supported route exists or an explicit version-locked risk decision is acceptable.

## Evidence discipline
Record exact binary hash/version, decorated symbol, calling convention, failure behavior and restoration/cleanup path. A successful one-version call is not a general contract.

Related: `F-OBS-001`, `F-ABI-014`, `docs/observability/trace-database.md`.

## Unknown frontier
Even when a private export can be called reproducibly, allocator ownership, initialization order, global state, thread affinity and teardown contracts may remain unknown. A successful read-only probe does not automatically justify mutation or use from inside the AE process.

Cross-version symbol continuity also does not establish ABI continuity; compiler/library changes can alter parameter passing while decorated names remain semantically similar.

When ownership cannot be proven, stop at observation. Prefer trace/log/export correlation and public behavioral experiments over escalating to private invocation solely to obtain a stronger-looking result.

Related: `docs/foundations/evidence-model.md`, `docs/observability/module-inventory.md`, `docs/observability/process-tracing.md`, `docs/troubleshooting/failure-model.md`.
