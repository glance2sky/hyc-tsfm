# HyC-TSFM Harness

这是一个面向研究 agent 的 `skills-first` harness，用于推进论文方向：

`Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`

当前仓库的核心目标不是“先把所有规范文档读完”，而是让 agent 像调用本地 skill 一样，按任务逐步读取所需上下文、工作流与参考资料。

## Start Here

- Agent 入口：`AGENTS.md` -> `skills/start-here/SKILL.md`
- 人类入口：本文件 -> `skills/`

## Repo Layout

- `skills/`
  仓库内置的本地研究技能。所有核心流程都从这里触发。
- `research/branches/`
  研究分支日志。一条 branch 是一个连续的研究线程，不再以 stage 作为主组织单位。
- `references/`
  只读参考资产区，存放论文 PDF、外部源码镜像和阅读笔记。
- `configs/`
  配置入口。按 `debug/`、`baselines/`、`controls/`、`branches/` 组织。
- `scripts/`
  稳定脚本入口，包括研究分支创建、环境检查、实验运行、结果收集和表格汇总。
- `runs/`
  每次实验的产物目录。
- `results/`
  结果汇总与主表。

## Minimal Commands

```bash
python scripts/research_branch.py start --branch electricity-hyc
python scripts/env_check.py
python scripts/run_experiment.py --config configs/debug/smoke.yaml
python scripts/collect_results.py --summary
python scripts/make_tables.py
```

`run_experiment.py` 会在 `runs/<run_id>/` 下写出 `config.yaml`、`run.log`、`metrics.json` 与 `summary.md`，并记录对应的 `git_branch`。当 config 显式设置 `record: true` 时，再使用 `collect_results.py` 将结果追加到 `results/experiments.jsonl`。

## Research Direction

- 默认 backbone：冻结的 `Chronos-2`
- 默认方法：`Lorentz HyC-Adapter`
- 默认注入方式：`input-side conditioning`
- 默认关键对照：frozen backbone baseline 与参数量匹配的 Euclidean Adapter

默认版本纪律：每个新实验线程先开 git 分支，结果更好则 keep，不更好则 discard 并回到 base branch。
