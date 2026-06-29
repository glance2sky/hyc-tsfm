# Research Brief

## 论文暂定题目

`Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`

## 一句话目标

研究轻量双曲关系/协变量 adapter 是否能提升时间序列 foundation model 对多变量依赖、层级结构和外生协变量的利用能力。

## 核心假设

- 多变量时间序列依赖图常有层级、树状、hub、社群和动态图结构。
- 双曲空间更适合低失真表示层级、树状和幂律关系。
- 轻量 adapter 比本地全参数微调 TSFM 更可行，也更容易做公平对照。
- 如果 HyC 有效，它的收益应在结构强、hyperbolicity 高、协变量重要的数据集上更明显。

## 主实验问题

- HyC-Adapter 是否优于 frozen Chronos-2？
- HyC-Adapter 是否优于参数量匹配的 Euclidean Adapter？
- 收益是否与数据集 hyperbolicity、tree-likeness、distortion 相关？
- HyC-Adapter 是否能更稳地利用 past/future covariates 和 static metadata？
- HyC 的收益是否能迁移到 Chronos-Bolt、Moirai、TTM 或 TimesFM？

## 成功标准

- 至少 6 个数据集主结果。
- 至少 2 个 TSFM backbone。
- 至少 4 类核心消融。
- 至少 3 seeds 的主表结果。
- 至少 1 个 covariate-rich benchmark。
- 至少 1 个几何诊断图证明“为什么双曲有效”。
- 所有主结论都有 baseline、参数量匹配对照和失败案例记录支撑。

## 预期论文故事

当前 TSFM 在 zero-shot 和通用预测上进展很快，但多变量依赖和协变量利用仍不稳定。HyC-Adapter 把变量和协变量关系编码为曲率自适应的双曲关系表示，再以轻量条件信号注入冻结 TSFM。该方法不需要重新预训练大模型，却能在结构型数据上带来稳定收益，并通过几何诊断解释收益来源。

