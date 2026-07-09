# Configs

配置按用途组织，而不是按 stage 组织：

- `debug/`
  smoke 与快速自检配置。
- `baselines/`
  frozen backbone 与其他基础对照。
- `controls/`
  参数量匹配或公平性控制实验，例如 Euclidean Adapter。
- `branches/<branch-id>/`
  某一研究分支下的正式配置族。

建议让 `branch` 字段与 `research/branches/<branch-id>.md` 对应。默认情况下，一条研究线程也应拥有同名 git branch slug，对应的 git branch 名称通常是 `research/<branch-id>`。

推荐额外填写的 trace 字段：

- `change_scope`: `structure` / `parameter` / `control` / `baseline` / `debug`
- `change_target`: 这次主要改动的模块或机制
- `observation_refs`: 支撑本次实验的观测日志引用
- `literature_refs`: 支撑本次实验的文献日志引用
- `proposal_refs`: 支撑本次实验的结构提案日志引用
