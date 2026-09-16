---
status: active
last_verified: 2026-09-16
primary_evidence:
  - canonical AEIG-L5 PREPARE/STATUS/FINISH wrappers
  - AEIG 1.0 L5 operator-session and verification pipeline
---
# AEIG 1.0 Final Operator Run

AEIG 1.0 の残る実観測は、After Effects 26.3 を使う **1回の disposable operator session** に集約されています。目的は `state-identity`、`render-graph`、`cache` のL5 evidenceと、locked prediction `PRED-004`〜`PRED-008` を解決することです。

通常の制作projectで実行しないでください。canonical fixtureは自動生成されるため、空のprojectで十分です。

## 現在地の確認

いつでも次を実行できます。

```text
D:\Developer\After Effects Internals Guide\experiments\user-run\AEIG-L5-STATUS.cmd
```

STATUSはAEを起動・終了せず、probe/raw/session/verificationの現在phaseだけを表示します。

## 実行前

1. 通常作業を保存します。
2. After Effects、`AfterFX.com`、`aerender.exe` を自分で終了します。
3. AEIG以外の重要作業を同時に行わない状態にします。
4. raw captureやprediction logを手作業で編集しません。
## Step 1 — PREPARE

AEを閉じた状態で次を実行します。

```text
D:\Developer\After Effects Internals Guide\experiments\user-run\AEIG-L5-PREPARE.cmd
```

PREPAREは順番に safety preflight、旧run archive、operator session発行、clean preflight、canonical probe installを行います。成功すると `READY: start After Effects 26.3 manually.` と表示されます。

PREPAREが失敗した場合は、その場で止めます。AEを起動して次へ進まないでください。

## Step 2 — After Effectsで1回だけ実行

1. After Effects 26.3 を自分で起動します。
2. 空のdisposable projectを使用します。
3. **File > Scripts > Run Script File...** を選びます。
4. 次のscriptを **1回だけ** 実行します。

```text
D:\Developer\After Effects Internals Guide\experiments\user-run\AEIG-1.0-L5\01_RUN_IN_AE.jsx
```

scriptは64×64 comp、中央32×32 3D solid、Gaussian Blur / Fill / Tintを作成し、AEIG Receipt Probe rendererでPass A/Bをrenderします。Blurは10→75へmutationされ、Receipt、PICA selector matrix、BEE/TDB/RG trace、runtime Reflection、environment、A/B outputを取得します。
## Step 3 — AEを終了してFINISH

script完了後、After Effectsを自分で終了します。`AfterFX.exe` が残っている状態ではFINISHしません。

次を実行します。

```text
D:\Developer\After Effects Internals Guide\experiments\user-run\AEIG-L5-FINISH.cmd
```

FINISHはtemporary probe removal、Static RC verification、diagnostic、raw capture verification、prediction finalization、domain decision、guarded 1.0 promotion、repository integrity、release readinessを順番に実行します。

## 成功条件

完全成功では最終的に次が成立します。

- raw capture 10/10が同一operator sessionに属する。
- Blur read-backが10→75で、A/B outputがmaterializeされる。
- Receipt / PICA / RG trace / Reflection analyzerがmechanically complete。
- locked predictionが観測結果で解決される。
- `state-identity` / `render-graph` / `cache` がL5へ到達する。
- coverageが27/27になる。
- final repository/release auditsがPASSする。
- repository rootに `VERSION` が作られ、内容が `1.0` になる。

STATUSでは完成後にfinalized stateが表示されます。
## 失敗・反証時の扱い

**complete captureなのにpredictionが外れた場合は、失敗runではありません。** その観測自体が重要なevidenceです。FINISHはcanonical prediction logとdomain decisionへ結果を保存し、`model_revision_required` を立ててpromotionを止めます。

その場合はraw artifactを削除・編集・上書きせず、そのまま保存してください。自動再実行もしません。モデルを修正してから別runとして扱います。

mechanically incompleteの場合もrawを保持します。再実行が必要になった場合はPREPAREがtimestamp付き `prior-runs` へ旧runをarchiveします。

## やってはいけないこと

- probeを通常作業へ常設する。
- scriptを同じsessionで複数回実行する。
- capture中に別project/通常作業を混ぜる。
- raw TSV/log/outputを手編集して辻褄を合わせる。
- predictionが外れたからという理由だけで再実行する。
- AE起動中にPREPARE/FINISHを強行する。

## Evidence discipline

このrunは「予測を当てるため」のものではありません。事前locked predictionに対して、実際のAE 26.3が何を返すかを記録するためのものです。確認・反証・inconclusiveのどれも観測結果として扱い、証拠より先にモデルを優先しません。

Related: `docs/reference/release-readiness.md`, `docs/reference/roadmap-status.md`, `docs/cache-system/state-identity.md`, `docs/render-graph/render-graph-model.md`, `docs/evaluation/dirty-invalidation.md`.
