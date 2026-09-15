@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
set "PKG=%ROOT%\experiments\user-run\AEIG-1.0-L5"
set "AEIG_NO_PAUSE=1"

echo [1/4] Safety preflight (AE must be stopped; stale prior captures are allowed here)...
python "%ROOT%\probes\process-tools\preflight_aeig_l5_operator_run.py" --allow-stale-capture
if errorlevel 1 (
  echo.
  echo ERROR: safety preflight failed. Do not archive or install anything.
  pause
  exit /b 1
)

echo [2/4] Archive previous mutable run state...
call "%PKG%\00_PREPARE_RESULTS.cmd"
if errorlevel 1 exit /b 2

echo [3/4] Full clean preflight...
python "%ROOT%\probes\process-tools\preflight_aeig_l5_operator_run.py"
if errorlevel 1 (
  echo ERROR: clean preflight failed after archival. Do not start AE.
  pause
  exit /b 3
)

echo [4/4] Install temporary probe...
call "%PKG%\INSTALL_26_3.cmd"
if errorlevel 1 exit /b 4

echo.
echo READY: start After Effects 26.3 manually.
echo In an empty disposable project, run:
echo %PKG%\01_RUN_IN_AE.jsx
echo Then close After Effects manually and run AEIG-L5-FINISH.cmd.
pause
