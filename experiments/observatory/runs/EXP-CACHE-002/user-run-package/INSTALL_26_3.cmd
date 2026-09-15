@echo off
setlocal EnableExtensions
set "SRC=%~dp0plugin\AEGP\Artie.aex"
set "ROOT=D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins"
set "DST=%ROOT%\AEIG-Probes"

tasklist /fi "imagename eq AfterFX.exe" | find /i "AfterFX.exe" >nul
if not errorlevel 1 (
  echo ERROR: After Effects is running. Save your work and close AE yourself first.
  pause
  exit /b 2
)
if not exist "%SRC%" (
  echo ERROR: staged probe not found: %SRC%
  pause
  exit /b 3
)
if not exist "%DST%" mkdir "%DST%"
copy /y "%SRC%" "%DST%\AEIGReceiptArtie.aex" >nul
if errorlevel 1 (
  echo ERROR: copy failed. You may need permission to write the AE Plug-ins folder.
  pause
  exit /b 4
)
echo Installed only: %DST%\AEIGReceiptArtie.aex
echo Now start After Effects normally yourself.
pause
