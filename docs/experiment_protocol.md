# Experiment Protocol

## 默认配置

- 主 backbone：Chronos-2。
- 主 adapter：Lorentz HyC-Adapter。
- 主 injection：input-side conditioning。
- 默认冻结 TSFM 主干。
- 默认训练参数只包括 adapter、projection、gating、optional LoRA。
- 默认 precision：bf16，失败则 fp16。
- 默认 seeds：原型阶段 1 seed，主实验 3 seeds。
- 默认 metrics：MSE、MAE；概率预测可加 NLL/CRPS。
- 默认资源指标：peak VRAM、training time、trainable params、inference latency。

## 公平比较规则

- HyC 必须与参数量匹配的 Euclidean Adapter 比较。
- 同一数据集上所有方法使用同一 split、horizon、normalization。
- 同一表内训练预算必须一致。
- 如果某方法 OOM，记录为 OOM，不删除。
- 如果只跑了 1 seed，表格必须标注 `preliminary`。
- 主结论只允许来自 3 seeds 或明确说明的稳定结果。
- HyC 和 Euclidean adapter 参数量差距超过 20% 时，不能声称公平。

## 固定字段

每个 config 必须包含：

- `dataset`
- `split`
- `horizon`
- `context_length`
- `backbone`
- `adapter`
- `graph_builder`
- `curvature_mode`
- `injection_mode`
- `seed`
- `batch_size`
- `precision`
- `max_epochs` 或 `max_steps`
- `early_stopping`
- `output_dir`
- `hypothesis`

## 主指标

- 点预测：MSE、MAE。
- 概率预测：NLL、CRPS，如果 backbone 输出支持。
- 资源指标：peak VRAM、training minutes、trainable params、inference latency。

## 预算纪律

不要在主表中混用明显不同的训练预算。为了调试可以缩短训练，但必须把结果标为 debug 或 preliminary。

