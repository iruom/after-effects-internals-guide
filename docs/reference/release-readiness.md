---
status: generated
last_verified: 2026-09-16
---
# AEIG 1.0 Release Readiness

Checks: **16** — PASS 13, BLOCKER 2, WARN 0, INFO 1.

| Check | Status | Detail |
|---|---|---|
| `bug-quirk-registry` | **PASS** | BUG/QUIRK REGISTRY: PASS / entries 32 fixed 15 nonfixed 17 / sources {'adobe-fixed-issue': 14, 'adobe-known-issue': 2, 'adobe-sdk-known-issue': 1, 'sdk-contract-warning': 7, 'sdk-contract-quirk': 1, 'aeig-finding': 1, 'sdk-sample-pitfall': 2, 'sdk-contract-lifecycle': 1, 'sdk-contract-pitfall': 1, 'historical-abi-bug': 1, 'historical-compat-quirk': 1} / statuses {'fixed': 15, 'known/mitigated': 1, 'active-risk': 1, 'active-contract': 9, 'historical-pitfall': 1, 'sample-pitfall': 2, 'historical': 1, 'historical-compat': 1, 'known': 1} / wrote D:\Developer\After Effects Internals Guide\datasets\aeig-bug-quirk-registry.csv / wrote D:\Developer\After Effects Internals Guide\docs\reference\bug-quirk-registry.md |
| `page-depth-audit` | **PASS** | scored=162 below_developed=0 tiers={'deep': 68, 'developed': 94} |
| `domain-targets` | **BLOCKER** | 24/27 domains meet target; unmet=state-identity,render-graph,cache |
| `finding-registry` | **PASS** | findings=127 duplicate_rows=0 missing_frontmatter=0 |
| `observatory-manifests` | **PASS** | valid=7 invalid=0 |
| `observatory-evidence` | **INFO** | observed_or_replicated=4 runnable=2 |
| `api-surface-completeness` | **PASS** | identifiers=5023 parser_gap=0 surface_unresolved=0 |
| `api-guide-relations` | **PASS** | reviewed=113 open=0 |
| `master-surface-registry` | **PASS** | rows=53728 classes=13 missing= blanks={'name': 0, 'support_class': 0, 'host_scope': 0, 'source': 0} |
| `predictive-validation` | **BLOCKER** | prospective=7 locked=7 confirmed=2 unresolved=5 refuted_unrevised=0 |
| `l5-user-run-package` | **PASS** | package_files=7/7 / aex_sha256=884E9CB19AF32AFA1DBFB11A4777E66107C71B13C16A759FBB9B299572382792 / python_compile=26/26 / manifest_json=ok / jsx_syntax=ok / AEIG-L5 package audit: GREEN |
| `static-rc-freeze` | **PASS** | AEIG static RC verification: PASS / artifacts 70 predictions 7 / fingerprint 79E7481B91E14E18C9EC3D5049827774B400EA882A761CA7DF2F641994BFCE95 |
| `seed-pages` | **PASS** | seed_pages=0 |
| `doc-todo-markers` | **PASS** | docs_with_todo_like_markers=0 |
| `markdown-local-links` | **PASS** | checked=0 broken=0 |
| `inline-artifact-references` | **PASS** | checked=715 unresolved=0 |

## Blocking rule
AEIG 1.0 cannot be declared complete while any `BLOCKER` remains.
Current domain gate: `state-identity,render-graph,cache`; prediction gate is reported independently above.
