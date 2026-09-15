@echo off
setlocal EnableExtensions
set "ROOT=D:\Developer\After Effects Internals Guide"
set "CACHE=%ROOT%\experiments\observatory\runs\EXP-CACHE-002"
set "PLUGIN=%ROOT%\experiments\observatory\runs\EXP-PLUGIN-001"
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set "D=%%a-%%b-%%c-%%d"
for /f "tokens=1-3 delims=:., " %%a in ("%time%") do set "T=%%a%%b%%c"
set "STAMP=%D%-%T%"
set "ARC=%CACHE%\prior-attempts\%STAMP%"
set "MOVED=0"
for %%F in (receipt-matrix.tsv fixture-script.log fixture-output.avi analysis-summary.md) do (
  if exist "%CACHE%\%%F" (
    if not exist "%ARC%" mkdir "%ARC%"
    move /y "%CACHE%\%%F" "%ARC%\%%F" >nul
    set "MOVED=1"
  )
)
if exist "%PLUGIN%\suite-acquisition.tsv" (
  if not exist "%ARC%" mkdir "%ARC%"
  move /y "%PLUGIN%\suite-acquisition.tsv" "%ARC%\suite-acquisition.tsv" >nul
  set "MOVED=1"
)
if "%MOVED%"=="1" echo Previous AEIG captures archived under: %ARC%
if "%MOVED%"=="0" echo No previous core captures needed archiving.
echo Preparation complete. This script did not launch or modify After Effects.
pause
