---
status: confirmed
last_verified: 2026-09-14
evidence: AE-25.6-distributed-header + public-guide
---
# F-CACHE-010 — Dynamic flags can race with rendering and poison cache validity

The AE 25.6 Header warns that asynchronously changing watermark state is unsafe unless the next render matches the state last returned from `PF_Cmd_QUERY_DYNAMIC_FLAGS`; otherwise incorrect frames can be cached.

The selector may be sent at arbitrary times, so this is an explicit race between capability/state publication and render execution.

## Internal interpretation
Dynamic output flags participate in the semantic description of the render request. They are therefore part of the effective render-state contract even when they are not literally mixed into the same frame GUID.

## Safer design
Publish a versioned immutable snapshot used both for Query Dynamic Flags and the subsequent render. Avoid reading independently changing license/UI/external state during render unless its identity is also tracked.