from __future__ import annotations
import csv, json, re
from pathlib import Path

SDK_ROOT = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples")
OUT_ROOT = Path(r"D:\Developer\After Effects Internals Guide\datasets\sdk-25.6")
EXTS = {'.h', '.hpp', '.c', '.cpp', '.r', '.rc', '.py'}

MARKERS = re.compile(
    r"deprecated|obsolete|legacy|internal|private|not thread safe|thread safe|"
    r"do not|don't|must not|must be|warning|todo|fixme|workaround|confusing|"
    r"cache|receipt|guid|timestamp|render|flatten|unflatten|sequence|roi|bounds|"
    r"async|speculative|invalidate|dirty|mutex|deadlock",
    re.I,
)
SUITE_DEF = re.compile(r"^\s*#define\s+(k\w*Suite\w*)\s+(.+?)\s*$")
SYMBOL = re.compile(r"\b(?:AEGP|PF|PR)_[A-Za-z0-9_]+\b")
INTERNAL = re.compile(r"\b(?:AEGP_INTERNAL|A_INTERNAL)\b|_Private\.h")
def read_text(path: Path) -> str:
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'cp932'):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            pass
    return path.read_text(encoding='utf-8', errors='replace')


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    files, suites, hits = [], [], []
    symbol_files: dict[str, set[str]] = {}

    for path in SDK_ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        text = read_text(path)
        lines = text.splitlines()
        rel = str(path.relative_to(SDK_ROOT))
        internal_hits = len(INTERNAL.findall(text))
        files.append({'path': rel, 'lines': len(lines), 'bytes': path.stat().st_size,
                      'internal_markers': internal_hits})
        for no, line in enumerate(lines, 1):
            sm = SUITE_DEF.match(line)
            if sm:
                suites.append({'path': rel, 'line': no, 'macro': sm.group(1),
                               'definition': sm.group(2).strip()})
            if MARKERS.search(line):
                snippet = line.strip()
                if snippet:
                    hits.append({'path': rel, 'line': no, 'text': snippet[:500]})
            for sym in set(SYMBOL.findall(line)):
                symbol_files.setdefault(sym, set()).add(rel)

    symbols = [
        {'symbol': sym, 'file_count': len(paths), 'files': sorted(paths)}
        for sym, paths in sorted(symbol_files.items())
    ]
    result = {
        'sdk_root': str(SDK_ROOT),
        'file_count': len(files),
        'suite_macro_count': len(suites),
        'marker_hit_count': len(hits),
        'symbol_count': len(symbols),
        'files': files,
        'suites': suites,
        'marker_hits': hits,
        'symbols': symbols,
    }
    (OUT_ROOT / 'sdk_corpus_index.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    with (OUT_ROOT / 'suite_index.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['path', 'line', 'macro', 'definition'])
        w.writeheader(); w.writerows(suites)

    with (OUT_ROOT / 'marker_hits.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['path', 'line', 'text'])
        w.writeheader(); w.writerows(hits)

    summary = [
        '# AE 25.6 SDK Corpus Index', '',
        f'- Files indexed: {len(files)}',
        f'- Suite macro definitions: {len(suites)}',
        f'- Research-marker line hits: {len(hits)}',
        f'- Unique AEGP/PF/PR symbols: {len(symbols)}', '',
        'Generated from the local distributed SDK. Marker hits are discovery leads, not findings.'
    ]
    (OUT_ROOT / 'README.md').write_text('\n'.join(summary) + '\n', encoding='utf-8')
    print('\n'.join(summary))

if __name__ == '__main__':
    main()
