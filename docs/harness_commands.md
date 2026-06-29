# Harness Commands

正式实验和汇总优先使用这些稳定入口。

## 环境检查

```bash
python scripts/env_check.py
```

产物：

- `reports/env_report.md`

## 数据下载占位入口

```bash
python scripts/download_data.py --dataset electricity
```

当前 v1 默认只登记数据需求，不自动下载大数据。后续接入真实数据下载器时必须保留来源、缓存路径和 split 说明。

## 跑实验

```bash
python scripts/run_experiment.py --config configs/debug/smoke.yaml
```

产物：

- `runs/<run_id>/config.yaml`
- `runs/<run_id>/run.log`
- `runs/<run_id>/metrics.json`
- `runs/<run_id>/summary.md`

## 汇总结果

```bash
python scripts/collect_results.py --run-id <run_id>
python scripts/collect_results.py --summary
```

## 生成表格

```bash
python scripts/make_tables.py
```

产物：

- `results/main_table.md`

## 几何诊断占位入口

```bash
python scripts/geometry_report.py --dataset electricity
```

产物：

- `reports/geometry_<dataset>.md`

