# Agent Rules

这是本项目最重要的规则文件。任何 agent 在执行实验、改代码或写结论前都必须遵守。

## 可以做

- 新增或修改模型代码、adapter 代码、训练脚本、配置文件。
- 新增实验配置、日志脚本、可视化脚本。
- 跑小规模 sanity check、baseline、ablation。
- 记录 crash、OOM、无提升实验。
- 在失败后提出修复方案并重跑同一实验。
- 用明确配置下载数据或模型，并记录来源、缓存路径和命令。
- 写阶段 review、结果表和失败分析。

## 不能做

- 不能修改测试集标签、验证集、数据切分或评估指标来制造提升。
- 不能把 test set 用于 early stopping 或超参搜索。
- 不能删除失败实验记录。
- 不能只报告最好的 seed。
- 不能把未完成或不稳定结果写成主结论。
- 不能把不同训练预算的模型直接公平比较。
- 不能在未记录理由的情况下改变 dataset split、horizon、normalization、context length。
- 不能让 HyC-Adapter 比 Euclidean Adapter 多很多参数后仍声称公平。
- 不能默认联网下载大数据或大模型，除非命令、来源和缓存路径已明确记录。
- 不能绕过 `scripts/run_experiment.py` 写入正式结果。

## 实验伦理

失败实验是科研证据的一部分。OOM、crash、无提升、只在单 seed 提升，都必须保留。不要把失败清理掉，也不要用漂亮叙事覆盖不确定性。

## 结果措辞

- `preliminary`：只跑了 1 seed 或 debug 规模。
- `stable`：至少 3 seeds，方差可接受。
- `inconclusive`：方向有信号但证据不足。
- `failed`：按当前实现或设置没有支持假设。

主结论只能来自 `stable` 或明确说明限制的 `inconclusive` 结果。

