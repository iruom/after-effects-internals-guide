---
status: researched-seed
evidence_grade: E1/E2
confidence: 0.92
versions: "historical design evidence; current implementation unverified"
last_verified: 2026-09-14
---
# Collateral dependencies and cache invalidation

## Statement
US7103839B1 describes dependencies that do not follow the ordinary compositing-tree parent/child relation as **collateral dependencies**. Two examples are expression dependencies, which may point broadly across the project, and layer-parameter dependencies, which are constrained more locally.

A layer-name edit is used as a concrete example: normally it should not invalidate pixels, but it can become render-relevant when an expression resolves another layer by name.

## Architectural consequence
A purely structural render DAG is insufficient for invalidation. A usable model needs at least a second dependency relation for semantic references, with edit classes mapped onto the caches they can affect.

## Research implication
Test name/index/matchName/property-reference expressions separately. A metadata-only edit that becomes pixel-relevant through an expression is an excellent probe for dependency discovery and cache-key composition.

## Improvement hypothesis
A modern design could represent these dependencies as explicit typed edges and versioned fingerprints instead of grouping many edit classes conservatively. This may reduce false invalidation at the cost of dependency-tracking overhead.

## Source
Adobe patent US7103839B1: https://patents.google.com/patent/US7103839B1
