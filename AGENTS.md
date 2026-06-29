# HyC-TSFM Agent Entry

你正在进入一个阶段门控的自主科研 harness。你的任务不是随意刷榜，而是审慎推进一篇关于 **HyC-Adapter 是否能提升 TSFM 对多变量依赖和协变量结构利用能力** 的高质量论文。

## 当前唯一主线

- 论文方向：`Curvature-Aware Hyperbolic Adapters for Covariate-Aware Time-Series Foundation Models`
- 主模型：Chronos-2 frozen backbone
- 主方法：Lorentz HyC-Adapter
- 主插入方式：input-side conditioning
- 主目标：证明双曲关系/协变量 adapter 在结构型多变量时间序列上优于 frozen TSFM 和参数量匹配的 Euclidean Adapter

不要突然改成 unrelated forecasting model、纯 benchmark 工程、纯大模型微调或无几何分析的刷分项目。

## 每次工作前必须阅读

按顺序阅读：

1. `docs/research_brief.md`
2. `docs/agent_rules.md`
3. `docs/experiment_loop.md`
4. `docs/experiment_protocol.md`
5. `docs/adapter_spec.md`
6. 最近的 `reports/stage_N_review.md`，如果存在

只读完 `AGENTS.md` 还不能开始实验。

## 绝对规则

- 不得跳过 baseline。
- 不得修改评估指标、测试集标签、验证集或数据切分来制造提升。
- 不得删除失败、crash、OOM、无提升实验记录。
- 默认每轮只提出并执行一个实验 idea。
- 每个实验必须有 `hypothesis`、`config`、`commit` 或 workspace 状态说明、日志、指标和结论。
- 如果实验失败，记录失败原因；不要悄悄换下一个实验。
- 如果只跑了 1 seed，所有结论必须标注 `preliminary`。
- HyC-Adapter 与 Euclidean Adapter 参数量差距超过 20% 时，不能声称公平。

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

4. 每次正式实验使用：
   
   ```bash
   python scripts/run_experiment.py --config configs/debug/smoke.yaml
   python scripts/collect_results.py --run-id <run_id>
   ```

5. 阶段结束后写 `reports/stage_N_review.md`，并按 `docs/reviewer_checklist.md` 自查。

## 输出纪律

每个正式实验必须产生：

- `runs/<run_id>/config.yaml`
- `runs/<run_id>/run.log`
- `runs/<run_id>/metrics.json`
- `runs/<run_id>/summary.md`

每个可汇总实验必须追加到：

- `results/experiments.jsonl`

不要把临时 debug 结果混入主结果，除非 config 明确 `record: true` 或人工要求记录。
