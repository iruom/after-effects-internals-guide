from pathlib import Path
import re
ROOT=Path(r"D:\Developer\After Effects Internals Guide\docs")
changed=[]
for p in ROOT.rglob("*.md"):
    text=p.read_text(encoding="utf-8-sig",errors="replace")
    if not re.search(r"(?m)^status:\s*seed\s*$",text): continue
    lines=len(text.splitlines())
    new=None
    if p.name=="index.md" and lines<=10: new="index"
    elif lines>=20: new="active"
    if not new: continue
    text2=re.sub(r"(?m)^status:\s*seed\s*$",f"status: {new}",text,count=1)
    p.write_text(text2,encoding="utf-8")
    changed.append((p.relative_to(ROOT),lines,new))
print('changed',len(changed))
for x in changed: print(x[2],x[1],x[0])
