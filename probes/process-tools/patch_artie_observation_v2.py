from pathlib import Path

ROOT = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie")
CPP = ROOT / "Artie.cpp"
STAGE = ROOT / "AEIGArtisanStage.h"

STAGE.write_text(r'''#pragma once
#include <windows.h>
#include <stdio.h>

static const char* AEIG_ARTISAN_STAGE_LOG =
    "D:\\Developer\\After Effects Internals Guide\\experiments\\observatory\\runs\\EXP-RG-001\\artisan-stage.tsv";

static void AEIG_ArtisanStage(const char* stage, long value, long err_code) {
    HANDLE h = CreateFileA(AEIG_ARTISAN_STAGE_LOG, FILE_APPEND_DATA,
                           FILE_SHARE_READ | FILE_SHARE_WRITE, nullptr,
                           OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    if (h == INVALID_HANDLE_VALUE) return;
    char pass[32] = {}; AEIG_ReadPass(pass, sizeof(pass));
    char line[512] = {};
    int n = sprintf_s(line, sizeof(line), "%lu\t%s\t%s\t%ld\t%ld\r\n",
                      GetCurrentProcessId(), pass, stage ? stage : "", value, err_code);
    if (n > 0) { DWORD w = 0; WriteFile(h, line, (DWORD)n, &w, nullptr); }
    CloseHandle(h);
}
''', encoding="utf-8")
t = CPP.read_text(encoding="utf-8-sig")
if '#include "AEIGArtisanStage.h"' not in t:
    t = t.replace('#include "AEIGTraceCapture.h"\n',
                  '#include "AEIGTraceCapture.h"\n#include "AEIGArtisanStage.h"\n', 1)

old = '''\t\t} else {\n\t\t\tconst bool aeig_trace_began = AEIG_BeginTraceCapture();\n\t\t\tAEIG_ProbeReceiptMatrix(in_dataP, render_contextH, polygonP->layer_contextH);\n\t\t\tERR(suites.CanvasSuite5()->AEGP_RenderTexture(\trender_contextH,'''
new = '''\t\t} else {\n\t\t\tAEIG_ArtisanStage("GET_POLYGON_TEXTURE", 0, err);\n\t\t\tERR(suites.CanvasSuite5()->AEGP_RenderTexture(\trender_contextH,'''
if old in t:
    t = t.replace(old, new, 1)

old = '''\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t&polygonP->texture));\n\t\t\tAEIG_EndTraceCapture(aeig_trace_began);\n\n\t\t}'''
new = '''\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t&polygonP->texture));\n\t\t\tAEIG_ArtisanStage("RENDER_TEXTURE_DONE", polygonP->texture ? 1 : 0, err);\n\n\t\t}'''
if old in t:
    t = t.replace(old, new, 1)
old = '''\tAEGP_MemHandle\tlightsH\t\t\t\t= NULL;\n\t\n\tAEGP_SuiteHandler\tsuites(in_dataP->pica_basicP);'''
new = '''\tAEGP_MemHandle\tlightsH\t\t\t\t= NULL;\n\tbool\t\t\t\taeig_receipt_done\t= false;\n\t\n\tAEGP_SuiteHandler\tsuites(in_dataP->pica_basicP);'''
if old in t:
    t = t.replace(old, new, 1)

old = '''\tERR(Artie_CreateListOfLayerContexts(in_dataP, \n\t\t\t\t\t\t\t\t\t\trender_contextH,\n\t\t\t\t\t\t\t\t\t\t&layers_to_renderL, \n\t\t\t\t\t\t\t\t\t\t&layer_contexts));\n\n\tERR(Artie_BuildLights(in_dataP, render_contextH, &lightsH));'''
new = '''\tERR(Artie_CreateListOfLayerContexts(in_dataP, \n\t\t\t\t\t\t\t\t\t\trender_contextH,\n\t\t\t\t\t\t\t\t\t\t&layers_to_renderL, \n\t\t\t\t\t\t\t\t\t\t&layer_contexts));\n\tAEIG_ArtisanStage("LAYER_CONTEXTS", layers_to_renderL, err);\n\n\tERR(Artie_BuildLights(in_dataP, render_contextH, &lightsH));\n\tAEIG_ArtisanStage("BUILD_LIGHTS_DONE", lightsH ? 1 : 0, err);'''
if old in t:
    t = t.replace(old, new, 1)
old = '''\t\tif (item_flags & AEGP_ItemFlag_HAS_VIDEO){ \n\t\t\tERR(Artie_AddPolygonToScene(\tin_dataP,'''
new = '''\t\tif (item_flags & AEGP_ItemFlag_HAS_VIDEO){ \n\t\t\tif (!aeig_receipt_done) {\n\t\t\t\tAEIG_ArtisanStage("RECEIPT_PROBE_BEGIN", iL, err);\n\t\t\t\tAEIG_ProbeReceiptMatrix(in_dataP, render_contextH, layer_contexts.layer_contexts[iL]);\n\t\t\t\taeig_receipt_done = true;\n\t\t\t\tAEIG_ArtisanStage("RECEIPT_PROBE_END", iL, err);\n\t\t\t}\n\t\t\tERR(Artie_AddPolygonToScene(\tin_dataP,'''
if old in t:
    t = t.replace(old, new, 1)

old = '''\tAEFX_CLR_STRUCT(layer_contexts);\n\n\tERR(Artie_BuildCamera(in_dataP, render_contextH, &cameraH));\n\t\n\tif (cameraH){\n\t\tERR(Artie_BuildScene(in_dataP, layer_contexts, render_contextH, &sceneH));\n\t\tif (sceneH){\n\t\t\tERR(Artie_Paint(in_dataP, render_contextH, sceneH, cameraH));\n\t\t\tERR2(Artie_DisposeScene(in_dataP, render_contextH, sceneH)); \t\n\t\t\tERR2(Artie_DisposeCamera(in_dataP,  cameraH));\n\t\t}\n\t}\n\treturn err;'''
new = '''\tAEFX_CLR_STRUCT(layer_contexts);\n\n\tAEIG_ArtisanStage("RENDER_ENTER", 0, err);\n\tconst bool aeig_trace_began = AEIG_BeginTraceCapture();\n\tAEIG_ArtisanStage("TRACE_BEGIN", aeig_trace_began ? 1 : 0, err);\n\tERR(Artie_BuildCamera(in_dataP, render_contextH, &cameraH));\n\tAEIG_ArtisanStage("BUILD_CAMERA_DONE", cameraH ? 1 : 0, err);\n\t\n\tif (cameraH){\n\t\tERR(Artie_BuildScene(in_dataP, layer_contexts, render_contextH, &sceneH));\n\t\tAEIG_ArtisanStage("BUILD_SCENE_DONE", sceneH ? 1 : 0, err);\n\t\tif (sceneH){\n\t\t\tERR(Artie_Paint(in_dataP, render_contextH, sceneH, cameraH));\n\t\t\tAEIG_ArtisanStage("PAINT_DONE", 0, err);\n\t\t\tERR2(Artie_DisposeScene(in_dataP, render_contextH, sceneH)); \t\n\t\t\tERR2(Artie_DisposeCamera(in_dataP,  cameraH));\n\t\t}\n\t}\n\tAEIG_EndTraceCapture(aeig_trace_began);\n\tAEIG_ArtisanStage("RENDER_EXIT", 0, err);\n\treturn err;'''
if old in t:
    t = t.replace(old, new, 1)
CPP.write_text(t, encoding="utf-8")
print("AEIG Artie observation v2 patch applied")
