# Research Branches

每个研究线程维护两个状态文件和一对活动日志：

- `<branch-id>.md`
  人类可读的研究 ledger。
- `<branch-id>.json`
  机器可读的分支状态，记录 git_branch、base_branch、base_commit 与 keep/discard 决策。
- `../activity/<branch-id>.md`
  人类可读的研究时间线。
- `../activity/<branch-id>.jsonl`
  结构化事件流。

一个 branch 对应一个连续的问题家族，例如：

- `electricity-baseline`
- `electricity-hyc`
- `covariate-injection`

默认 git branch 名称是 `research/<branch-id>`。配置中的 `branch` 字段应与这里的 branch id 对齐。
