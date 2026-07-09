# HyC-TSFM

这是一个以本地 `skills/` 为入口的论文研究 harness。不要先批量阅读 `docs/`；进入仓库后，第一步只读取 `skills/start-here/SKILL.md`，再按触发条件渐进式获取上下文。

## 论文主线

- 题目方向：`Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`
- 默认 backbone：冻结的 `Chronos-2`
- 默认方法：`Lorentz HyC-Adapter`
- 默认注入方式：`input-side conditioning`
- 默认目标：证明 HyC 在结构型多变量时间序列上优于 frozen TSFM 与参数量匹配的 Euclidean Adapter

不要把项目改成 unrelated forecasting model、纯 benchmark 工程、纯大模型微调或无几何分析的刷分项目。

## 绝对约束

- 每一条新的研究线程都应该先从干净工作区创建 git 分支，再开始改代码、调参数或改模型结构。
- 如果一个研究分支没有带来更好的证据，就应该标记为 discard 并回到它的 base branch，而不是把失败版本继续堆在主线上。
- 不要把“多跑几个超参”当成默认改进策略；当性能停滞或行为异常时，优先收集观测指标、查找文献依据，再做结构级探索。
- 正式实验结果必须通过 `scripts/run_experiment.py` 产生，再由 `scripts/collect_results.py` 追加到结果汇总。
- 不允许修改测试集标签、验证集、数据切分或评估指标来制造提升。
- 不允许把 test set 用于 early stopping 或超参搜索。
- 不允许删除失败实验记录，也不允许只挑最好 seed 报告。
- 不允许在没有记录理由的情况下改变 split、horizon、normalization 或 context length。
- `references/papers/` 与 `references/external-code/` 是只读参考区；可以下载和阅读，但不要在其中继续开发。
- 如果借鉴外部论文源码中的模块，应该重写或复制到项目自有区域，如 `src/`、`scripts/` 或新的项目实现目录中。

## 目录约定

- `skills/`：项目的核心工作流与按需披露入口。
- `research/branches/`：研究分支日志，一条 branch 对应一个连续研究线程。
- `research/activity/`：研究过程活动日志，记录改动、观测、文献与实验结果。
- `references/`：论文 PDF、外部源码镜像与参考笔记。
- `configs/`：debug、baseline、control 与 branch 配置。
- `runs/`：单次运行产物。
- `results/`：汇总表与结果索引。

## 人类入口

- 如果你是 agent：从 `skills/start-here/SKILL.md` 开始。
- 如果你是人类：先看 `README.md` 了解仓库布局，再按需查看 `skills/`。
