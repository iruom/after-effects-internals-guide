---
status: active
last_verified: 2026-09-16
evidence: current Adobe expression docs + AE-team performance statement + local Debug/Trace lineage
---
# Expression Engine Architecture

After Effects Expressions are a property-evaluation subsystem, not simply JavaScript pasted onto the timeline. A useful architecture separates language engine, AE object binding, dependency lookup, evaluated values and downstream render identity.

```text
expression source
    |
    +--> preprocessing / syntax adaptation
    +--> engine selection / code preparation
    v
JavaScript execution context
    |
    +--> AE object/property bridge
    +--> property/time/dependency reads
    +--> nested expression evaluation
    v
evaluated property value
    |
    +--> post-expression property state
    +--> TDB/BEE dependency + render identity
```

This decomposition matters because "expression performance" can be dominated by different layers even when source code looks similar.
## Language-engine boundary

Current Adobe documentation distinguishes the modern JavaScript expression engine from Legacy ExtendScript. On Windows, the modern engine uses V8 and supports a newer JavaScript language level; projects retain an engine choice because syntax/behavior compatibility is not perfect.

Do not confuse the expression engine with the scripting engine. Expressions evaluate property values in render/evaluation context; scripts issue commands against the application/project object model. They share JavaScript-like syntax but have different lifetimes, permissions and semantics.

The current expression language also wraps AE-native property objects. Those objects are not always plain JavaScript values: operations such as destructuring can require explicit `.value` extraction before the result behaves like an ordinary iterable JS value.

This is an important implementation clue: AE object/property wrappers form a binding layer between JavaScript semantics and the host property graph.
## Preprocessing and code preparation

Adobe's syntax-difference documentation notes that complex expressions called from a `.jsx` expression library can avoid some preprocessing work and may perform better than equivalent source written directly on a property. This is evidence for a preparation layer ahead of evaluation, but it does not expose its private representation or cache key.

Local Debug Database vocabulary independently includes expression preprocessing/code-cache candidates. AEIG therefore models preprocessing/compiled-code reuse as a distinct layer, while keeping its exact implementation open.

Whitespace/source changes, library indirection and engine choice are useful experimental axes because they may alter preparation cost without changing the semantic dependency graph.

## Dependency resolution and nested expressions

A property reference is not just a JavaScript object lookup. It can request another time-varying AE property, another expression, a layer/effect property chain or a different composition/time mapping.

In a 2025 Adobe Community reply, an After Effects team member described simple property links as generally cached, while explaining that calls into other expression-driven properties can require another JS engine evaluation. Deep chains can therefore create nested evaluation and stack pressure rather than behaving like one globally memoized DAG.

Treat this as implementation guidance from the AE team, not a stable SDK contract. The exact engine-pool policy can change between releases.
## Time and render identity

Expressions operate in AE's time/property system, so dependency identity can change with time even when source code is unchanged. A time-varying upstream property, remapped precomp, marker/keyframe query or expression-driven dependency can alter the evaluated value and therefore downstream render identity.

The property bridge also means that time semantics are host semantics, not generic JavaScript semantics. For example, an explicit time argument can bypass remapped-time behavior that a normal property access would inherit.

AEIG therefore treats expression output as part of the TDB/property state feeding BEE/RG rather than as a final cosmetic transform performed after render identity is chosen.

## Failure and performance patterns

Common high-cost structures include O(N) layer/property searches inside per-frame evaluation, long chains where each expression asks another expression-driven property, repeated cross-comp lookups and unnecessarily time-varying code that could be constant.

A practical design rule from the AE team is to keep expression references close to O(1) where possible. `posterizeTime(0)` or other explicit constant-time techniques can reduce reevaluation only when the intended semantics are genuinely time-invariant.

Do not optimize by assuming a private cache will save an expensive expression. Cache lifetime can be tied to rendered-frame lifetime, dependency state or engine reuse and may change across versions.
## Version lineage and hidden controls

Local Debug Database lineage from retained 23.4 through 26.3 profiles repeatedly exposes controls for engine recycling, subproperty population/caching, time-invariant expression-value caching, a code-cache delegate candidate and post-expression shape caching.

The names are useful because they show that Adobe itself separates several expression lifetime/cache concerns. They are **not** supported preferences and do not prove the same private implementation persisted behind a stable name.

The modern JavaScript engine has also gained expression-language features over time, while Legacy ExtendScript remains a compatibility engine. A project-level engine choice is therefore part of reproducibility metadata for any expression benchmark or bug report.

## Experiments and falsification

Build micro-fixtures that vary one axis at a time: source text only, whitespace/comments, `.jsx` library indirection, property path, nested-expression depth, dependency value, dependency topology, current time, `posterizeTime`, engine choice, project reload and MFR state.

Measure evaluation time and rendered output while recording relevant Debug/Trace categories. A proposed cache layer is only supported if its reuse boundary can be independently changed without changing the other layers.

Open questions include the exact code-cache key, engine-pool/recycling strategy, dependency-registration representation, post-expression cache contents and how expression dependency identity is mixed into TDB/BEE render GUID state.

Cross-links: `caching.md`, `../cache-system/expression-cache.md`, `../evaluation/dirty-invalidation.md`, `../cache-system/state-identity.md`, and findings `F-EXPR-001` / `F-EXPR-002`.
