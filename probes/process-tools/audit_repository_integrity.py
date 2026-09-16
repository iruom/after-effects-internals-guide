from pathlib import Path
from datetime import date
import csv, json, py_compile, re, shutil, subprocess, sys
from collections import Counter
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DOCS=ROOT/"docs"; DATA=ROOT/"datasets"
rows=[]
def add(check,status,detail): rows.append((check,status,detail))

# Documentation frontmatter and maturity.
docs=list(DOCS.rglob("*.md")); missing=[]; seeds=[]; statuses=Counter()
for p in docs:
    text=p.read_text(encoding="utf-8-sig",errors="replace")
    m=re.search(r"(?m)^status:\s*([^\r\n]+)",text)
    if not text.lstrip("\ufeff").startswith("---\n") or not m: missing.append(p)
    else: statuses[m.group(1).strip()]+=1
    if m and m.group(1).strip()=="seed": seeds.append(p)
add("docs-frontmatter","BLOCKER" if missing else "PASS",f"docs={len(docs)} missing={len(missing)}")
add("docs-seed-state","BLOCKER" if seeds else "PASS",f"seed={len(seeds)} statuses={dict(statuses)}")
# Python syntax for first-party probes/experiments only.
py_roots=[ROOT/"probes"/"process-tools", ROOT/"experiments"/"user-run"]
py_files=[]; py_bad=[]
for base in py_roots:
    if not base.exists(): continue
    for p in base.rglob("*.py"):
        py_files.append(p)
        try: py_compile.compile(str(p),doraise=True)
        except Exception as e: py_bad.append((p,str(e)))
add("python-compile","BLOCKER" if py_bad else "PASS",f"files={len(py_files)} failed={len(py_bad)}")

# Documentation quality gates: regenerate curated bug/quirk index and page-depth audit.
for tool,check in (("build_bug_quirk_registry.py","bug-quirk-registry"),("audit_page_depth.py","page-depth-audit")):
    q=subprocess.run([sys.executable,str(ROOT/"probes"/"process-tools"/tool)],capture_output=True,text=True,encoding="utf-8",errors="replace")
    add(check,"BLOCKER" if q.returncode else "PASS",(q.stdout+q.stderr).strip().replace("\n"," | ")[-900:])

depth_path=DATA/"aeig-page-depth-audit.csv"
if depth_path.exists():
    with depth_path.open(encoding="utf-8-sig",newline="") as f: depth=list(csv.DictReader(f))
    scored=[r for r in depth if r.get("role") in {"article","overview"}]
    weak=[r for r in scored if r.get("tier") in {"basic","thin","stub-like"}]
    add("docs-depth-floor","BLOCKER" if weak else "PASS",f"scored={len(scored)} below_developed={len(weak)}")
else:
    add("docs-depth-floor","BLOCKER","page depth dataset missing")

# Observatory manifests and generated JSON.
json_files=list((ROOT/"experiments"/"observatory"/"manifests").glob("*.json"))+list(DATA.glob("*.json"))
json_bad=[]
for p in json_files:
    try: json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e: json_bad.append((p,str(e)))
add("json-parse","BLOCKER" if json_bad else "PASS",f"files={len(json_files)} failed={len(json_bad)}")
# Dataset CSV structural parse.
csv_files=list(DATA.glob("*.csv")); csv_bad=[]; csv_empty=[]
for p in csv_files:
    try:
        with p.open(encoding="utf-8-sig",newline="") as f:
            r=csv.reader(f); header=next(r,None)
            if not header: csv_empty.append(p)
            else:
                for i,row in enumerate(r, start=2):
                    if len(row)!=len(header):
                        csv_bad.append((p,f"row {i}: {len(row)} != {len(header)}")); break
    except Exception as e: csv_bad.append((p,str(e)))
add("dataset-csv-structure","BLOCKER" if csv_bad or csv_empty else "PASS",
    f"files={len(csv_files)} malformed={len(csv_bad)} empty={len(csv_empty)}")

# Canonical package must pass its own audit.
pkg=ROOT/"probes"/"process-tools"/"audit_aeig_l5_package.py"
pr=subprocess.run([sys.executable,str(pkg)],capture_output=True,text=True,encoding="utf-8",errors="replace")
add("canonical-user-run-package","BLOCKER" if pr.returncode else "PASS",
    (pr.stdout+pr.stderr).strip().replace("\n"," | ")[-800:])
# Documentation build tooling is repository-declared even if not installed locally.
req=ROOT/"requirements-docs.txt"
add("docs-build-dependencies","PASS" if req.exists() else "BLOCKER",
    f"requirements-docs.txt={'present' if req.exists() else 'missing'}; mkdocs_local={'yes' if shutil.which('mkdocs') else 'no'}")
sitegen=ROOT/"probes"/"process-tools"/"generate_site_config.py"
sg=subprocess.run([sys.executable,str(sitegen),"--check"],capture_output=True,text=True,encoding="utf-8",errors="replace")
assets=[ROOT/"docs"/"stylesheets"/"extra.css", ROOT/".github"/"workflows"/"docs.yml"]
add("docs-site-config","BLOCKER" if sg.returncode or any(not x.exists() for x in assets) else "PASS",
    (sg.stdout+sg.stderr).strip().replace("\n"," | ")+f"; assets={sum(x.exists() for x in assets)}/{len(assets)}")
venv_py=ROOT/"scratch"/".venv-docs"/"Scripts"/"python.exe"
if venv_py.exists():
    site=ROOT/"scratch"/"site-strict-audit"
    br=subprocess.run([str(venv_py),"-m","mkdocs","build","--strict","-f",str(ROOT/"mkdocs.yml"),"-d",str(site)],capture_output=True,text=True,encoding="utf-8",errors="replace")
    add("docs-strict-build","BLOCKER" if br.returncode else "PASS",(br.stdout+br.stderr).strip().replace("\n"," | ")[-500:] or "mkdocs build --strict succeeded")
else:
    add("docs-strict-build","WARN","isolated docs venv not prepared; requirements are declared but strict build was not executed")

# Persist report.
out=DATA/"aeig-repository-integrity.csv"
with out.open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f); w.writerow(["check","status","detail"]); w.writerows(rows)
counts=Counter(status for _,status,_ in rows)
md=["---","status: generated",f"last_verified: {date.today().isoformat()}","---","# Repository Integrity","",
    f"PASS **{counts['PASS']}**, BLOCKER **{counts['BLOCKER']}**, WARN **{counts['WARN']}**.","",
    "| Check | Status | Detail |","|---|---|---|"]
for check,status,detail in rows: md.append(f"| `{check}` | **{status}** | {detail.replace('|','/')} |")
(ROOT/"docs"/"reference"/"repository-integrity.md").write_text("\n".join(md)+"\n",encoding="utf-8")
for r in rows: print(*r)
print("wrote",out)
sys.exit(1 if counts["BLOCKER"] else 0)
