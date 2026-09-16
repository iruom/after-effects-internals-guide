from pathlib import Path
import argparse, re

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DOCS = ROOT / "docs"
OUT = ROOT / "mkdocs.yml"

SECTION_ORDER = [
    "foundations", "architecture", "state-model", "evaluation", "render-graph",
    "cache-system", "temporal-system", "image-pipeline", "color-pipeline", "gpu-system",
    "memory-system", "media-system", "audio-system", "text-system", "vector-shape-system",
    "three-d-system", "animation-system", "expression-engine", "tracking-analysis", "ai-analysis",
    "mfr", "threading-system", "host-integration", "ui-system", "product-shell", "headless-system",
    "interop", "persistence", "observability", "troubleshooting", "capability-recipes",
    "archaeology", "reference",
]

SECTION_TITLES = {
    "foundations": "Foundations", "architecture": "Architecture", "state-model": "State Model",
    "evaluation": "Evaluation", "render-graph": "Render Graph", "cache-system": "Cache System",
    "temporal-system": "Temporal System", "image-pipeline": "Image Pipeline", "color-pipeline": "Color Pipeline",
    "gpu-system": "GPU System", "memory-system": "Memory System", "media-system": "Media System",
}
SECTION_TITLES.update({
    "audio-system": "Audio System", "text-system": "Text System", "vector-shape-system": "Vector / Shape System",
    "three-d-system": "3D System", "animation-system": "Animation System", "expression-engine": "Expression Engine",
    "tracking-analysis": "Tracking & Analysis", "ai-analysis": "AI / Analysis", "mfr": "Multi-Frame Rendering",
    "threading-system": "Threading System", "host-integration": "Host Integration", "ui-system": "UI System",
    "product-shell": "Product Shell", "headless-system": "Headless / Command Line", "interop": "Inter-Application Interop",
    "persistence": "Persistence", "observability": "Observability", "troubleshooting": "Troubleshooting",
    "capability-recipes": "Capability Recipes", "archaeology": "Architecture Archaeology", "reference": "Reference",
})

FRIENDLY_DIRS = {
    "cpp-sdk": "C++ SDK", "premiere-pro": "Premiere Pro Comparison", "pica-sweetpea": "PICA / SweetPea",
    "uxp-cep": "UXP / CEP", "aegps": "AEGPs", "aeios": "AEIOs", "artisans": "Artisans",
    "effect-basics": "Effect Basics", "effect-details": "Effect Details", "effect-ui-events": "Effect UI & Events",
    "premiere-other-hosts": "Premiere / Other Hosts", "menu-commands": "Menu Commands", "object-model": "Object Model",
}

def title_for(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    m = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    if m:
        return re.sub(r"[`*_]", "", m.group(1)).strip()
    return path.stem.replace("-", " ").title()

def q(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
def emit_dir(directory: Path, indent: int) -> list[str]:
    pad = " " * indent
    out = []
    index = directory / "index.md"
    if index.exists():
        rel = index.relative_to(DOCS).as_posix()
        out.append(f"{pad}- {q(title_for(index))}: {rel}")
    for path in sorted(directory.glob("*.md"), key=lambda p: title_for(p).lower()):
        if path.name == "index.md":
            continue
        rel = path.relative_to(DOCS).as_posix()
        out.append(f"{pad}- {q(title_for(path))}: {rel}")
    for child in sorted((p for p in directory.iterdir() if p.is_dir()), key=lambda p: p.name.lower()):
        md_files = list(child.rglob("*.md"))
        if not md_files:
            continue
        label = FRIENDLY_DIRS.get(child.name, child.name.replace("-", " ").title())
        out.append(f"{pad}- {q(label)}:")
        out.extend(emit_dir(child, indent + 4))
    return out

nav = ["nav:", "    - Home: index.md"]
seen = set()
for section in SECTION_ORDER:
    directory = DOCS / section
    if not directory.exists():
        continue
    seen.add(section)
    nav.append(f"    - {q(SECTION_TITLES.get(section, section.title()))}:")
    nav.extend(emit_dir(directory, 8))
for directory in sorted((p for p in DOCS.iterdir() if p.is_dir() and p.name not in seen), key=lambda p: p.name):
    if not list(directory.rglob("*.md")):
        continue
    nav.append(f"    - {q(directory.name.replace('-', ' ').title())}:")
    nav.extend(emit_dir(directory, 8))

config = '''site_name: After Effects Internals Guide
site_description: Evidence-graded architecture and implementation archaeology guide for Adobe After Effects
site_url: https://ken-eizo.github.io/after-effects-internals-guide/
repo_url: https://github.com/ken-eizo/after-effects-internals-guide
repo_name: ken-eizo/after-effects-internals-guide
edit_uri: edit/main/docs/
docs_dir: docs
copyright: Unofficial research project. Adobe and After Effects are trademarks of Adobe.

''' + "\n".join(nav) + "\n\n"
config += '''theme:
    name: material
    language: en
    icon:
        repo: fontawesome/brands/github
    features:
        - announce.dismiss
        - content.action.edit
        - content.action.view
        - content.code.copy
        - navigation.footer
        - navigation.indexes
        - navigation.sections
        - search.highlight
        - search.suggest
        - toc.follow
    palette:
        - media: "(prefers-color-scheme: dark)"
          primary: black
          scheme: slate
          toggle:
              icon: material/brightness-4
              name: Switch to light mode
        - media: "(prefers-color-scheme: light)"
          primary: white
          scheme: default
          toggle:
              icon: material/brightness-7
              name: Switch to dark mode

plugins:
    - search:
          separator: '[\\s\\-,\\.:!=\\[\\]()"/]+'
    - git-revision-date-localized:
          enable_git_follow: false
          strict: false
          type: date
    - print-site:
          add_cover_page: true
          add_print_site_banner: true
          print_page_title: Offline Docs

markdown_extensions:
    - admonition
    - attr_list
    - def_list
    - footnotes
    - md_in_html
    - tables
    - pymdownx.details
    - pymdownx.highlight:
          line_spans: __span
          pygments_lang_class: true
    - pymdownx.inlinehilite
    - pymdownx.superfences
    - pymdownx.tabbed:
          alternate_style: true
    - pymdownx.tasklist:
          custom_checkbox: true
    - toc:
          title: Page Contents
          permalink: true
          toc_depth: 3

extra_css:
    - stylesheets/extra.css

extra:
    social:
        - icon: fontawesome/brands/github
          link: https://github.com/ken-eizo/after-effects-internals-guide
'''

ap = argparse.ArgumentParser()
ap.add_argument("--check", action="store_true")
args = ap.parse_args()
if args.check:
    current = OUT.read_text(encoding="utf-8-sig") if OUT.exists() else ""
    if current != config:
        raise SystemExit("mkdocs.yml is stale; run generate_site_config.py")
    print("site config: PASS")
else:
    OUT.write_text(config, encoding="utf-8")
    print("wrote", OUT)
print("markdown pages", len(list(DOCS.rglob("*.md"))))
