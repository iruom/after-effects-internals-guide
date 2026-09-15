#include <windows.h>
#include <iostream>
#include <string>
#include <cstring>

using MakeDirFn = void* (__cdecl *)(void* out_dir);
using FullPathFn = std::string* (__cdecl *)(void* dir, std::string* out);
using DtorFn = void (__cdecl *)(void* dir);

template<class T> T sym(HMODULE m, const char* n) {
    auto p = reinterpret_cast<T>(GetProcAddress(m, n));
    if (!p) std::cerr << "missing " << n << " err=" << GetLastError() << "\n";
    return p;
}

static void show(HMODULE m, const char* label, const char* maker_name) {
    auto make = sym<MakeDirFn>(m, maker_name);
    auto full = sym<FullPathFn>(m,
        "?FullPathMultiByte@Dir@filesupport@dvacore@@QEBA?AV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@XZ");
    auto dtor = sym<DtorFn>(m, "??1Dir@filesupport@dvacore@@QEAA@XZ");
    if (!make || !full || !dtor) return;
    alignas(16) unsigned char dir[64]; std::memset(dir, 0, sizeof(dir));
    make(dir);
    std::string path; full(dir, &path);
    std::cout << label << "=" << path << "\n";
    dtor(dir);
}

int main() {
    const wchar_t* root = L"C:\\Program Files\\Adobe\\Adobe After Effects 2025\\Support Files";
    SetDllDirectoryW(root);
    HMODULE m = LoadLibraryW((std::wstring(root) + L"\\dvacore.dll").c_str());
    if (!m) return 2;
    show(m, "plugins", "?PluginsDir@commondirs@filesupport@dvacore@@YA?AVDir@23@XZ");
    show(m, "required", "?RequiredPluginsDir@commondirs@filesupport@dvacore@@YA?AVDir@23@XZ");
    show(m, "alluser", "?AllUserPluginsDir@commondirs@filesupport@dvacore@@YA?AVDir@23@XZ");
    show(m, "user", "?UserPluginsDir@commondirs@filesupport@dvacore@@YA?AVDir@23@XZ");
    return 0;
}
