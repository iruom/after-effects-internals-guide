---
status: researched-seed
evidence_grade: E0
confidence: 0.98
versions: "MFR-era contract"
last_verified: 2026-09-14
---
# Host callbacks define a dangerous lock boundary

## Statement
The MFR SDK warns that plug-ins using mutexes or other blocking synchronization must not hold those locks while calling back into the host via suites or checkout calls; Adobe says this will very likely deadlock.

## Internal implication
Host callbacks can block, re-enter scheduling paths, or require locks whose order is outside plug-in control. There is therefore an implicit lock-order boundary at the host API.

## Design lesson
Shared render state should prefer immutable data, single-flight tasks, atomics or lock-free handoff around host calls. If blocking locks are unavoidable, release them before crossing the host boundary and revalidate state afterwards.

## Research direction
Instrument host callback durations and thread IDs under MFR pressure. Look for re-entrant callbacks, worker migration, and cases where a checkout stalls behind another computation.

## Source
Multi-Frame Rendering in AE: https://ae-plugins.docsforadobe.dev/effect-details/multi-frame-rendering-in-ae/
