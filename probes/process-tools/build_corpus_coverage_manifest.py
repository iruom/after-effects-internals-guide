from __future__ import annotations
import csv, hashlib, json, os, urllib.request
from pathlib import Path
from typing import Iterable

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
OUT=ROOT/"datasets"/"aeig-corpus-coverage-manifest.csv"
STATUS=ROOT/"docs"/"reference"/"corpus-coverage-status.md"

CORPORA=[
 ("sdk-25.6-headers","native-sdk","25.6","local Adobe SDK distribution",Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers"),"*.h","inventory_api_capability_atlas.py","ae-api-symbol-atlas.csv"),
 ("sdk-25.6-mac-headers","native-sdk","25.6","local Adobe Mac SDK archive; AppleDouble excluded; provenance.json retained",ROOT/"research"/"external-sources"/"ae-sdk-25.6-mac"/"Headers","*.h","compare_sdk25_platform_semantics.py","ae-sdk-25_6-platform-semantic-parity.csv"),
 ("sdk-local-pre25.6-headers","native-sdk","unknown-pre25.6","local retained SDK snapshot",Path(r"E:\AfterEffectsSDK\Examples\Headers"),"*.h","inventory_api_capability_atlas.py","ae-api-symbol-atlas.csv"),
 ("sdk-cs6-headers","historical-sdk","CS6/11.0","third-party archive; provenance.json retained",ROOT/"research"/"external-sources"/"ae-sdk-cs6"/"Headers","*.h","inventory_api_capability_atlas.py","ae-api-symbol-atlas.csv"),
 ("sdk-cc2014-headers","historical-sdk","CC2014/13.0","third-party archive; git commit + provenance.json retained",ROOT/"research"/"external-sources"/"ae-sdk-cc2014"/"Headers","*.h","inventory_api_capability_atlas.py","ae-api-symbol-atlas.csv"),
 ("ae-2025-runtime-pe","runtime-binary","AE 2025 installed","local installed application",Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files"),"PE_ATLAS","inventory_runtime_export_atlas.py","ae-2025-runtime-export-atlas.csv"),
 ("ae-debug-trace-stable","observability","9.0-26.3 retained","local retained AE profiles",Path(os.environ.get("APPDATA",r"C:\Users\Public"))/"Adobe"/"After Effects","DEBUG_TRACE","inventory_debug_trace_lineage.py","ae-debug-trace-vocabulary.csv"),
 ("aexlo-snapshot","independent-reimplementation","local snapshot","external source snapshot",ROOT/"research"/"external-sources"/"aexlo","SOURCE_TREE","audit_aexlo_suite_dispatch.py","aexlo-suite-dispatch-audit.csv"),
 ("aexexecutor-source","independent-reimplementation","local historical project","user-owned source corpus",Path(r"D:\Developer\AexExecutor"),"SOURCE_TREE","manual + targeted probes",""),
 ("aexexecutor-failure-logs","failure-corpus","local historical project","top-level retained host/test logs",Path(r"D:\Developer\AexExecutor"),"TOP_TXT","manual + targeted probes",""),
]

WEB=[
 ("guide-26.5","public-guide","26.5","current Docs for Adobe / Adobe-derived guide","https://ae-plugins.docsforadobe.dev/print_page/","inventory_api_capability_atlas.py","ae-api-symbol-atlas.csv"),
 ("scripting-guide-current","scripting","26.5 changelog","Docs for Adobe scripting guide","https://ae-scripting.docsforadobe.dev/print_page/","inventory_script_expression_surfaces.py","ae-script-expression-api-atlas.csv"),
 ("expression-reference-current","expressions","26.0 changelog","Docs for Adobe expression reference","https://ae-expressions.docsforadobe.dev/print_page/","inventory_script_expression_surfaces.py","ae-script-expression-api-atlas.csv"),
]
SKIP_DIRS={".git",".dotnet",".vs","target","node_modules","__pycache__","build","dist","scratch","test_renders","publish","bin","obj"}
SOURCE_EXTS={".c",".cc",".cpp",".cxx",".h",".hpp",".cs",".py",".rs",".toml",".md",".json",".yaml",".yml",".cmake",".vcxproj",".props",".targets",".bat",".ps1",".lua",".js",".ts",".xaml"}

def tree_files(root:Path, mode:str)->list[Path]:
    if not root.exists(): return []
    if mode=="DEBUG_TRACE":
        return sorted(p for p in root.rglob("*.txt") if p.name in {"Debug Database.txt","Trace Database.txt"})
    if mode=="PE_ATLAS":
        exts={".dll",".exe",".aex",".prm"}
        return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    if mode=="SOURCE_TREE":
        return sorted(p for p in root.rglob("*") if p.is_file() and not any(x in SKIP_DIRS for x in p.parts) and (p.suffix.lower() in SOURCE_EXTS or p.name.lower() in {"cmakelists.txt","makefile"}))
    if mode=="TOP_TXT":
        return sorted(p for p in root.glob("*.txt") if p.is_file())
    if mode=="PANEL_SDK":
        exts={".xml",".html",".js",".jsx",".css"}
        return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    if mode=="GUIDE_HISTORY":
        exts={".rst",".md",".json"}
        return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    return sorted(p for p in root.rglob(mode) if p.is_file())

def digest_files(files:list[Path], root:Path)->tuple[int,int,str]:
    h=hashlib.sha256(); total=0; ok=0
    for p in files:
        try:
            data=p.read_bytes(); rel=str(p.relative_to(root)).replace("\\","/")
        except (OSError,ValueError): continue
        fh=hashlib.sha256(data).hexdigest(); size=len(data)
        h.update(rel.encode("utf-8",errors="replace")+b"\0"+str(size).encode()+b"\0"+fh.encode()+b"\n")
        total+=size; ok+=1
    return ok,total,h.hexdigest() if ok else ""

def unresolved_for(cid:str)->str:
    notes={
      "sdk-25.6-headers":"structured parser gap against Guide-declared/header-declared candidates is 0; semantic/doc aliases remain separate",
      "sdk-25.6-mac-headers":"public header surface is normalized-text identical to Windows 25.6 in the retained archives; binary/sample platform parity remains a separate question",
      "sdk-local-pre25.6-headers":"exact release provenance unresolved",
      "sdk-cs6-headers":"third-party archive provenance; verify against an original Adobe package when obtainable",
      "sdk-cc2014-headers":"third-party archive provenance pinned to git commit ec12dfd17a9566ea17f2095a47795bc80e68518f; verify against an original Adobe package when obtainable",
      "ae-2025-runtime-pe":"exports are binary-visible surfaces, not supported API contracts; non-exported internals remain outside this corpus",
      "ae-debug-trace-stable":"retained profiles are incomplete between 11.0 and 23.4 and do not prove key semantics",
      "aexlo-snapshot":"independent host implementation, not Adobe authority",
      "aexexecutor-source":"independent implementation source; not an Adobe authority",
      "aexexecutor-failure-logs":"historical failure observations; coverage is limited to retained top-level text logs",
      "guide-26.5":"documentation corpus; does not enumerate private host internals",
      "scripting-guide-current":"documentation-derived surface; runtime Reflection differential still pending",
      "expression-reference-current":"documentation-derived surface; runtime engine-only names still pending",
      "after-effects-sys-bindings":"independent generated binding corroboration only; not an Adobe authority and not a historical SDK substitute",
      "cc2015-panel-sdk-samples":"sample corpus proves distributed CEP/CSXS panel contract; does not enumerate every CEP runtime API",
      "official-guide-git-history":"official Guide snapshots preserve documentation state for selected commits; they do not substitute for matching distributed SDK headers",
    }
    return notes.get(cid,"")
CORPORA += [
 ("sdk-25.6-premiere-shared","cross-host-sdk","25.6-bundled","PrSDK/shared headers inside AE SDK",Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers"),"PrSDK*.h","inventory_api_capability_atlas.py","ae-api-symbol-atlas.csv"),
 ("extension-substrate-ae2025","extension-runtime","AE 2025 installed","AE + Common Files CEP/UXP manifests and native bridges",ROOT/"datasets","ae-2025-extension-substrates.csv","inventory_extension_substrates.py","ae-2025-extension-substrates.csv"),
 ("aep-experiment-corpus","project-format-experiments","mixed","AEIG controlled experiment fixtures",ROOT/"experiments","SOURCE_TREE","experiment-specific probes",""),
 ("after-effects-sys-bindings","independent-generated-binding","25.6-compatible/pre-26.5","third-party bindgen snapshot; git commit retained",ROOT/"research"/"external-sources"/"after-effects-rs"/"after-effects-sys","bindings_win.rs","compare_after_effects_sys_binding.py","ae-after-effects-sys-binding-corroboration.csv"), ("cc2015-panel-sdk-samples","historical-extension-sdk","CC 2015 / AE 13.x","local retained Adobe Panel SDK sample corpus",Path(r"E:\Adobe_After_Effects_CC_2015_Panel_SDK"),"PANEL_SDK","inventory_cc2015_panel_sdk.py","ae-cc2015-panel-sdk-surface.csv"),
]

def make_row(cid,scope,version,prov,source,count,bytes_n,digest,parser,dataset,status):
    return dict(corpus_id=cid,scope=scope,version=version,provenance=prov,source=str(source),files_scanned=count,
                bytes_scanned=bytes_n,aggregate_sha256=digest,parser=parser,generated_dataset=dataset,
                unresolved=unresolved_for(cid),status=status)

def main():
    rows=[]
    for cid,scope,version,prov,root,mode,parser,dataset in CORPORA:
        files=tree_files(root,mode)
        count,total,digest=digest_files(files,root) if files else (0,0,"")
        status="scanned" if count else "missing-or-empty"
        rows.append(make_row(cid,scope,version,prov,root,count,total,digest,parser,dataset,status))
    for cid,scope,version,prov,url,parser,dataset in WEB:
        try:
            data=urllib.request.urlopen(url,timeout=30).read()
            digest=hashlib.sha256(data).hexdigest()
            rows.append(make_row(cid,scope,version,prov,url,1,len(data),digest,parser,dataset,"scanned-live"))
        except Exception as e:
            row=make_row(cid,scope,version,prov,url,0,0,"",parser,dataset,"fetch-failed")
            row["unresolved"]=(row["unresolved"]+f"; fetch error: {type(e).__name__}").strip("; ")
            rows.append(row)
    fields=["corpus_id","scope","version","provenance","source","files_scanned","bytes_scanned","aggregate_sha256","parser","generated_dataset","unresolved","status"]
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    scanned=[r for r in rows if r["status"].startswith("scanned")]
    unresolved=[r for r in rows if r["unresolved"] or not r["status"].startswith("scanned")]
    lines=["---","status: generated","last_verified: 2026-09-15","---","# Corpus Coverage Status","",
      "AEIG completeness is measured against explicit corpora. A successful scan never implies that unacquired private or historical corpora do not exist.","",
      f"Registered corpora: **{len(rows)}**. Scanned/fetched: **{len(scanned)}**. Corpora with an unresolved note or scan failure: **{len(unresolved)}**.","",
      "## Coverage manifest",""]
    for r in rows:
        mb=int(r["bytes_scanned"])/1048576
        lines.append(f"- `{r['corpus_id']}` — {r['status']}; {r['files_scanned']} files/items; {mb:.1f} MiB; SHA-256 `{r['aggregate_sha256'][:16] or 'n/a'}…`")
    lines += ["","## Completeness rule","",
      "A corpus is reproducibly scanned only when its source/provenance, item count, byte count, aggregate digest and parser are recorded. `missing-or-empty` and `fetch-failed` remain explicit gaps.",
      "Binary export coverage means exported PE surface coverage for the installed build; it does not cover non-exported internal functions, dynamic registrations, stripped symbols, or semantic contracts.",
      "Historical completeness is open-ended until original SDK/install artifacts for missing release eras are acquired and hashed.","",
      "See `datasets/aeig-corpus-coverage-manifest.csv` for full provenance and unresolved notes."]
    STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("wrote",OUT,"rows",len(rows)); print("wrote",STATUS)
    for r in rows: print(r["corpus_id"],r["status"],r["files_scanned"],r["bytes_scanned"],r["aggregate_sha256"][:12])

if __name__=="__main__": main()
