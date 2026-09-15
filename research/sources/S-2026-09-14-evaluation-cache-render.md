# Source Set: Evaluation / Cache / Render Graph

## Primary / near-primary
1. After Effects C++ SDK Guide, What's New 13.5 — separate UI/render threads, project-copy synchronization, GUID mix-in, sequence-data serialization: https://ae-plugins.docsforadobe.dev/intro/whats-new/
2. AEGP Suites — frame receipts, rendered region, project timestamps, speculative render APIs, receipt GUIDs: https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
3. Parameter Supervision — PF_State as opaque receipt used by AE's internal frame caching database: https://ae-plugins.docsforadobe.dev/effect-details/parameter-supervision/
4. SmartFX — request/result/max-result rectangles, content bounds, zero-alpha RGB, pre-render/render split: https://ae-plugins.docsforadobe.dev/smartfx/smartfx/
5. Multi-Frame Rendering — sequence-data replication, thread-local render state, Compute Cache: https://ae-plugins.docsforadobe.dev/effect-details/multi-frame-rendering-in-ae/
6. Global/Sequence/Frame Data — flattening, persistence and private cache validation: https://ae-plugins.docsforadobe.dev/effect-details/global-sequence-frame-data/
7. Adobe patent US7103839B1 — time-aware cached-frame validity over a compositing hierarchy: https://patents.google.com/patent/US7103839B1
8. Adobe patent US6084597 — concatenated rendering / delayed rasterization in After Effects: https://patents.justia.com/patent/6084597
9. Adobe patent US5917549A — pixel-aspect-aware image transforms in After Effects: https://patents.google.com/patent/US5917549A/en
10. Adobe patent US5872564 — controlling time in digital compositions: https://patents.justia.com/patent/5872564
11. Adobe 2015 architecture note — complete re-architecture: https://blog.adobe.com/en/publish/2015/06/15/keeping-previous-versions-installed-when-installing-cc-2015-applications
12. Adobe 13.5.1 fixes — threading and I_MIX_GUID_DEPENDENCIES failures: https://blog.adobe.com/en/publish/2015/07/27/after-effects-cc-2015-13-5-1-bug-fix-update-fixes-previews
13. Adobe Sci-Tech Award — Natkin/Simons among AE design/development awardees: https://blog.adobe.com/en/publish/2018/12/13/adobe-after-effects-cc-photoshop-cc-wins-sci-tech-academy-award

## Secondary / corroborating
14. RE:Vision Effects CC 2015 note — reproducible I_MIX_GUID_DEPENDENCIES failure: https://revisionfx.com/faq/cc_2015/
15. Adobe Community 2026 expression resolver report — dependency traversal may expose mixed pre/post-expression state; unverified lead: https://community.adobe.com/questions-529/possible-expression-engine-bug-resolver-state-depends-on-dependency-traversal-1639507

## Use rule
Patents that explicitly name After Effects are strong historical implementation evidence, but no patent should be treated as proof that AE 26.x still uses the same algorithm or data structure. Current SDK contracts and local artifacts are used to test continuity.
