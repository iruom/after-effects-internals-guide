---
status: confirmed-developer-statement + local-corroboration
evidence_grade: E1 + E2-L
versions: "2025 statement; modern local debug keys"
last_verified: 2026-09-14
---
# Nested expression-driven property references can instantiate additional JS engines

## Adobe team statement
An After Effects team member stated that when an expression calls another expression-driven property, evaluating the second expression requires a new JS engine; deeper chains can produce stack overruns. Simple property links are generally cached, while dependency-sensitive expressions often require reevaluation.

## Local corroboration
Debug Database exposes `Expressions.RecycleEnginesAggressively`, `Expressions.CacheSubProperties`, and `CacheTimeInvariantExpressionValues`.

## Performance implication
Expression dependency chains can scale much worse than their source text suggests. A chain of properties is not equivalent to one shared DAG evaluation context.

## Improvement direction
A graph-native expression system could evaluate expression nodes in a shared memoized context, detect cycles explicitly, and avoid nested VM creation.

## Source
https://community.adobe.com/t5/after-effects-discussions/do-expressions-use-caching-expression-performance-help/td-p/15535992