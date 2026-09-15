@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"
python "%ROOT%\probes\process-tools\verify_user_core_probes.py"
set "BASE=%errorlevel%"
echo.
python "%ROOT%\probes\process-tools\analyze_plugin_host_experiment.py"
echo.
python "%ROOT%\probes\process-tools\analyze_receipt_experiment.py"
echo.
python "%ROOT%\probes\process-tools\validate_observatory_manifests.py"
echo.
if not "%BASE%"=="0" (
  echo Captures are incomplete. Read fixture-script.log first; do not rerun blindly.
  pause
  exit /b %BASE%
)
echo Core captures are present and analyzers completed.
echo Return to ChatGPT and say: AEIG experiment completed.
pause
