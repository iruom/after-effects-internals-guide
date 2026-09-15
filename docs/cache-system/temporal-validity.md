---
status: researched-seed
last_verified: 2026-09-14
---
# Temporal Cache Validity

A cache entry is only reusable if every render-relevant dependency that intersects its temporal footprint is unchanged relative to the state under which the entry was produced.

Historical Adobe evidence provides a concrete model using edit timestamps and per-node interval lists. Current SDK behavior still exposes time-range state receipts, project timestamps and automatically tracked wide-time checkouts, so the underlying problem remains present even if the data structure changed.

## Historical algorithm sketch
```text
edit(x, [t0,t1])
    stamp = ++global_edit_stamp
    update_local_interval_list(x, [t0,t1], stamp)

validate(frame, node, footprint)
    newest = newest_relevant_edit(node, footprint)
    if newest > frame.render_stamp: return invalid
    for dependency in dependencies(node, footprint):
        if !validate(frame, dependency, map_time(footprint)): return invalid
    return valid
```

This is conceptual pseudocode reconstructed from the patent, not claimed AE source.

## Complexity and fragmentation
Interval lists are attractive when long time ranges share the same edit state: lookup can use ordered endpoints, and localized edits split only affected ranges. Their worst practical behavior appears when edits create many tiny alternating intervals, increasing metadata and traversal cost.

A precise modern design could combine:
- interval/version summaries for dense ranges;
- sparse sample sets for isolated temporal checkouts;
- persistent segment trees for versioned history;
- dependency fingerprints for non-temporal state;
- an `unknown/all-time` fallback for opaque effects.

## Current evidence to correlate
- `PF_State` can describe parameter/layer state over a requested time span.
- Automatic wide-time input tracks actual checkout ranges.
- AEGP project timestamps expose render-relevant edit epochs.
- Global Performance Cache can reuse results when a prior state reappears.
- Local trace vocabulary includes `BEE_Cache` and `MixHashGuid`.

## Open questions
- Does modern AE store interval validity per render node, per stream, or in a central dependency service?
- Are exact sparse time samples retained, or widened to ranges?
- Does Undo reactivate an old state identity or construct a new state equal under hashing?
- How are expression dependencies versioned when target resolution changes by name/index?

## Sources
- https://patents.google.com/patent/US7103839B1
- https://ae-plugins.docsforadobe.dev/effect-details/parameter-supervision/
- https://ae-plugins.docsforadobe.dev/effect-basics/PF_OutData/

## `PF_HaveInputsChangedOverTimeSpan()` reveals a dual-purpose dependency API
The deprecated Param Utils header explains an important behavior more directly than the modern prose Guide. A simulation effect can validate cached state for a requested time span against a previously captured `PF_State`.

The host checks all parameters over the span, including layer inputs and param[0], except parameters explicitly excluded by `PF_ParamFlag_EXCLUDE_FROM_HAVE_INPUTS_CHANGED`. The implementation is described as efficient because change tracking uses timestamps.

Crucially, if the call returns `changed = FALSE`, two things happen conceptually: the plug-in may safely reuse its own cache, and AE's internal cache system records that the current render has a temporal dependency on the queried range so later upstream edits invalidate the correct frames.

This makes the API both a **cache validator** and a **dependency declaration side effect**. That dual role is easy to miss if one reads it only as a boolean comparison helper.
## Temporal closure is explicit in the current Param Utils contract
The current `PF_ParamUtilsSuite3` documentation adds an important refinement: `PF_GetCurrentState()` can capture selected inputs over a time range, and for simulation effects using `PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT`, that range is expanded to include times needed to produce the requested range.

This is more than a timestamp comparison primitive. It implies a host-known temporal **closure** over observed dependencies: a requested output interval may depend on an expanded upstream interval discovered from wide-time behavior.

The older `PF_HaveInputsChangedOverTimeSpan()` contract and the current state API therefore fit one model:
`requested interval -> dependency-expanded interval -> state equivalence -> cache validity`.

The exact internal representation of that expanded footprint remains unknown; do not assume the historical patent's interval-list structure survives unchanged.