@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cl /nologo /std:c++17 /O2 /EHsc "D:\Developer\After Effects Internals Guide\probes\process-tools\rip_sampler.cpp" /Fe:"D:\Developer\After Effects Internals Guide\probes\process-tools\rip_sampler.exe"
exit /b %errorlevel%