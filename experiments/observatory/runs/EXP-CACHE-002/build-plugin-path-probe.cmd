@echo off
setlocal
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cd /d "D:\Developer\After Effects Internals Guide\experiments\observatory\runs\EXP-CACHE-002"
cl /nologo /EHsc /std:c++17 /O2 plugin_path_probe.cpp /Fe:plugin_path_probe.exe
exit /b %errorlevel%
