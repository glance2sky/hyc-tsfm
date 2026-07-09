# Branch Note: <branch-id>

- question: <one main question family>
- owner_backbone: <chronos-2 or other>
- primary_dataset_scope: <dataset or dataset family>
- status: active
- git_branch: `research/<branch-id>`
- base_branch: <branch you started from>
- base_commit: <commit you started from>
- current_belief: <what the branch currently believes>
- promotion_bar: <what evidence would justify keeping or expanding this branch>
- kill_signal: <what evidence would stop this branch and send us back to the base branch>

## Why This Branch Exists

<two to five sentences>

## Observation Focus

- <which internal signals or diagnostics matter most for this branch>

## Literature Anchors

- <papers, repos, or notes that justify likely structure moves>

## Structural Hypotheses

- <proposed model change and why>

## Active Configs

- `configs/...`

## Run Ledger

| run_id | config | result | meaning |
| --- | --- | --- | --- |
| pending | `configs/...` | pending | first planned run |

## Decisions

- Branch created from `<base_branch>` at `<base_commit>`.
- Default rule: keep this branch only if evidence improves over the current best comparison; otherwise discard it and return to `<base_branch>`.

## Next Moves

- <next move>
