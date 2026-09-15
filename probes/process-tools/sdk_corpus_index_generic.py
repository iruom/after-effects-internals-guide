from __future__ import annotations
import argparse, csv, json, re
from collections import Counter
from pathlib import Path

EXTS = {'.h', '.hpp', '.c', '.cpp', '.r', '.rc', '.mm', '.m', '.py'}
MARKERS = re.compile(
    r"deprecated|obsolete|legacy|internal|private|not thread safe|thread safe|"
    r"do not|don't|must not|must be|warning|todo|fixme|workaround|confusing|"
    r"cache|receipt|guid|timestamp|render|flatten|unflatten|sequence|roi|bounds|"
    r"async|speculative|invalidate|dirty|mutex|deadlock|main thread|background|"
    r"GPU|device|memory|thread|queue|deferred|accelerated|smart render",
    re.I,
)
SUITE_DEF = re.compile(r"^\s*#define\s+(k\w*Suite\w*|[A-Za-z0-9_]*Suite[A-Za-z0-9_]*)\s+(.+?)\s*$")
SYMBOL = re.compile(r"\b(?:AEGP|PF|PR|PrSDK|Pr|csSDK)_[A-Za-z0-9_]+\b")
INTERNAL = re.compile(r"\b(?:AEGP_INTERNAL|A_INTERNAL|PR_INTERNAL)\b|_Private\.h|Internal", re.I)
def read_text(path: Path) -> str:
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'cp932'):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            pass
    return path.read_text(encoding='utf-8', errors='replace')


def index_corpus(root: Path) -> dict:
    files, suites, hits = [], [], []
    symbol_files: dict[str, set[str]] = {}
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        text = read_text(path)
        lines = text.splitlines()
        rel = str(path.relative_to(root))
        internal_hits = len(INTERNAL.findall(text))
        marker_count = 0
        for no, line in enumerate(lines, 1):
            sm = SUITE_DEF.match(line)
            if sm:
                suites.append({'path': rel, 'line': no, 'macro': sm.group(1), 'definition': sm.group(2).strip()})
            if MARKERS.search(line):
                snippet = line.strip()
                if snippet:
                    marker_count += 1
                    hits.append({'path': rel, 'line': no, 'text': snippet[:500]})
            for sym in set(SYMBOL.findall(line)):
                symbol_files.setdefault(sym, set()).add(rel)
        files.append({'path': rel, 'lines': len(lines), 'bytes': path.stat().st_size,
                      'internal_markers': internal_hits, 'marker_hits': marker_count})
    symbols = [{'symbol': sym, 'file_count': len(paths), 'files': sorted(paths)}
               for sym, paths in sorted(symbol_files.items())]
    return {'root': str(root), 'file_count': len(files), 'suite_macro_count': len(suites),
            'marker_hit_count': len(hits), 'symbol_count': len(symbols),
            'files': files, 'suites': suites, 'marker_hits': hits, 'symbols': symbols}


def write_outputs(data: dict, out: Path, label: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / 'sdk_corpus_index.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    with (out / 'suite_index.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['path', 'line', 'macro', 'definition']); w.writeheader(); w.writerows(data['suites'])
    with (out / 'marker_hits.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['path', 'line', 'text']); w.writeheader(); w.writerows(data['marker_hits'])

    ranked = sorted(data['files'], key=lambda x: (x['marker_hits'], x['internal_markers'], x['lines']), reverse=True)
    with (out / 'file_ranking.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['path','lines','bytes','marker_hits','internal_markers']); w.writeheader(); w.writerows(ranked)
    top = ranked[:25]
    lines = [f'# {label} SDK Corpus Index', '',
             f'- Files indexed: {data["file_count"]}',
             f'- Suite macro definitions: {data["suite_macro_count"]}',
             f'- Research-marker line hits: {data["marker_hit_count"]}',
             f'- Unique API symbols: {data["symbol_count"]}', '', '## Highest-density files', '']
    lines.extend(f'- {x["marker_hits"]:4d} hits / {x["lines"]:5d} lines - `{x["path"]}`' for x in top)
    lines += ['', 'Marker hits are discovery leads, not findings.']
    (out / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines[:12]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--label', required=True)
    args = ap.parse_args()
    data = index_corpus(Path(args.root))
    write_outputs(data, Path(args.out), args.label)


if __name__ == '__main__':
    main()
