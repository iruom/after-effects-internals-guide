@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
set "SRC=%~dp0plugin\AEGP\AEIGReceiptArtie.aex"
set "DST=D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\AEIG-Probes"

python "%ROOT%\probes\process-tools\preflight_aeig_l5_operator_run.py"
if errorlevel 1 (
  echo ERROR: canonical preflight failed. Prepare a clean operator session before install.
  if not defined AEIG_NO_PAUSE pause
  exit /b 1
)

for %%P in (AfterFX.exe AfterFX.com aerender.exe) do (
  tasklist /FI "IMAGENAME eq %%P" | find /I "%%P" >nul
  if not errorlevel 1 (
    echo ERROR: %%P is running. Close AE processes yourself before installing the probe.
    if not defined AEIG_NO_PAUSE pause
    exit /b 2
  )
)
if not exist "%SRC%" (
  echo ERROR: probe binary missing: %SRC%
  if not defined AEIG_NO_PAUSE pause
  exit /b 3
)
mkdir "%DST%" 2>nul
copy /Y "%SRC%" "%DST%\AEIGReceiptArtie.aex" >nul
if errorlevel 1 (
  del /Q "%DST%\AEIGReceiptArtie.aex" 2>nul
  echo ERROR: copy failed. Any partial destination was removed; no AE process was touched.
  if not defined AEIG_NO_PAUSE pause
  exit /b 4
)
fc /B "%SRC%" "%DST%\AEIGReceiptArtie.aex" >nul
if errorlevel 1 (
  del /Q "%DST%\AEIGReceiptArtie.aex" 2>nul
  echo ERROR: installed probe did not byte-match the canonical package and was removed.
  if not defined AEIG_NO_PAUSE pause
  exit /b 5
)
echo Installed and byte-verified temporary AEIG probe to:
echo %DST%\AEIGReceiptArtie.aex
if not defined AEIG_NO_PAUSE pause
