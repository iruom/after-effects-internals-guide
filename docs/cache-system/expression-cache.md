---
status: active
last_verified: 2026-09-16
evidence: expression-engine cache lineage + TDB/BEE identity model + current Adobe expression behavior
---
# Expression Cache as Part of AE's Cache System

Expression caching sits upstream of rendered pixels. It can reduce expression/property work, but it must ultimately feed the same dependency and render-identity system that decides whether downstream image/audio results are reusable.

AEIG therefore keeps three questions separate:

1. **Can expression execution work be reused?**
2. **Is the evaluated property value still semantically valid?**
3. **Can downstream render/cache results that consumed that value be reused?**

A yes at one level is not a yes at the others.

## Cross-system model

```text
expression source/runtime caches
        |
        v
evaluated property value + dependency footprint
        |
        v
TDB/property state identity
        |
        v
BEE render GUID / request identity
        |
        v
RG/frame/cache validity
```
## Identity versus runtime reuse

Engine recycling and code-cache reuse are execution optimizations. They should not participate directly in semantic render identity unless the engine implementation version itself changes observable expression semantics.

By contrast, an evaluated expression value and every host property/time dependency required to produce it are render-relevant state. If those dependencies change, downstream identity must change even if the same JS engine and compiled source are reused.

This is why a fast expression cache cannot legally turn a stale value into a valid render dependency.

## Time-invariant values

A value proven independent of time can have a longer reuse lifetime than a rendered frame at one time coordinate, but only while all non-time dependencies remain equivalent. "Time invariant" is not the same as "project invariant".

An expression that ignores `time` but reads a Slider, marker, layer transform or Essential Property can still become invalid when that dependency changes.

## Cache failure modes

- **under-invalidation**: a dependency changes but a cached expression result survives;
- **over-invalidation**: harmless edits force expression and downstream render recomputation;
- **identity collapse**: distinct expression-engine modes or semantics are treated as equivalent;
- **benchmark confusion**: a warm rendered-frame cache is mistaken for an expression-engine optimization.
## Version lineage

The retained Debug Database corpus shows multiple expression cache/lifetime keys continuously present across stable 23.4 through 26.3 profiles. That continuity is evidence that expression reuse remains a multi-layer implementation concern across recent generations.

It is not proof that key names, defaults or behavior are stable public contracts. Private controls may be dead, experimental, renamed internally or interpreted differently by different builds.

Project expression-engine choice is part of semantic version state. A project evaluated under Legacy ExtendScript and the modern JavaScript engine can differ in supported syntax, behavior and performance, so engine choice belongs in reproducibility metadata and may affect downstream identity.

## Experiments

To connect expression caches to render identity, mutate one expression dependency while holding source text constant and compare property state, BEE/TDB trace footprint, frame receipt/GUID and rendered output. Then alter only source formatting or engine context and observe which layers invalidate.

A strong result would separate "expression runtime cache miss" from "semantic value changed" and from "downstream frame cache miss".

Cross-links: `../expression-engine/architecture.md`, `../expression-engine/caching.md`, `state-identity.md`, `cache-architecture.md`, and `../evaluation/dirty-invalidation.md`.
