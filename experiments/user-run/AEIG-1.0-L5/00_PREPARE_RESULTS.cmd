@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
python "%ROOT%\probes\process-tools\prepare_aeig_l5_user_run.py"
if errorlevel 1 (
  echo.
  echo ERROR: result archival failed. Do not start the AE experiment.
  if not defined AEIG_NO_PAUSE pause
  exit /b 1
)
echo.
echo Previous mutable captures and derived run state were archived. Static evidence was left untouched.
echo This command does not start, stop, or modify After Effects.
if not defined AEIG_NO_PAUSE pause
