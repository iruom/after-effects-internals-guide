---
status: active
last_verified: 2026-09-15
---
# Independent Effect-API Reimplementations

Independent SDK/host projects are executable probes of the Effect API boundary. They are useful precisely because they can be wrong: every mismatch identifies an ABI assumption that must be checked against Adobe headers or AE behavior.

## `ePi5131/aex`: plug-in-side ABI clone
`aex` attempts to build AE effects while redefining core Effect API structures and suites instead of including most Adobe SDK headers. It recreates `PF_InData`, `PF_OutData`, parameter unions, interaction callbacks, PICA `SPBasicSuite`, flags and selected suites.

This shows which fields an outside developer considered necessary to generate a working Effect plug-in ABI. It is not a complete current specification: the project describes itself as incomplete and still requires Adobe's PiPL tooling/resources.

### Confirmed conformance warning
At snapshot `09090f34fb68cfb877cdbf3ec8db6982da1ecf8b`, `aex` defines `PF_MAX_EFFECT_MSG_LEN = 31`. The AE 25.6 distributed `AE_Effect.h` defines `PF_MAX_EFFECT_MSG_LEN = 255`.

Because `return_msg` appears before later `PF_OutData` fields, this is not only a string-capacity difference; it changes struct offsets. Treat the current `aex` definition as version-drift or an ABI defect until experimentally scoped.
### Incomplete suite reconstruction is itself evidence
`aex`'s `AEGP_SuiteHandler` contains a large catalogue of historical Suite slots, but only a small subset has concrete types in the current implementation. Its destructor currently does not run `ReleaseAllSuites()`.

Therefore use the catalogue as a lead for suite names/version archaeology, not proof that every listed suite contract has been independently reconstructed.

## `potistudio/aexlo`: host-side Effect runtime emulator
`aexlo` attacks the opposite boundary: load an existing `.aex`, drive Effect commands, and emulate the host callbacks/suites without After Effects.

At snapshot `61bf0c1846c6eb843102ba18404d88033de46383`, the emulator implements core setup/render paths, SmartFX callbacks, selected GPU paths, handle/world/iterate/color/transform suites and a process-wide suite dispatcher. Many host-dependent callbacks remain explicit stubs.

This project is especially valuable for host-side lifetime contracts because a plug-in immediately exposes incorrect pointers, missing initialization, invalid callback sequencing or insufficient suite behavior.
## Host-side implementation traps exposed by `aexlo`
The SmartFX emulator documents several practical requirements:
- `checkout_layer` must fully initialize the caller's output structure; the plug-in can pass uninitialized storage.
- `checkout_layer_pixels` writes a world pointer into an output slot; it must not treat the slot as an already-valid world.
- `checkout_output` must return storage whose lifetime survives the callback; returning a pointer to a temporary wrapper is a dangling-pointer bug.
- popup option strings are copied during parameter setup because the plug-in-owned `namesptr` may not remain valid after the add-param callback.
- queued GPU work can outlive the plug-in callback; a host that immediately reads pixels must synchronize the device stream/queue first.

These are `E2-R` observations until checked against Adobe contracts/runtime. Several align with the pointer ownership patterns documented in the distributed SDK and are candidates for controlled host/plug-in probes.

## Suite-emulation hypothesis
`aexlo` represents many suites as process-wide stateless vtables and treats some later suite layouts as append-only supersets capable of satisfying older version requests. This is an emulator design choice, not yet an AE fact.

Audit each suite generation before adopting prefix-compatibility: compare function order/size across distributed old headers, then test whether AE returns the requested exact table/version or a compatible later table.
## Plug-in self-description boundary
`aexlo` first looks for the modern `PluginDataEntryFunction2` symbol and asks the plug-in to report its real effect entry point through the plug-in-data callback. AE 25.6 distributes the corresponding signature in `AE_PluginData.h`, including `SPBasicSuite`, host name and host version inputs.

This means a host need not infer every registration detail by parsing only a platform resource before it can discover an entry point; modern plug-ins have a code-level self-description path in addition to PiPL/resource metadata. The exact precedence and compatibility behavior across AE generations remains an archaeology target.

## Teardown ordering observed by the emulator
`aexlo` releases plug-in GPU state, then issues sequence setdown, then global setdown before unloading the module. Treat this ordering as an emulator hypothesis to compare against Adobe command-selector documentation and instrumented plug-ins.
## Local AexExecutor: host-reimplementation failure corpus
A historical local AexExecutor project provides a third, independent host-side attempt. Its value is not completeness; it preserves actual suite-acquisition logs, host stubs, disassembly/RVA/string investigations and render comparisons from compatibility work against real plug-ins.

A key dispatcher pattern returns implemented AEGP suite tables by suite **name** while ignoring the requested integer version after logging it. For broad Adobe-looking unknown suite names it can also return a generic dummy table as successful acquisition.

Combined with the distributed Old Header corpus, this exposes a concrete ABI failure class: some historical suite layouts are not prefix-compatible, so a caller compiled for one generation can execute the wrong function index when handed a different table.

Observed log integers that initially look like private future suites decode cleanly through public historical headers—for example Comp integer 21 is `AEGP_CompSuite10`, not a secret `CompSuite21`. This is a useful warning against over-interpreting raw PICA logs.

Use AexExecutor as `E2-R`/local reimplementation evidence at the individual-claim level. Its failures are research leads; they become AE claims only after triangulation with distributed headers, Adobe documentation, another implementation or controlled runtime behavior.

See `suite-versioning-and-abi.md` and `host-reimplementation-failure-patterns.md`.

## Completed aexlo Suite-alias audit seed
The dispatcher aliases reviewed in the current snapshot are now recorded in `datasets/aexlo-suite-dispatch-audit.csv`.

Header-supported aliases: Iterate8 v1→v2, Iterate16 v1→v2, IterateFloat v1→v2, and PixelData v1→v2.

Confirmed hazards: PF AE App range aliasing, Param Utils old→current aliasing, and PF Utility v4. The AEGP Utility `1..=18` range is especially weak: the emulator returns a hand-built `CompatV11` table even though AE 25.6 publishes sparse PICA integers 3/5/7/10/11/13, and UtilitySuite3→4 plus UtilitySuite5→6 are not prefix-compatible.

The `PF AE App Suite` implementation contains an informative workaround: it deliberately places the render-engine callback into both its modern slot and the older shifted offset associated with headers lacking `PF_AppGetLanguage`. That workaround is valuable failure evidence because it independently acknowledges the very layout shift that makes a blanket append-only claim unsafe.

Use `probes/process-tools/audit_aexlo_suite_dispatch.py` to regenerate the audit after updating the external snapshot or compatibility datasets.