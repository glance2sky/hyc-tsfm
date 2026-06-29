# Adapter Spec

主版本：`HyC-v1`

## Dynamic Relation Graph Builder

输入：

- 历史窗口 `X`
- 可选 past covariates
- 可选 future covariates
- 可选 static metadata

输出：

- 变量关系图 `A_t`
- top-k 稀疏边
- 可选边特征

默认设计：

- 先用 correlation 或 lagged correlation 初始化。
- 再用可学习 attention refinement。
- 默认 top-k 稀疏图，`k=16`。
- 可选边特征包括滞后相关、Granger-style score、DTW 距离、空间距离、行业或层级标签。

## Lorentz Hyperbolic Encoder

默认使用 Lorentz model。

步骤：

- 每个变量节点先通过 Euclidean MLP 得到 tangent embedding。
- 使用 exponential map 投到 Lorentz space。
- learnable curvature 使用 `softplus(raw_c) + eps`。
- 默认使用 adaptive curvature。

曲率模式：

- `fixed`：固定 `c=1`
- `global`：全局 learnable curvature
- `adaptive`：group/time-adaptive curvature

## Hyperbolic Message Passing

默认设置：

- 层数：2
- hidden dim：128
- dropout：0.1
- 先在 Lorentz space message passing
- 再通过 log map 回 tangent space

输出：

- `H_var`: variable-level condition token
- `H_global`: global condition token

## Injection

主线：

- `input_side_conditioning`
- Adapter 产生 `H_var` 和 `H_global`
- 通过 gate 注入 TSFM input 或 covariate embedding

Fallback：

- 如果 TSFM 内部接口难改，改用 `output_residual_calibration`。
- `mid_layer_cross_attention` 只作为增强实验，不作为第一实现。

## 必须实现的 ablation

- `no_adapter`
- `euclidean_adapter`
- `hyc_lorentz_v1`
- `fixed_curvature`
- `adaptive_curvature`
- `static_graph`
- `dynamic_graph`
- `with_covariates`
- `without_covariates`

## 模型设计推荐做法
- adapter的模型设计应该有所依据。依据之前的实验分析和最新的论文研究进展来进行综合考虑。
- 参考最新学术科研进展时候，可以将论文的pdf保存在主目录下的reference文件夹下，如果需要下载论文源码或者复现论文模型，可将相关文件写在asserts下的子目录中。
- 对一篇学术论文进行分析的时候，可以使用已经安装在本地的相关research skill，要明白该论文创新在哪里，为什么有效，在本项目中可以借鉴哪些点，总结在asserts的相关文件夹下。
- 在同一种实验配置下，在一种adapter结构下进行的调参实验不能超过3次。如果3次有效性调参实验都没有提升，就应该主动尝试改变adapter的结构。
