from pathlib import Path
root = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie")
cpp = root / "Artie.cpp"
t = cpp.read_text(encoding="utf-8-sig")
if '#include "AEIGReceiptProbe.h"' not in t:
    t = t.replace('#include "Artie.h"', '#include "Artie.h"\n#include "AEIGReceiptProbe.h"', 1)
needle = "\t\t} else {\n\t\t\tERR(suites.CanvasSuite5()->AEGP_RenderTexture("
insert = "\t\t} else {\n\t\t\tAEIG_ProbeReceiptMatrix(in_dataP, render_contextH, polygonP->layer_contextH);\n\t\t\tERR(suites.CanvasSuite5()->AEGP_RenderTexture("
if "AEIG_ProbeReceiptMatrix(in_dataP" not in t:
    assert needle in t, "render insertion point not found"
    t = t.replace(needle, insert, 1)
cpp.write_text(t, encoding="utf-8")
h = root / "Artie.h"
u = h.read_text(encoding="utf-8-sig")
u = u.replace('"ADBE SDK Artie"', '"AEIG Receipt Probe"')
u = u.replace('#define Artie_ARTISAN_NAME\t\t\t"Artie"', '#define Artie_ARTISAN_NAME\t\t\t"AEIG Receipt Probe"')
h.write_text(u, encoding="utf-8")
print("patched", cpp, h)
