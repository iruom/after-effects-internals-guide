@echo off
setlocal
set "ROOT=D:\Developer\After Effects Internals Guide"

echo AEIG 1.0 L5 operator status
python "%ROOT%\probes\process-tools\status_aeig_l5_operator_run.py"
set "ERR=%ERRORLEVEL%"
echo.
echo Phase meanings:
echo   NEEDS_PREPARE              = run AEIG-L5-PREPARE.cmd after closing AE
echo   READY_NOT_STARTED          = preparation complete; start AE manually
echo   AE_RUNNING_WITH_PROBE      = run 01_RUN_IN_AE.jsx once in AE
echo   CAPTURE_COMPLETE_VERIFY_PENDING = close AE, then run AEIG-L5-FINISH.cmd
echo   FINALIZED_PROMOTABLE         = evidence is complete and promotion can proceed
echo   FINALIZED_REVIEW_REQUIRED    = preserve evidence; prediction/model review required
echo   CAPTURE_PARTIAL/INVALID      = preserve raw evidence; do not rerun automatically
pause
exit /b %ERR%
