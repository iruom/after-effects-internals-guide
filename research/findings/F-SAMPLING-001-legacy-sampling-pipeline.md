---
id: F-SAMPLING-001
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-SAMPLING-001 — Legacy Sampling Pipeline Exposes Stateful Precomputation

## Status
Confirmed from AE 25.6 `AE_EffectCB.h`; historical implementation details may not describe the current renderer literally.

## Evidence
`PF_SampPB` contains source world, sampling radii, area, edge behavior, `allow_asynch`, motion-blur fields, compositing state, a per-pixel mask, lookup-table pointers, and reserved state initialized by `begin_sampling`.

Adobe describes `begin_sampling` as a setup phase that may initialize hardware, build scanline index tables, or otherwise prepare repeated resampling. `end_sampling` reverses this state.

A deprecated batch-sampling path is described as reducing call overhead, pipelining requests, and reusing sample-weight context.
## Mathematical limits
The historical `area_sample` path is explicitly limited to at most a 256×256 averaging region because of overflow constraints. This is a rare direct example where numeric representation determines an API-level spatial limit.

High quality uses alpha-weighted interpolation/averaging; low quality falls back to nearest-neighbor sampling. This should be tested against modern transform/effect sampling rather than assumed to remain the current implementation.

## Research direction
Use impulse/ramp/hidden-RGB probes to distinguish legacy callback sampling, modern transform sampling, SmartFX sampling, and GPU sampling. Record kernel support, alpha weighting, border behavior, precision, and CPU/GPU parity separately.