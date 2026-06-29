# Reviewer Checklist

阶段结束前，主 agent 必须逐项自查。

## Baseline

- 是否有 frozen backbone baseline？
- 是否有 naive 或 classical baseline？
- 是否 baseline 的 split、horizon、normalization 与后续方法一致？

## Fairness

- 是否有 Euclidean 参数量匹配对照？
- HyC 与 Euclidean Adapter 参数量差距是否小于 20%？
- 是否所有方法使用相同 split/horizon/context length？
- 是否训练预算一致？

## Integrity

- 是否记录了失败实验？
- 是否存在只挑最好 seed 的情况？
- 是否修改过评估代码？
- 是否把 test set 用于 early stopping？
- 是否删除过 OOM/crash 记录？

## Evidence

- HyC 的收益是否超过噪声？
- 结果是否能被 geometry diagnostics 解释？
- 是否至少有一个强结构数据集和一个弱结构数据集？
- 是否报告了训练时间、显存和可训练参数量？

## Reproducibility

- 是否每个结果都有 config？
- 是否每个结果都有 run.log？
- 是否每个结果都有 metrics.json？
- 是否每个结果都有 summary.md？
- 另一个 agent 是否能从 `AGENTS.md` 和 config 复现实验？

## Conclusion Discipline

- 结论是否超过了实验支持范围？
- 1 seed 结果是否标注 preliminary？
- 失败边界是否写入 stage review？

