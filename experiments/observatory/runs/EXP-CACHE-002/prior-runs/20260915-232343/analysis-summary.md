# EXP-CACHE-002 analysis

- Parsed rows: **2**
- Successful receipt checks: **0**
- Prefix-model matches: **0/0**
- Prefix-model mismatches: **0**
- Status counts: `{}`
- Geometry-check off matches: `(0, 0)`
- Geometry-check on matches: `(0, 0)`

## Passes


Prefix prediction: `ALL_EFFECTS (-1)` is normalized to `num_effects`; generated-prefix >= requested-prefix predicts VALID, while generated-prefix < requested-prefix predicts VALID_BUT_INCOMPLETE.
INVALID is not predicted in the unchanged same-context baseline. Pass A/B are analyzed independently so a state mutation cannot be mistaken for an effect-prefix encoding difference.
