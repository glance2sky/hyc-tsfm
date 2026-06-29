# HyC-TSFM

这是一篇关于 **HyC-Adapter 是否能提升 TSFM 对多变量依赖和协变量结构利用能力** 高质量论文的自动实验项目。

## 当前唯一主线

- 论文方向：`Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`
- 主模型：Chronos-2 frozen backbone
- 主方法：Lorentz HyC-Adapter
- 主插入方式：input-side conditioning
- 主目标：证明双曲关系/协变量 adapter 在结构型多变量时间序列上优于 frozen TSFM 和参数量匹配的 Euclidean Adapter

不要突然改成 unrelated forecasting model、纯 benchmark 工程、纯大模型微调或无几何分析的刷分项目。

## 参考阅读

在一些特定条件/情况下，你应该参考不同文件指导：

1. 这是一个论文研究项目，如果你需要了解更多该论文的信息来确定查找论文的类型和方向，参考：`docs/research_brief.md`。
2. 对于试验阶段和实验循环的说明，参考：`docs/experiment_loop.md`。
4. 实验中需要遵循的协议，参考`docs/experiment_protocol.md`。
5. 对于Adapter的结构设计和调参细节，可以参考`docs/adapter_spec.md`。
6. 最近的 `reports/stage_N_review.md`，如果存在

只读完 `AGENTS.md` 还不能开始实验。

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

## 推荐启动流程

1. 运行环境检查：
   
   ```bash
   python scripts/env_check.py
   ```

2. 检查当前阶段：
   
   ```bash
   python scripts/collect_results.py --summary
   ```

3. 如果还没有 baseline，先跑 baseline config。不要先跑 HyC。

4. 一种新的实验配置下的实验应该在新的分支下进行，所以首先检查git state，检查我们所在的分支/提交。如果只是seed不同，算作同一种实验。

5. 每次正式实验使用：
   
   ```bash
   python scripts/run_experiment.py --config configs/debug/smoke.yaml
   python scripts/collect_results.py --run-id <run_id>
   ```


## 输出纪律

每个正式实验必须产生：

- `runs/<run_id>/config.yaml`
- `runs/<run_id>/run.log`
- `runs/<run_id>/metrics.json`
- `runs/<run_id>/summary.md`

每个可汇总实验必须追加到：

- `results/experiments.jsonl`

不要把临时 debug 结果混入主结果，除非 config 明确 `record: true` 或人工要求记录。
