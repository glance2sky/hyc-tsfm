# Results Schema

所有正式实验必须能追溯到 config、log、metrics 和 summary。

## 主结果文件

`results/experiments.jsonl` 每行一个实验：

```json
{
  "run_id": "2026-06-26_001",
  "stage": 2,
  "commit": "abcdef1",
  "hypothesis": "Lorentz geometry improves Electricity forecasting over Euclidean adapter",
  "backbone": "chronos-2",
  "adapter": "hyc_lorentz_v1",
  "dataset": "electricity",
  "horizon": 336,
  "seed": 42,
  "status": "keep",
  "mse": 0.123,
  "mae": 0.234,
  "peak_vram_gb": 11.2,
  "trainable_params_m": 4.8,
  "training_minutes": 38.5,
  "notes": "Stable improvement over Euclidean adapter"
}
```

## 允许的 status

- `keep`
- `discard`
- `crash`
- `oom`
- `inconclusive`
- `needs_rerun`

## 每次实验目录

每次实验必须生成：

- `runs/<run_id>/config.yaml`
- `runs/<run_id>/run.log`
- `runs/<run_id>/metrics.json`
- `runs/<run_id>/summary.md`

## 最小 metrics 字段

`metrics.json` 至少包含：

- `run_id`
- `stage`
- `status`
- `dataset`
- `horizon`
- `seed`
- `backbone`
- `adapter`
- `mse`
- `mae`
- `peak_vram_gb`
- `trainable_params_m`
- `training_minutes`
- `notes`

失败实验中未知数值可以为 `null`，但 `status` 和 `notes` 必须说明原因。

