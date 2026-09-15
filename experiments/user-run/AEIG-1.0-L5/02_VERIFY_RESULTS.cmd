@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
python "%ROOT%\probes\process-tools\finalize_aeig_l5_user_run.py"
set "ERR=%ERRORLEVEL%"
echo.
if "%ERR%"=="0" (
  echo AEIG L5 user-run captures passed verification and finalization gates.
  echo The guarded promotion step may now be run.
) else (
  echo Capture is incomplete or an evidence/model gate requires review.
  echo Preserve all raw captures unchanged; do not rerun automatically.
)
if not defined AEIG_NO_PAUSE pause
exit /b %ERR%
