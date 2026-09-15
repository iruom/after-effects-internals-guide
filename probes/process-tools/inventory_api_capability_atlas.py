from __future__ import annotations
import csv, html, re, urllib.request
from collections import Counter
from pathlib import Path

REPO = Path(r"D:\Developer\After Effects Internals Guide")
OUT = REPO / "datasets" / "ae-api-symbol-atlas.csv"
STATUS = REPO / "docs" / "reference" / "api-completeness-status.md"
SOURCES = [
    ("sdk-25.6", Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers"), "25.6"),
    ("sdk-local-pre25.6", Path(r"E:\AfterEffectsSDK\Examples\Headers"), "unknown-pre25.6"),
    ("sdk-cs6-thirdparty-archive", REPO / "research" / "external-sources" / "ae-sdk-cs6" / "Headers", "CS6-11.0"),
    ("sdk-cc2014-thirdparty-archive", REPO / "research" / "external-sources" / "ae-sdk-cc2014" / "Headers", "CC2014-13.0"),
    ("sdk-13.5-thirdparty-snapshot", REPO / "research" / "external-sources" / "ae-sdk-13_5-thirdparty" / "Headers", "AE13.5"),
]
GUIDE_URL = "https://ae-plugins.docsforadobe.dev/print_page/"
PREFIX = r"(?:AEGP|AEIO|AEFX|AE_|A_|PF|DRAWBOT|PrSDK|PrPixelFormat|PR_|kAEGP|kAEIO|kPF|kPr|SP|kSP|FIEL|PT|PICA|PiPL)"
IDENT_RE = re.compile(r"\b(" + PREFIX + r"[A-Za-z0-9_]*)\b")
rows: list[dict[str, str]] = []

def add(surface, version, visibility, source, line, kind, symbol, container="", value="", notes=""):
    rows.append(dict(surface=surface, version=version, visibility=visibility, source=source,
                     line=str(line or ""), kind=kind, symbol=symbol, container=container,
                     value=value.strip(), notes=notes))
def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1

def iter_typedef_aggregates(text: str):
    rx=re.compile(r"\btypedef\s+(struct|union|enum)\b(?:\s+([A-Za-z_]\w*))?\s*\{")
    for m in rx.finditer(text):
        brace=text.find("{",m.start(),m.end()); depth=1; i=brace+1
        while i < len(text) and depth:
            if text[i]=="{": depth+=1
            elif text[i]=="}": depth-=1
            i+=1
        if depth: continue
        am=re.match(r"\s*([A-Za-z_]\w*)\s*;",text[i:])
        if not am: continue
        yield m.group(1),m.group(2) or "",brace+1,i-1,am.group(1),m.start(),i+am.end()

def header_visibility(surface: str, name: str, context: str) -> str:
    if surface in {"sdk-cs6-thirdparty-archive", "sdk-cc2014-thirdparty-archive", "sdk-13.5-thirdparty-snapshot"}:
        return "thirdparty-historical-archive"
    if "Old" in name:
        return "historical-compat-distributed"
    if re.search(r"\b(?:AEGP_INTERNAL|AE_INTERNAL|PF_INTERNAL)\b", context):
        return "private-gate-reference"
    if name.startswith("PrSDK") or name == "PR_Public.h":
        return "cross-host-distributed"
    return "public-distributed"

def scan_header(surface: str, version: str, path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"^\s*#\s*define\s+([A-Za-z_]\w*)(?:\([^\n]*?\))?\s*([^\n]*)", text, re.M):
        name = m.group(1)
        if IDENT_RE.fullmatch(name) or "Suite" in name or name.startswith(("k", "A_")):
            ctx = text[max(0, m.start()-500):m.start()]
            add(surface, version, header_visibility(surface,path.name, ctx), path.name, line_of(text,m.start()),
                "macro", name, value=m.group(2))
    for m in re.finditer(r"typedef\s+(?:struct|union|enum)?[^;{}]*?\b([A-Za-z_]\w*)\s*;", text, re.S):
        name=m.group(1)
        if IDENT_RE.fullmatch(name):
            ctx=text[max(0,m.start()-500):m.start()]
            add(surface, version, header_visibility(surface,path.name,ctx), path.name,line_of(text,m.start()),"typedef",name)
    # Brace-aware aggregate aliases survive nested unions/structs.
    for akind, tag, body_start, body_end, alias, agg_start, agg_end in iter_typedef_aggregates(text):
        if IDENT_RE.fullmatch(alias):
            ctx=text[max(0,agg_start-500):agg_start]
            add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,agg_start),akind,alias)
    # Standalone callback typedefs are API symbols too.
    for m in re.finditer(r"\btypedef\s+[^;{}]*?\(\s*\*\s*("+PREFIX+r"[A-Za-z0-9_]*)\s*\)\s*\(", text, re.S):
        name=m.group(1); ctx=text[max(0,m.start()-500):m.start()]
        add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,m.start()),"callback-typedef",name)
    struct_spans=[]
    for m in re.finditer(r"typedef\s+struct(?:\s+([A-Za-z_]\w*))?\s*\{(.*?)\}\s*([A-Za-z_]\w*)\s*;", text, re.S):
        tag, body, alias = m.group(1) or "", m.group(2), m.group(3)
        container = alias or tag
        struct_spans.append((m.start(),m.end(),container))
        if IDENT_RE.fullmatch(container):
            ctx=text[max(0,m.start()-500):m.start()]
            add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,m.start()),"struct",container)
        for fm in re.finditer(r"\(\s*(?:SPAPI\s*)?\*\s*([A-Za-z_]\w*)\s*\)", body):
            name=fm.group(1); pos=m.start(2)+fm.start()
            ctx=text[max(0,pos-500):pos]
            add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,pos),"callback",name,container=container)
    for m in re.finditer(r"enum\s*(?:[A-Za-z_]\w*)?\s*\{(.*?)\}", text, re.S):
        body=m.group(1)
        for em in re.finditer(r"^\s*([A-Za-z_]\w*)\s*(?:=\s*([^,\n]+))?\s*,?", body, re.M):
            name=em.group(1)
            if IDENT_RE.fullmatch(name):
                pos=m.start(1)+em.start(); ctx=text[max(0,pos-500):pos]
                add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,pos),"enum",name,value=em.group(2) or "")
    for m in re.finditer(r"\b("+PREFIX+r"[A-Za-z0-9_]*)\s*\(", text):
        name=m.group(1)
        if any(a <= m.start() < b for a,b,_ in struct_spans):
            continue
        ctx=text[max(0,m.start()-500):m.start()]
        add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,m.start()),"function-like",name)
