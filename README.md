# HyC-TSFM Harness

这是一个面向自主科研 agent 的轻量 harness，用于推进 HyC-TSFM 论文路线：

`Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`

它借鉴 `autoresearch` 的 Markdown program 和实验循环思想，但采用阶段门控、结果审计、固定日志 schema 和 reviewer checklist，目标是让 agent 能长期推进项目，同时尽量避免虚假提升、丢失失败记录和实验不可复现。

## Quick Start

```bash
python scripts/env_check.py
python scripts/run_experiment.py --config configs/debug/smoke.yaml
python scripts/collect_results.py --run-id <run_id>
python scripts/make_tables.py
```

`run_experiment.py` 会在 `runs/<run_id>/` 下生成 config、log、metrics 和 summary。`collect_results.py` 会把单次实验追加到 `results/experiments.jsonl`。

## For Agents

从 `AGENTS.md` 开始，不要直接跳进代码。正式实验必须通过 `configs/` 下的 YAML 配置驱动。

## Current Status

当前仓库是 harness v1：包含文档、配置骨架和可运行的结果记录脚本。真实 TSFM 训练代码、数据下载器和 HyC-Adapter 实现应在阶段 1-2 按文档逐步加入。

