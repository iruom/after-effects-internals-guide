#include <windows.h>
#include <tlhelp32.h>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <chrono>

struct ModuleRange {
    uintptr_t base{};
    DWORD size{};
    std::wstring name;
    std::wstring path;
};

static std::vector<ModuleRange> Modules(DWORD pid) {
    std::vector<ModuleRange> out;
    HANDLE s = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid);
    if (s == INVALID_HANDLE_VALUE) return out;
    MODULEENTRY32W m{}; m.dwSize = sizeof(m);
    if (Module32FirstW(s, &m)) do {
        out.push_back({reinterpret_cast<uintptr_t>(m.modBaseAddr), m.modBaseSize, m.szModule, m.szExePath});
    } while (Module32NextW(s, &m));
    CloseHandle(s);
    return out;
}
static std::vector<DWORD> Threads(DWORD pid) {
    std::vector<DWORD> out;
    HANDLE s = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (s == INVALID_HANDLE_VALUE) return out;
    THREADENTRY32 t{}; t.dwSize = sizeof(t);
    if (Thread32First(s, &t)) do {
        if (t.th32OwnerProcessID == pid) out.push_back(t.th32ThreadID);
    } while (Thread32Next(s, &t));
    CloseHandle(s);
    return out;
}

static const ModuleRange* FindModule(const std::vector<ModuleRange>& mods, uintptr_t rip) {
    for (const auto& m : mods) {
        if (rip >= m.base && rip < m.base + m.size) return &m;
    }
    return nullptr;
}

static std::string Narrow(const std::wstring& s) {
    if (s.empty()) return {};
    int n = WideCharToMultiByte(CP_UTF8, 0, s.c_str(), -1, nullptr, 0, nullptr, nullptr);
    std::string out(n ? n - 1 : 0, '\0');
    if (n > 1) WideCharToMultiByte(CP_UTF8, 0, s.c_str(), -1, out.data(), n, nullptr, nullptr);
    return out;
}
int wmain(int argc, wchar_t** argv) {
    if (argc < 5) {
        std::wcerr << L"usage: rip_sampler <pid> <duration_ms> <interval_ms> <output.tsv>\n";
        return 2;
    }
    DWORD pid = std::wcstoul(argv[1], nullptr, 10);
    long long duration_ms = std::wcstoll(argv[2], nullptr, 10);
    long long interval_ms = std::wcstoll(argv[3], nullptr, 10);
    std::ofstream out(Narrow(argv[4]), std::ios::binary);
    if (!out) return 3;
    FILETIME ft{}; GetSystemTimePreciseAsFileTime(&ft);
    ULARGE_INTEGER u{}; u.LowPart = ft.dwLowDateTime; u.HighPart = ft.dwHighDateTime;
    unsigned long long start_unix_ns = (u.QuadPart - 116444736000000000ULL) * 100ULL;
    out << "# start_unix_ns=" << start_unix_ns << '\n';
    out << "elapsed_us\ttid\trip\tmodule\trva\tpath\n";
    auto mods = Modules(pid);
    auto tids = Threads(pid);
    auto begin = std::chrono::steady_clock::now();
    long long rounds = 0, samples = 0, failures = 0;
    for (;;) {
        auto now = std::chrono::steady_clock::now();
        auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now - begin).count();
        if (elapsed_ms >= duration_ms) break;
        if ((rounds % 20) == 0) tids = Threads(pid);
        for (DWORD tid : tids) {
            HANDLE th = OpenThread(THREAD_SUSPEND_RESUME | THREAD_GET_CONTEXT | THREAD_QUERY_INFORMATION, FALSE, tid);
            if (!th) { ++failures; continue; }
            DWORD prev = SuspendThread(th);
            if (prev == static_cast<DWORD>(-1)) { CloseHandle(th); ++failures; continue; }
            CONTEXT c{}; c.ContextFlags = CONTEXT_CONTROL;
            BOOL ok = GetThreadContext(th, &c);
            ResumeThread(th); CloseHandle(th);
            if (!ok) { ++failures; continue; }
            uintptr_t rip = static_cast<uintptr_t>(c.Rip);
            const ModuleRange* m = FindModule(mods, rip);
            auto us = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::steady_clock::now() - begin).count();
            out << us << '\t' << tid << "\t0x" << std::hex << rip << std::dec;
            if (m) out << '\t' << Narrow(m->name) << "\t0x" << std::hex << (rip - m->base) << std::dec << '\t' << Narrow(m->path);
            else out << "\t<unknown>\t0x0\t";
            out << '\n'; ++samples;
        }
        ++rounds;
        std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));
    }
    std::cerr << "rounds=" << rounds << " samples=" << samples << " failures=" << failures << " modules=" << mods.size() << "\n";
    return 0;
}