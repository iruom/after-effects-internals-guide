@echo off
setlocal
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
set "AE_PLUGIN_BUILD_DIR=D:\Developer\After Effects Internals Guide\experiments\observatory\runs\EXP-CACHE-002\artie-build"
msbuild "E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\AEGP\Artie\Win\Artie.vcxproj" /m /p:Configuration=Release /p:Platform=x64 /v:minimal
exit /b %errorlevel%
