@echo off
setlocal
set "DST=D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\AEIG-Probes"
for %%P in (AfterFX.exe AfterFX.com aerender.exe) do (
  tasklist /FI "IMAGENAME eq %%P" | find /I "%%P" >nul
  if not errorlevel 1 (
    echo ERROR: %%P is running. Close AE processes yourself before removing the probe.
    if not defined AEIG_NO_PAUSE pause
    exit /b 2
  )
)
del /Q "%DST%\AEIGReceiptArtie.aex" 2>nul
if exist "%DST%\AEIGReceiptArtie.aex" (
  echo ERROR: probe still exists; remove it manually before normal work.
  if not defined AEIG_NO_PAUSE pause
  exit /b 3
)
rmdir "%DST%" 2>nul
echo Temporary AEIG probe removed.
if not defined AEIG_NO_PAUSE pause
