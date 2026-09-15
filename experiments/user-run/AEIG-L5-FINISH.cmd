@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
set "PKG=%ROOT%\experiments\user-run\AEIG-1.0-L5"
set "AEIG_NO_PAUSE=1"

echo [1/2] Remove temporary probe. AE must already be closed.
call "%PKG%\REMOVE_26_3.cmd"
if errorlevel 1 (
  echo ERROR: probe removal failed. Stop and inspect before normal AE work.
  pause
  exit /b 1
)

echo [2/2] Verify, finalize, and run guarded AEIG 1.0 promotion...
python "%ROOT%\probes\process-tools\complete_aeig_1_0_after_operator_run.py"
set "ERR=%ERRORLEVEL%"
if "%ERR%"=="0" (
  echo.
  echo AEIG 1.0 completion pipeline PASS.
) else (
  echo.
  echo Completion stopped at a gate. Preserve all raw captures unchanged.
  echo A complete but refuting observation must be reviewed, not automatically rerun.
)
pause
exit /b %ERR%
