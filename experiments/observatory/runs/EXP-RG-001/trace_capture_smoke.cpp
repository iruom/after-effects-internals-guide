#include <windows.h>
#include <stdio.h>
#include <string>
#include "AEIGTraceCapture.h"

int wmain(int argc, wchar_t** argv) {
    if (argc != 2) { fwprintf(stderr, L"usage: trace_capture_smoke <dvacore.dll>\n"); return 2; }
    std::wstring path(argv[1]);
    size_t cut = path.find_last_of(L"\\/");
    if (cut != std::wstring::npos) SetDllDirectoryW(path.substr(0, cut).c_str());
    HMODULE m = LoadLibraryW(path.c_str());
    if (!m) { printf("load_error=%lu\n", GetLastError()); return 3; }
    bool began = AEIG_BeginTraceCapture();
    printf("begin=%d master=%d seq=%d\n", began ? 1 : 0,
           g_aeig_trace.getMaster ? g_aeig_trace.getMaster() : -1,
           g_aeig_trace.seq);
    if (began) {
        for (int i=0; i<9; ++i) {
            printf("cat=%s volume=%d\n", AEIG_TRACE_CATEGORIES[i],
                   AEIG_GetTraceVolume(AEIG_TRACE_CATEGORIES[i]));
        }
    }
    AEIG_EndTraceCapture(began);
    printf("end active=%d\n", g_aeig_trace.active ? 1 : 0);
    return began ? 0 : 4;
}
