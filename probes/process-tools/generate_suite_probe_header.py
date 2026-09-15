from pathlib import Path
import csv

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
NAMES = ROOT / "datasets" / "ae-sdk-25.6-suite-names.csv"
OUT = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie\AEIGSuiteProbe.h")
with NAMES.open(encoding="utf-8", newline="") as f:
    suites = list(csv.DictReader(f))

lines = [
    "#pragma once", "#include <windows.h>", "#include <stdio.h>", "",
    "static const char* AEIG_SUITE_LOG =",
    '    "D:\\\\Developer\\\\After Effects Internals Guide\\\\experiments\\\\observatory\\\\runs\\\\EXP-PLUGIN-001\\\\suite-acquisition.tsv";',
    "", "struct AEIG_SuiteName { const char* label; const char* name; };", "",
    "static const AEIG_SuiteName AEIG_SUITE_NAMES[] = {",
]
for r in suites:
    label = r["suite_macro"].removeprefix("k")
    name = r["suite_name"].replace('\\', '\\\\').replace('"', '\\"')
    lines.append(f'    {{"{label}", "{name}"}},')
lines += ["};", "", "static const long AEIG_MAX_SUITE_SELECTOR = 32;", ""]
lines += [
    "static void AEIG_WriteSuiteRow(const char* label, const char* suite_name, long selector, long err, const void* suiteP, long host_major, long host_minor)",
    "{",
    "    HANDLE h = CreateFileA(AEIG_SUITE_LOG, FILE_APPEND_DATA, FILE_SHARE_READ | FILE_SHARE_WRITE, nullptr, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);",
    "    if (h == INVALID_HANDLE_VALUE) return;",
    "    char line[768] = {};",
    "    int n = sprintf_s(line, sizeof(line), \"%lu\\t%ld\\t%ld\\t%s\\t%s\\t%ld\\t%ld\\t%p\\r\\n\", GetCurrentProcessId(), host_major, host_minor, label, suite_name, selector, err, suiteP);",
    "    if (n > 0) { DWORD written = 0; WriteFile(h, line, (DWORD)n, &written, nullptr); }",
    "    CloseHandle(h);",
    "}", "",
    "static void AEIG_ProbeSuiteMatrix(SPBasicSuite* pica_basicP, A_long host_major, A_long host_minor)",
    "{",
    "    if (!pica_basicP || !pica_basicP->AcquireSuite) return;",
    "    static volatile LONG once = 0;",
    "    if (InterlockedCompareExchange(&once, 1, 0) != 0) return;",
    "    for (const auto& s : AEIG_SUITE_NAMES) {",
    "        for (long selector = 1; selector <= AEIG_MAX_SUITE_SELECTOR; ++selector) {",
    "            const void* suiteP = nullptr;",
    "            SPErr err = pica_basicP->AcquireSuite(s.name, selector, &suiteP);",
    "            AEIG_WriteSuiteRow(s.label, s.name, selector, (long)err, suiteP, host_major, host_minor);",
    "            if (!err && suiteP && pica_basicP->ReleaseSuite) pica_basicP->ReleaseSuite(s.name, selector);",
    "        }",
    "    }",
    "}",
]
OUT.write_text("\n".join(lines), encoding="utf-8")
print("wrote prefix", OUT, "suites", len(suites))
