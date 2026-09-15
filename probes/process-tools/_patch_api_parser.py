from pathlib import Path
p=Path(r"D:\Developer\After Effects Internals Guide\probes\process-tools\inventory_api_capability_atlas.py")
s=p.read_text(encoding="utf-8")
needle='def header_visibility(surface: str, name: str, context: str) -> str:\n'
helper='''def iter_typedef_aggregates(text: str):\n    rx=re.compile(r"\\btypedef\\s+(struct|union|enum)\\b(?:\\s+([A-Za-z_]\\w*))?\\s*\\{")\n    for m in rx.finditer(text):\n        brace=text.find("{",m.start(),m.end()); depth=1; i=brace+1\n        while i < len(text) and depth:\n            if text[i]=="{": depth+=1\n            elif text[i]=="}": depth-=1\n            i+=1\n        if depth: continue\n        am=re.match(r"\\s*([A-Za-z_]\\w*)\\s*;",text[i:])\n        if not am: continue\n        yield m.group(1),m.group(2) or "",brace+1,i-1,am.group(1),m.start(),i+am.end()\n\n'''
if 'def iter_typedef_aggregates' not in s:
    s=s.replace(needle,helper+needle)
needle2='    struct_spans=[]\n'
insert='''    # Brace-aware aggregate aliases survive nested unions/structs.\n    for akind, tag, body_start, body_end, alias, agg_start, agg_end in iter_typedef_aggregates(text):\n        if IDENT_RE.fullmatch(alias):\n            ctx=text[max(0,agg_start-500):agg_start]\n            add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,agg_start),akind,alias)\n    # Standalone callback typedefs are API symbols too.\n    for m in re.finditer(r"\\btypedef\\s+[^;{}]*?\\(\\s*\\*\\s*("+PREFIX+r"[A-Za-z0-9_]*)\\s*\\)\\s*\\(", text, re.S):\n        name=m.group(1); ctx=text[max(0,m.start()-500):m.start()]\n        add(surface,version,header_visibility(surface,path.name,ctx),path.name,line_of(text,m.start()),"callback-typedef",name)\n'''
if 'Brace-aware aggregate aliases' not in s:
    s=s.replace(needle2,insert+needle2)
p.write_text(s,encoding="utf-8")
print('patched',p)