def scan_guide() -> None:
    raw=urllib.request.urlopen(GUIDE_URL, timeout=30).read().decode("utf-8","replace")
    plain=html.unescape(re.sub(r"<[^>]+>"," ",raw))
    for name in sorted(set(IDENT_RE.findall(plain))):
        add("guide-current","26.5","official-public-guide",GUIDE_URL,"","guide-identifier",name)

def main() -> None:
    for surface, root, version in SOURCES:
        if not root.exists():
            add(surface,version,"missing-corpus",str(root),"","corpus-missing",surface)
            continue
        for p in sorted(root.rglob("*.h")):
            scan_header(surface,version,p)
    scan_guide()
    dedup={tuple(r.values()):r for r in rows}
    final=sorted(dedup.values(), key=lambda r:(r["symbol"],r["surface"],r["source"],r["line"],r["kind"]))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(final[0])); w.writeheader(); w.writerows(final)
    counts=Counter(r["surface"] for r in final); vis=Counter(r["visibility"] for r in final); kinds=Counter(r["kind"] for r in final)
    symbols={r["symbol"] for r in final}; guide={r["symbol"] for r in final if r["surface"]=="guide-current"}; cur={r["symbol"] for r in final if r["surface"]=="sdk-25.6"}; legacy={r["symbol"] for r in final if r["surface"]=="sdk-local-pre25.6"}; cs6={r["symbol"] for r in final if r["surface"]=="sdk-cs6-thirdparty-archive"}; cc2014={r["symbol"] for r in final if r["surface"]=="sdk-cc2014-thirdparty-archive"}; ae135={r["symbol"] for r in final if r["surface"]=="sdk-13.5-thirdparty-snapshot"}
    raw_cur="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in SOURCES[0][1].rglob("*.h"))
    raw_legacy="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in SOURCES[1][1].rglob("*.h"))
    raw_cs6="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in SOURCES[2][1].rglob("*.h"))
    raw_cc2014="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in SOURCES[3][1].rglob("*.h"))
    raw_ae135="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in SOURCES[4][1].rglob("*.h"))
    raw_cur_tokens=set(IDENT_RE.findall(raw_cur)); raw_legacy_tokens=set(IDENT_RE.findall(raw_legacy)); raw_cs6_tokens=set(IDENT_RE.findall(raw_cs6)); raw_cc2014_tokens=set(IDENT_RE.findall(raw_cc2014)); raw_ae135_tokens=set(IDENT_RE.findall(raw_ae135))
    def declared_candidate(text: str, name: str) -> bool:
        n=re.escape(name)
        pats=[rf"^\s*#\s*define\s+{n}\b", rf"typedef[^;{{}}]*\b{n}\s*;", rf"}}\s*{n}\s*;", rf"\(\s*(?:SPAPI\s*)?\*\s*{n}\s*\)", rf"^\s*{n}\s*(?:=|,)"]
        return any(re.search(p,text,re.M|re.S) for p in pats)
    delta_rows=[]
    for s in sorted(symbols):
        in_cur_raw=s in raw_cur_tokens; in_legacy_raw=s in raw_legacy_tokens; in_cs6_raw=s in raw_cs6_tokens; in_cc2014_raw=s in raw_cc2014_tokens; in_ae135_raw=s in raw_ae135_tokens; decl_cur=declared_candidate(raw_cur,s)
        delta_rows.append(dict(symbol=s,
            in_guide_26_5=s in guide,
            in_sdk_25_6=s in cur,
            in_sdk_25_6_raw=in_cur_raw,
            in_local_pre25_6=s in legacy,
            in_local_pre25_6_raw=in_legacy_raw,
            in_cs6=s in cs6,
            in_cs6_raw=in_cs6_raw,
            in_cc2014=s in cc2014,
            in_cc2014_raw=in_cc2014_raw,
            in_ae135=s in ae135,
            in_ae135_raw=in_ae135_raw,
            guide_only=(s in guide and not in_cur_raw),
            parser_gap_25_6=(s in guide and decl_cur and s not in cur),
            raw_reference_only_25_6=(s in guide and in_cur_raw and not decl_cur and s not in cur),
            header_only_25_6=(s in cur and s not in guide),
            disappeared_from_25_6=(in_legacy_raw and not in_cur_raw),
            cs6_only=(in_cs6_raw and not in_cur_raw),
            cc2014_only=(in_cc2014_raw and not in_cs6_raw and not in_cur_raw),
            introduced_cs6_to_cc2014=(in_cc2014_raw and not in_cs6_raw),
            disappeared_cc2014_to_25_6=(in_cc2014_raw and not in_cur_raw),
            introduced_after_cc2014=(in_cur_raw and not in_cc2014_raw),
            ae135_only=(in_ae135_raw and not in_cc2014_raw and not in_cur_raw),
            introduced_cc2014_to_ae135=(in_ae135_raw and not in_cc2014_raw),
            disappeared_ae135_to_25_6=(in_ae135_raw and not in_cur_raw),
            introduced_after_ae135=(in_cur_raw and not in_ae135_raw),
            introduced_after_cs6=(in_cur_raw and not in_cs6_raw)))
    delta_path=REPO/"datasets"/"ae-api-surface-deltas.csv"
    with delta_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(delta_rows[0])); w.writeheader(); w.writerows(delta_rows)
    lines=["---","status: generated","last_verified: 2026-09-15","---","# API Completeness Status","",
           "This page is generated from the locally scanned SDK/header corpora plus the current official Guide identifier surface.","",
           f"Unique discoverable identifiers: **{len(symbols)}**.","",
           "## Corpus counts",""]
    lines += [f"- `{k}`: {v} rows" for k,v in sorted(counts.items())]
    lines += ["","## Visibility classes",""]+[f"- `{k}`: {v}" for k,v in sorted(vis.items())]
    guide_absent_raw=sum(1 for r in delta_rows if r["guide_only"])
    parser_gap=sum(1 for r in delta_rows if r["parser_gap_25_6"])
    disappeared_raw=sum(1 for r in delta_rows if r["disappeared_from_25_6"])
    cs6_only=sum(1 for r in delta_rows if r["cs6_only"])
    post_cs6=sum(1 for r in delta_rows if r["introduced_after_cs6"])
    cc2014_only=sum(1 for r in delta_rows if r["cc2014_only"])
    cs6_to_cc2014=sum(1 for r in delta_rows if r["introduced_cs6_to_cc2014"])
    cc2014_removed=sum(1 for r in delta_rows if r["disappeared_cc2014_to_25_6"])
    post_cc2014=sum(1 for r in delta_rows if r["introduced_after_cc2014"])
    lines += ["","## Cross-surface deltas","",
              f"- Guide 26.5 identifiers absent from the raw local SDK 25.6 corpus: **{guide_absent_raw}**",
              f"- Guide identifiers present in raw 25.6 headers but missed by structured extraction: **{parser_gap}**",
              f"- SDK 25.6 structured identifiers absent from current Guide: **{len(cur-guide)}**",
              f"- Local pre-25.6 raw identifiers absent from SDK 25.6 raw corpus: **{disappeared_raw}**",
              f"- CS6 archive identifiers absent from raw SDK 25.6: **{cs6_only}**",
              f"- Raw SDK 25.6 identifiers absent from the CS6 archive: **{post_cs6}**",
              f"- CC2014-only identifiers absent from both CS6 and SDK 25.6: **{cc2014_only}**",
              f"- Identifiers introduced between CS6 and CC2014: **{cs6_to_cc2014}**",
              f"- CC2014 identifiers absent from SDK 25.6: **{cc2014_removed}**",
              f"- Raw SDK 25.6 identifiers absent from the CC2014 archive: **{post_cc2014}**","",
              "The `sdk-local-pre25.6` snapshot is deliberately not assigned an exact AE release until its provenance is independently verified.",
              "Header-only does not automatically mean hidden/unsupported; it can be ABI detail, sample support, cross-host support, deprecated compatibility, or documentation lag."]
    STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("wrote",OUT,"rows",len(final),"unique symbols",len(symbols)); print("wrote",delta_path); print("wrote",STATUS)

if __name__ == "__main__":
    main()
