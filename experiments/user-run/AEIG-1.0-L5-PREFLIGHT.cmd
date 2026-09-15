@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
python "%ROOT%\probes\process-tools\preflight_aeig_l5_operator_run.py"
set "ERR=%ERRORLEVEL%"
echo.
if "%ERR%"=="0" (
  echo Preflight passed. Follow experiments\user-run\AEIG-1.0-L5\README.md exactly.
) else (
  echo Preflight has blockers. Do not install or start the AEIG probe yet.
)
pause
exit /b %ERR%
