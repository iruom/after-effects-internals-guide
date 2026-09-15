@echo off
setlocal
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cl /nologo /EHsc /std:c++14 /MD /I"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\AEIGReceiptArtie" "D:\Developer\After Effects Internals Guide\experiments\observatory\runs\EXP-RG-001\trace_capture_smoke.cpp" /Fe:"D:\Developer\After Effects Internals Guide\experiments\observatory\runs\EXP-RG-001\trace_capture_smoke.exe"
exit /b %errorlevel%
