@echo off
setlocal EnableExtensions
set "DST=D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\AEIG-Probes"

tasklist /fi "imagename eq AfterFX.exe" | find /i "AfterFX.exe" >nul
if not errorlevel 1 (
  echo ERROR: After Effects is running. Close AE yourself before removing the probe.
  pause
  exit /b 2
)
if exist "%DST%\AEIGReceiptArtie.aex" del /q "%DST%\AEIGReceiptArtie.aex"
if exist "%DST%\AEIGReceiptArtie.aex" (
  echo ERROR: probe removal failed.
  pause
  exit /b 3
)
2>nul rmdir "%DST%"
echo AEIGReceiptArtie.aex removed.
echo The directory was removed only if it was empty.
pause
