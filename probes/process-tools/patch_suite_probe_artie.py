from pathlib import Path

p = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie\Artie.cpp")
t = p.read_text(encoding="utf-8-sig")

if '#include "AEIGSuiteProbe.h"' not in t:
    t = t.replace(
        '#include "AEIGReceiptProbe.h"',
        '#include "AEIGReceiptProbe.h"\n#include "AEIGSuiteProbe.h"',
        1,
    )

needle = '\tAEIG_WriteReceiptRow("ENTRY", -99, -99, -99, 0, -99, 0);'
insert = needle + '\n\tAEIG_ProbeSuiteMatrix(pica_basicP, major_versionL, minor_versionL);'
if "AEIG_ProbeSuiteMatrix(pica_basicP" not in t:
    assert needle in t, "EntryPoint marker not found"
    t = t.replace(needle, insert, 1)

p.write_text(t, encoding="utf-8")
print("patched", p)
