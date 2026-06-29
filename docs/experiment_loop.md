# Experiment Loop

本项目采用阶段门控，不采用无限随机循环。每个阶段结束必须写 `reports/stage_N_review.md`。

## 阶段 0：环境与数据检查

目标：

- 确认 GPU、CUDA、PyTorch、显存、磁盘空间。
- 确认模型缓存路径。
- 确认数据集下载状态。
- 产出 `reports/env_report.md`。

入口命令：

```bash
python scripts/env_check.py
```

验收条件：

- 环境报告存在。
- 如果 GPU 或显存异常，报告中明确写出。
- 数据和模型缓存目录已记录，即使为空。

## 阶段 1：Baseline 复现

目标：

- 跑 Chronos-2 frozen。
- 跑 naive seasonal、DLinear/NLinear、PatchTST 或 iTransformer。
- 记录每个 dataset/horizon 的 MSE、MAE、训练时间、显存。

验收条件：

- baseline 能稳定复现。
- `results/experiments.jsonl` schema 完整。
- 至少一个 debug run 能从 config 复现。

## 阶段 2：Adapter 最小原型

目标：

- 实现 Euclidean Adapter。
- 实现 Lorentz HyC-Adapter。
- 只在 ETT、Weather、Electricity 小规模跑。

验收条件：

- HyC 不 crash。
- 至少一个结构型数据集有正收益或明确失败解释。
- Euclidean 参数量匹配对照存在。

## 阶段 3：主实验扩展

目标：

- 加入 Traffic/PEMS、Solar、M5 子集。
- 加入 covariates。
- 跑 static graph、dynamic graph、fixed curvature、adaptive curvature。

验收条件：

- 主表形成。
- 至少 4 个数据集结果可信。
- OOM/crash 记录完整。

## 阶段 4：几何诊断

目标：

- 计算 graph hyperbolicity、tree-likeness、distortion。
- 做收益 vs 几何指标相关性。
- 画 learned curvature 可视化。

验收条件：

- 能解释哪些数据集有效、哪些无效。
- 不把弱结构数据上的失败包装成全面成功。

## 阶段 5：多 backbone 验证

目标：

- Chronos-Bolt 必跑。
- Moirai 或 TTM 二选一。
- TimesFM 作为可选附加验证。

验收条件：

- 方法不是 Chronos-2 特化。
- 至少一个非 Chronos-2 backbone 有可解释结果。

## 阶段 6：论文材料冻结

目标：

- 锁定主表、消融表、效率表。
- 生成 figure。
- 整理失败案例和 limitation。
- 不再随意改协议，只允许 bug fix。

验收条件：

- reviewer checklist 通过。
- 每个主结论都能追溯到 config、log、metrics、summary。

## 单轮实验循环

每轮正式实验必须按以下顺序：

1. 阅读当前阶段目标和最近 `stage_review`。
2. 写一句 `hypothesis`。
3. 选择或新增 config。
4. 跑 dry-run shape check。
5. 跑正式实验。
6. 解析 metrics。
7. 写 `summary.md`。
8. 追加 `experiments.jsonl`。
9. 判断 `keep/discard/crash/oom/inconclusive`。
10. 如果通过阶段门槛，写 stage review。

