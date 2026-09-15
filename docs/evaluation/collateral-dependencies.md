---
status: researched-seed
last_verified: 2026-09-16
evidence: Adobe cache-validity patent US7103839B1 + current expression lookup contracts
---
# Collateral Dependencies

A render dependency does not have to follow the visible compositing tree. Historical Adobe architecture explicitly describes **collateral dependencies**: semantic references that can make apparently unrelated edits invalidate cached results.

## Historical model
Adobe patent `US7103839B1`, filed in 2000, describes cache-frame validity in a digital movie compositing system and separates ordinary structural dependencies from collateral ones. The important architectural lesson is that an edit can affect a cached frame even when the edited object is not a normal upstream image child.

The canonical example is a layer-name edit. A rename is normally metadata-only, but it becomes pixel-relevant when another expression resolves that layer by name.

This is historical design evidence, not proof that current BEE/RG uses the patent's exact data structures.

## Current expression contract makes resolution dependencies observable
Current After Effects expressions support both `thisComp.layer(index)` and `thisComp.layer(name)`. Name lookup resolves by layer name, falling back to source name when appropriate; duplicate names select the first/topmost matching layer. Index lookup follows Timeline ordering.

Therefore several edits can change **target resolution** without directly changing the target property's numeric value:

- rename a referenced layer;
- create a duplicate name above it;
- reorder layers when index lookup is used;
- insert/delete layers before an indexed target;
- rename/reorder effects or masks when an expression addresses them dynamically;
- replace a source whose source name participates in fallback lookup.

These are dependency mutations, not merely value mutations.

## Dependency classes to keep separate
1. structural image dependency: ordinary upstream pixel producer;
2. local parameter dependency: effect/property state inside the same render chain;
3. expression object dependency: arbitrary project object/property reference;
4. resolution dependency: name/index/order determines which object is referenced;
5. temporal dependency: `valueAtTime`, wide-time checkout, frame blending or motion blur;
6. matte/reference dependency: track matte, layer-control or other explicit cross-layer relation;
7. external dependency: file/network/system state declared through host mechanisms.

The same output can depend on several classes at once.

## Why a pure render DAG is insufficient
A graph built only from current image-producing edges can miss dependencies that affect **which edge should exist**. Dynamic resolution is especially important: the dependency target itself is a function of project structure.

A useful conceptual split is:

`project semantic graph -> dependency/resolution graph -> render request graph -> execution graph`.

The exact current implementation is unknown, but treating these as separate concerns prevents a common reverse-engineering error: assuming the visible RG node graph is the complete dependency database.

## Failure modes
- stale output after rename/reorder implies missing semantic invalidation or unsupported cached external state;
- excessive rerender after metadata-only edits can indicate conservative dependency tracking;
- name-based expressions with duplicate names are intentionally order-sensitive and can change target after reorder;
- index-based references are structurally fragile even when property values are unchanged;
- a dependency discovered only at evaluation time may make static graph inspection incomplete.

## Controlled experiments
Build a comp where one property is driven by `thisComp.layer("TARGET").transform.position`, then vary exactly one condition per run:

- rename `TARGET` away and back;
- insert a second `TARGET` above/below it;
- reorder layers while preserving values;
- switch the expression between name and numeric index;
- use `valueAtTime()` to add a temporal dimension;
- precompose or replace the source without changing the sampled value.

For each edit record expression result, rendered output hash, cache reuse, BEE/RG/TDB trace footprint and whether Undo restores reuse of the earlier result.

The highest-value outcome is not merely whether pixels changed, but **which edit classes change identity while the sampled numeric result remains equal**.

## Unknown frontier
Still unresolved in current AE:
- whether expression dependency edges are retained statically, discovered dynamically, or both;
- granularity of invalidation for name/index lookup changes;
- how dependency resolution identity is mixed into TDB/BEE Render GUIDs;
- how cross-comp and recursive expression dependencies are cycle-checked;
- whether equivalent dependency targets reached through different lookup syntax share cache identity.

Related: `F-CACHE-004`, `docs/evaluation/dirty-invalidation.md`, `docs/expression-engine/architecture.md`, `docs/temporal-system/temporal-dependencies.md`.
