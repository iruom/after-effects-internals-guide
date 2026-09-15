# EXP-CACHE-001 — Temporal invalidation topology

## Goal
Test whether modern AE cache invalidation behaves like time-local version tracking rather than whole-node dirtying.

## Project
- Comp A: 300 frames.
- Layer L: expensive deterministic SmartFX chain.
- Animate one parameter only over frames 100-110.
- Add a Probe Effect downstream that logs render/pre-render and input fingerprints.

## Mutations
1. Change a key at frame 105.
2. Change a key at frame 250.
3. Change layer name only.
4. Add an expression dependency by layer name, then repeat rename.
5. Enable motion blur and repeat a change just outside/inside shutter support.
6. Undo/redo each mutation.

## Capture
- render callback times and requested times;
- SmartFX checkout times;
- cache-hit inference via probe generation watermark;
- `BEE_Cache`, `BEE_Eval`, `MixHashGuid`, `RenderNode.RG_CacheNodeBase` traces;
- timeline cache indicators before/after.

## Discriminator
Whole-node invalidation predicts broad loss. Time-local validity predicts loss bounded around affected temporal support. Name changes should matter only when a semantic dependency observes the name.

## Historical hypothesis
Compare results with US7103839B1 without assuming the current implementation is identical.
