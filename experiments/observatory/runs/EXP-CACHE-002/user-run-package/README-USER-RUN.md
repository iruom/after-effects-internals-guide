# AEIG Core User-Run Experiment

This package collects two experiments in one disposable After Effects session:

- `EXP-PLUGIN-001`: full PICA suite-name / integer-selector negotiation at AEGP EntryPoint.
- `EXP-CACHE-002`: Canvas effect-prefix receipt status matrix from a real Artisan render context.

The ChatGPT-side workflow intentionally does **not** start, close, click, render, or manipulate After Effects. Those AE operations are delegated to the user.

## Built probe

Staged binary: `plugin\AEGP\Artie.aex`

SHA-256:
`8FAD5221BC5AA270CFF9505F6E3F2ABF7916F4B4DFE7820BA653DFDA759E9FEE`

The probe is built from Adobe SDK 25.6 Artie. Stock Artie remains on CanvasSuite5 while AEIG receipt measurement uses CanvasSuite8. At EntryPoint it probes **48 suite-name families × PICA selectors 1..32**. Successful `AcquireSuite` calls are immediately balanced with `ReleaseSuite`; discovered tables are not dereferenced by the negotiation matrix.

## Before the run

Use a disposable blank project/session, not a production project. Save existing work and quit After Effects yourself before installing the probe.

Run `00_PREPARE_RESULTS.cmd`. It archives any previous AEIG captures with a timestamp instead of deleting them.

For the installed 26.3 build on this machine, `INSTALL_26_3.cmd` can copy the staged AEX into the known writable AE plug-in root. **You run it yourself while AE is closed.**

## User actions

1. Save work and close After Effects yourself.
2. Run `00_PREPARE_RESULTS.cmd`.
3. Run `INSTALL_26_3.cmd` yourself, or manually copy `plugin\AEGP\Artie.aex` into an `AEIG-Probes` folder under the tested AE plug-in root.
4. Start After Effects normally yourself with a disposable blank project.
5. In AE choose **File > Scripts > Run Script File...** and run `01_RUN_IN_AE.jsx`.
6. The script creates a temporary 64×64 comp, selects renderer `AEIG Receipt Probe`, adds Gaussian Blur → Fill → Tint, renders one frame, then removes its temporary render-queue item and comp.
7. After the script completes, close AE yourself.
8. Run `REMOVE_26_3.cmd` yourself, or manually remove the copied probe folder.
9. Run `02_VERIFY_RESULTS.cmd`, or return to ChatGPT and say `AEIG experiment completed`; the assistant can inspect the files without operating AE.

If AE blocks script file writes, enable the normal After Effects preference that permits scripts to write files, then rerun the JSX in the disposable session.

## Expected captures

`EXP-PLUGIN-001\suite-acquisition.tsv` should exist after the plug-in EntryPoint runs. With the current probe, the raw matrix can contain up to **1,536 acquisition attempts** before filtering.

`EXP-CACHE-002\fixture-script.log` and `EXP-CACHE-002\receipt-matrix.tsv` should exist after the fixture render. `fixture-output.avi` is disposable evidence that the one-frame render completed.

The analysis pipeline reduces the raw captures into:

- `datasets\exp-plugin-001-suite-acquisition.csv`
- `datasets\exp-cache-002-receipt-matrix-summary.csv`
- runtime-vs-published selector diagnostics
- receipt-prefix model diagnostics

Do not manually edit the TSV captures. AEIG hashes and preserves raw files before promoting either experiment to `observed` / `replicated`.
