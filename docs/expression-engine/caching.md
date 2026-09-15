---
status: active
last_verified: 2026-09-16
evidence: local Debug Database lineage 23.4-26.3 + current Adobe expression docs + AE-team performance guidance
---
# Expression Caching and Runtime Reuse

There is no evidence for one universal "expression cache". AE exposes enough independent vocabulary and behavior to justify several cache/lifetime layers, each with different invalidation rules.

```text
source text
  -> preprocessing / code preparation
  -> engine/context reuse
  -> property/subproperty resolution
  -> dependency evaluation
  -> time-invariant/value reuse
  -> post-expression derived objects
  -> rendered-frame/cache dependency
```

A hit at one layer says nothing about reuse at the others.

## Retained-version hidden vocabulary

Across 13 retained stable profiles from 23.4 through 26.3, AEIG observes `CacheTimeInvariantExpressionValues`, `Expressions.CacheSubProperties`, `Expressions.PopulateSubProperties`, `Expressions.RecycleEnginesAggressively` and `AE.RecycleExpressionEnginesR` with stable enabled defaults. Separate candidates `AE.UseAEExpCodeCacheDelegateImpl` and `AE.PostExprShapeCache` are present with disabled defaults.

These are private Debug Database keys. They prove implementation vocabulary and lineage, not public switch semantics.
## Code/preprocessing reuse

Current Adobe documentation notes a performance difference when complex expression logic is called from a `.jsx` expression library versus placed directly on a property, attributing it to preprocessing behavior. That makes source preparation a real optimization layer distinct from final-value caching.

A code-cache hit would only avoid some source/compile preparation. It cannot by itself skip property dependency reads whose values may have changed.

Use experiments that alter comments/whitespace or library indirection while keeping semantic dependencies constant to isolate this layer.

## Engine/context reuse

Engine recycling controls concern runtime context lifetime, not property-value identity. Reusing a JavaScript engine can reduce context startup/allocation while still executing the expression again.

Conversely, a fresh engine does not imply the host forgot every dependency/cache result. Host property state and rendered-frame caches live outside the JS engine itself.

An AE-team performance explanation states that referencing another expression-driven property can require another JS engine evaluation. This means nested-expression graphs can multiply engine/evaluation work even when the top-level expression is simple.
## Property/subproperty reuse

`Expressions.PopulateSubProperties` and `Expressions.CacheSubProperties` strongly suggest a private distinction between discovering/constructing host property wrappers and reusing them. Do not equate this with caching the numerical value of the property.

A property path can stay structurally identical while the sampled value changes with time, keyframes, Essential Property overrides or upstream expressions. Wrapper/path reuse is therefore compatible with mandatory reevaluation.

## Time-invariant value reuse

`CacheTimeInvariantExpressionValues` is the clearest private name suggesting value reuse. The safe semantic interpretation is still narrow: only values proven independent of time and changing dependencies can be reused without reevaluation.

The AE-team explanation that simple property links are generally cached while time-varying values share rendered-frame-like cache lifetimes is consistent with this layered model.

`posterizeTime(0)` can intentionally make an expression time-invariant, but it should not be used to hide a dependency that actually changes with time. Correctness comes before reuse.
## Post-expression derived caches

`AE.PostExprShapeCache` should be treated as a candidate for caching derived shape/post-expression structures rather than as evidence for generic expression-value memoization. Similar post-expression caches may exist for specialized property types.

This distinction matters because changing an expression can invalidate derived geometry even when the JS engine or property wrapper is reused.

## Failure and benchmark traps

Expression benchmarks are easy to misread. Warm engine state, warm rendered-frame cache, cached property wrappers and cached final values can all reduce runtime for different reasons. A single second-run timing cannot identify which layer was reused.

Likewise, changing source text can invalidate code preparation while leaving dependency values identical; changing an upstream value can invalidate the result while leaving code/engine caches warm.

Always record engine type, AE version, project reload state, current time, MFR state and whether the rendered frame itself was already cached.

## Test matrix

Cross one axis at a time: source text, whitespace, library indirection, engine choice, property path, nested-expression depth, upstream value, time, `posterizeTime`, project reload and cache purge. Use instrumented expressions or controlled render timing to infer which layer repeated.

Unknowns remain the private cache-key representation, eviction policy, engine-pool size, post-expression cache types and the exact bridge from expression dependency state into TDB/BEE render identity.

Cross-links: `architecture.md`, `../cache-system/expression-cache.md`, `../evaluation/dirty-invalidation.md`, and findings `F-EXPR-001` / `F-EXPR-002`.
