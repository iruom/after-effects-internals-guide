---
status: active-hypothesis
last_verified: 2026-09-16
evidence: retained Debug Database lineage 23.4-26.3 + public expression source/engine behavior; semantics not yet experimentally isolated
---
# Expression Preprocessing

Local internal settings expose `AE.DisableGlobalPreProcessorR`, which confirms that modern AE contains a host-level concept named as a global preprocessor.

The key is present in every retained stable Debug Database snapshot from AE 23.4 through 26.3 (13 observed versions) with default `false`. This continuity is useful evidence of a durable subsystem boundary. It does **not** reveal the transformations performed, implementation class, cache lifetime or which expression engines use it.

## Evidence boundary
The public expression contract exposes source text, engine selection, JavaScript execution and the AE object/property bridge, but it does not document a public preprocessing API. AEIG therefore keeps preprocessing as an internal architectural hypothesis rather than a supported third-party capability.

Nearby retained expression controls are independently named: `AE.RecycleExpressionEnginesR`, `Expressions.RecycleEnginesAggressively`, `AE.UseAEExpCodeCacheDelegateImpl`, `CacheTimeInvariantExpressionValues`, `Expressions.CacheSubProperties` and `Expressions.PopulateSubProperties`.

Their separation is evidence **against** treating "the expression cache" or "the expression compiler" as one monolithic mechanism.

## Working model
A conservative pipeline is:

`raw expression text -> host preprocessing candidate -> parser/compiler input -> engine execution -> AE object/property bridge -> dependency evaluation -> value/result caches -> render dependency`.

Only the existence of a preprocessing concept is currently supported. Its exact placement and responsibilities remain hypotheses.

## Candidate responsibilities — not established facts
Possible responsibilities include source normalization, compatibility rewriting, engine-specific wrappers, generated host glue, or source preparation before compilation. These are experiment targets, not conclusions.

In particular, the debug-key name does not prove C-style macro expansion, localization substitution, dependency extraction, syntax lowering, or property-name canonicalization.

## Failure modes to separate experimentally
If a preprocessing stage exists, errors can be wrongly attributed to the JavaScript engine. Distinct candidate failure classes include:
- raw source accepted by one engine mode but rejected before execution in another;
- source-equivalent edits invalidating code reuse despite identical semantics;
- generated versus manually authored equivalent text taking different preparation paths;
- transformed-source line offsets differing from raw-source diagnostics;
- stale prepared source after engine/project/context changes.

None of these failures is currently claimed as confirmed merely from the internal key.

## Discriminating corpus
Compare expressions that preserve runtime semantics while changing one source dimension at a time:
- whitespace/comments only;
- equivalent literal and parenthesization forms;
- local variables versus direct property access;
- name lookup versus an equivalent already-resolved object/index reference;
- generated/pasted source versus manually entered source;
- identical syntax under Legacy ExtendScript and modern JavaScript engines;
- disable/enable expression, project reload and full host restart.

Record raw source bytes, engine mode, expression error text/line, first-evaluation latency, repeated-evaluation latency, relevant trace categories, evaluated value, downstream render identity and cache behavior.

A useful falsification target is whether toggling the internal preprocessor in a disposable research profile changes only source preparation while later engine/value-cache behavior remains structurally similar. Because the key is unsupported internal state, this is research-only and should never become production guidance.

## Version boundary
`AE.DisableGlobalPreProcessorR` is currently confirmed from 23.4 through 26.3. AEIG has not established when the concept first appeared, whether older expression engines used an equivalent differently named stage, or whether implementation changed while the key remained stable.

## Unknown frontier
Still unproven:
- whether preprocessing is global, per-project, per-expression or per-engine;
- whether transformed source is cached and by what identity;
- whether code-cache keys consume raw or processed source;
- whether dependency discovery happens before, during or after preprocessing;
- whether localization/property aliases are rewritten textually or resolved only through the AE object bridge;
- whether error locations map to raw source or transformed source;
- whether Legacy and modern engines share one preprocessor.

Until controlled experiments isolate the stage, `AE.DisableGlobalPreProcessorR` remains an observability clue rather than a supported plug-in capability.

Related: `docs/expression-engine/architecture.md`, `docs/expression-engine/caching.md`, `docs/cache-system/expression-cache.md`, `docs/observability/debug-database.md`.