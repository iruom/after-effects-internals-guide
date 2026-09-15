#include <windows.h>
#include <iostream>
#include <fstream>
#include <string>
#include <string_view>

using SetDbFn = void (__cdecl *)(const std::string&);
using GetVolFn = int (__cdecl *)(const std::string_view&);
using SetVolFn = void (__cdecl *)(const std::string_view&, int);
using EnabledFn = bool (__cdecl *)(const std::string_view&, int, bool);
using SetMasterFn = void (__cdecl *)(int);
using GetMasterFn = int (__cdecl *)();
using StderrFn = void (__cdecl *)();
using TraceFn = void (__cdecl *)(int, const std::string_view&, const std::string_view&);
using ChangeFn = int (__cdecl *)();

template <class T> T sym(HMODULE m, const char* name) {
    auto p = reinterpret_cast<T>(GetProcAddress(m, name));
    if (!p) std::cerr << "missing=" << name << " err=" << GetLastError() << "\n";
    return p;
}

int main() {
    const wchar_t* root = L"C:\\Program Files\\Adobe\\Adobe After Effects 2025\\Support Files";
    SetDllDirectoryW(root);
    HMODULE m = LoadLibraryW((std::wstring(root) + L"\\dvacore.dll").c_str());
    if (!m) { std::cerr << "load_error=" << GetLastError() << "\n"; return 2; }
    auto setDb = sym<SetDbFn>(m, "?SetTraceDatabaseFromString@debug@dvacore@@YAXAEBV?$basic_string@EU?$char_traits@E@std@@U?$STLAllocator@E@allocator@dvacore@@@std@@@Z");
    auto getVol = sym<GetVolFn>(m, "?GetTraceVolume@debug@dvacore@@YAHAEBV?$basic_string_view@DU?$char_traits@D@std@@@std@@@Z");
    auto setVol = sym<SetVolFn>(m, "?SetTraceVolume@debug@dvacore@@YAXAEBV?$basic_string_view@DU?$char_traits@D@std@@@std@@H@Z");
    auto enabled = sym<EnabledFn>(m, "?TraceEnabled@debug@dvacore@@YA_NAEBV?$basic_string_view@DU?$char_traits@D@std@@@std@@H_N@Z");
    auto setMaster = sym<SetMasterFn>(m, "?SetMasterTraceVolume@debug@dvacore@@YAXH@Z");
    auto getMaster = sym<GetMasterFn>(m, "?GetMasterTraceVolume@debug@dvacore@@YAHXZ");
    auto toErr = sym<StderrFn>(m, "?MasterTraceToStdErr@debug@dvacore@@YAXXZ");
    auto trace = sym<TraceFn>(m, "?Trace@debug@dvacore@@YAXHAEBV?$basic_string_view@DU?$char_traits@D@std@@@std@@0@Z");
    auto change = sym<ChangeFn>(m, "?TraceChangeCount@debug@dvacore@@YAHXZ");
    if (!getVol || !setVol || !enabled || !setDb) return 3;

    std::ifstream f("C:\\Users\\kenta\\AppData\\Roaming\\Adobe\\After Effects\\25.6\\Trace Database.txt", std::ios::binary);
    std::string db((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
    std::cout << "db_bytes=" << db.size() << "\n";
    setDb(db);

    for (const char* name : {"BEE_Cache", "BEE_WorkQueue", "DiskCache", "GPUFoundation", "NoSuchAEIGCategory"}) {
        std::string_view v(name);
        std::cout << "category=" << name << " volume=" << getVol(v)
                  << " enabled1=" << enabled(v,1,false)
                  << " enabled5=" << enabled(v,5,false)
                  << " enabled6=" << enabled(v,6,false) << "\n";
    }
    std::string_view cat("dvacore.threads");
    int c0 = change ? change() : -1;
    int v0 = getVol(cat);
    setVol(cat, 2);
    int v2 = getVol(cat);
    bool e1 = enabled(cat,1,false), e2 = enabled(cat,2,false), e3 = enabled(cat,3,false);
    setVol(cat, 7);
    int v7 = getVol(cat);
    bool e6 = enabled(cat,6,false), e7 = enabled(cat,7,false), e8 = enabled(cat,8,false);
    int c1 = change ? change() : -1;
    std::cout << "mutation before=" << v0 << " low=" << v2
              << " e123=" << e1 << e2 << e3
              << " high=" << v7 << " e678=" << e6 << e7 << e8
              << " change=" << c0 << "->" << c1 << "\n";

    if (setMaster && getMaster && toErr && trace) {
        int m0 = getMaster();
        toErr();
        setMaster(3);
        int m3 = getMaster();
        bool m3l2 = enabled(cat,2,false), m3l4 = enabled(cat,4,false), m3l6 = enabled(cat,6,false);
        if (m3l2) trace(2, cat, std::string_view("AEIG_M3_L2"));
        if (m3l4) trace(4, cat, std::string_view("AEIG_M3_L4"));
        setMaster(10);
        int m10 = getMaster();
        bool m10l2 = enabled(cat,2,false), m10l4 = enabled(cat,4,false), m10l6 = enabled(cat,6,false);
        if (m10l4) trace(4, cat, std::string_view("AEIG_M10_L4"));
        if (m10l6) trace(6, cat, std::string_view("AEIG_M10_L6"));
        std::cout << "master=" << m0 << "->" << m3 << " enabled246=" << m3l2 << m3l4 << m3l6
                  << " ->" << m10 << " enabled246=" << m10l2 << m10l4 << m10l6 << "\n";
    }
    return 0;
}



