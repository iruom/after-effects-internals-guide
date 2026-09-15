---
status: generated
last_verified: 2026-09-16
---
# AEIG 1.0 Release Readiness

Checks: **14** — PASS 11, BLOCKER 2, WARN 0, INFO 1.

| Check | Status | Detail |
|---|---|---|
| `domain-targets` | **BLOCKER** | 24/27 domains meet target; unmet=state-identity,render-graph,cache |
| `finding-registry` | **PASS** | findings=127 duplicate_rows=0 missing_frontmatter=0 |
| `observatory-manifests` | **PASS** | valid=7 invalid=0 |
| `observatory-evidence` | **INFO** | observed_or_replicated=4 runnable=2 |
| `api-surface-completeness` | **PASS** | identifiers=5023 parser_gap=0 surface_unresolved=0 |
| `api-guide-relations` | **PASS** | reviewed=113 open=0 |
| `master-surface-registry` | **PASS** | rows=53728 classes=13 missing= blanks={'name': 0, 'support_class': 0, 'host_scope': 0, 'source': 0} |
| `predictive-validation` | **BLOCKER** | prospective=7 locked=7 confirmed=2 unresolved=5 refuted_unrevised=0 |
| `l5-user-run-package` | **PASS** | package_files=7/7 / aex_sha256=9768BC9B463F6377E1AE246303D6AEDD8BF11725E8D96034DF14E85F1AD9BE98 / python_compile=24/24 / manifest_json=ok / jsx_syntax=ok / AEIG-L5 package audit: GREEN |
| `static-rc-freeze` | **PASS** | AEIG static RC verification: PASS / artifacts 56 predictions 7 / fingerprint 406B70458F0D808891879AFAD610981C518ED7D7BADCC9C7720ACB31C6F64433 |
| `seed-pages` | **PASS** | seed_pages=0 |
| `doc-todo-markers` | **PASS** | docs_with_todo_like_markers=0 |
| `markdown-local-links` | **PASS** | checked=0 broken=0 |
| `inline-artifact-references` | **PASS** | checked=146 unresolved=0 |

## Blocking rule
AEIG 1.0 cannot be declared complete while any `BLOCKER` remains.
Current domain gate: `state-identity,render-graph,cache`; prediction gate is reported independently above.
