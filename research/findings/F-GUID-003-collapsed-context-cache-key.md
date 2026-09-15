---
status: confirmed-local
last_verified: 2026-09-14
---
# F-GUID-003 — Project parentage can be the wrong dependency source under collapsed rendering

Adobe's `SmartyPants` sample hashes the parent comp background color through `GuidMixInPtr()` and explicitly warns that the example does not handle the collapsed-comp case.

The sample obtains the effect's project layer and then its ordinary parent comp. Under Collapse Transformations/collapsed geometrics, render-context APIs separately expose a root/top layer, demonstrating that render topology can diverge from project topology.

Consequence: a plug-in can construct an incorrect cache fingerprint even while using the intended GUID-mixing API, if it queries the wrong semantic context.
